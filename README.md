# Code Review Reminder Script

- Grabs open MR's from GitLab repo
- Sorts into 4 issues categorised by age and no. of required approvals
- Sends msg to slack channel regarding the MR's
  
`python3 service.py <gitlab_url> <gitlab_access_token> <slack_webhook>`
