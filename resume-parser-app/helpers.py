import os
import re
import json
import PyPDF2
import google.generativeai as genai

def extract_text_from_pdf(pdf_file_stream):
    """
    Extracts text from a PDF file stream.
    """
    try:
        reader = PyPDF2.PdfReader(pdf_file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    
def get_gemini_response(resume_text):
    """
    Sends the resume text to the Gemini API and gets the structured data.
    """
    # Configure the API key from environment variables
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    except Exception as e:
        raise ValueError("Failed to configure Google AI. Is the GOOGLE_API_KEY set correctly in your .env file?") from e
        
    # Load the generative model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # The updated prompt including the 'projects' section
    final_prompt = f"""
    You are a highly skilled information extraction system.
    Your task is to meticulously analyze the following resume and return a single, valid JSON object.
    Do not include any text or markdown formatting before or after the JSON object.

    The JSON object must contain the following fields:
    - name (string)
    - surname (string)
    - phone_number (string, or null if not found)
    - email (string, or null if not found)
    - location (string, e.g. "City, Country", or null if not found)
    - certificates (list of strings, should be an empty list [] if none are found)
    - experience (list of objects, each with:
        - job_title (string)
        - company (string)
        - start_date (string or null if not available)
        - end_date (string or "Present" if ongoing, or null if not available)
        - description (string summarizing responsibilities)
      )
    - projects (list of objects, each with:
        - title (string)
        - description (string summarizing the project)
        - technologies (list of strings, empty if not available)
      )

    If a field is missing in the resume, return it as null for strings or an empty list for lists.
    Do not skip any fields. Ensure the output is only the JSON.

    Resume text:
    ---
    {resume_text}
    ---
    """

    try:
        response = model.generate_content(final_prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None
    
def clean_and_parse_json(response_text):
    """
    Cleans a JSON-like string that might be wrapped in markdown and parses it.
    """
    # Find the start and end of the JSON object
    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if not match:
        raise ValueError("No valid JSON object found in the model's response.")
    
    json_str = match.group(0)
    
    # Parse the JSON string into a Python dictionary
    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON from the model's response: {e}") from e