# from vyzeai.tools.raw_functions import *
from pydantic import BaseModel, Field, EmailStr, AnyUrl, FilePath, StringConstraints
from enum import Enum
from wyge.tools.base_tool import add_function, Tool
from typing import List, Optional, Annotated, Dict, Any
import warnings
warnings.filterwarnings("ignore")

def extract_relevant_sections_from_website():
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        import re
        import requests
        from bs4 import BeautifulSoup
    except ImportError as e:
        raise ImportError(f"Required library for extract_relevant_sections_from_website is not installed: {e}. Please install it using `pip install youtube-transcript-api beautifulsoup4 requests`.")
    from wyge.tools.raw_functions import extract_relevant_sections_from_website as rf
    decorated_model = add_function(rf)(ExtractRelevantSectionsFromWebsite)
    tool = Tool(decorated_model)()
    return tool

#@add_function(extract_relevant_sections_from_website)
class ExtractRelevantSectionsFromWebsite(BaseModel):
    """This tool helps to extract specific sections from a website based on the given keywords."""
    url : AnyUrl = Field(description="URL of a website")
    keywords : List[str] = Field(description="A list of keywords(single word) used to find relevant content about a topic from a website. More keywords gives best result. ")
    class Config:
        protected_namespaces = ()

def post_on_twitter():
    try:
        import tweepy
    except ImportError as e:
        raise ImportError(f"Required library for post_on_twitter is not installed: {e}. Please install it using `pip install tweepy`.")
    from wyge.tools.raw_functions import post_on_twitter as rf
    decorated_model = add_function(rf)(PostOnTwitter)
    tool = Tool(decorated_model)()
    return tool

#@add_function(post_on_twitter)
class PostOnTwitter(BaseModel):
    """This tool helps to post a tweet on a specific Twitter account given their credentials."""
    tweet: str = Field(description="Twitter tweet content")
    consumer_key: str = Field(description="consumer_key - one of the four credentials")
    consumer_secret: str = Field(description="consumer_secret - one of the four credentials")
    access_token: str = Field(description="access_token - one of the four credentials")
    access_token_secret: str = Field(description="access_token_secret - one of the four credentials")

def post_on_linkedin():
    try:
        import requests
        import json
    except ImportError as e:
        raise ImportError(f"Required library for post_on_linkedin is not installed: {e}. Please install it using `pip install requests`.")
    from wyge.tools.raw_functions import post_on_linkedin as rf
    decorated_model = add_function(rf)(PostOnLinkedIn)
    tool = Tool(decorated_model)()
    return tool

#@add_function(post_on_linkedin)
class PostOnLinkedIn(BaseModel):
    """This tool helps to post on a specific LinkedIn account given his/her LinkedIn access token."""
    token: str = Field(description="LinkedIn access token")
    text_content: str = Field(description="LinkedIn post content")
    image_path: Optional[FilePath] = Field(default=None, description="Image path for the post")

def send_email():
    try:
        from email.mime.text import MIMEText
        import base64
        import os
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from email.mime.multipart import MIMEMultipart
    except ImportError as e:
        raise ImportError(f"Required library for send_email is not installed: {e}. Please install it using `pip install google-auth google-auth-oauthlib google-auth-httplib2`.")

    from wyge.tools.raw_functions import send_email as rf
    decorated_model = add_function(rf)(SendEmail)
    tool = Tool(decorated_model)()
    return tool

#@add_function(send_email)
class SendEmail(BaseModel):
    """This tool helps to send an email."""
    to_email: EmailStr = Field(description="Receiver email address")
    subject: str = Field(description="Email subject")
    body: str = Field(description="Email content")
    attachments: List = Field(default=None, description="A list of attachments(file paths) to send in mail, example: doc files, images, videos")
    credentials_json_file_path: Optional[FilePath] = Field(
        default='credentials.json', description="The file path to the JSON file containing the sender's email credentials."
    )
    token_json_file_path: Optional[FilePath] = Field(
        default='token.json', description="The file path to the JSON file containing the OAuth token for authentication."
    )

