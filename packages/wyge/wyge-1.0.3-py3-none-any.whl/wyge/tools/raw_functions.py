# from bs4 import BeautifulSoup
# from langchain_community.document_loaders import YoutubeLoader
# import re
# import tweepy
# import requests
# import json
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from email.mime.text import MIMEText
# import base64
# import os
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from email.mime.multipart import MIMEMultipart
# import pypandoc
# import tempfile
# import cv2
# import numpy as np
# from openai import OpenAI
# from pydub import AudioSegment
# from PIL import Image, ImageDraw, ImageFont
# from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip
# import wikipedia
# import wikipediaapi
import warnings
warnings.filterwarnings('ignore')

def extract_sections(url):
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    sections = []
    for link in soup.find_all('a', href=True):
        sections.append({
            'text': link.get_text().strip(),
            'url': link['href']
        })
        
    return sections

def filter_relevant_sections(sections, keywords):
    relevant_sections = []
    for section in sections:
        if any(keyword.lower() in section['text'].lower() for keyword in keywords):
            relevant_sections.append(section)
    
    return relevant_sections

def filter_youtube_links(sections, keywords):
    youtube_sections = []
    for section in sections:
        if 'youtube' not in section['url']:
            sections.remove()

def gather_info_from_sections(relevant_sections):
    import requests
    from bs4 import BeautifulSoup

    content = {}
    for section in relevant_sections:
        try:
            response = requests.get(section['url'])
            soup = BeautifulSoup(response.content, 'html.parser')
            clean_text = clean_scraped_text(soup.get_text())
            content[section['url']] = clean_text
        except Exception as e:
            # print(e)
            pass
    
    return content

def clean_scraped_text(text):
    import re

    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)

    patterns = [
        r'Home\s+About Us.*?\s+Contact Us',
        r'This website uses cookies.*?Privacy & Cookies Policy',  
        r'Copyright.*?Powered by.*',  
    ]

    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)

    text = re.sub(r'\|.*?\|', '', text)  
    text = text.strip()  

    return text

def youtube_transcript_loader(url):
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        video_id = url.split('/')[-1].split('=')[-1]
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])

        if transcript is None:
            raise ValueError('No English transcript found for video: {}'.format(video_id))

        list_t =  transcript.fetch()
    
        transcript_text = ""
        for transcript in list_t:
            transcript_text += transcript['text'] + " "
        return transcript_text
    except Exception as e:
        return f"Error: {e}"
        # raise str(Exception(f"Error: {e}"))
    
def gather_youtube_data(sections, keywords):

    youtube_sections = []
    for i, section in enumerate(sections):
        if 'youtube' in section['url']:
            youtube_sections.append(section)

    content = {}
    for section in youtube_sections:
        text = youtube_transcript_loader(section['url'])
        if text is not None:
            content[section['url']] = text

    relevant_content = {}
    for k, v in content.items():
        if any(keyword.lower() in v.lower() for keyword in keywords):
            relevant_content[k] = v

    return relevant_content

def extract_relevant_sections_from_website(url, keywords):

    sections = extract_sections(url)
    filtered_sections = filter_relevant_sections(sections, keywords)
    gathered_info = gather_info_from_sections(filtered_sections)
    youtube_info = gather_youtube_data(sections, keywords)
    total_info = gathered_info | youtube_info
    refined_info = {url: text for url, text in total_info.items() if len(text) > 200}  # Example threshold for content length
    return refined_info

# twitter

def post_on_twitter(tweet, consumer_key, consumer_secret, access_token, access_token_secret):
    import tweepy
    try:
        client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, 
                        access_token=access_token, access_token_secret=access_token_secret)
    
        tweet = tweet.strip('"')
        res = client.create_tweet(text=tweet)
        return 'Twitter tweet generated and posted to user twitter account successfully'
    except Exception as e:
        return Exception(f"Failed to tweet: {e}")
    
# linkedin

def escape_text(text):
    chars = ["\\", "|", "{", "}", "@", "[", "]", "(", ")", "<", ">", "#", "*", "_", "~"]
    for char in chars:
        text = text.replace(char, "\\"+char)
    return text

def get_urn(token):
    import requests

    url = 'https://api.linkedin.com/v2/userinfo'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        # print(user_info['sub'])
        return user_info['sub']
    else:
        print(f'Failed to fetch user info: {response.status_code}')
        # print(response.text)

