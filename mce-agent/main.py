from strands import Agent, tool
from strands_tools import calculator # Import the calculator tool
from strands.models import BedrockModel
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

# Create a custom tool 
@tool
def weather():
    """ Get weather """ # Dummy implementation
    return "sunny"

@tool
def get_mce_environments():
    """ Get MCE(Managed Container Environment) environments """
    url = f"{BASE_URL}/environments"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        fields = ['id', 'name', 'runningState']
        environments = response.json().get("environments", [])
        return [{field: env.get(field) for field in fields} for env in environments]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
model = BedrockModel(
    model_id=model_id,
)
agent = Agent(
    model=model,
    tools=[calculator, weather, get_mce_environments],
    system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather."
)

def strands_agent_bedrock(payload):
    """
    Invoke the agent with a payload
    """
    user_input = payload.get("prompt")
    response = agent(user_input)
    return response.message['content'][0]['text']

if __name__ == "__main__":
    # environments = get_mce_environments()
    # print("MCE Environments:", json.dumps(environments, indent=2))
    # exit(0)
    while True:
        user_input = input("\n🤵 User: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        if not user_input:
            continue
        print("🤖 Agent: ")
        agent(user_input)
