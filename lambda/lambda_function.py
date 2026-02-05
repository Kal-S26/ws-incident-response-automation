import os, json, uuid
import boto3
from datetime import datetime, timezone

sns = boto3.client("sns")
dynamodb = boto3.resource("dynamodb")

SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
INCIDENTS_TABLE = os.environ["INCIDENTS_TABLE"]
table = dynamodb.Table(INCIDENTS_TABLE)

def lambda_handler(event, context):
    # Works with real GuardDuty findings AND simulated events
    incident_id = str(uuid.uuid4())
    ts = datetime.now(timezone.utc).isoformat()

    # try to parse common GuardDuty fields safely
    detail = event.get("detail", {})
    finding_type = detail.get("type", "UnknownFindingType")
    severity = detail.get("severity", "UnknownSeverity")
    account = event.get("account", "UnknownAccount")
    region = event.get("region", "UnknownRegion")
    title = detail.get("title", "Security Finding")
    description = detail.get("description", "")

    message = {
        "incidentId": incident_id,
        "time": ts,
        "account": account,
        "region": region,
        "findingType": finding_type,
        "severity": severity,
        "title": title,
        "description": description,
        "rawEvent": event
    }

    # 1) Write audit log to DynamoDB
    table.put_item(Item={
        "incidentId": incident_id,
        "time": ts,
        "account": account,
        "region": region,
        "findingType": finding_type,
        "severity": str(severity),
        "title": title
    })

    # 2) Send alert via SNS
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"[ALERT] {finding_type} | Sev: {severity}",
        Message=json.dumps(message, indent=2, default=str)
    )

    print("Incident logged + alert sent:", incident_id)
    return {"statusCode": 200, "incidentId": incident_id}
