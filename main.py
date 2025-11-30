#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
崩铁货币战争策略助手主程序
"""

import os
import sys
import time
import threading
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('strategy_assistant.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 添加PaddleOCR API路径到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'PaddleOCR-json-main', 'api', 'python'))

try:
    from PPOCR_api import GetOcrApi
    from data_matcher import DataMatcher
    from screen_capture import ScreenCapture
    from ocr_engine import OCREngine
    from gui import StrategyGUI
    
    # GUI相关导入
    from tkinter import Tk
    from PIL import Image, ImageTk
    import mss
    import mss.tools
except ImportError as e:
    logger.error(f"导入模块失败: {e}")
    sys.exit(1)


def main():
    """主函数"""
    try:
        logger.info("启动崩铁货币战争策略助手")
        
        # 配置PaddleOCR引擎路径
        ocr_exe_path = os.path.join(os.path.dirname(__file__), 'PaddleOCR-json_v1.4.1_windows_x64', 'PaddleOCR-json_v1.4.1', 'PaddleOCR-json.exe')
        
        # 检查OCR引擎路径是否存在
        if not os.path.exists(ocr_exe_path):
            logger.error(f"PaddleOCR引擎路径不存在: {ocr_exe_path}")
            return
        
        # 配置策略数据路径
        strategy_data_path = os.path.join(os.path.dirname(__file__), '货币战争策略数据.csv')
        
        # 检查策略数据路径是否存在
        if not os.path.exists(strategy_data_path):
            logger.error(f"策略数据路径不存在: {strategy_data_path}")
            return
        
        # 创建各个模块实例
        logger.info("创建屏幕捕获实例")
        screen_capture = ScreenCapture()
        
        logger.info("创建OCR引擎实例")
        ocr_engine = OCREngine(ocr_exe_path)
        
        logger.info("创建数据匹配实例")
        data_matcher = DataMatcher(strategy_data_path)
        
        # 创建GUI实例
        logger.info("创建GUI实例")
        root = Tk()
        gui = StrategyGUI(root, screen_capture, ocr_engine, data_matcher)
        
        # 启动GUI主循环
        logger.info("启动GUI主循环")
        root.mainloop()
        
    except Exception as e:
        logger.error(f"程序运行错误: {e}", exc_info=True)


if __name__ == '__main__':
    main()