def post_on_linkedin(token, text_content, image_path=None):
    """
    Posts an article on LinkedIn with or without an image.

    Args:
    token: LinkedIn OAuth token.
    title: LinkedIn post title.
    text_content: LinkedIn post content.
    image_path: file path of the image (optional).
    """
    import requests
    import json

    title = ""
    text_content = escape_text(text_content)
    owner = get_urn(token)

    # If an image is provided, initialize upload and post with image
    if image_path:
        if image_path.startswith('sandbox'):
            image_path = image_path.split(':')[1].strip()

        # Initialize the upload to get the upload URL and image URN
        init_url = "https://api.linkedin.com/rest/images?action=initializeUpload"
        headers = {
            "LinkedIn-Version": "202401",
            "X-RestLi-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        init_data = json.dumps({"initializeUploadRequest": {"owner": f'urn:li:person:{owner}'}})
        init_response = requests.post(init_url, headers=headers, data=init_data)

        if init_response.status_code != 200:
            raise str(Exception(f"Failed to initialize upload: {init_response.text}"))

        init_response_data = init_response.json()["value"]
        upload_url = init_response_data["uploadUrl"]
        image_urn = init_response_data["image"]

        # Upload the file
        with open(image_path, "rb") as f:
            upload_response = requests.post(upload_url, files={"file": f})
            if upload_response.status_code not in [200, 201]:
                raise str(Exception(f"Failed to upload file: {upload_response.text}"))

        # Create the post with the uploaded image URN as thumbnail
        post_data = json.dumps({
            "author": f'urn:li:person:{owner}',
            "commentary": text_content,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "content": {
                "media": {
                    "title": title,
                    "id": image_urn,
                }
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        })
    else:
        # Create a post without image
        post_data = json.dumps({
            "author": f'urn:li:person:{owner}',
            "commentary": text_content,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        })

    # Send the post request
    post_url = "https://api.linkedin.com/rest/posts"
    headers = {
        "LinkedIn-Version": "202401",
        "X-RestLi-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    post_response = requests.post(post_url, headers=headers, data=post_data)

    if post_response.status_code in [200, 201]:
        return "Linkedin article has been posted successfully!"
    else:
        raise str(Exception(f"Failed to post article: {post_response.text}"))

SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive']

def authenticate_drive(service_account_file_path):
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file_path, scopes=SCOPES_DRIVE)
    return credentials

def upload_to_drive(filepath, filename, parent_folder_id, service_account_file_path='service_account.json'):
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    creds = authenticate_drive(service_account_file_path)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': filename,
        'parents': [parent_folder_id]
    }

    media = MediaFileUpload(filepath, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

SCOPES_EMAIL_SEND = ["https://www.googleapis.com/auth/gmail.send"]

def authenticate_gmail(credentials_json_file_path=None, token_json_file_path=None):
    """Authenticate and return the Gmail service."""
    import os
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    creds = None
    if os.path.exists(token_json_file_path):
        creds = Credentials.from_authorized_user_file(token_json_file_path, SCOPES_EMAIL_SEND)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_json_file_path, SCOPES_EMAIL_SEND)
            creds = flow.run_local_server(port=0)
        with open(token_json_file_path, "w") as token:
            token.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    return service

def send_email(to_email, subject, body, attachments=None, credentials_json_file_path='credentials.json', token_json_file_path='token.json'):
    """Tool to send email with attachments."""
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    import base64
    import os

    try:
        # Create a multipart message and set headers
        msg = MIMEMultipart()
        msg['to'] = to_email
        msg['subject'] = subject

        # Add the HTML body to the email
        msg.attach(MIMEText(body, 'html'))

        # Add attachments, if provided
        if attachments:
            for attachment in attachments:
                filename = os.path.basename(attachment)  # Get the file name
                with open(attachment, 'rb') as attachment_file:
                    part = MIMEBase('application', 'octet-stream')  # For generic binary attachments
                    part.set_payload(attachment_file.read())
                
                encoders.encode_base64(part)  # Encode to base64
                
                # Add the header for attachment
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={filename}',
                )
                
                # Attach the file to the message
                msg.attach(part)

        # Encode the message to base64
        raw_string = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        # Send the email using Gmail API
        service = authenticate_gmail(credentials_json_file_path, token_json_file_path)
        sent_message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()

        print(sent_message)
        print('Email sent successfully!')
        return 'Email sent successfully!'
    except Exception as e:
        raise str(Exception(f'Error sending email: {str(e)}'))
    
