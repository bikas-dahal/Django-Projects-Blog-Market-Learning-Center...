import google.generativeai as genai

from decouple import config


API_KEY = config('GEMINI_API_KEY')
print(API_KEY)

genai.configure(api_key=API_KEY)
# The Gemini 1.5 models are versatile and work with both text-only and multimodal prompts
model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("Write a story about a magic backpack.")
print(response.text)