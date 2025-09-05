import time
from bedrock_agentcore_starter_toolkit import Runtime

agentcore_runtime = Runtime()
status_response = agentcore_runtime.status()
status = status_response.endpoint['status']
end_status = ['READY', 'CREATE_FAILED', 'DELETE_FAILED', 'UPDATE_FAILED']
while status not in end_status:
    print(f"Current status: {status}, waiting for 10 seconds...")
    time.sleep(10)
    status_response = agentcore_runtime.status()
    status = status_response.endpoint['status']