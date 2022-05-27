from uuid import uuid4
import requests
import json


WIP_BLOCKS = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Open Merge Requests",
            "emoji": True
        }
    },
    {
        "type": "context",
        "elements": [
            {
                "type": "image",
                "image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
                "alt_text": "cute cat"
            },
            {
                "type": "mrkdwn",
                "text": "Authors: please check the box when you've reviewed your open MR's"
            }
        ]
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*15 older than 3 months* :x:"
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "View MR's",
                "emoji": True
            },
            "style": "primary",
            "value": "click_me_123",
            "url": "https://google.com",
            "action_id": "button-action"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": " *Authors - no. of MR's:*"
        },
        "accessory": {
            "type": "checkboxes",
            "options": [
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Karthik Meon - 3"
                    },
                    "value": "value-0"
                },
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Mark Harrison - 2"
                    },
                    "value": "value-1"
                },
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Lisa Cotton - 1"
                    },
                    "value": "value-2"
                },
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Tom Halson - 1"
                    },
                    "value": "value-3"
                }
            ],
            "action_id": "checkboxes-action"
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*7 ready to merge* :100:"
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "View MR's",
                "emoji": True
            },
            "style": "primary",
            "value": "click_me_123",
            "url": "https://google.com",
            "action_id": "button-action"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": " *Authors - no. of MR's:*"
        },
        "accessory": {
            "type": "checkboxes",
            "options": [
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Karthik Meon - 3"
                    },
                    "value": "value-0"
                },
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Mark Harrison - 2"
                    },
                    "value": "value-1"
                },
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Lisa Cotton - 1"
                    },
                    "value": "value-2"
                },
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Tom Halson - 1"
                    },
                    "value": "value-3"
                }
            ],
            "action_id": "checkboxes-action"
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*12 need 1 reviewer* :eyes:"
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "View MR's",
                "emoji": True
            },
            "style": "primary",
            "value": "click_me_123",
            "url": "https://google.com",
            "action_id": "button-action"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": " *Authors - no. of MR's:*"
        },
        "accessory": {
            "type": "checkboxes",
            "options": [
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Karthik Meon - 3"
                    },
                    "value": "value-0"
                },
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Mark Harrison - 2"
                    },
                    "value": "value-1"
                },
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Lisa Cotton - 1"
                    },
                    "value": "value-2"
                },
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Tom Halson - 1"
                    },
                    "value": "value-3"
                }
            ],
            "action_id": "checkboxes-action"
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*7 need 2 reviewers* :eyes::eyes:"
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "View MR's",
                "emoji": True
            },
            "style": "primary",
            "value": "click_me_123",
            "url": "https://google.com",
            "action_id": "button-action"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": " *Authors - no. of MR's:*"
        },
        "accessory": {
            "type": "checkboxes",
            "options": [
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Karthik Meon - 3"
                    },
                    "value": "value-0"
                },
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Mark Harrison - 2"
                    },
                    "value": "value-1"
                },
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Lisa Cotton - 1"
                    },
                    "value": "value-2"
                },
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": "Tom Halson - 1"
                    },
                    "value": "value-3"
                }
            ],
            "action_id": "checkboxes-action"
        }
    }
]


BLOCKS = [

        {
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Open merge requests that need addressed",
				"emoji": True
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "Click through to view each list",
					"emoji": True
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "DEFAULT TEXT",
						"emoji": True
					},
					"value": "click_me_123",
					"url": "https://google.com",
					"action_id": "actionId-0"
				}
			]
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "Oldest was created at random date",
					"emoji": True
				}
			]
		},
        # {
		# 	"type": "section",
		# 	"text": {
		# 		"type": "mrkdwn",
		# 		"text": "*Authors - MR's:*"
		# 	},
		# 	"accessory": {
		# 		"type": "checkboxes",
		# 		"options": [
				
		# 		],
		# 		"action_id": "checkboxes-action"
		# 	}
        # },
		{
			"type": "divider"
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "DEFAULT TEXT",
						"emoji": True
					},
					"value": "click_me_123",
					"url": "https://google.com",
					"action_id": "actionId-0"
				}
			]
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "Oldest was created at random date",
					"emoji": True
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "DEFAULT TEXT",
						"emoji": True
					},
					"value": "click_me_123",
					"url": "https://google.com",
					"action_id": "actionId-0"
				}
			]
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "Oldest was created at random date",
					"emoji": True
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "DEFAULT TEXT",
						"emoji": True
					},
					"value": "click_me_123",
					"url": "https://google.com",
					"action_id": "actionId-0"
				}
			]
		},
        {
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "Oldest was created at random date",
					"emoji": True
				}
			]
		}
]


def add_authors_checklist(authors):
     for author, count in authors.items():
        entry = {
						"text": {
							"type": "mrkdwn",
							"text": f"{author} - {count}"
						},
						"value": f"value{uuid4()}"
			}
            
        BLOCKS[4]['accessory']['options'].append(entry)



def notify_slack_channel(webhook_url, lists_of_merge_requests, issue_urls):
    total_open_mrs = 0
    for key in lists_of_merge_requests:
        total_open_mrs += len(lists_of_merge_requests[key]['merge_requests'])

    BLOCKS[0]['text']['text'] = f'{total_open_mrs} open non-WIP merge requests that need addressed'
    BLOCKS[2]['elements'][0]['text'][
        'text'] = f"{len(lists_of_merge_requests['ready_to_merge']['merge_requests'])} ready to merge :100:"
    BLOCKS[5]['elements'][0]['text'][
        'text'] = f"{len(lists_of_merge_requests['need_one_reviewer']['merge_requests'])} need one reviewer :eyes: "
    BLOCKS[8]['elements'][0]['text'][
        'text'] = f"{len(lists_of_merge_requests['need_two_reviewers']['merge_requests'])} need two reviewers :eyes::eyes:"
    BLOCKS[11]['elements'][0]['text']['text'] = f"{len(lists_of_merge_requests['older_than_3_months']['merge_requests'])} > three months old :axe:"

    BLOCKS[2]['elements'][0]['url'] = issue_urls['ready_to_merge']
    BLOCKS[5]['elements'][0]['url'] = issue_urls['need_one_reviewer']
    BLOCKS[8]['elements'][0]['url'] = issue_urls['need_two_reviewers']
    BLOCKS[11]['elements'][0]['url'] = issue_urls['older_than_3_months']


    BLOCKS[3]['elements'][0]['text'] = f"Oldest created at {lists_of_merge_requests['ready_to_merge']['oldest_merge_request'].created_at.strftime('%B %d, %Y')}"
    BLOCKS[6]['elements'][0]['text'] = f"Oldest created at {lists_of_merge_requests['need_one_reviewer']['oldest_merge_request'].created_at.strftime('%B %d, %Y')}"
    BLOCKS[9]['elements'][0]['text'] = f"Oldest created at {lists_of_merge_requests['need_two_reviewers']['oldest_merge_request'].created_at.strftime('%B %d, %Y')}"
    BLOCKS[12]['elements'][0]['text'] = f"Oldest created at {lists_of_merge_requests['older_than_3_months']['oldest_merge_request'].created_at.strftime('%B %d, %Y')}"

    #add_authors_checklist(lists_of_merge_requests['ready_to_merge']['authors'])

    message_data = {
        "blocks": BLOCKS,
        "username": "Code Review Notifier",
        "icon_emoji": ":eyes:"}

    response = requests.post(
        webhook_url, data=json.dumps(message_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            f"Error sending message to slack: {response.status_code}, {response.text}"
        )
