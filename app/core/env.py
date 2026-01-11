from dotenv import load_dotenv
import os

load_dotenv()  # force load .env

# Optional debug (remove later)
print("AZURE_OPENAI_API_KEY loaded:", bool(os.getenv("AZURE_OPENAI_API_KEY")))