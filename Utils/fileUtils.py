from Utils.llmUtils import invoice_transform_table_detailed,invoice_transform_table_summary
from Utils.locationMapper import location_mapper
import pymupdf4llm
import json
from datetime import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv

MD_OUTPUTFILE_STORAGE_DIRECTORY = "generated_files\markdowns"
JSON_OUTPUTFILE_STORAGE_DIRECTORY = "generated_files"

# Secrets
load_dotenv()
OPENAI_APIKEY= os.getenv('OPENAI_API_KEY') 

# Instantiating client
client = OpenAI(api_key=OPENAI_APIKEY)

# Ensure the directory exists
os.makedirs(MD_OUTPUTFILE_STORAGE_DIRECTORY, exist_ok=True)

# Method to extract file content using OCR 
def extract_and_transform_from_pdf_for_llm(payload):
    file_path = payload['file_path']
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    md_filename = f"{timestamp}_{payload['filename']}.md"
    md_filepath = os.path.join(MD_OUTPUTFILE_STORAGE_DIRECTORY, md_filename)
    # Convert pdf to md
    md_text = pymupdf4llm.to_markdown(file_path)
    output = open(md_filepath, "w")
    output.write(md_text)
    output.close()
    payload['file_path_llm'] = md_filepath

    # From the markdown extract the required fields
    sum_result = invoice_transform_table_summary(payload=payload,client=client)
    detail_result = invoice_transform_table_detailed(payload=payload,client=client)
    payload['summary'] = sum_result
    payload['detailed'] = detail_result

    # Map pdf locations to the fields
    payload = location_mapper(payload)
    # Write to JSON
    # Define the path to save the JSON file with a unique timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    json_filename = f"{payload['filename'].replace('.pdf','')}_{timestamp}.json"
    json_filepath = os.path.join(JSON_OUTPUTFILE_STORAGE_DIRECTORY, json_filename)

    # Write the JSON response to the file
    with open(json_filepath, "w") as json_file:
        json.dump(payload, json_file, indent=4)
    return(payload)