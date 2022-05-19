from datetime import datetime
import pytz
import sys
import gitlab
from dateutil.parser import parse

from send_message import notify_slack_channel
from exceptions import MergeRequestRetrievalError
import logging


class Service:
    GL_URL = None
    gitlab_url = None

    def get_body_attr(self, key: str, required=True):
        key = key.lower()
        if required and (key not in self.body):
            raise KeyError('Event body does not contain '
                           f'required attribute `{key}`.')
        return self.body.get(key)

    def sort_dict_by_value(self, d):
        return dict(sorted(d.items(), key=lambda x: x[1], reverse=True))

    def create_author_table(self, authors):
        html_table = '<table border="1"><tr><th>Author</th><th>Number of MRs</th></tr>'
        for author, count in authors.items():
            html_table += '<tr><td>' + author + \
                '</td><td>' + str(count) + '</td></tr>'
        html_table += '</table>'
        return html_table

    def create_mr_table(self, mrs):
        html_table = '<table border="1"><tr><th>Author</th><th>Merge Request</th><th>Repository</th><th>Upvotes</th><th>Created At</th></tr>'
        for merge_request in mrs:
            author_link = "<a href=" + \
                merge_request.author['web_url']+">" + \
                merge_request.author['name']+"</a>"
            project = self.GL_URL.projects.get(merge_request.project_id)
            html_table += '<tr><td>' + author_link + \
                '</td><td>' + '<a href="' + merge_request.web_url + '">' + merge_request.title + '</a>' + '</td><td>' + '<a href="' + self.gitlab_url+project.path_with_namespace + '">' + project.name + '</a>' + '</td><td>' + \
                str(merge_request.upvotes) + '</td><td>' + \
                merge_request.created_at.strftime(
                    "%B %d, %Y") + '</td></tr>'
        html_table += '</table>'
        return html_table

    def lambda_handler(self, gitlab_url, access_token, webhook_url):
        try:
            self.gitlab_url = gitlab_url
            self.GL_URL = gitlab.Gitlab(url=gitlab_url,
                                        private_token=access_token)
            group = self.GL_URL.groups.get(304)
            lambdas = self.GL_URL.projects.get(353)
        except Exception as e:
            raise(f"Error connecting to Gitlab: {e}")

        ready_to_merge = {'merge_requests': [], 'authors': {}}
        older_than_3_months = {'merge_requests': [], 'authors': {}}
        need_one_reviewer = {'merge_requests': [], 'authors': {}}
        need_two_reviewers = {'merge_requests': [], 'authors': {}}

        try:
            mrs = group.mergerequests.list(
                state='opened', scope="all", all=True)
            for merge_request in mrs:
                author = "<a href=" + \
                    merge_request.author['web_url']+">" + \
                    merge_request.author['name']+"</a>"
                merge_request.created_at = parse(merge_request.created_at)
                time_between_insertion = datetime.utcnow().replace(
                    tzinfo=pytz.utc) - merge_request.created_at

                if(time_between_insertion.days > 90):
                    older_than_3_months['merge_requests'].append(merge_request)
                    if author in older_than_3_months['authors']:
                        older_than_3_months['authors'][author] += 1
                    else:
                        older_than_3_months['authors'][author] = 1
                    continue

                if merge_request.work_in_progress == True:
                    continue

                if merge_request.upvotes == 0:
                    need_two_reviewers['merge_requests'].append(merge_request)
                    if author in need_two_reviewers['authors']:
                        need_two_reviewers['authors'][author] += 1
                    else:
                        need_two_reviewers['authors'][author] = 1

                if merge_request.upvotes == 1:
                    need_one_reviewer['merge_requests'].append(merge_request)
                    if author in need_one_reviewer['authors']:
                        need_one_reviewer['authors'][author] += 1
                    else:
                        need_one_reviewer['authors'][author] = 1

                if merge_request.upvotes >= 2:
                    ready_to_merge['merge_requests'].append(merge_request)
                    if author in ready_to_merge['authors']:
                        ready_to_merge['authors'][author] += 1
                    else:
                        ready_to_merge['authors'][author] = 1
        except Exception as e:
            raise MergeRequestRetrievalError(
                f"Error retrieving merge requests, {e}")

        issue_urls = {}

        # Need two reviewers
        need_two_reviewers_table = self.create_mr_table(
            need_two_reviewers['merge_requests'])
        need_two_reviewers_author_table = self.create_author_table(
            self.sort_dict_by_value(
                need_two_reviewers['authors']))
        need_two_reviewers_issue = lambdas.issues.get(
            3, lazy=True)
        need_two_reviewers_issue.title = "Open MR's that need 2 reviewers and < 3 months old"
        need_two_reviewers_issue.description = "<h3>Total MR's: " + str(len(need_two_reviewers['merge_requests'])) + "</h3>" + "<h3>MR's marked as WIP have been excluded from this list<h3>" + need_two_reviewers_author_table + \
            need_two_reviewers_table
        need_two_reviewers_issue.save()
        issue_urls['need_two_reviewers'] = need_two_reviewers_issue.web_url

        # Need one reviewer
        need_one_reviewer_table = self.create_mr_table(
            need_one_reviewer['merge_requests'])
        need_one_reviewer_author_table = self.create_author_table(
            self.sort_dict_by_value(
                need_one_reviewer['authors']))
        need_one_reviewer_issue = lambdas.issues.get(4, lazy=True)
        need_one_reviewer_issue.title = "Open MR's that need 1 reviewer and < 3 months old"
        need_one_reviewer_issue.description = '<h3>Total merge requests: ' + str(len(need_one_reviewer['merge_requests'])) + '</h3>' + "<h3>MR's marked as WIP have been excluded from this list<h3>" + need_one_reviewer_author_table + \
            need_one_reviewer_table
        need_one_reviewer_issue.save()
        issue_urls['need_one_reviewer'] = need_one_reviewer_issue.web_url

        # Ready to merge
        ready_to_merge_table = self.create_mr_table(
            ready_to_merge['merge_requests'])
        ready_to_merge_author_table = self.create_author_table(
            self.sort_dict_by_value(ready_to_merge['authors']))
        ready_to_merge_issue = lambdas.issues.get(5, lazy=True)
        ready_to_merge_issue.title = "Open MR's that are ready to merge and < 3 months old"
        ready_to_merge_issue.description = '<h3>Total merge requests: ' + \
            str(len(ready_to_merge['merge_requests'])) + '</h3>' + "<h3>MR's marked as WIP have been excluded from this list<h3>" + \
            ready_to_merge_author_table + ready_to_merge_table
        ready_to_merge_issue.save()
        issue_urls['ready_to_merge'] = ready_to_merge_issue.web_url

        # Older than 3 months
        older_than_3_months_table = self.create_mr_table(
            older_than_3_months['merge_requests'])
        older_than_3_months_author_table = self.create_author_table(
            self.sort_dict_by_value(
                older_than_3_months['authors']))
        older_than_3_months_issue = lambdas.issues.get(6, lazy=True)
        older_than_3_months_issue.title = "Open MR's that are > 3 months old"
        older_than_3_months_issue.description = '<h3>Total merge requests: ' + \
            str(len(older_than_3_months['merge_requests'])) + '</h3>' + \
            older_than_3_months_author_table + older_than_3_months_table
        older_than_3_months_issue.save()
        issue_urls['older_than_3_months'] = older_than_3_months_issue.web_url

        lists_of_merge_requests = {'ready_to_merge': ready_to_merge, 'older_than_3_months': older_than_3_months,
                                   'need_one_reviewer': need_one_reviewer, 'need_two_reviewers': need_two_reviewers}

        notify_slack_channel(webhook_url, lists_of_merge_requests, issue_urls)


if __name__ == '__main__':
    LOG = logging.getLogger().setLevel(logging.INFO)

    if(len(sys.argv) != 4):
        raise ValueError(
            f"3 arguments expected, but {len(sys.argv)-1} were given")

    gitlab_url = sys.argv[1]
    access_token = sys.argv[2]
    webhook_url = sys.argv[3]

    if not gitlab_url:
        raise ValueError("No gitlab URL given")

    if not access_token:
        raise ValueError("No access token given")

    if not webhook_url:
        raise ValueError("No webhook URL given")

    service = Service()
    service.lambda_handler(gitlab_url, access_token, webhook_url)
