# Code Review Reminder Bot

- Grabs open MR's from GitLab repo
- Sorts into 4 issues categorised by age and no. of required approvals
- Sends msg to slack channel regarding the MR's

Collates open merge requests from a GitLab repo then sorts into 4 issues by number of reviews and age then posts issue links to slack in formatted message

## To run: `python service.py <gitlab_url> <gitlab_access_token> <slack_webhook>`
