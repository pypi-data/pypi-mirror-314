# from package import MODEL_REGION
# from package.utils import timelog
import boto3

# printout color ref: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal

MODEL_REGION = "us-west-2"
# bedrock_model = "us.meta.llama3-2-1b-instruct-v1:0"
bedrock_model = "us.meta.llama3-2-3b-instruct-v1:0"
# bedrock_model = "meta.llama3-2-3b-instruct-v1:0"
# bedrock_model = "us.meta.llama3-2-11b-instruct-v1:0"
client = boto3.client("bedrock-runtime", region_name=MODEL_REGION)

# @timelog
def chat_llm(messages):
    """
    Args:
        conversation (list) : a list of conversations between user and assistant
    """
    response = client.converse(
        modelId=bedrock_model,
        messages=messages,
        inferenceConfig={
            "maxTokens": 256 * 4 * 2,  # Adjust for token length as needed
            "temperature": 0,          # Set to 0 for deterministic output
            "topP": 1,                # Full probability space (no restrictions)
            # "top_k": 1                 # Strictly choose the highest-probability token
            # "stopSequences": "",
        },
    )
    response = response["output"]["message"]["content"][0]["text"]
    return response

def BaseMessage(role, message):
    return {'role': role, 'content': [{'text': message}]}

def AIMessage(message):
    return BaseMessage('assistant', message)

def UserMessage(message):
    return BaseMessage('user', message)