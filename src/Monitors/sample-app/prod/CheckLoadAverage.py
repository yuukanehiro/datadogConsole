import os
from dateutil.parser import parse as dateutil_parser
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import monitors_api
from datadog_api_client.v1.models import *
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

TAG_HOST = "service:sample-app"
TAG_ENV = "env:production" # env:develop|env:staging|env:dev-stg|env:production
MONITOR_NAME = "LoadAverageチェック:" + TAG_HOST + ":" + TAG_ENV
CRITICAL_LOAD_AVERAGE_5MINUTE = 1.0
CRITICAL_LOAD_AVERAGE_5MINUTE_STR = "1.0"
CRITICAL_RECOVERY_AVERAGE_5MINUTE = 0.98
OK_AVERAGE_5MINUTE = 0.5
QUERY="avg(last_5m):avg:system.load.5{" + TAG_HOST + ", " + TAG_ENV + "} > " + CRITICAL_LOAD_AVERAGE_5MINUTE_STR

# https://docs.datadoghq.com/ja/api/latest/monitors/

# See configuration.py for a list of all supported configuration parameters.
configuration = Configuration()

# Enter a context with an instance of the API client
with ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = monitors_api.MonitorsApi(api_client)
    body = Monitor(
        message=os.environ['SLACK_CHANNEL_AND_MENTION_CHANNEL'],
        name=MONITOR_NAME,
        options=MonitorOptions(
		    notify_audit=True,
		    locked=True,
		    timeout_h=0,
		    require_full_window=True,
		    notify_no_data=False,
		    renotify_interval=0,
		    escalation_message="",
		    no_data_timeframe=None,
		    include_tags=True,
            thresholds=MonitorThresholds(
                critical=CRITICAL_LOAD_AVERAGE_5MINUTE,
                critical_recovery=CRITICAL_RECOVERY_AVERAGE_5MINUTE,
                ok=OK_AVERAGE_5MINUTE,
            )
        ),
        priority=1,
        query=QUERY,
        restricted_roles=None,
        tags=[
            TAG_HOST,
            TAG_ENV
        ],
        type=MonitorType("metric alert"),
    )  # Monitor | Create a monitor request body.

    # example passing only required values which don't have defaults set
    try:
        # Create a monitor
        api_response = api_instance.create_monitor(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MonitorsApi->create_monitor: %s\n" % e)
