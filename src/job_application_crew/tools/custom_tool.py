import os
import re
import shutil
from datetime import datetime
from typing import Type
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

# Load environment variables from .env file for API keys and configuration
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))
load_dotenv(dotenv_path=dotenv_path)

openai_key = os.getenv("OPENAI_API_KEY")
