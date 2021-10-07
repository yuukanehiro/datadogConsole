
# deploy datadog console
  
## required
  
* python3
  
## git clone
  
```
git clone https://github.com/yuukanehiro/datadogConsole.git
```
  
## setting environment
  
```
$ export DD_SITE="datadoghq.com" DD_API_KEY={DD_API_KEY} DD_APP_KEY={DD_APP_KEY}
```
  
## setting .env
  
```
$ cd datadogConsole
$ cp example.env .env
$ sudo pip install python-dotenv
```
  
## setting .env for notify Slack
  
Please do Slack Integration in advance.
  
https://docs.datadoghq.com/ja/integrations/slack/?tab=slackapplicationus
  
setting .env for notify slack (ex. slack channel=notify_datadog)
```
$ vi .env

- SLACK_CHANNEL="@xxx"
- SLACK_CHANNEL_AND_MENTION_CHANNEL="@notify_datadog <!channel>"
+ SLACK_CHANNEL="@xxx"
+ SLACK_CHANNEL_AND_MENTION_CHANNEL="@notify_datadog <!channel>"
```
  
## deploy Monitors
  
```
$ cd src/Monitors
$ sh deploy_prod.sh
```