def convert_md_to_docx(md_file_path, docx_file_path):
    import pypandoc

    output = pypandoc.convert_file(md_file_path, 'docx', outputfile=docx_file_path)
    assert output == "", "Conversion failed"
    # print(f"Converted {md_file_path} to {docx_file_path}")

def generate_image_openai(text, openai_api_key=None, model_name="dall-e-2", resolution="512x512", quality='standard', n=1, save_temp = False, _i=1):
    import tempfile
    from openai import OpenAI
    import requests
    import os
    
    output_image = f'image_{_i}.png'
    if save_temp:
        temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        output_image = temp_output_file.name

    api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
    print(api_key)
    client = OpenAI(api_key=api_key)

    try:
        response = client.images.generate(
            model=model_name,
            prompt=text,
            size=resolution,
            quality=quality,
            n=n
        )
        image_url = response.data[0].url
        # print(image_url)

        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(output_image, 'wb') as file:
                file.write(image_response.content)
        else:
            raise str(Exception(f"Failed to download image with status code {image_response.status_code} and message: {image_response.text}"))

    except Exception as e:
        print(e)
        raise str(Exception(f"Image generation failed: {e}"))

    return output_image

def generate_images_and_add_to_blog(blog_content, save_temp=False):
    """This tool is used to generate images and add them to blog
    Args:
    blog_content: A complete blog with image prompts enclosed in <image> prompt </image> tag.
    Returns:
    A complete blog"""
    import tempfile
    import os
    import re
    import base64

    blog_content = str(blog_content)
    # print(f"****************\n{blog_content}\n**********")
    image_descriptions = re.findall(r'<image>(.*?)</image>', blog_content)
    
    md_file_path = 'blog_post.md'
    docx_file_path = 'blog_post.docx'
    if save_temp:
        temp_folder = tempfile.gettempdir()
        md_file_path = os.path.join(temp_folder, 'blog_post.md')
        docx_file_path = os.path.join(temp_folder, 'blog_post.docx')
    
    if os.path.exists(md_file_path):
        os.remove(md_file_path)
    if os.path.exists(docx_file_path):
        os.remove(docx_file_path)
    
    print(image_descriptions)
    images = []
    # base64_images = []
    for i, text in enumerate(image_descriptions):
        try:
            img_path = generate_image_openai(text,save_temp=save_temp, _i=i)
            print("image_generated")
            blog_content = blog_content.replace(f'<image>{text}</image>', f'![]({img_path})')
            images.append(img_path)
            
            # with open(img_path, 'rb') as img_file:
            #     base64_encoded = base64.b64encode(img_file.read()).decode('utf-8')
            #     base64_images.append(base64_encoded)
        except Exception as e:
            raise str(Exception(f"Image generation failed: {e}"))

    try:
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(blog_content)
        
        convert_md_to_docx(md_file_path, docx_file_path)
        # print(f"Markdown file saved at: {md_file_path}")
        # print(f"Document file saved at: {docx_file_path}")
    except Exception as error:
        print(error)
    
    return blog_content, docx_file_path, images

def process_script(script):
    """Used to process the script into dictionary format"""
    import re
    dict = {}
    text_for_image_generation = re.findall(r'<image>(.*?)</?image>', script, re.DOTALL)
    text_for_speech_generation = re.findall(r'<narration>(.*?)</?narration>', script, re.DOTALL)
    dict['text_for_image_generation'] = text_for_image_generation
    dict['text_for_speech_generation'] = text_for_speech_generation
    return dict

def generate_speech(text, lang='en', speed=1.0, num=0):
    """
    Generates speech for the given script using gTTS and adjusts the speed.
    """
    from openai import OpenAI
    import tempfile
    from pydub import AudioSegment

    temp_speech_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_speech_path = temp_speech_file.name

    
    client = OpenAI()

    speech_file_path = temp_speech_path
    response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    input= text
    )

    response.stream_to_file(speech_file_path)

    sound = AudioSegment.from_file(temp_speech_path)
    if speed != 1.0:
        sound_with_altered_speed = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed)
        }).set_frame_rate(sound.frame_rate)
        sound_with_altered_speed.export(temp_speech_path, format="mp3")
    else:
        sound.export(temp_speech_path, format="mp3")

    temp_speech_file.close()
    return temp_speech_path

