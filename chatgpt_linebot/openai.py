from fastapi.responses import JSONResponse
from fastapi import Request, Header
import hmac
import hashlib
import base64
import json
import os

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

def create_line_reply(body: bytes, signature: str):
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

    # JSONとして読み取り
    data = json.loads(body_str)
    print("✅ LINEメッセージ受信")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    return JSONResponse(content={"message": "OK"}, status_code=200)
