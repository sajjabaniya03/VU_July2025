from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    aws_cloudwatch as cw
)
from constructs import Construct
import os

class MultiRegionMonitorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_fn = _lambda.Function(
            self, "WebsiteCanaryFn",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="site_canary.lambda_handler",
            code=_lambda.Code.from_asset("lambda_src"),
            timeout=Duration.seconds(30)
        )

        lambda_fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"]
            )
        )

        schedule_rule = events.Rule(
            self, "FiveMinuteSchedule",
            schedule=events.Schedule.rate(Duration.minutes(5))
        )
        schedule_rule.add_target(targets.LambdaFunction(lambda_fn))

        dashboard = cw.Dashboard(self, "WebHealthDashboard")

        for site in ["https://example.com", "https://openai.com"]:
            dashboard.add_widgets(
                cw.GraphWidget(
                    title=f"{site} Availability",
                    left=[cw.Metric(
                        namespace="CustomWebHealth",
                        metric_name="Availability",
                        dimensions_map={"Website": site}
                    )]
                ),
                cw.GraphWidget(
                    title=f"{site} Latency",
                    left=[cw.Metric(
                        namespace="CustomWebHealth",
                        metric_name="Latency",
                        dimensions_map={"Website": site}
                    )]
                )
            )