def upload_to_drive():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError as e:
        raise ImportError(f"Required library for upload_to_drive is not installed: {e}. Please install it using `pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`.")
    from wyge.tools.raw_functions import upload_to_drive as rf
    decorated_model = add_function(rf)(UploadToDrive)
    tool = Tool(decorated_model)()
    return tool

#@add_function(upload_to_drive)
class UploadToDrive(BaseModel):
    """This tool helps upload a file to Google Drive."""
    filepath: FilePath = Field(description="The path to the file to be uploaded.")
    filename: str = Field(description="The desired name for the file in Google Drive.")
    parent_folder_id: str = Field(description="The ID of the parent folder in Google Drive where the file will be uploaded.")
    service_account_file_path: Optional[FilePath] = Field(
        default='service_account.json', description="The path to the service account JSON file for authentication."
    )

def convert_md_to_docx():
    try:
        import pypandoc
    except ImportError as e:
        raise ImportError(f"Required library for convert_md_to_docx is not installed: {e}. Please install it using `pip install pypandoc`. Additionally, pypandoc requires Pandoc to be installed on your system")
    from wyge.tools.raw_functions import convert_md_to_docx as rf
    decorated_model = add_function(rf)(ConvertMDToDocx)
    tool = Tool(decorated_model)()
    return tool

#@add_function(convert_md_to_docx)
class ConvertMDToDocx(BaseModel):
    """Model for converting a Markdown file to a DOCX file."""
    md_file_path: FilePath = Field(description="The path to the Markdown file to be converted.")
    docx_file_path: FilePath = Field(description="The path where the converted DOCX file will be saved.")

class ModelName(Enum):
    """Enum for the available OpenAI models."""
    DALL_E_2 = "dall-e-2"
    DALL_E_3 = "dall-e-3"

class Quality(Enum):
    """Enum for the available image qualities."""
    STANDARD = "standard"
    HD = "hd"

def generate_image_openai():
    try:
        import tempfile
        from openai import OpenAI
        import requests
    except ImportError as e:
        raise ImportError(f"Required library for generate_image_openai is not installed: {e}. Please install it using `pip install requests openai`.")
    from wyge.tools.raw_functions import generate_image_openai as rf
    decorated_model = add_function(rf)(GenerateImageOpenAI)
    tool = Tool(decorated_model)()
    return tool

#@add_function(generate_image_openai)
class GenerateImageOpenAI(BaseModel):
    """Model for generating an image using OpenAI's image generation API."""
    text: str = Field(description="The text prompt for generating the image.")
    openai_api_key: Optional[str] = Field(description="The OpenAI API key for authentication.")
    model_name: Optional[ModelName] = Field(default=ModelName.DALL_E_2, description="The name of the OpenAI image generation model.")
    resolution: Optional[Annotated[str, StringConstraints(pattern=r'^\d+x\d+$')]] = Field(default="512x512", description="The resolution of the generated image, e.g., ['256x256', '512x512', '1024x1024', '1024x1792', '1792x1024'].")
    save_temp: Optional[bool] = Field(default=False, description="if True, files and images are stored temporarily. (always prefer False, unless specified)")

# # class GenerateImageOpenAIModel(BaseModel):
# #     """Model for generating an image using OpenAI's image generation API."""
# #     text: str = Field(description="The text prompt for generating the image.")
# #     same_temp: Optional[bool] = Field(default=False, description="Whether to use a temporary file for the output image.")
# #     model_name: Optional[str] = Field(default="dall-e-2", description="The name of the OpenAI image generation model.")
# #     resolution: Optional[constr(regex=r'^\d+x\d+$')] = Field(default="512x512", description="The resolution of the generated image, e.g., '512x512'.")
# #     quality: Optional[str] = Field(default='standard', description="The quality of the generated image.")
# #     n: Optional[conint(ge=1)] = Field(default=1, description="The number of images to generate.")

