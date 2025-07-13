from fastapi.responses import JSONResponse
from fastapi import Request, Header
import hmac
import hashlib
import base64
import json
import os
import requests  # ←これを追加

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

def create_line_reply(body: bytes, signature: str):
    # --- 署名の検証 ---
    body_str = body.decode()
    hash = hmac.new(
        LINE_CHANNEL_SECRET.encode("utf-8"),
        body,
        hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(hash).decode()
    if signature != expected_signature:
        print("❌ 署名が一致しません")
        return JSONResponse(content={"message": "Invalid signature"}, status_code=400)

    # --- イベント処理 ---
    data = json.loads(body_str)
    print("✅ LINEメッセージ受信")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    for event in data["events"]:
        if event["type"] == "message":
            reply_token = event["replyToken"]
            user_message = event["message"]["text"]

            # --- LINEに返信 ---
            reply_data = {
                "replyToken": reply_token,
                "messages": [
                    {"type": "text", "text": f"あなたはこう言いました：{user_message}"}
                ]
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
            }
            requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=reply_data)

    return JSONResponse(content={"message": "OK"}, status_code=200)
