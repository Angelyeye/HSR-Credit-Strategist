#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR引擎模块
"""

import os
import time
from PIL import Image

from PPOCR_api import GetOcrApi


class OCREngine:
    """OCR引擎类"""
    
    def __init__(self, ocr_exe_path):
        """初始化OCR引擎
        
        Args:
            ocr_exe_path: PaddleOCR-json.exe路径
        """
        self.ocr_exe_path = ocr_exe_path
        self.ocr_api = None
        self.init_ocr()
    
    def init_ocr(self):
        """初始化OCR引擎"""
        try:
            # 初始化OCR引擎
            self.ocr_api = GetOcrApi(self.ocr_exe_path)
            print("OCR引擎初始化成功")
        except Exception as e:
            print(f"OCR引擎初始化失败: {e}")
            self.ocr_api = None
    
    def preprocess_image(self, image):
        """图像预处理
        
        Args:
            image: PIL.Image对象
            
        Returns:
            PIL.Image: 预处理后的图像
        """
        try:
            # 转换为灰度图
            gray_image = image.convert("L")
            
            # 二值化处理
            threshold = 128
            binary_image = gray_image.point(lambda p: p > threshold and 255)
            
            return binary_image
        except Exception as e:
            print(f"图像预处理失败: {e}")
            return image
    
    def recognize_text(self, image, preprocess=True):
        """识别图像中的文本
        
        Args:
            image: PIL.Image对象
            preprocess: 是否进行图像预处理
            
        Returns:
            list: 识别结果，格式为[{"text": "文本内容", "score": 置信度}, ...]
        """
        try:
            if not self.ocr_api:
                # 重新初始化OCR引擎
                self.init_ocr()
                if not self.ocr_api:
                    return []
            
            # 图像预处理
            if preprocess:
                processed_image = self.preprocess_image(image)
            else:
                processed_image = image
            
            # 转换为字节流
            import io
            img_byte_arr = io.BytesIO()
            processed_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # 调用OCR API
            result = self.ocr_api.runBytes(img_byte_arr)
            
            # 处理识别结果
            if result["code"] == 100:
                # 识别成功
                ocr_results = []
                for item in result["data"]:
                    ocr_results.append({
                        "text": item["text"],
                        "score": item["score"]
                    })
                return ocr_results
            else:
                # 识别失败
                print(f"OCR识别失败: {result['data']}")
                return []
        except Exception as e:
            print(f"OCR识别异常: {e}")
            return []
    
    def recognize_image_path(self, image_path, preprocess=True):
        """识别指定路径图像中的文本
        
        Args:
            image_path: 图像路径
            preprocess: 是否进行图像预处理
            
        Returns:
            list: 识别结果
        """
        try:
            # 打开图像
            image = Image.open(image_path)
            
            # 调用识别函数
            return self.recognize_text(image, preprocess)
        except Exception as e:
            print(f"识别图像路径失败: {e}")
            return []
    
    def close(self):
        """关闭OCR引擎"""
        try:
            if self.ocr_api:
                self.ocr_api.exit()
                print("OCR引擎已关闭")
        except Exception as e:
            print(f"关闭OCR引擎失败: {e}")
    
    def __del__(self):
        """析构函数，关闭OCR引擎"""
        self.close()
