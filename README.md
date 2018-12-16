# slack-thug

[![license](https://img.shields.io/github/license/jerry-git/slack-thug.svg)](https://github.com/jerry-git/slack-thug/blob/master/LICENSE)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

<p align="center">
  <img src="https://github.com/jerry-git/slack-thug/blob/master/doc/demo.gif" alt="example gif"/>
</p>

## What
Thug memes from Slack image uploads.
 
Messages that are posted in threads of uploaded images and start with _thug_ or _Thug_ are considered as commands to create and upload thug memes based on the original image and given command.
Any member of a public channel (which thug bot is also part of) can thug anyone's uploads.

#### Calling api
* _thug_: creates a thug meme without any texts
* _thug some message_: creates a thug meme with _some message_ as text in the upper part of the image
* _thug "some message" "some other message"_: creates a thug meme with _some message_ as text in the upper part and _some other message_ in the lower part of the image
* _thug "some message" "some other message" -o configoption foo_: same as previous but also overrides default value of _configoption_ by value _foo_ while creating thug meme. 
Multiple config options can be overridden by mentioning `-o` flag multiple times. See full list of available thug meme configuration options [here](https://github.com/jerry-git/thug-memes/blob/master/src/thug/default.conf). 
`slack-thug` uses dlib detector of `thug-memes` so _opencv*_ config options in _detect_ section are not relevant.

If there's an issue while creating the thug meme, the bot will reply nicely in the Slack thread of the given thug command with some additional details about what went wrong. 

#### Tech stack
* Python all the way
* Minimal [Flask](http://flask.pocoo.org/) app
* Redis Queue [rq](http://python-rq.org/)
* [SQLite db](https://docs.python.org/3/library/sqlite3.html)
* [Docker Compose](https://docs.docker.com/compose/)
* [slackclient](https://slackapi.github.io/python-slackclient/)

## Setup
### Slack
#### Create a Slack App
1. Access the web UI of your workspace, e.g. click your workspace name in Slack desktop application and select _Customize Slack_ 
2. Configure apps -> Build (top right corner) -> Your Apps -> Create an App
3. Give you app a dope name and select workspace

#### Create a bot user
1. Bot Users -> Add a bot user -> configure display name and default name -> Add Bot User -> Save changes

#### Install the app to the workspace
1. Your Apps -> your app name -> Install your app to your workspace -> Install App to Workspace -> Authorize

#### Get the token
1. OAuth & Permissions -> Bot User OAuth Access Token
2. Save the token as env variable, e.g. `export SLACK_TOKEN=<the token>`

**NOTE: the `slack-thug` application should be running before the next step.** 

#### Configure event subscription
1. Event Subscriptions -> Enable Events
2. Fill Request URL: _<your_url>/event_ (see _Endpoint for Slack App_ below), you should see green at this point if everything is ok
3. The bot requires access to messages: Add Bot User Event -> add `message.channels` -> Save Changes


#### Start having fun
* Invite the bot to **public** channel(s) in which you want to thug image uploads.

### slack-thug

**NOTE: make sure `SLACK_TOKEN` env variable is configured at this point.**

#### Option 1 - docker-compose (the easy way):
1. Install Docker Engine and Docker Compose if you don't have those.
2. Run docker-compose up. Hold your horses though, installing `dlib` inside a docker image takes a while.   
```console
docker-compose up
```

#### Option 2 - manual installation, running services separately:
1. `slack-thug` relies heavily on [`thug-memes`](https://github.com/jerry-git/thug-memes) which in turn uses `dlib` under the hood. Here's one [guide](https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/) for installing `dlib` on different platforms.
2. `slack-thug` uses [`poetry`](https://poetry.eustace.io/) for dependency management, install deps by:
```console
poetry install
```
3. `slack-thug` uses `redis` for the communication between the web app and the worker process. Install redis and run redis server.
4. Run the worker
```console
poetry run python -m slack_thug.worker
```
5. Run the web app (on a separate console)
```console
poetry run python -m slack_thug.app
```

### Endpoint for Slack App
Regardless which installation/running option you used for `slack-thug`, the endpoint for Slack App will be accessible in _http://localhost:5000/event_ if default configuration is used. To access this endpoint from outside, you can use e.g. [ngrok](https://ngrok.com/). 
After running `ngrok http 5000`, the endpoint (accessible from outside) will be something like _https://asfsdfdsg.ngrok.io/event_. You can use this while configuring the event subscription for the Slack App. 
 
Better option compared to running stuff locally is obviously to deploy it on your (employer's) favorite hosting provider, which is not covered here. 

## Development

#### Installation
```console
poetry install
```

#### Testing
```console
poetry run pytest
```

#### pre-commit
* Install it and it'll be ran automatically with every commit
```console
pre-commit install
```
* Running manually
```console
pre-commit run -a
```
