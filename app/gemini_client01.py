from google import genai
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

client = genai.Client(api_key="....")

response = client.models.generate_content(
  model = "gemini-2.5-flash", 
  contents = "오늘 날씨 알려줘"
)
print(response.text)