def image_generator(script):
    """Generates images for the given script.
    Saves it to a temporary directory and returns the path.
    Args:
    script: a complete script containing narrations and image descriptions."""
    
    import tempfile
    from openai import OpenAI
    import requests
    import os

    images_dir = tempfile.mkdtemp()

    client = OpenAI()
    dict = process_script(script)
    for i, text in enumerate(dict['text_for_image_generation']):
        try:
            response = client.images.generate(
                model="dall-e-2",
                prompt=text,
                size="512x512",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url

            print(f'image {i} generated')
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                with open(os.path.join(images_dir, f'image_{i}.png'), 'wb') as file:
                    file.write(image_response.content)
            else:
                raise str(Exception(f"Failed to download image with status code {image_response.status_code} and message: {image_response.text}"))

        except Exception as e:
            raise str(Exception(f"Image generation failed: {e}"))

    return images_dir

def speech_generator(script):
    """
    Generates speech files for the given script using gTTS.
    Saves them to a temporary directory and returns the path.
    Args:
    script: a complete script containing narrations and image descriptions.
    """
    import tempfile
    import os
    speeches_dir = tempfile.mkdtemp()

    dict = process_script(script)
    for i, text in enumerate(dict['text_for_speech_generation']):
        speech_path = generate_speech(text, num=i)
        print(f'speech {i} generated')
        os.rename(speech_path, os.path.join(speeches_dir, f'speech_{i}.mp3'))

    return speeches_dir, dict['text_for_speech_generation']

def split_text_into_chunks(text, chunk_size):
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def add_text_to_video(input_video, text, duration=1, fontsize=40, fontcolor=(255, 255, 255),
                      outline_thickness=2, outline_color=(0, 0, 0), delay_between_chunks=0.3,
                      font_name="arial.ttf"):
    
    import tempfile
    import numpy as np
    import cv2
    from PIL import Image, ImageDraw, ImageFont

    temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    output_video = temp_output_file.name

    chunks = split_text_into_chunks(text, 3)  

    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        raise str(ValueError("Error opening video file."))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    chunk_duration_frames = duration * fps
    delay_frames = int(delay_between_chunks * fps)

    try:
        font = ImageFont.truetype(font_name, fontsize)
    except Exception as e:
        raise str(RuntimeError(f"Error loading font: {e}"))

    current_frame = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(frame_pil)

        chunk_index = current_frame // (chunk_duration_frames + delay_frames)

        if current_frame % (chunk_duration_frames + delay_frames) < chunk_duration_frames and chunk_index < len(chunks):
            chunk = chunks[chunk_index]
            text_bbox = draw.textbbox((0, 0), chunk, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
            text_x = (width - text_width) // 2
            text_y = height - 100  

            if text_width > width:
                words = chunk.split()
                half = len(words) // 2
                line1 = ' '.join(words[:half])
                line2 = ' '.join(words[half:])

                text_size_line1 = draw.textsize(line1, font=font)
                text_size_line2 = draw.textsize(line2, font=font)
                text_x_line1 = (width - text_size_line1[0]) // 2
                text_x_line2 = (width - text_size_line2[0]) // 2
                text_y = height - 250 - text_size_line1[1]  

                for dx in range(-outline_thickness, outline_thickness + 1):
                    for dy in range(-outline_thickness, outline_thickness + 1):
                        if dx != 0 or dy != 0:
                            draw.text((text_x_line1 + dx, text_y + dy), line1, font=font, fill=outline_color)
                            draw.text((text_x_line2 + dx, text_y + text_size_line1[1] + dy), line2, font=font, fill=outline_color)
                
                draw.text((text_x_line1, text_y), line1, font=font, fill=fontcolor)
                draw.text((text_x_line2, text_y + text_size_line1[1]), line2, font=font, fill=fontcolor)

            else:
                for dx in range(-outline_thickness, outline_thickness + 1):
                    for dy in range(-outline_thickness, outline_thickness + 1):
                        if dx != 0 or dy != 0:
                            draw.text((text_x + dx, text_y + dy), chunk, font=font, fill=outline_color)
                
                draw.text((text_x, text_y), chunk, font=font, fill=fontcolor)

            frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)

        out.write(frame)
        current_frame += 1

        if current_frame >= frame_count:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    return output_video

def apply_zoom_in_effect(clip, zoom_factor=1.2):
    import cv2
    width, height = clip.size
    duration = clip.duration

    def zoom_in_effect(get_frame, t):
        frame = get_frame(t)
        zoom = 1 + (zoom_factor - 1) * (t / duration)
        new_width, new_height = int(width * zoom), int(height * zoom)
        resized_frame = cv2.resize(frame, (new_width, new_height))
        
        x_start = (new_width - width) // 2
        y_start = (new_height - height) // 2
        cropped_frame = resized_frame[y_start:y_start + height, x_start:x_start + width]
        
        return cropped_frame

    return clip.fl(zoom_in_effect, apply_to=['mask'])

def create_video_from_images_and_audio(images_dir, speeches_dir, final_video_filename, all_captions):
    """Creates video using images and audios.
    Args:
    images_dir: path to images folder
    speeches_dir: path to speeches folder
    final_video_filename: the topic name which will be used as final video file name"""
    import tempfile
    import os
    from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip

    images_paths = sorted([os.path.join(images_dir, img) for img in os.listdir(images_dir) if img.endswith('.png') or img.endswith('.jpg')])
    audio_paths = sorted([os.path.join(speeches_dir, speech) for speech in os.listdir(speeches_dir) if speech.endswith('.mp3')])
    clips = []
    temp_files = []
    temp_folder = tempfile.gettempdir()
    
    for i in range(min(len(images_paths), len(audio_paths))):
        img_clip = ImageClip(os.path.join(images_dir, images_paths[i]))
        audioclip = AudioFileClip(os.path.join(speeches_dir, audio_paths[i]))
        videoclip = img_clip.set_duration(audioclip.duration)
        zoomed_clip = apply_zoom_in_effect(videoclip, 1.3)
        
        # with open(os.path.join(speeches_dir, audio_paths[i]), "rb") as file:
        #     transcription = client.audio.transcriptions.create(
        #         file=(audio_paths[i], file.read()),
        #         model="whisper-large-v3",
        #         response_format="verbose_json",
        #     )
        #     caption = transcription.text
        temp_video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
        zoomed_clip.write_videofile(temp_video_path, codec='libx264', fps=24)
        temp_files.append(temp_video_path)
        
        caption = all_captions[i]
        final_video_path = add_text_to_video(temp_video_path, caption, duration=1, fontsize=20)
        temp_files.append(final_video_path)
        
        final_clip = VideoFileClip(final_video_path)
        final_clip = final_clip.set_audio(audioclip)

        print(f'create small video {i}')
        clips.append(final_clip)
    
    final_clip = concatenate_videoclips(clips)
    video_file_path = os.path.join(temp_folder, 'video.mp4')
    if os.path.exists(video_file_path):
        os.remove(video_file_path)
    final_clip.write_videofile(video_file_path, codec='libx264', fps=24)
    
    for clip in clips:
        clip.close()

    print(video_file_path)
    
    return video_file_path

def generate_video(pairs, final_video_filename='video.mp4'):

    """ Generates video using narration and image prompt pairs.

    Args:
        pairs:A string of arration and image prompt pairs enclosed in <narration> and <image> tags.
        final_video_filename: the topic name which will be used as final video file name

    Returns:
        Generated video path"""

    images_dir = image_generator(pairs)
    print(images_dir)
    speeches_dir, all_captions = speech_generator(pairs)
    print(speeches_dir)
    video_path = create_video_from_images_and_audio(images_dir, speeches_dir, final_video_filename, all_captions)
    print('video', video_path)

    return video_path


# def image_generator(script):   
#     images_dir = tempfile.mkdtemp()

#     client = OpenAI()
#     dict = process_script(script)
#     for i, text in enumerate(dict['text_for_image_generation']):
#         try:
#             response = client.images.generate(
#                 model="dall-e-2",
#                 prompt=text,
#                 size="512x512",
#                 quality="standard",
#                 n=1
#             )
#             image_url = response.data[0].url

#             print(f'image {i} generated')
#             image_response = requests.get(image_url)
#             if image_response.status_code == 200:
#                 with open(os.path.join(images_dir, f'image_{i}.png'), 'wb') as file:
#                     file.write(image_response.content)
#             else:
#                 raise str(Exception(f"Failed to download image with status code {image_response.status_code} and message: {image_response.text}"))

#         except Exception as e:
#             raise str(Exception(f"Image generation failed: {e}"))

#     return images_dir

# def generate_image_openai(text, openai_api_key=None, model_name="dall-e-2", resolution="512x512", qualilty='standard', n=1, save_temp = False, _i=1):

#     output_image = f'image_{_i}.png'
#     if save_temp:
#         temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
#         output_image = temp_output_file.name

#     api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
#     client = OpenAI(api_key=api_key)

#     try:
#         response = client.images.generate(
#             model=model_name,
#             prompt=text,
#             size=resolution,
#             quality=qualilty,
#             n=n
#         )
#         image_url = response.data[0].url
#         # print(image_url)

#         image_response = requests.get(image_url)
#         if image_response.status_code == 200:
#             with open(output_image, 'wb') as file:
#                 file.write(image_response.content)
#         else:
#             raise str(Exception(f"Failed to download image with status code {image_response.status_code} and message: {image_response.text}"))

#     except Exception as e:
#         raise str(Exception(f"Image generation failed: {e}"))

#     return output_image

def extract_audio_from_video(video_path):
    from moviepy.editor import VideoFileClip
    import tempfile
    print(video_path)
    with VideoFileClip(video_path) as video:
        audio = video.audio
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        audio.write_audiofile(temp_audio_file.name)
    return temp_audio_file.name

def transcribe_audio(audio_file_path):
    from openai import OpenAI
    client = OpenAI()
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )   
    return transcription.text

