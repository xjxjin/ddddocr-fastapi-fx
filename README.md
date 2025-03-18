# 验证码识别服务 API 调用示例

## 简介
本项目提供了验证码识别服务的 API 调用示例，包含多种调用方式和功能演示，帮助用户快速上手使用验证码识别服务。

## 功能说明
1. **OCR 验证码识别 - 文件上传方式**：通过上传本地验证码图片文件进行识别。
2. **OCR 验证码识别 - Base64 编码方式**：将验证码图片转为 Base64 编码后进行识别。
3. **从 URL 识别验证码**：通过提供验证码图片的 URL 进行识别。
4. **滑动验证码匹配**：对滑动验证码的滑块和背景图进行匹配分析。
5. **图像文本检测**：检测图像中的文本内容及其位置。
6. **使用 token header 进行身份验证**：演示使用 token 在请求头中进行身份验证的方式。

## 使用方法

### 环境准备
- Python 3.x
- requests 库
- base64 模块
- json 模块

### 配置信息
在代码中修改以下配置信息以适配你的环境：
```python
BASE_URL = "http://localhost:8000"  # 替换为实际服务地址
API_TOKEN = "your_secure_token_here"  # 替换为实际 token
```

### 运行示例
运行脚本后，将依次执行所有示例函数，展示不同 API 接口的调用方式和结果。

## 注意事项
1. 确保提供的验证码图片路径、URL 及其他参数正确无误。
2. 根据实际需求调整请求参数，如 `probability`、`png_fix` 等。
3. 处理好文件的打开与关闭操作，避免资源泄露。
4. 对于网络请求，注意异常处理，以应对网络波动或其他不可预见的情况。
5. 确保你的网络环境可以正常访问目标 API 服务地址。

## 示例运行输出
运行脚本后，将输出每个示例的请求状态码和响应内容，帮助你了解 API 调用的结果。

## 联系与支持
如在使用过程中遇到问题，或有任何建议，请及时与我们联系。


```python
import requests
import base64
import json

"""
验证码识别服务API调用示例
包含所有API接口的调用示例
"""

# API配置信息
BASE_URL = "http://localhost:8000"  # 替换为实际服务地址
API_TOKEN = "your_secure_token_here"  # 替换为实际token


def demo_ocr_file():
    """
    示例1: OCR验证码识别 - 文件上传方式
    """
    print("\n===== 示例1: OCR验证码识别(文件上传) =====")
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    # API端点
    url = f"{BASE_URL}/ocr"
    
    try:
        # 准备文件和参数
        captcha_file_path = "captcha.png"  # 替换为实际验证码图片路径
        
        files = {
            "file": open(captcha_file_path, "rb")
        }
        
        data = {
            "probability": "False",
            "png_fix": "False"
        }
        
        # 发送请求
        response = requests.post(url, headers=headers, files=files, data=data)
        
        # 输出结果
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 关闭文件
        files["file"].close()
        
    except Exception as e:
        print(f"请求失败: {str(e)}")


def demo_ocr_base64():
    """
    示例2: OCR验证码识别 - Base64编码方式
    """
    print("\n===== 示例2: OCR验证码识别(Base64编码) =====")
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    # API端点
    url = f"{BASE_URL}/ocr"
    
    try:
        # 读取图片并转为Base64
        captcha_file_path = "captcha.png"  # 替换为实际验证码图片路径
        
        with open(captcha_file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        
        # 准备请求数据
        data = {
            "image": encoded_string,
            "probability": "False",
            "png_fix": "False"
        }
        
        # 发送请求
        response = requests.post(url, headers=headers, data=data)
        
        # 输出结果
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"请求失败: {str(e)}")


def demo_ocr_from_url():
    """
    示例3: 从URL识别验证码
    """
    print("\n===== 示例3: 从URL识别验证码 =====")
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    # API端点
    url = f"{BASE_URL}/ocr_from_url"
    
    try:
        # 准备请求数据
        image_url = "https://example.com/captcha.jpg"  # 替换为实际验证码图片URL
        
        data = {
            "url": image_url,
            "probability": "False",
            "png_fix": "False"
        }
        
        # 发送请求
        response = requests.post(url, headers=headers, data=data)
        
        # 输出结果
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"请求失败: {str(e)}")


def demo_slide_match():
    """
    示例4: 滑动验证码匹配
    """
    print("\n===== 示例4: 滑动验证码匹配 =====")
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    # API端点
    url = f"{BASE_URL}/slide_match"
    
    try:
        # 准备文件和参数
        target_path = "target.png"  # 替换为实际滑块图片路径
        background_path = "background.png"  # 替换为实际背景图片路径
        
        files = {
            "target_file": open(target_path, "rb"),
            "background_file": open(background_path, "rb")
        }
        
        data = {
            "simple_target": "false"
        }
        
        # 发送请求
        response = requests.post(url, headers=headers, files=files, data=data)
        
        # 输出结果
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 关闭文件
        files["target_file"].close()
        files["background_file"].close()
        
    except Exception as e:
        print(f"请求失败: {str(e)}")


def demo_detection():
    """
    示例5: 图像文本检测
    """
    print("\n===== 示例5: 图像文本检测 =====")
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    # API端点
    url = f"{BASE_URL}/detection"
    
    try:
        # 准备文件
        image_path = "text_image.png"  # 替换为实际包含文本的图片路径
        
        files = {
            "file": open(image_path, "rb")
        }
        
        # 发送请求
        response = requests.post(url, headers=headers, files=files)
        
        # 输出结果
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 关闭文件
        files["file"].close()
        
    except Exception as e:
        print(f"请求失败: {str(e)}")


def demo_token_header():
    """
    示例6: 使用token header进行身份验证
    """
    print("\n===== 示例6: 使用token header进行身份验证 =====")
    
    # 设置请求头 - 使用token而非Authorization
    headers = {
        "token": API_TOKEN
    }
    
    # API端点
    url = f"{BASE_URL}/ocr"
    
    try:
        # 准备文件和参数
        captcha_file_path = "captcha.png"  # 替换为实际验证码图片路径
        
        files = {
            "file": open(captcha_file_path, "rb")
        }
        
        data = {
            "probability": "False"
        }
        
        # 发送请求
        response = requests.post(url, headers=headers, files=files, data=data)
        
        # 输出结果
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 关闭文件
        files["file"].close()
        
    except Exception as e:
        print(f"请求失败: {str(e)}")


if __name__ == "__main__":
    print("验证码识别服务API调用示例")
    print("=" * 50)
    print(f"API地址: {BASE_URL}")
    print(f"Token: {API_TOKEN}")
    print("=" * 50)
    
    # 运行所有示例
    demo_ocr_file()
    demo_ocr_base64()
    demo_ocr_from_url()
    demo_slide_match()
    demo_detection()
    demo_token_header()
    
    print("\n所有示例已完成!")
```