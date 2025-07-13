import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from chatgpt_linebot.urls import line_app

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(line_app)


@app.get("/", response_class=JSONResponse)
async def home() -> JSONResponse:
    """Home Page

    Returns:
        JSONResponse: Hello World!
    """
    message = {"stauts": "success", "message": "Hello World!"}
    return JSONResponse(content=message)

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
