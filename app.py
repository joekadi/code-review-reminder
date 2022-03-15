import requests
import json
from dateutil import parser
from datetime import datetime
import pytz
import sys

HEADERS = {'PRIVATE-TOKEN': sys.argv[1]}

response_raw = requests.get(
    'http://git.spine2.ncrs.nhs.uk/api/v4/groups/304/merge_requests?&state=opened&scope=all', headers=HEADERS)

total_pages = int(response_raw.headers['X-Total-Pages'])
total_items = int(response_raw.headers['X-Total'])
response = response_raw.json()

for page in range(int(response_raw.headers['X-Page'])+1, int(response_raw.headers['X-Total-Pages'])+1):
    response_raw = requests.get('http://git.spine2.ncrs.nhs.uk/api/v4/groups/304/merge_requests?page={page}&state=opened&scope=all'.format(
        page=page), headers=HEADERS)

    for merge_request in response_raw.json():
        response.append(merge_request)

if total_items == len(response):
    print('Got correct number of MRs as ', len(response), '=', total_items)
else:
    raise Exception('Got wrong number of MRs',
                    len(response), '!=', total_items)

response_string = json.dumps(response)
with open('json_data.json', 'w') as outfile:
    outfile.write(response_string)

ready_to_merge = []
older_than_a_month = []
need_one_reviewer = []
need_two_reviewers = []
for merge_request in response:

    time_between_insertion = datetime.utcnow().replace(tzinfo=pytz.utc) - \
        parser.parse(merge_request['created_at'])

    if(time_between_insertion.days > 30):
        older_than_a_month.append(merge_request)
        continue

    if merge_request['upvotes'] >= 2:
        ready_to_merge.append(merge_request)

    if merge_request['upvotes'] == 1:
        need_one_reviewer.append(merge_request)

    if merge_request['upvotes'] == 0:
        need_two_reviewers.append(merge_request)


print('Older than a month: ', len(older_than_a_month))
print('Ready to merge ', len(ready_to_merge))
print('Need 1 reviewer ', len(need_one_reviewer))
print('Need 2 reviewer ', len(need_two_reviewers))