def wikipedia_search(query, lang='en', result_count=5, full_content=False):
    import wikipedia
    import wikipediaapi  
    user_agent = "MyWikipediaSearchBot/1.0 (https://example.com)"
    
    wiki_api = wikipediaapi.Wikipedia(user_agent=user_agent, language=lang)
    
    search_results = wikipedia.search(query, results=result_count)
    
    results = {}

    for result in search_results:
        page = wiki_api.page(result)
        
        if page.exists():
            if full_content:
                results[result] = page.text if page.text else "No content available."
            else:
                if len(page.summary) > 200:
                    results[result] = page.summary if page.summary else "No summary available."
        else:
            results[result] = f"'{result}' not found on Wikipedia."
    
    return results

def calculate(operation: str) -> float:
    try:
        return eval(operation, {"__builtins__": None}, {})
    except Exception as e:
        return f"Error in calculation: {e}"

def create_mysql_engine(user, password, host, db_name):
    from sqlalchemy import create_engine, text

    if db_name:
        connection_str = f'postgresql://{user}:{password}@{host}/{db_name}'
    else:
        connection_str = f'postgresql://{user}:{password}@{host}/'
    engine = create_engine(connection_str)
    return engine

def file_to_sql(file_path, table_name, user, password, host, db_name):
    import pandas as pd
    import os
    from sqlalchemy import create_engine
    
    # engine = create_engine(f"postgresql://{user}:{password}@{host}/{db_name}")
    engine = create_mysql_engine(user, password, host, db_name)

    if not table_name:
        table_name = os.path.splitext(os.path.basename(file_path))[0]
    
    file_extension = os.path.splitext(file_path)[-1].lower()
    if file_extension == '.xlsx':
        df = pd.read_excel(file_path)
    elif file_extension == '.csv':
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide an Excel (.xlsx) or CSV (.csv) file.")

    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    return f"Data from '{file_path}' stored in table '{table_name}'."

