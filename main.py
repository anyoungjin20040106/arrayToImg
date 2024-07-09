from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from PIL import Image
import numpy as np
import io
import uvicorn
import base64

app = FastAPI()
templete=Jinja2Templates("templete")
@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templete.TemplateResponse("index.html",{"request":request,"hasimg":False})

@app.post("/")
async def convert_to_image(request: Request,array_data: str = Form(...)):
    try:
        
        array = eval(array_data.replace("\n",""))
        array = np.array(array, dtype=np.uint8)
        image = Image.fromarray(array, 'L')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # 이미지를 base64로 인코딩
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        # HTML 템플릿에 이미지 데이터 전달
        return templete.TemplateResponse("index.html", {"request": request,"hasimg":True, "image_data": img_base64})
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}", status_code=400)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
