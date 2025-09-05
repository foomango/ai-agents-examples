from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session
import time
import argparse
from IPython.display import display, Markdown
import json

boto_session = Session()
region = boto_session.region_name
agentcore_runtime = Runtime()
agent_name = "strands_claude_getting_started"


def check_status():
    print("Checking the status of the agent...")
    status_response = agentcore_runtime.status()
    status = status_response.endpoint['status']
    end_status = ['READY', 'CREATE_FAILED', 'DELETE_FAILED', 'UPDATE_FAILED']
    
    print('Current status:', status)

    while status not in end_status:
        print(f"Current status: {status}, waiting for 10 seconds...")
        time.sleep(10)
        status_response = agentcore_runtime.status()
        status = status_response.endpoint['status']

def configure():
    print("Configuring the agent...")
    response = agentcore_runtime.configure(
        entrypoint="strands_claude.py",
        auto_create_execution_role=True,
        auto_create_ecr=True,
        requirements_file="requirements.txt",
        agent_name=agent_name
    )
    print("Configuration response:", response)



def launch():
    print("Launching the agent...")
    launch_result = agentcore_runtime.launch()
    print("Launch response:", launch_result)

def invoke(payload):
    print("Invoking the agent with payload:", payload)
    response = agentcore_runtime.invoke({"prompt": payload})
    print("Response from the agent:")
    response_text = json.loads(response['response'][0].decode('utf-8'))
    print("Response text:", response_text)
    display(Markdown(response_text))
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--configure", action="store_true", help="Configure the agent")
    parser.add_argument("--launch", action="store_true", help="Launch the agent")
    parser.add_argument("--status", action="store_true", help="Check the status of the agent")
    parser.add_argument("--invoke", type=str, help="Invoke the agent with a prompt")
    args = parser.parse_args()

    if args.configure:
        configure()
        exit(0)
    if args.launch:
        configure()
        launch()
        check_status
        exit(0)
    if args.status:
        configure()
        check_status()
        exit(0)
    if args.invoke:
        configure()
        invoke(args.invoke)
        exit(0)