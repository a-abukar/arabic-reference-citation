import openai
import pyperclip
import re
from datetime import datetime, timedelta

def get_clipboard_data():
    return pyperclip.paste()

def find_hijri_date(text):
    day_month_match = re.search(r'(\b[٠١٢٣٤٥٦٧٨٩]+) ذو الحجة', text)
    year_match = re.search(r'\b([٠١٢٣٤٥٦٧٨٩]+)هـ\b', text)

    if day_month_match and year_match:
        day = int(day_month_match.group(1).translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')))
        month = 12  
        year = int(year_match.group(1).translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')))
        print(f"Extracted Hijri Date: Year {year}, Month {month}, Day {day}")
        return (year, month, day)
    return None

def hijri_to_gregorian(year, month, day):
    hijri_start = datetime(622, 7, 16)
    lunar_year = 354.367
    days_passed = (year - 1) * lunar_year + (month - 1) * 29.53059 + (day - 1)
    gregorian_date = hijri_start + timedelta(days=round(days_passed))
    return gregorian_date

def create_citation_request(arabic_text):
    prompt = (f"Please provide an exact Chicago-style citation with Library of Congress transliteration "
              f"for the following Arabic text. The citation should be in the format typically used "
              f"in academic publications, with transliteration of Arabic names and terms. "
              f"Exclude any translations of the text. Also exclude ANY conversions of Hijri calendar, and do not include any mention of this in your response. Just provide the citation in English.\n\nArabic Text: {arabic_text}")
    return prompt

def integrate_gregorian_date(citation, gregorian_date):
    return citation + f" (Gregorian date: {gregorian_date.strftime('%Y-%m-%d')})"

def generate_citation(prompt):
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
        last_response = response['choices'][0]['message']['content'].strip()
        return last_response
    except Exception as e:
        print(f"Error in generating citation: {e}")
        return None

def main():
    openai.api_key = '' 

    arabic_text = get_clipboard_data()
    hijri_date = find_hijri_date(arabic_text)
    full_citation = ""
    if hijri_date:
        gregorian_date = hijri_to_gregorian(*hijri_date)
        if gregorian_date:
            prompt = create_citation_request(arabic_text)
            citation = generate_citation(prompt)
            if citation:
                full_citation = integrate_gregorian_date(citation, gregorian_date)
    else:
        prompt = create_citation_request(arabic_text)
        citation = generate_citation(prompt)
        if citation:
            full_citation = citation

    if full_citation:
        print(full_citation)
    else:
        print("No citation generated.")

if __name__ == "__main__":
    main()