# Function to execute a custom SQL query and print results
def execute_query(query, user, password, host, db_name):
    from sqlalchemy import create_engine, text

    engine = create_mysql_engine(user, password, host, db_name)
    with engine.connect() as connection:
        try:
            result_set = connection.execute(text(query))
            output = []
            for row in result_set:
                print(row)
                output.append(str(row))
            return output
        except Exception as e:
            return str(e)
        
def get_metadata(host, user, password, db, tables):
    metadata = []
    for table in tables:
        table_info = {}
        query_columns = f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = '{table}';
        """
        table_info['columns'] = execute_query(query_columns, user, password, host, db)
        
        query_sample = f'SELECT * FROM "{table}" LIMIT 5;'
        table_info['sample_rows'] = execute_query(query_sample, user, password, host, db)

        metadata.append({table: table_info})
    
    return metadata

def execute_code(command, timeout):
    from python_repl import repl_tool
    try:
        out = repl_tool.run(command, timeout)
    except Exception as e:
        return f"Error: {str(e)}"
    
    return out

def install_library(library_name):

    import subprocess
    import sys
    print(f"Attempting to install missing library: {library_name}")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
    except Exception as e:
        return f"Unable to install {library_name}. Error: {e}"

    return f"{library_name} has been installed sucessfully."