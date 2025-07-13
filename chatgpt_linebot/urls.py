from urllib.parse import urlparse
from icrawler.builtin import BingImageCrawler as ImageCrawler
from linebot.models import ImageSendMessage, TextSendMessage
from linebot import LineBotApi
import config
from chatgpt_linebot.openai import chat

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)

def is_url(string: str) -> bool:
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def agent(query: str) -> tuple[str]:
    """Auto use correct tool by user query."""
    prompt = config.agent_template + query
    message = [{'role': 'user', 'content': prompt}]

    response = chat(message, config.GPT_METHOD, config.GPT_API_KEY)
    tool = "gpt"

    print(f"""
Agent
========================
Query: {query}
Tool: {tool}
========================
""")

    return response

def search_image_url(query: str) -> str:
    """Fetches image URL from different search sources."""
    img_crawler = ImageCrawler(num=5)
    img_url = img_crawler.get_url(query)

    if not img_url:
        img_serp = ImageCrawler(engine="serpapi", num=5, api_key=config.SERPAPI_API_KEY)
        img_url = img_serp.get_url(query)
        print("Used Serpapi search image instead of icrawler.")
    
    return img_url

def send_image_reply(reply_token, img_url: str) -> None:
    """Sends an image message to the user."""
    if not img_url:
        send_text_reply(reply_token, 'Cannot get image.')
        return

    image_message = ImageSendMessage(
        original_content_url=img_url,
        preview_image_url=img_url
    )
    line_bot_api.reply_message(reply_token, messages=image_message)

def send_text_reply(reply_token, text: str) -> None:
    """Sends a text message to the user."""
    if not text:
        text = "There's some problem in server."
    text_message = TextSendMessage(text=text)
    line_bot_api.reply_message(reply_token, messages=text_message)
