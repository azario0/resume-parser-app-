import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from helpers import extract_text_from_pdf, get_gemini_response, clean_and_parse_json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# A secret key is needed for flashing messages
app.secret_key = 'supersecretkey' 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB max upload size

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'resume' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['resume']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file. Please choose a PDF to upload.')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # 1. Extract text from the uploaded PDF
                resume_text = extract_text_from_pdf(file.stream)
                if not resume_text:
                    flash('Could not extract text from the PDF. The file might be empty, corrupted, or image-based.')
                    return redirect(request.url)

                # 2. Get the structured data from Gemini API
                api_response = get_gemini_response(resume_text)
                if not api_response:
                    flash('Error communicating with the AI model. Please check your API key and try again.')
                    return redirect(request.url)

                # 3. Clean and parse the JSON response
                extracted_data = clean_and_parse_json(api_response)

                # 4. Render the page with the extracted data
                return render_template('index.html', data=extracted_data)

            except Exception as e:
                flash(f'An error occurred: {str(e)}')
                return redirect(request.url)

        else:
            flash('Invalid file type. Please upload a PDF file.')
            return redirect(request.url)
            
    # For GET requests, just show the upload page
    return render_template('index.html', data=None)

if __name__ == '__main__':
    app.run(debug=True)