# Arabic Reference Citation App

## Overview
The Arabic Reference Citation App is a Django-based web application designed to automatically generate Chicago-style citations for Arabic texts. Utilizing the power of OpenAI's GPT-4 model, the app provides precise and academically-formatted citations, including Library of Congress transliteration.

## Acess the live Application

[Arabic Reference Citation App](http://3.10.219.115:8000/)

## Features
- Extracts Hijri dates from the text and converts them to the Gregorian calendar.
- Generates citations based on a specific format required for academic publications.
- Incorporates both Arabic names and terms in the citation with proper transliteration.

## Local Setup

### Prerequisites
- Python 3.9 or higher
- pip and virtualenv
- OpenAI API key

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/a-abukar/arabic-reference-citation
   cd arabic-reference-citation
    ```

2. **Setup Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirement.txt
    ```

4. **Environment Variables**
    ```bash
    OPENAI_API_KEY=your_openai_api_key_here
    ```

5. **Run the application**
    ```bash
    python3 manage.py runserver
    ```

Access the application at http://127.0.0.1:8000/.

## Usage

To generate a citation:

- Enter the Arabic text in the provided form.
- Submit the form to receive the Chicago-style citation.

## Contributing

Contributions to improve the Arabic Reference Citation App are welcome. Please feel free to fork the repository and submit pull requests.

