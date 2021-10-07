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
TARGET_DEVICE = "device:/dev/xvda1"
MONITOR_NAME = "DISK容量チェック:" + TAG_HOST + ":" + TAG_ENV
LIMIT_DISK_FREE_BYTE = "10737418240" # 10GB以下でアラート
QUERY="avg(last_5m):min:system.disk.free{" + TAG_ENV + "," + TAG_HOST + "," + TARGET_DEVICE + "} < " + LIMIT_DISK_FREE_BYTE

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
            enable_logs_sample=True,
            escalation_message="none",
            evaluation_delay=1,
            groupby_simple_monitor=True,
            include_tags=True,
            locked=True,
            min_failure_duration=0,
            min_location_failed=1,
            no_data_timeframe=2,
            notify_audit=False,
            notify_no_data=False,
            renotify_interval=1,
            require_full_window=True,
            new_host_delay=300,
            silenced={
                "key": 1,
            },
            timeout_h=0,
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
