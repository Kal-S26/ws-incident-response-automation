# AWS Automated Security Incident Response (EventBridge → Lambda → SNS + DynamoDB)

## Overview
Event-driven security automation that responds to security finding events by triggering a Lambda function, sending an email alert, and logging the incident to DynamoDB for audit purposes.

## Architecture
EventBridge Rule → Lambda (Incident Handler) → SNS (Email Alerts) + DynamoDB (Incident Audit Log)

## AWS Services Used
- Amazon EventBridge
- AWS Lambda (Python)
- Amazon SNS
- Amazon DynamoDB
- Amazon CloudWatch

## Workflow
1. Event matches the EventBridge rule pattern.
2. EventBridge invokes Lambda.
3. Lambda logs the incident to DynamoDB.
4. Lambda publishes an alert to SNS (email).

## Testing
For demo/testing, a custom event source is used:
- `source`: `custom.guardduty`
- `detail-type`: `GuardDuty Finding`

Sample event: `events/sample_guardduty_finding.json`

## Proof
See `/screenshots` for:
- EventBridge matched events + invocations
- Lambda CloudWatch logs
- DynamoDB inserted items
- SNS email alert

## Cleanup (avoid cost)
- Delete EventBridge rule
- Delete Lambda function
- Delete DynamoDB table
- Delete SNS topic/subscription