def generate_images_and_add_to_blog():
    from wyge.tools.raw_functions import generate_images_and_add_to_blog as rf
    decorated_model = add_function(rf)(AddImagesToBlog)
    tool = Tool(decorated_model)()
    return tool

# @add_function(generate_images_and_add_to_blog)
class AddImagesToBlog(BaseModel):
    """This tool helps to generate images and add them to blog. Blog should contain image prompts in <image> prompt </image> tag."""
    blog_content : str = Field(description="content of a blog")
    save_temp : Optional[bool] = Field(False, description="if True, files and images are stored temporarily. (always prefer False, unless specified)")

def generate_video():
    try:
        import tempfile
        from openai import OpenAI
        import requests
        import os
        import numpy as np
        import cv2
        from PIL import Image, ImageDraw, ImageFont
        from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip
    except ImportError as e:
        raise ImportError(f"Required library for generate_video is not installed: {e}. Please install it using `pip install openai requests numpy opencv-python Pillow moviepy`.")
    from wyge.tools.raw_functions import generate_video as rf
    decorated_model = add_function(rf)(GenerateVideo)
    tool = Tool(decorated_model)()
    return tool

#@add_function(generate_video)
class GenerateVideo(BaseModel):
    """Given image prompt pairs and narration pairs, this tool helps to generate a video.
    Images are generated using image prompts and speech is generated using narration prompts."""
    pairs: str = Field(description="A string of narration and image prompt pairs enclosed in <narration> and <image> tags.")
    final_video_filename: Optional[str] = Field(default='video.mp4', description="Final video file name used to save the video.")

def extract_audio_from_video():
    try:
        from moviepy.editor import VideoFileClip
        import tempfile
    except ImportError as e:
        raise ImportError(f"Required library for extract_audio_from_video is not installed: {e}. Please install it using `pip install moviepy`.")
    from wyge.tools.raw_functions import extract_audio_from_video as rf
    decorated_model = add_function(rf)(ExtractAudioFromVideo)
    tool = Tool(decorated_model)()
    return tool

#@add_function(extract_audio_from_video)
class ExtractAudioFromVideo(BaseModel):
    """This tool is used for extracting audio from a video."""
    video_path: FilePath = Field(description="The path to the video file from which to extract audio.")

def transcribe_audio():
    try:
        from openai import OpenAI
    except ImportError as e:
        raise ImportError(f"Required library for transcribe_audio is not installed: {e}. Please install it using `pip install openai`.")
    from wyge.tools.raw_functions import transcribe_audio as rf
    decorated_model = add_function(rf)(TranscribeAudio)
    tool = Tool(decorated_model)()
    return tool

#@add_function(transcribe_audio)
class TranscribeAudio(BaseModel):
    """This tool is used for transcribing audio using OpenAI Whisper."""
    audio_file_path: FilePath = Field(description="The path to the audio file for transcription.")

def youtube_transcript_loader():
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError as e:
        raise ImportError(f"Required library for youtube_transcript_loader is not installed: {e}. Please install it using `pip install youtube_transcript_api`.")
    from wyge.tools.raw_functions import youtube_transcript_loader as rf
    decorated_model = add_function(rf)(YouTubeTranscriptLoader)
    tool = Tool(decorated_model)()
    return tool

#@add_function(youtube_transcript_loader)
class YouTubeTranscriptLoader(BaseModel):
    """This tool helps to load transcript of a YouTube video."""
    url: AnyUrl = Field(description="YouTube video URL.")

def wikipedia_search():
    try:
        import wikipedia
        import wikipediaapi
    except ImportError as e:
        raise ImportError(f"Required library for Wikipedia search is not installed: {e}. Please install it using `pip install wikipedia wikipedia-api`.")
    from wyge.tools.raw_functions import wikipedia_search as rf
    decorated_model = add_function(rf)(WikipediaSearch)
    tool = Tool(decorated_model)()
    return tool

