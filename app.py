from datetime import datetime
import pytz
import sys
import gitlab
from dateutil.parser import parse

access_token = sys.argv[1]
HEADERS = {'PRIVATE-TOKEN': access_token}
GL_URL = 'http://git.spine2.ncrs.nhs.uk/'
gl = gitlab.Gitlab(url=GL_URL,
                   private_token=access_token)
group = gl.groups.get(304)
lambdas = gl.projects.get(353)


def sort_dict_by_value(d):
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=True))


def create_author_table(authors):
    html_table = '<table border="1"><tr><th>Author</th><th>Number of MRs</th></tr>'
    for author, count in authors.items():
        html_table += '<tr><td>' + author + \
            '</td><td>' + str(count) + '</td></tr>'
    html_table += '</table>'
    return html_table


def create_mr_table(mrs):
    html_table = '<table border="1"><tr><th>Author</th><th>Merge Request</th><th>Repository</th><th>Upvotes</th><th>Created At</th></tr>'
    for merge_request in mrs:
        author_link = "<a href=" + \
            merge_request.author['web_url']+">" + \
            merge_request.author['name']+"</a>"
        project = gl.projects.get(merge_request.project_id)
        html_table += '<tr><td>' + author_link + \
            '</td><td>' + '<a href="' + merge_request.web_url + '">' + merge_request.title + '</a>' + '</td><td>' + '<a href="' + GL_URL+project.path_with_namespace + '">' + project.name + '</a>' + '</td><td>' + \
            str(merge_request.upvotes) + '</td><td>' + \
            merge_request.created_at.strftime(
                "%B %d, %Y") + '</td></tr>'
    html_table += '</table>'
    return html_table


ready_to_merge = {'merge_requests': [], 'authors': {}}
older_than_3_months = {'merge_requests': [], 'authors': {}}
need_one_reviewer = {'merge_requests': [], 'authors': {}}
need_two_reviewers = {'merge_requests': [], 'authors': {}}

mrs = group.mergerequests.list(state='opened', scope="all", all=True)

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

# programatically create html for issue description
# {'id': 35500, 'iid': 2, 'project_id': 729, 'title': 'NFT Locust P0 Registration Journey', 'description': 'Sets up the P0 Registration journey on Locust', 'state': 'opened', 'created_at': '2022-03-22T09:46:44.009Z', 'updated_at': '2022-04-13T15:05:24.122Z', 'merged_by': None, 'merged_at': None, 'closed_by': None, 'closed_at': None, 'target_branch': 'develop', 'source_branch': 'nft-locust-dev', 'user_notes_count': 42, 'upvotes': 1, 'downvotes': 0, 'author': {'id': 814, 'name': 'Athavan Srividiyakaran', 'username': 'athavan.srividiyakaran', 'state': 'active', 'avatar_url': 'http://git.spine2.ncrs.nhs.uk/uploads/-/system/user/avatar/814/avatar.png', 'web_url': 'http://git.spine2.ncrs.nhs.uk/athavan.srividiyakaran'}, 'assignees': [], 'assignee': None, 'reviewers': [], 'source_project_id': 729,
# 'target_project_id': 729, 'labels': [], 'work_in_progress': False, 'milestone': None, 'merge_when_pipeline_succeeds': False, 'merge_status': 'can_be_merged', 'sha': '8affd90c488b7e8f48a3680bd9d6837d514e0884', 'merge_commit_sha': None, 'squash_commit_sha': None, 'discussion_locked': None, 'should_remove_source_branch': None, 'force_remove_source_branch': True, 'reference': '!2', 'references': {'short': '!2', 'relative': 'nft-tests!2', 'full': 'cid/nft-tests!2'}, 'web_url': 'http://git.spine2.ncrs.nhs.uk/cid/nft-tests/-/merge_requests/2', 'time_stats': {'time_estimate': 0, 'total_time_spent': 0, 'human_time_estimate': None, 'human_total_time_spent': None}, 'squash': True, 'task_completion_status': {'count': 0, 'completed_count': 0}, 'has_conflicts': False, 'blocking_discussions_resolved': True}

# Need two reviewers
need_two_reviewers_table = create_mr_table(
    need_two_reviewers['merge_requests'])
need_two_reviewers_author_table = create_author_table(
    sort_dict_by_value(
        need_two_reviewers['authors']))

need_two_reviewers_issue = lambdas.issues.get(
    3, lazy=True)  # this is the REAL issue
# need_two_reviewers_issue = lambdas.issues.get(
#     7, lazy=True)  # this is the FAKE issue

need_two_reviewers_issue.title = "Open MR's that need 2 reviewers and < 3 months old"
need_two_reviewers_issue.description = "<h3>Total MR's: " + str(len(need_two_reviewers['merge_requests'])) + "</h3>" + "<h3>MR's marked as WIP have been excluded from this list<h3>" + need_two_reviewers_author_table + \
    need_two_reviewers_table
need_two_reviewers_issue.save()

# Need one reviewer
need_one_reviewer_table = create_mr_table(
    need_one_reviewer['merge_requests'])
need_one_reviewer_author_table = create_author_table(
    sort_dict_by_value(
        need_one_reviewer['authors']))
need_one_reviewer_issue = lambdas.issues.get(4, lazy=True)
need_one_reviewer_issue.title = "Open MR's that need 1 reviewer and < 3 months old"
need_one_reviewer_issue.description = '<h3>Total merge requests: ' + str(len(need_one_reviewer['merge_requests'])) + '</h3>' + "<h3>MR's marked as WIP have been excluded from this list<h3>" + need_one_reviewer_author_table + \
    need_one_reviewer_table
need_one_reviewer_issue.save()

# Ready to merge
ready_to_merge_table = create_mr_table(
    ready_to_merge['merge_requests'])
ready_to_merge_author_table = create_author_table(
    sort_dict_by_value(ready_to_merge['authors']))
ready_to_merge_issue = lambdas.issues.get(5, lazy=True)
ready_to_merge_issue.title = "Open MR's that are ready to merge and < 3 months old"
ready_to_merge_issue.description = '<h3>Total merge requests: ' + \
    str(len(ready_to_merge['merge_requests'])) + '</h3>' + "<h3>MR's marked as WIP have been excluded from this list<h3>" + \
    ready_to_merge_author_table + ready_to_merge_table
ready_to_merge_issue.save()


# Older than 3 months
older_than_3_months_table = create_mr_table(
    older_than_3_months['merge_requests'])
older_than_3_months_author_table = create_author_table(
    sort_dict_by_value(
        older_than_3_months['authors']))
older_than_3_months_issue = lambdas.issues.get(6, lazy=True)
older_than_3_months_issue.title = "Open MR's that are > 3 months old"
older_than_3_months_issue.description = '<h3>Total merge requests: ' + \
    str(len(older_than_3_months['merge_requests'])) + '</h3>' + \
    older_than_3_months_author_table + older_than_3_months_table
older_than_3_months_issue.save()
