import os
import argparse
import logging
import json

import slack


logging.basicConfig()
LOG = logging.getLogger(__name__)


def main():
    if os.environ['SLACK_API_TOKEN'] in (None, ''):
        LOG.exception('Failed to parse Slack API token.')
        return

    parser = argparse.ArgumentParser(description='Upload a file to Slack.')

    parser.add_argument('--channel', dest='channelName', type=str, required=True, help='Slack channel name.')
    parser.add_argument('--file', dest='srcFile', required=True, help='File path you want to upload.')

    args = parser.parse_args()

    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
    response = client.files_upload(channels=args.channelName, file=args.srcFile)
    
    if not response['ok']:
        err = {
            'status': 'FAILED',
            'error': {
                'errors': [
                    {
                        'reason': response['error'],
                        'message': 'Failed to upload file: {0}'.format(args.srcFile)
                    }
                ]
            }
        }
        LOG.error(err['error']['errors'][0]['message'])
        return json.dumps(err)
    
    return json.dumps({'status': 'OK'})

if __name__ == '__main__':
    main()