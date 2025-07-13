from fastapi.responses import JSONResponse
from fastapi import Request, Header

def create_line_reply(body: bytes, signature: str):
    # LINEからのWebhookイベントを処理（ここでは仮処理）
    print("✅ Webhook受信（テスト）")
    print("署名:", signature)
    print("ボディ:", body.decode())

    # 仮で200 OK返す（Webhook検証パス用）
    return JSONResponse(content={"message": "OK"}, status_code=200)
