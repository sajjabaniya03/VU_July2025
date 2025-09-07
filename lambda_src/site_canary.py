import os
import json
import time
import urllib3
import boto3
from datetime import datetime

http_client = urllib3.PoolManager()
cw_client = boto3.client("cloudwatch")

def lambda_handler(event, context):
    config_path = os.path.join(os.path.dirname(__file__), "watch_targets.json")
    with open(config_path) as f:
        targets = json.load(f)

    for site in targets:
        start_time = time.time()
        try:
            resp = http_client.request("GET", site, timeout=5.0)
            latency = round(time.time() - start_time, 3)
            availability = 1 if resp.status == 200 else 0
        except Exception:
            latency = 0
            availability = 0

        cw_client.put_metric_data(
            Namespace="CustomWebHealth",
            MetricData=[
                {
                    "MetricName": "Availability",
                    "Dimensions": [{"Name": "Website", "Value": site}],
                    "Timestamp": datetime.utcnow(),
                    "Value": availability,
                    "Unit": "Count"
                },
                {
                    "MetricName": "Latency",
                    "Dimensions": [{"Name": "Website", "Value": site}],
                    "Timestamp": datetime.utcnow(),
                    "Value": latency,
                    "Unit": "Seconds"
                }
            ]
        )

    return {"status": "metrics_sent", "sites_checked": len(targets)}
