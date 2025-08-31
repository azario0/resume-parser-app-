# AI Resume Parser

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern Flask web application that uses the Google Gemini API to intelligently extract and display structured information from PDF resumes. Upload a resume, and the app will parse details like contact information, work experience, projects, and certifications into a clean, easy-to-read format.

## Features

-   **PDF Upload:** Simple drag-and-drop or file selection interface for uploading resumes.
-   **AI-Powered Extraction:** Leverages the `gemini-1.5-flash` model to accurately parse unstructured resume text.
-   **Structured Data Output:** Extracts the following fields:
    -   Full Name & Contact Info (Email, Phone, Location)
    -   Work Experience (Job Title, Company, Dates, Description)
    -   Projects (Title, Description, Technologies Used)
    -   Certifications
-   **Clean UI:** Presents the extracted data in a professional and responsive web interface.
-   **Secure:** Keeps your Google API key safe using environment variables.

## Tech Stack

-   **Backend:** Python, Flask
-   **AI Model:** Google Gemini
-   **PDF Processing:** PyPDF2
-   **Frontend:** HTML5, CSS3
-   **Environment Variables:** python-dotenv

## Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

-   Python 3.8+
-   A Google AI API Key. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/azario0/resume-parser-app.git
    cd resume-parser-app
    ```

2.  **Create and activate a virtual environment:**
    -   On macOS/Linux:
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```
    -   On Windows:
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure your API Key:**
    -   Create a new file named `.env` in the root of the project directory.
    -   Add your Google AI API key to this file:
        ```
        GOOGLE_API_KEY="YOUR_GOOGLE_AI_API_KEY"
        ```


### Running the Application

1.  **Start the Flask server:**
    ```sh
    flask run
    ```

2.  **Open the application in your browser:**
    Navigate to `http://127.0.0.1:5000`

## Project Structure

/resume-parser-app
|-- app.py                    # Main Flask application logic
|-- helpers.py                # Helper functions for PDF, Gemini API, and JSON
|-- requirements.txt          # Python dependencies
|-- .env                      # For storing the API key (create this yourself)
|-- .gitignore                # Files to be ignored by Git
|-- templates/
|   |-- index.html            # Main HTML template for the UI
|-- static/
|   |-- css/style.css         # Custom stylesheets
|   |-- img/upload-icon.svg   # UI icon
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Crafted by **[azario0](https://github.com/azario0)**