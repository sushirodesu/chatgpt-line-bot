from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import os
import uvicorn

from chatgpt_linebot.urls import line_app
from chatgpt_linebot.openai import create_line_reply, push_market_analysis  # ←★ 追加（自動分析送信）

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ◆ LINE Webhookエンドポイント
@app.post("/callback")
async def callback(request: Request):
    body = await request.body()
    signature = request.headers.get("x-line-signature")
    response = create_line_reply(body, signature)
    return response

# ◆ 動作確認用エンドポイント
@app.get("/")
async def root():
    return {"message": "Hello World!"}

# ◆ 自動相場分析送信用エンドポイント（※アクセスすると分析結果がLINEに届く）
@app.get("/push-analysis")
async def push_analysis():
    push_market_analysis()
    return {"message": "Analysis pushed to LINE"}

# ◆ 他のルーティング（例：画像検索など）も含めてマウント
app.include_router(line_app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