#@add_function(search_multiple_wikipedia_pages)
class WikipediaSearch(BaseModel):
    """Search multiple Wikipedia pages based on a query and return summaries or full content."""
    query: str = Field(..., description="Search term for querying Wikipedia.")
    lang: str = Field(default="en", description="Language of Wikipedia to query, default is 'en' for English.")
    result_count: int = Field(default=3, description="Number of search results to return, default is 3.")
    full_content: bool = Field(default=False, description="Whether to return full page content or just summary, default is summary.")

def calculate():
    from wyge.tools.raw_functions import calculate as rf
    decorated_model = add_function(rf)(Calculate)
    tool = Tool(decorated_model)()
    return tool

#@add_function(calculate)
class Calculate(BaseModel):
    """This tool is used to evaluate a mathematical expression."""
    operation: str = Field(..., description="Mathematical expression to evaluate (no symbols or text allowed).")

# @add_function(excel_to_sql)
class ExcelToSQL(BaseModel):
    """
    Model for storing Excel data into a SQL table.
    
    Attributes:
    - excel_file_path: Path to the Excel file.
    - table_name: Name of the SQL table where data will be stored.
    """
    excel_file_path: str = Field(..., description="Path to the Excel file")
    table_name: str = Field(..., description="Name of the table to store data")
    user: str = Field(..., description="Username for the MySQL connection")
    password: str = Field(..., description="Password for the MySQL connection")
    host: str = Field(..., description="Hostname or IP address of the MySQL server")
    db_name: str = Field(..., description="Database name")

def excel_to_sql():
    from wyge.tools.raw_functions import excel_to_sql as rf
    decorated_model = add_function(rf)(ExcelToSQL)
    tool = Tool(decorated_model)()
    return tool

# @add_function(execute_query)
class QueryExecution(BaseModel):
    """
    Model for executing a SQL query.
    
    Attributes:
    - query: The SQL query to execute.
    """
    query: str = Field(..., description="SQL query string to be executed")
    user: str = Field(..., description="Username for the MySQL connection")
    password: str = Field(..., description="Password for the MySQL connection")
    host: str = Field(..., description="Hostname or IP address of the MySQL server")
    db_name: str = Field(..., description="Database name")

    class Config:
        arbitrary_types_allowed = True

def execute_query():
    from wyge.tools.raw_functions import execute_query as rf
    decorated_model = add_function(rf)(QueryExecution)
    tool = Tool(decorated_model)()
    return tool

# @add_function(execute_code_parts)
class PythonCodeExecution(BaseModel):
    """
    A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.

    Usage:
        - To execute a single-line command:
            run(command="print('Hello, World!')")
        
        - To execute a multi-line command:
            run(command=\"\"\"  # Use triple quotes for multi-line strings
                for i in range(3):
                    print(i)
                \"\"\")
    """
    command: str = Field(..., description="The Python code to execute. This should be a valid Python expression or statement. Ensure to handle multi-line statements appropriately by using proper indentation and `print(...)` for output.")
    timeout: Optional[int] = Field(
        None, description="Maximum allowed execution time in seconds. Defaults to None."
    )

def execute_code():
    from wyge.tools.python_repl import repl_tool as rf
    decorated_model = add_function(rf.run)(PythonCodeExecution)
    tool = Tool(decorated_model)()
    return tool

# @add_function(install_library)
class InstallLibrary(BaseModel):
    """
    Installs the required library using pip.
    """
    library_name: str = Field(description="Name of the library to install.")

def install_library():
    from wyge.tools.raw_functions import install_library as rf
    decorated_model = add_function(rf)(InstallLibrary)
    tool = Tool(decorated_model)()
    return tool

