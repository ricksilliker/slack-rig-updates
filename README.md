# Rig Tools for Slack


## Setup


### Slack

Just mentioning the details on how to setup the app on Slack. I have no plans on distributing this.

1. Create a new app for your Slack workspace
2. Add the `Incoming Webhooks` feature to the app
3. Configure the `Permissions`, make sure the `Permission Scopes` include the following
    - Send message updates as <App Name>
    - Post to specific channels in Slack
    - Upload and modify files as user


### File Uploader

This small tool requires Python 3.7 and the `slackclient` package installed.


## Tools


### Rig Updater

This widget for Maya has two goals:
1. Make it easier to get feedback on rig changes.
2. Make it faster to communicate rig changes with your team.

When rigs change you can quickly add notes and post to the channel of your choice.

If you need to get feedback from your team, you can focus the discussion by posing a few questions or keynotes to ask to start a thread about.

Both these tools can be used with the provided UI widget or hooked into an existing system to auto post for you.


### File Uploader

Simple CLI to upload files to a specific channel.

**Example:**
```bash
python -m slack_file_uploader --channelName '#MyChannel' --file '/path/to/my/file'
```