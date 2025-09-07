#!/usr/bin/env python3
import aws_cdk as cdk
from multi_region_monitor.multi_region_monitor_stack import MultiRegionMonitorStack

app = cdk.App()
MultiRegionMonitorStack(app, "MultiRegionMonitorStack")
app.synth()
