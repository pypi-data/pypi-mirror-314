from wyge.models.openai import ChatOpenAI
from wyge.tools.prebuilt_tools import extract_relevant_sections_from_website, generate_images_and_add_to_blog, generate_video, youtube_transcript_loader, extract_audio_from_video, transcribe_audio, post_on_linkedin, send_email, generate_image_openai, upload_to_drive
from wyge.tools.base_tool import Tool
import warnings
warnings.filterwarnings("ignore")

class ResearchAgent:
    def __init__(self, api_key=None) -> None:
        web_tool = extract_relevant_sections_from_website()
        yt_tool = youtube_transcript_loader()
        video_to_audio_tool = extract_audio_from_video()
        audio_to_text_tool = transcribe_audio()
        self.tools = [web_tool, yt_tool, video_to_audio_tool, audio_to_text_tool]

        self.llm = ChatOpenAI(tools=self.tools, api_key=api_key)
        # self.video_formats = ["mp4", "avi", "mkv", "mov", "flv", "wmv", "webm", "mpeg", "mpg", "3gp", "m4v", "mxf", "vob", "ogv"]
        # self.audio_formats = ["mp3", "wav", "aac", "flac", "ogg", "m4a"]

    def research_website(self, topic, url): 
        prompt1 = (
            f"Gather relavent information about topic from the website. "
            f"\nTopic: {topic} "
            f"\nWebsite: {url} "
        )
        context = self.llm.run(prompt1, system_message="You are a senior research agent.", return_tool_output=True)
        return context
    
    def extract_transcript_from_yt_video(self, url):
        prompt1 = f"Extract the text content from the youtube video. video url: {url}"
        context = self.llm.run(prompt1, return_tool_output=True)
        return context
    
    def _video_to_text(self, video_path):
        audio_path = self.llm.run(f"Extract audio fromt the video. video path: {video_path}", return_tool_output=True)[0]
        print(audio_path)
        text = self.llm.run(f"Transcribe the audio into text. audio_path: {audio_path}", return_tool_output=True)[0]
        return text

    def _audio_to_text(self, audio_path):
        text = self.llm.run(f"Transcribe the audio into text. audio_path: {audio_path}", return_tool_output=True)[0]
        return text
    
    def extract_text_from_audio_or_video(self, file_path):
        file_format = 'Audio file' if file_path.endswith('mp3') else 'Video file'
        if file_format == 'Video file':
            text = self._video_to_text(file_path)
        elif file_format == 'Audio file':
            text = self._audio_to_text(file_path)
        return text
    

    
class LinkedInAgent:
    def __init__(self, api_key=None) -> None:
        linkedin_tool = post_on_linkedin()
        
        self.tools = [linkedin_tool]

        self.llm = ChatOpenAI(tools=self.tools, api_key=api_key)

    def generate_linkedin_post(self, content):
        prompt1 = (
            "Create a LinkedIn post based on the following topic and blog. The post should be professional, engaging, and suitable for a LinkedIn audience. "
            "It should introduce the topic, provide a brief summary, and include a call-to-action if relevant. The text should be concise yet informative."
            f"Blog content:\n{content}\n\n"
            
            "Expected Output: A well-structured LinkedIn post(around 250 words)."
            "Note: Do not post it on LinkedIn."
        )
        content = self.llm.run(prompt1)
        return content

    def post_content_on_linkedin(self, token, post_content, image_path=None):
        prompt5 = (
            "Post the following content as linkedin post. "
            f"Post content: {post_content}"
            f"image path: {image_path}"
            f"linkedin token: {token}"
        )
        ack = self.llm.run(prompt5, return_tool_output=True)[0]
        return ack
    
class EmailAgent:
    def __init__(self, api_key) -> None:
        email_tool = send_email()
        self.tools = [email_tool]

        self.llm = ChatOpenAI(api_key=api_key, tools=self.tools)

    def generate_email(self, context):
        pass

    def send_email(self, to_mail, subject, body, attachments=None, credentials_json_file_path = 'credentials.json', token_json_file_path='token.json'):
        prompt = (
            f"Send an email to {to_mail} "
            f"subject: {subject} "
            f"body: {body} "
            f"attachments: {attachments}"
            f"\n sender details: and token_json_file_path = {token_json_file_path} "
            "use only token file for sender details"
        )
        ack = self.llm.run(prompt, return_tool_output=True)
        return ack
    
