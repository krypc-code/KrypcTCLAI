# Libraries
import json
import time


# Method to extract schematics-summary from the text
def invoice_transform_table_summary(payload,client):
    # Get assistant 
    # Table assistant ID
    table_assistant_id = "asst_FRtClkapLDyUKQNqz911Zn5O"    # Summary Assistant
    # Upload the md file to OpenAI
    message_file = client.files.create(
        file=open(payload['file_path_llm'], "rb"), purpose="assistants"
    )
    # Create thread
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Extract invoice information from the following file:\n",
        # Attach the new file to the message.
        attachments= [
            { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
        ],
    )
    # Instantiate a run request
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=table_assistant_id,
    )
    time.sleep(2)
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
    else:
        raise Exception("Request yet to be processed!")
    result = messages.data[0].content[0].text.value
    json_object = json.loads(result.replace('\n','').replace('```json','').replace('```',''))
    return(json_object)


# Method to extract schematics-detailed from the text
def invoice_transform_table_detailed(payload,client):
    # Get assistant 
    # Table assistant ID
    table_assistant_id = "asst_Rot0SxlzMfq4d6x3jNrIemJH"    # Summary Detailed
    # Upload the md file to OpenAI
    message_file = client.files.create(
        file=open(payload['file_path_llm'], "rb"), purpose="assistants"
    )
    # Create thread
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Extract invoice information from the following file:\n",
        # Attach the new file to the message.
        attachments= [
            { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
        ],
    )
    # Instantiate a run request
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=table_assistant_id,
    )
    time.sleep(2)
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
    else:
        raise Exception("Request yet to be processed!")
    result = messages.data[0].content[0].text.value
    json_object = json.loads(result.replace('\n','').replace('```json','').replace('```',''))
    return(json_object)