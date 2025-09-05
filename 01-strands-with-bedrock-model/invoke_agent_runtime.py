import boto3
from dotenv import load_dotenv
import os
from IPython.display import display, Markdown
import json

load_dotenv()

agent_arn = os.getenv("AGENT_ARN")
region = os.getenv("REGION", "us-east-1")

agent_arn = agent_arn
agentcore_client = boto3.client(
    'bedrock-agentcore',
    region_name=region
)

print("Invoking the agent with ARN:", agent_arn)
boto3_response = agentcore_client.invoke_agent_runtime(
    agentRuntimeArn=agent_arn,
    qualifier="DEFAULT",
    payload=json.dumps({"prompt": "What is 2+2?"})
)
if "text/event-stream" in boto3_response.get("contentType", ""):
    content = []
    for line in boto3_response["response"].iter_lines(chunk_size=1):
        if line:
            line = line.decode("utf-8")
            if line.startswith("data: "):
                line = line[6:]
                print(line)
                content.append(line)
    print("Final content:", content)
    display(Markdown("\n".join(content)))
else:
    try:
        events = []
        for event in boto3_response.get("response", []):
            events.append(event)
    except Exception as e:
        events = [f"Error reading EventStream: {e}"]
    print("Events:", events)
    display(Markdown(json.loads(events[0].decode("utf-8"))))