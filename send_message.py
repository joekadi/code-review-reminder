import requests
import json


webhook_url = "https://hooks.slack.com/services/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"
plain_test = "There are: \n <http://git.spine2.ncrs.nhs.uk/cid/lambdas/-/issues/6|72 open MR's that are more than 3 months old :x:>\n<http://git.spine2.ncrs.nhs.uk/cid/lambdas/-/issues/5|11 open MR's that are ready to merge :100:>\n<http://git.spine2.ncrs.nhs.uk/cid/lambdas/-/issues/4|5 open MR's that need 1 reviewer :eyes:>\n<http://git.spine2.ncrs.nhs.uk/cid/lambdas/-/issues/3|9 open MR's that need 2 reviewers :eyes::eyes:>",

blocks = [
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


message_data = {
    "blocks": blocks,
    "username": "Code Review Notifier",
    "icon_emoji": ":eyes:"}

response = requests.post(
    webhook_url, data=json.dumps(message_data),
    headers={'Content-Type': 'application/json'}
)


if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )
