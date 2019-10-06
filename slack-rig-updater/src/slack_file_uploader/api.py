import os
import logging

from flask import Flask, request
import slack


app = Flask(__name__)

logging.basicConfig()
LOG = logging.getLogger(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/update', methods=['POST'])
def api_update():
    err = { 
        'error': {
            'errors': []
        }
    }

    json_data = request.get_json(force=True) 

    # Validate incoming parameters.
    channel = json_data.get('channel', None)
    if channel is None:
        err['error']['errors'].append({
            'reason': 'Missing channel parameter.',
            'message': 'channel is a required parameter.'
        })

    asset = json_data.get('asset', None)
    LOG.info(asset)
    if asset is None:
        err['error']['errors'].append({
            'reason': 'Missing asset parameter.',
            'message': 'asset is a required parameter.'
        })

    filepath = json_data.get('file', None)
    LOG.info(filepath)
    notes = json_data.get('notes')
    LOG.info(notes)
    
    if err['error']['errors']:
        return err, 400

    # Start the request.
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    # Upload the associated file if there is one, first, so we can
    # get the link/thumbnail for the new message.
    fileReponse = None
    if filepath is not None:
        fileResponse = client.files_upload(file=filepath)
        if not fileResponse['ok']:
            err['error']['errors'].append({
                'reason': fileResponse['error'],
                'message': 'Failed to upload file: {0}'.format(filepath)
            })

            return err, 400

    # Post a new message in the Slack Channel with the formatted message.
    msgResponse = client.chat_postMessage(channel=channel, blocks=createUpdateBlocks(asset, notes))
    if not msgResponse['ok']:
        err['error']['errors'].append({
            'reason': msgResponse['error'],
            'message': 'Failed to post update message.'
        })

        return err, 400

    return {"ok": True}, 201

@app.route('/feedback', methods=['GET', 'POST'])
def api_feedback():
    return {"ok": True}


def createUpdateBlocks(asset, notes):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "{0} was updated!".format(asset),
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*CHANGELOG*",
            }
        }
    ]

    notesFormatted = ''

    if notes is not None:
        for n, note in enumerate(notes):        
            noteFormatted = "{0}. {1} \n".format(n+1, note)
            notesFormatted += noteFormatted

    if notesFormatted:
        blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": notesFormatted,
                }
            })

    return blocks