class GoogleDriveAgent:
    def __init__(self, api_key) -> None:
        drive_tool = upload_to_drive()
        self.tools = [drive_tool]
        self.llm = ChatOpenAI(api_key=api_key, tools=self.tools)

    def upload(self, file_path, file_name, parent_folder_id, service_account='service_account.json'):
        prompt = (
            "Upload the following file to google drive"
            f"file path: {file_path}"
            f"file name: {file_name}"
            f"parent folder id: {parent_folder_id}"
            f"service account file path: {service_account}"
        )
        ack = self.llm.run(prompt, return_tool_output=True)
        return ack
    
class ImageGenerationAgent:
    def __init__(self, api_key=None):
        self.llm1 = ChatOpenAI(api_key=api_key)
        dalle_tool = generate_image_openai()
        blog_img_tool = generate_images_and_add_to_blog()
        self.tools1 = [blog_img_tool]
        self.tools2 = [dalle_tool]

        self.llm2 = ChatOpenAI(tools=self.tools, api_key=api_key)
        self.llm3 = ChatOpenAI(tools=self.tools, api_key=api_key)

    def add_image_prompts(self,blog_content):
        prompt3 = (
            # "Please replace all instances of '<-IMAGE->' with specific image prompts. "
            "Add image prompt to the below blog. "
            "Each image prompt should be enclosed within XML tag ('<image>'). "
            "Ensure that the image prompts avoid including any text, names of individuals, company names, logos, or other identifiable information. "
            "Think of the image prompt as 'what you want to see in the final image.' "
            "Provide a descriptive prompt that clearly defines the elements, colors, and subjects. "
            "For instance: 'The sky was a crisp (blue:0.3) and (green:0.8)' indicates a sky that is predominantly green with a hint of blue. "
            "The weights (e.g., 0.3 and 0.8) apply to all words in the prompt, guiding the emphasis of the colors and elements. "
            f"Blog: \n{blog_content}\n\n"
            "Expected Output: A complete blog with image prompt(total 1 image only) enclosed in <image> tags."
        )
        blog = self.llm1.run(prompt3, system_message="You are an effective Blog writer. Output only blog, without any additional text. ")
        return blog
    
    def _add_images_to_blog(self, blog_content):
        prompt4 = f"Use tool to generate images and add them to below blog. \n\n Blog: {blog_content} \n\n"
        final_blog = self.llm.run(prompt4, return_tool_output=True)
        return final_blog
    
    def add_to_blog(self, blog_text):
        blog_content = self.add_image_prompts(blog_text)
        self.blog_content = blog_content
        print(blog_content)
        output = self._add_images_to_blog(blog_content)
        self.image_path = output[-1][-1][0]
        doc_file = output[0][1]
        return doc_file, self.image_path
    
    def generate_image(self, content):
        prompt2 = (
            f"Generate image for the follwing content."
            f"Content: \n{content}"
            "\nNote: "
            "Think of the image prompt as 'what you want to see in the final image.' "
            "For instance: 'The sky was a crisp (blue:0.3) and (green:0.8)' indicates a sky that is predominantly green with a hint of blue. "
            "The weights (e.g., 0.3 and 0.8) apply to all words in the prompt, guiding the emphasis of the colors and elements. "
            "Ensure that the image prompts avoid including any text, names of individuals, company names, logos, or other identifiable information. "
            "Note: save the images locally"
        )

        image_path = self.llm.run(prompt2)[0]
        return image_path

class BlogAgent:
    def __init__(self, api_key=None) -> None:
        self.llm1 = ChatOpenAI(api_key=api_key)

        # blog_img_tool = generate_images_and_add_to_blog()
        # self.tools = [blog_img_tool]

        # self.llm = ChatOpenAI(tools=self.tools, api_key=api_key)

    def write_blog_text(self, topic, context):
        prompt2 = (
            f"Write a comprehensive blog post based on the following details:\n\n"
            f"Topic: {topic}\n"
            f"Summarized context about the topic: {context}\n\n"
            f"The blog should include an engaging introduction to topic, then detailed stections about how the context addresses the topic, "
            f"and a conclusion summarizing the key points. Structure the blog with clear headings, and write it in a conversational style. "
            f"Output the blog in markdown format, including a title, introduction, body sections, and conclusion. Write in a conversational style to engage readers. "
        )
        # f"Use <-IMAGE-> placeholder where image image is required.(total 1 image only) "

        blog_text = self.llm1.run(prompt2, system_message="You are an effective Blog writer.  Output only blog, without any additional text. ")
        return blog_text

    def generate_blog(self, topic, content):
        self.topic = topic
        blog_text = self.write_blog_text(topic, content)
        # blog_content = self.add_image_prompts(blog_text)
        # self.blog_content = blog_content
        # print(blog_content)
        # output = self.add_images(blog_content)
        # self.image_path = output[-1][-1][0]
        # doc_file = output[0][1]
        # return blog_text.replace("<-IMAGE->", "") , doc_file, self.image_path
        return blog_text
    
