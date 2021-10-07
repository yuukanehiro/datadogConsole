import os
from dateutil.parser import parse as dateutil_parser
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import monitors_api
from datadog_api_client.v1.models import *
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

TAG_HOST = "service:sample-job"
TAG_ENV = "env:production" # env:develop|env:staging|env:dev-stg|env:production
MONITOR_NAME = "メモリ空き容量チェック:" + TAG_HOST + ":" + TAG_ENV
ALERT_BELOW_MEMORY_FREE = 1073741824.0
ALERT_BELOW_MEMORY_FREE_STRING = "1073741824.0" # Str型を求められる為
RECOVERY_BELOW_MEMORY_FREE = 1073741825.0
QUERY="avg(last_5m):min:system.mem.free{" + TAG_HOST + ", " + TAG_ENV + "} <= " + ALERT_BELOW_MEMORY_FREE_STRING

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
                critical=ALERT_BELOW_MEMORY_FREE,
                critical_recovery=RECOVERY_BELOW_MEMORY_FREE
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
