import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path = '.env')
token = os.getenv('VK_API_SERVICE_TOKEN')
version = os.getenv('VK_API_VERSION')
url = os.getenv('URL')