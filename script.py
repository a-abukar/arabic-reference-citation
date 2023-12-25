

# import openai
# import pyperclip
# import re
# from datetime import datetime, timedelta

# def get_clipboard_data():
#     # Retrieve text from clipboard
#     return pyperclip.paste()

# def find_hijri_date(text):
#     # Extract the day and month from the text
#     day_month_match = re.search(r'(\b[٠١٢٣٤٥٦٧٨٩]+) ذو الحجة', text)
#     # Extract the year from the text
#     year_match = re.search(r'\b([٠١٢٣٤٥٦٧٨٩]+)هـ\b', text)

#     if day_month_match and year_match:
#         day = int(day_month_match.group(1).translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')))
#         month = 12  # Dhu al-Hijjah is the 12th month
#         year = int(year_match.group(1).translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')))
#         print(f"Extracted Hijri Date: Year {year}, Month {month}, Day {day}")  # Debug print
#         return (year, month, day)
#     else:
#         print("No complete Hijri date match found in the text.")  # Debug print
#     return None

# def hijri_to_gregorian(year, month, day):
#     # Islamic calendar started in 622 AD (Gregorian), 1st Muharram
#     hijri_start = datetime(622, 7, 16)
    
#     # Average length of a lunar year is approximately 354.367 days
#     lunar_year = 354.367

#     # Calculate days passed in Hijri calendar
#     days_passed = (year - 1) * lunar_year + (month - 1) * 29.53059 + (day - 1)

#     # Convert to Gregorian date
#     gregorian_date = hijri_start + timedelta(days=round(days_passed))
#     return gregorian_date

# def create_citation_request(arabic_text):
#     # Create a more specific OpenAI API prompt for Chicago-style citation with Library of Congress transliteration
#     prompt = (f"Please provide a Chicago-style citation with Library of Congress transliteration "
#               f"for the following Arabic text. The citation should be in the format typically used "
#               f"in academic publications, with transliteration of Arabic names and terms. "
#               f"Exclude any translations of the text, or conversions of Hijri calendar. Just provide the citation in English.\n\nArabic Text: {arabic_text}")
#     return prompt

# def integrate_gregorian_date(citation, gregorian_date):
#     # Integrate the Gregorian date into the citation
#     return citation + f" (Gregorian date: {gregorian_date.strftime('%Y-%m-%d')})"

# def generate_citation(prompt):
#     # Calls the OpenAI API to generate the citation
#     try:
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=prompt,
#             max_tokens=150
#         )
#         return response.choices[0].text.strip()
#     except Exception as e:
#         print(f"Error in generating citation: {e}")
#         return None

# def main():
#     openai.api_key = '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'  # Replace with your OpenAI API key

#     arabic_text = get_clipboard_data()
#     print(f"Clipboard data: {arabic_text}")
#     hijri_date = find_hijri_date(arabic_text)
#     if hijri_date:
#         gregorian_date = hijri_to_gregorian(*hijri_date)
#         if gregorian_date:
#             prompt = create_citation_request(arabic_text)
#             citation = generate_citation(prompt)
#             if citation:
#                 full_citation = integrate_gregorian_date(citation, gregorian_date)
#                 print(full_citation)
#             else:
#                 print("No citation generated. Please check your input and try again.")
#         else:
#             print("Error in converting Hijri date.")
#     else:
#         print("No Hijri date found in the text.")

# if __name__ == "__main__":
#     main()


import openai
import pyperclip
import re
from datetime import datetime, timedelta

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

def main():
    openai.api_key = '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'  # Replace with your OpenAI API key

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
