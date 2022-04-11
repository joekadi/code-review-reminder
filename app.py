import requests
import json
from dateutil import parser
from datetime import datetime
import pytz
import sys


def sort_dict_by_value(d):
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=True))


HEADERS = {'PRIVATE-TOKEN': sys.argv[1]}

ready_to_merge = {'merge_requests': [], 'authors': {}}
older_than_a_month = {'merge_requests': [], 'authors': {}}
need_one_reviewer = {'merge_requests': [], 'authors': {}}
need_two_reviewers = {'merge_requests': [], 'authors': {}}

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
    print('Extracted the correct number of MRs as ',
          len(response), '=', total_items)
else:
    raise Exception('Got wrong number of MRs',
                    len(response), '!=', total_items)

response_string = json.dumps(response)
with open('json_data.json', 'w') as outfile:
    outfile.write(response_string)

for merge_request in response:
    author = merge_request['author']['name']

    time_between_insertion = datetime.utcnow().replace(tzinfo=pytz.utc) - \
        parser.parse(merge_request['created_at'])

    if(time_between_insertion.days > 30):
        older_than_a_month['merge_requests'].append(merge_request)
        if author in older_than_a_month['authors']:
            older_than_a_month['authors'][author] += 1
        else:
            older_than_a_month['authors'][author] = 1
        continue

    if merge_request['upvotes'] == 0:
        need_two_reviewers['merge_requests'].append(merge_request)
        if author in need_two_reviewers['authors']:
            need_two_reviewers['authors'][author] += 1
        else:
            need_two_reviewers['authors'][author] = 1

    if merge_request['upvotes'] == 1:
        need_one_reviewer['merge_requests'].append(merge_request)
        if author in need_one_reviewer['authors']:
            need_one_reviewer['authors'][author] += 1
        else:
            need_one_reviewer['authors'][author] = 1

    if merge_request['upvotes'] >= 2:
        ready_to_merge['merge_requests'].append(merge_request)
        if author in ready_to_merge['authors']:
            ready_to_merge['authors'][author] += 1
        else:
            ready_to_merge['authors'][author] = 1

print(older_than_a_month['merge_requests'][0])

older_than_a_month['authors'] = sort_dict_by_value(
    older_than_a_month['authors'])

ready_to_merge['authors'] = sort_dict_by_value(ready_to_merge['authors'])

need_one_reviewer['authors'] = sort_dict_by_value(
    need_one_reviewer['authors'])

need_two_reviewers['authors'] = sort_dict_by_value(
    need_two_reviewers['authors'])

print('Older than a month: ', len(older_than_a_month['merge_requests']))

# for author, count in older_than_a_month['authors'].items():
#     print(author, ':', count)

print('Ready to merge ', len(ready_to_merge['merge_requests']))
# for author, count in ready_to_merge['authors'].items():
#     print(author, ':', count)

print('Need 1 reviewer ', len(need_one_reviewer['merge_requests']))
# for author, count in need_one_reviewer['authors'].items():
#     print(author, ':', count)

print('Need 2 reviewer ', len(need_two_reviewers['merge_requests']))
# for author, count in need_two_reviewers['authors'].items():
#     print(author, ':', count)
