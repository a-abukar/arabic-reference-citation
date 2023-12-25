from django.shortcuts import render
from .forms import TextForm
import openai
import pyperclip
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

def get_clipboard_data():
    # Retrieve text from clipboard
    return pyperclip.paste()

def find_hijri_date(text):
    # Extract the day and month from the text
    day_month_match = re.search(r'(\b[٠١٢٣٤٥٦٧٨٩]+) ذو الحجة', text)
    # Extract the year from the text
    year_match = re.search(r'\b([٠١٢٣٤٥٦٧٨٩]+)هـ\b', text)

    if day_month_match and year_match:
        day = int(day_month_match.group(1).translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')))
        month = 12  # Dhu al-Hijjah is the 12th month
        year = int(year_match.group(1).translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')))
        print(f"Extracted Hijri Date: Year {year}, Month {month}, Day {day}")
        return (year, month, day)
    return None

def hijri_to_gregorian(year, month, day):
    # Islamic calendar started in 622 AD (Gregorian), 1st Muharram
    hijri_start = datetime(622, 7, 16)
    # Average length of a lunar year is approximately 354.367 days
    lunar_year = 354.367
    # Calculate days passed in Hijri calendar
    days_passed = (year - 1) * lunar_year + (month - 1) * 29.53059 + (day - 1)
    # Convert to Gregorian date
    gregorian_date = hijri_start + timedelta(days=round(days_passed))
    return gregorian_date

def create_citation_request(arabic_text):
    # Create a more specific OpenAI API prompt for Chicago-style citation with Library of Congress transliteration
    prompt = (f"Please provide an exact Chicago-style citation with Library of Congress transliteration "
              f"for the following Arabic text. The citation should be in the format typically used "
              f"in academic publications, with transliteration of Arabic names and terms. "
              f"The format should be like this: <Last name>, <first name/s>. <Name of title>, ed. <Name of editor/s>, <number of volts>.vols. <City of print>:<Publisher>, <Year of print>"
              f"Exclude any translations of the text. Also exclude ANY conversions of Hijri calendar, and do not include any mention of this in your response. Just provide the citation in English.\n\nArabic Text: {arabic_text}")
    return prompt

def integrate_gregorian_date(citation, gregorian_date):
    # Integrate the Gregorian date into the citation
    return citation + f" (Gregorian date: {gregorian_date.strftime('%Y-%m-%d')})"

def generate_citation(prompt):
    # Calls the OpenAI API to generate the citation
    print("Requesting citation from OpenAI...")
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=150
        )
        # The response structure is different for ChatCompletion
        last_response = response['choices'][0]['message']['content'].strip()
        return last_response
    except Exception as e:
        print(f"Error in generating citation: {e}")
        return None

def main(text):
    openai.api_key = os.getenv('OPENAI_API_KEY')  # Replace with your OpenAI API key

    # Initialize full_citation
    full_citation = None

    hijri_date = find_hijri_date(text)
    if hijri_date:
        gregorian_date = hijri_to_gregorian(*hijri_date)
        prompt = create_citation_request(text)
        citation = generate_citation(prompt)
        if citation:
            full_citation = integrate_gregorian_date(citation, gregorian_date)

    else:
        prompt = create_citation_request(text)
        citation = generate_citation(prompt)
        if citation:
            full_citation = citation

    if full_citation:
        print(full_citation)
        return full_citation
    else:
        print("No citation generated.")
        return None


# if __name__ == "__main__":
#     main()




def citation_view(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            # Call your script functions here with the text
            result = main(text)  # Assume main() is your script's entry point
            return render(request, 'result.html', {'result': result})
    else:
        form = TextForm()

    return render(request, 'index.html', {'form': form})