class VideoAgent:
    def __init__(self, api_key) -> None:
        self.llm1 = ChatOpenAI(api_key=api_key)
        web_tool = extract_relevant_sections_from_website()
        video_tool = generate_video()
        self.tools = [web_tool, video_tool]
        self.llm = ChatOpenAI(tools=self.tools)
    
    def generate_script(self, topic, context):
        prompt2 = (
            "Generate a video script with exactly two narration and image prompt pairs for the following topic, focusing on the company's expertise related to the topic. "
            "The script should contain around 200 words total. Start by explaining the topic and then highlight the company's role or expertise in relation to it. "
            "The Narration must start with topic name. "
            "Ensure that the image prompts do not include any text, names, logos, or other identifying features. "
            "Provide a descriptive image prompt that clearly defines elements, colors, and subjects. For instance, 'The sky was a crisp blue with green hues' is more descriptive than just 'blue sky'."
            f"\n\n**Topic:** \n{topic}\n\n"
            f"**Company Website content:** \n{context}\n\n"
            "Expected Output: 2 pairs of sentences. Enclose the narration in <narration> narration here </narration> tags and image prompts in <image> image prompt here </image> tags."
        )
        script = self.llm1.run(prompt2, return_tool_output=True)
        return script

    def create_video(self, script):
        prompt3 = f"Create a video for the follwing script. \n\n video script: {script}"
        video = self.llm.run(prompt3, return_tool_output=True)
        return video
    
    def generate_video(self, topic, content):
        script = self.generate_script(topic, content)
        # print(script)
        video = self.create_video(script)
        return video

class YTBlogAgent:
    def __init__(self, api_key) -> None:
        self.llm1 = ChatOpenAI(api_key=api_key)
        # yt_tool = youtube_transcript_loader()
        # blog_img_tool = generate_images_and_add_to_blog()
        # self.tools = [yt_tool, blog_img_tool]
        # self.llm = ChatOpenAI(tools=self.tools, api_key=api_key)

    def write_blog_text(self, url, context):
        prompt2 = (
            f"Given a youtube video content, write a comprehensive blog post. "
            f"Structure the blog with clear headings, and write it in a conversational style. "
            f"Output the blog in markdown format, including a title, introduction, body sections, and conclusion. Write in a conversational style to engage readers. "
            f"**\n\nYouTube video url: ** {url}"
            f"\n**YouTube video transcript: **{context}"
        )
        blog_text = self.llm1.run(prompt2, system_message="You are an effective Blog writer.  Output only blog, without any additional text. ", return_tool_output=True)
        return blog_text

    # def add_image_prompts(self,blog_content):
    #     prompt3 = (
    #         "Please replace all instances of '<-IMAGE->' with specific image prompts. "
    #         "Each image prompt should be enclosed within XML tag ('<image> promt here </image>'). "
    #         "Ensure that the image prompts avoid including any text, names of individuals, company names, logos, or other identifiable information. "
    #         "Think of the image prompt as 'what you want to see in the final image.' "
    #         "Provide a descriptive prompt that clearly defines the elements, colors, and subjects. "
    #         "For instance: 'The sky was a crisp (blue:0.3) and (green:0.8)' indicates a sky that is predominantly green with a hint of blue. "
    #         "The weights (e.g., 0.3 and 0.8) apply to all words in the prompt, guiding the emphasis of the colors and elements. "
    #         "While you may reduce the number of images, ensure that no two image prompts are identical."
    #         f"Blog: \n{blog_content}\n\n"
    #         "Expected Output: A complete blog with image prompt(total 1 image only) enclosed in <image> tags. save temporarily."
    #     )
    #     blog = self.llm1.run(prompt3, system_message="You are an effective Blog writer.  Output only blog, without any additional text. ", return_tool_output=True)
    #     return blog
    
    # def add_images(self, blog_content):
    #     prompt4 = f"Use tool to generate images and add them to below blog. \n\n Blog: {blog_content}\n\n Note: save the images locally. "
    #     final_blog = self.llm.run(prompt4, return_tool_output=True)
    #     return final_blog
    
    def generate_blog(self, url):
        self.url = url
        transcript = self.extract_transcript(url)
        blog_text = self.write_blog_text(url, transcript)
        # blog_content = self.add_image_prompts(blog_text)
        # self.blog_content = blog_content
        # output = self.add_images(blog_content)
        # self.image_path = output[-1][-1][0]
        # doc_file = output[0][1]
        # return blog_text.replace("<-IMAGE->", "") , doc_file, self.image_path
        return blog_text
    
