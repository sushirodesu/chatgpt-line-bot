from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

# openai.py がまだ無いため、この行をコメントアウトまたは削除
# from chatgpt_linebot.openai import chat

line_app = APIRouter()

@line_app.get("/webhook")
async def test_webhook():
    return JSONResponse(content={"message": "Webhook is working!"})
