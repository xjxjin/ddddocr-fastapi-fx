import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends, Header
from typing import Optional, Union
import base64
import requests
import os
from .models import OCRRequest, SlideMatchRequest, DetectionRequest, APIResponse
from .services import ocr_service

app = FastAPI()

from starlette.datastructures import UploadFile as StarletteUploadFile


async def verify_token(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Header(None)
):
    # 从环境变量获取有效token
    valid_token = os.environ.get("API_TOKEN", "default_token")
    
    # 检查是否提供了Authorization header
    provided_token = None
    if authorization:
        # 解析Authorization header (通常格式为"Bearer <token>")
        if authorization.startswith("Bearer "):
            provided_token = authorization.split("Bearer ")[1].strip()
        else:
            provided_token = authorization
    # 如果没有Authorization，则使用token header
    elif token:
        provided_token = token
    
    # 如果没有提供任何token，则返回错误
    if not provided_token:
        raise HTTPException(status_code=401, detail="未提供token")
    
    # 验证token
    if provided_token != valid_token:
        raise HTTPException(status_code=401, detail="无效的token")
    
    return provided_token


async def decode_image(image: Union[UploadFile, StarletteUploadFile, str, None]) -> bytes:
    if image is None:
        raise HTTPException(status_code=400, detail="No image provided")

    if isinstance(image, (UploadFile, StarletteUploadFile)):
        return await image.read()
    elif isinstance(image, str):
        try:
            # 检查是否是 base64 编码的图片
            if image.startswith(('data:image/', 'data:application/')):
                # 移除 MIME 类型前缀
                image = image.split(',')[1]
            return base64.b64decode(image)
        except:
            raise HTTPException(status_code=400, detail="Invalid base64 string")
    else:
        raise HTTPException(status_code=400, detail="Invalid image input")


async def get_image_from_url(url: str) -> bytes:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"无法从URL获取图像: {str(e)}")


@app.post("/ocr", response_model=APIResponse)
async def ocr_endpoint(
        file: Optional[UploadFile] = File(None),
        image: Optional[str] = Form(None),
        probability: bool = Form(False),
        charsets: Optional[str] = Form(None),
        png_fix: bool = Form(False),
        token: str = Depends(verify_token)
):
    try:
        if file is None and image is None:
            return APIResponse(code=400, message="Either file or image must be provided")

        image_bytes = await decode_image(file or image)
        result = ocr_service.ocr_classification(image_bytes, probability, charsets, png_fix)
        return APIResponse(code=200, message="Success", data=result)
    except Exception as e:
        return APIResponse(code=500, message=str(e))


@app.post("/ocr_from_url", response_model=APIResponse)
async def ocr_from_url_endpoint(
        url: str = Form(...),
        probability: bool = Form(False),
        charsets: Optional[str] = Form(None),
        png_fix: bool = Form(False),
        token: str = Depends(verify_token)
):
    try:
        image_bytes = await get_image_from_url(url)
        result = ocr_service.ocr_classification(image_bytes, probability, charsets, png_fix)
        return APIResponse(code=200, message="Success", data=result)
    except Exception as e:
        return APIResponse(code=500, message=str(e))


@app.post("/slide_match", response_model=APIResponse)
async def slide_match_endpoint(
        target_file: Optional[UploadFile] = File(None),
        background_file: Optional[UploadFile] = File(None),
        target: Optional[str] = Form(None),
        background: Optional[str] = Form(None),
        simple_target: bool = Form(False),
        token: str = Depends(verify_token)
):
    try:
        if (background is None and target is None) or (background_file.size == 0 and target_file.size == 0):
            return APIResponse(code=400, message="Both target and background must be provided")

        target_bytes = await decode_image(target_file or target)
        background_bytes = await decode_image(background_file or background)
        result = ocr_service.slide_match(target_bytes, background_bytes, simple_target)
        return APIResponse(code=200, message="Success", data=result)
    except Exception as e:
        return APIResponse(code=500, message=str(e))


@app.post("/detection", response_model=APIResponse)
async def detection_endpoint(
        file: Optional[UploadFile] = File(None),
        image: Optional[str] = Form(None),
        token: str = Depends(verify_token)
):
    try:
        if file is None and image is None:
            return APIResponse(code=400, message="Either file or image must be provided")

        image_bytes = await decode_image(file or image)
        bboxes = ocr_service.detection(image_bytes)
        return APIResponse(code=200, message="Success", data=bboxes)
    except Exception as e:
        return APIResponse(code=500, message=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