class VideoAudioBlogAgent:
    def __init__(self, api_key) -> None:
        import os
        os.environ['OPENAI_API_KEY'] = api_key
        self.llm1 = ChatOpenAI(api_key=api_key)
        # blog_img_tool = generate_images_and_add_to_blog()
        # self.tools = [video_to_audio_tool, audio_to_text_tool, blog_img_tool]
        # self.llm = ChatOpenAI(tools=self.tools, api_key=api_key)

    def write_blog_text(self, context):
        prompt2 = (
            f"Given transcription of a video, write a comprehensive blog post."
            f"The blog should include an engaging introduction to topic, then detailed stections about the content of the video, "
            f"and a conclusion summarizing the key points. Structure the blog with clear headings, and write it in a conversational style."
            f"Output the blog in markdown format, including a title, introduction, body sections, and conclusion. Write in a conversational style to engage readers. "
            f"\n\nVideo Transcript: {context}"
        )
        blog_text = self.llm1.run(prompt2, system_message="You are an effective Blog writer.  Output only blog, without any additional text. ")
        return blog_text

    # def add_image_prompts(self,blog_content):
    #     prompt3 = (
    #         "Please replace all instances of '<-IMAGE->' with specific image prompts. "
    #         "Each image prompt should be enclosed within XML tag ('<image>'). "
    #         "Ensure that the image prompts avoid including any text, names of individuals, company names, logos, or other identifiable information. "
    #         "Think of the image prompt as 'what you want to see in the final image.' "
    #         "Provide a descriptive prompt that clearly defines the elements, colors, and subjects. "
    #         "For instance: 'The sky was a crisp (blue:0.3) and (green:0.8)' indicates a sky that is predominantly green with a hint of blue. "
    #         "The weights (e.g., 0.3 and 0.8) apply to all words in the prompt, guiding the emphasis of the colors and elements. "
    #         "While you may reduce the number of images, ensure that no two image prompts are identical."
    #         f"Blog: \n{blog_content}\n\n"
    #         "Expected Output: A complete blog with image prompt(total 1 image only) enclosed in <image> tags. save temporarily."
    #     )
    #     blog = self.llm1.run(prompt3, system_message="You are an effective Blog writer.  Output only blog, without any additional text. ")
    #     return blog
    
    # def add_images(self, blog_content):
    #     prompt4 = f"Use tool to generate images and add them to below blog. \n\n Blog: {blog_content}\n\n Note: save the images locally. "
    #     final_blog = self.llm.run(prompt4, return_tool_output=True)
    #     print(final_blog)
    #     return final_blog
    
    def generate_blog(self, file_path):
        self.file_path = file_path
        file_format = self._classify_file(file_path)
        if file_format == 'Video file':
            text = self.video_to_text(file_path)
        elif file_format == 'Audio file':
            text = self. audio_to_text(file_path)
        else:
            raise("Invalid file format.")
        print("1111111111111")
        blog_text = self.write_blog_text(text)
        # print("1111111111111")
        # blog_content = self.add_image_prompts(blog_text)
        # print("1111111111111")
        # self.blog_content = blog_content
        # output = self.add_images(blog_content)
        # print("Output: ", output)
        # self.image_path = output[-1][-1][0]
        # doc_file = output[0][1]
        # return blog_text.replace("<-IMAGE->", "") , doc_file, self.image_path
        return blog_text
    
    def _classify_file(self, file_path):
        video_extensions = ("mp4", "avi", "mkv", "mov", "flv", "wmv", "webm", "mpeg", "mpg", "3gp", "m4v", "mxf", "vob", "ogv")
        audio_extensions = ("mp3", "wav", "aac", "flac", "ogg", "m4a")
        
        if file_path.lower().endswith(video_extensions):
            return "Video file"
        elif file_path.lower().endswith(audio_extensions):
            return "Audio file"
        else:
            return "Unknown type"
