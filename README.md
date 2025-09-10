# DevOps Canary Monitoring Project

## 1. Project Overview
This project uses **AWS CDK (Python)** to build a monitoring and alerting system for an application.  
The main purpose is to detect when the application’s **availability** drops or **latency** increases beyond acceptable limits, and then alert the right people while keeping a record of these events.

The system is designed to:
- Continuously watch key performance metrics.
- Trigger **CloudWatch alarms** when thresholds are crossed.
- Send alerts through **SNS notifications**.
- Store alarm event details in a **DynamoDB** table for later review and analysis.

---

## 2. Implementation Process

### Step 1 – Planning
- Decided on two main metrics:  
  **Availability** (percentage of uptime) and **Latency** (response time in milliseconds).
- Selected AWS services:
  - **CloudWatch** for metrics and alarms.
  - **SNS** for sending notifications.
  - **DynamoDB** for storing alarm history.
  - **Lambda** for processing alarm events and adding extra details before sending notifications.

### Step 2 – Infrastructure Setup
- Created a CDK stack to define all AWS resources in code.
- Added CloudWatch alarms for both metrics with clear thresholds.
- Created an SNS topic for notifications.
- Planned a DynamoDB table to store alarm logs.

### Step 3 – Lambda Function
- Designed a Lambda function to:
  - Receive alarm events from EventBridge.
  - Add a `metricType` tag (e.g., `availability` or `latency`) to help filter notifications.
  - Save alarm details into DynamoDB.
  - Forward enriched messages to SNS.

### Step 4 – Testing
- Adjusted alarm thresholds temporarily to trigger alarms.
- Verified that SNS notifications were sent to the test email.
- Checked DynamoDB for stored alarm records (logging was partially implemented due to errors).

---

## 3. Testing Approach

**Unit Testing**
- Tested Lambda logic with sample alarm events.
- Checked that the correct `metricType` tag was added.
- Verified DynamoDB write function (in isolation).

**Integration Testing**
- Deployed to a test AWS account.
- Triggered alarms by sending custom metrics to CloudWatch.
- Confirmed alarms changed state and SNS notifications were received.

**Manual Verification**
- Viewed CloudWatch alarm dashboards to confirm state changes.
- Checked SNS subscription emails for correct content.
- Looked for DynamoDB entries (partial success due to IAM issues).

---

## 4. Challenges and Solutions

**Challenge 1 – SNS Message Filtering**
- **Problem:** CloudWatch alarms sent directly to SNS do not include message attributes for filtering.
- **Solution:** Planned to route alarms through EventBridge and Lambda to add tags before sending to SNS.

**Challenge 2 – DynamoDB Logging Errors**
- **Problem:** Lambda could not write to DynamoDB due to missing IAM permissions.
- **Solution:** Updated IAM roles to allow `PutItem` on the specific table. Full logging still pending due to time limits.

**Challenge 3 – Alarm Flapping**
- **Problem:** Alarms triggered too often due to short evaluation periods and metric noise.
- **Solution:** Increased evaluation periods and adjusted thresholds to reduce false positives.

**Challenge 4 – Time Constraints**
- **Problem:** Could not fully implement and test all planned features.
- **Solution:** Prioritised core alarm and notification setup, leaving advanced features for future work.

---

## 5. Strengths and Limitations

**Strengths**
- Infrastructure as Code (CDK) makes deployment repeatable and version-controlled.
- Clear separation between monitoring, alerting, and logging components.
- Easy to extend for more metrics or services.

**Limitations**
- DynamoDB logging not fully functional yet.
- SNS message filtering not implemented due to missing attributes in direct alarm notifications.
- Only tested in one AWS region.
- No automated runbook links in notifications yet.

---

## 6. Future Expansion

Due to time limits and persistent errors, some planned features were not completed.  
These can be added in future versions:

1. **Full DynamoDB Logging**  
   - Ensure every alarm event is stored with details like timestamp, metric type, and state change.
   - Use this data for trend analysis and reporting.

2. **SNS Message Filtering**  
   - Add `metricType` tags to SNS messages so subscribers can choose which alerts to receive (e.g., only latency alerts).

3. **Runbook Integration**  
   - Include direct links to troubleshooting guides in SNS notifications for faster incident response.

4. **Multi‑Region Support**  
   - Deploy monitoring in multiple AWS regions for higher resilience.

5. **Anomaly Detection**  
   - Use CloudWatch anomaly detection to reduce false alarms by learning normal patterns.

6. **Alarm Severity Levels**  
   - Classify alarms as Critical, Warning, or Info, and route them to different notification channels.

7. **Automated Remediation**  
   - Trigger Lambda functions or Step Functions to attempt fixes automatically when certain alarms fire.

---

## 7. Ethical Considerations

- **Data Privacy:** Only store necessary alarm details in DynamoDB. Avoid storing sensitive user data.
- **Access Control:** Restrict DynamoDB and SNS access to authorised team members.
- **Alert Fatigue:** Tune alarms to avoid excessive notifications, which can cause stress and reduce response quality.
- **Transparency:** Document what is being monitored and why, so stakeholders understand the purpose of alerts.

---

## 8. References
- AWS Well‑Architected Framework – Reliability Pillar  
  https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html
- AWS CloudWatch Documentation  
  https://docs.aws.amazon.com/cloudwatch/
- AWS CDK Developer Guide  
  https://docs.aws.amazon.com/cdk/
