#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI界面模块
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import threading
import time


class StrategyGUI:
    """策略助手GUI类"""
    
    def __init__(self, root, screen_capture, ocr_engine, data_matcher):
        """初始化GUI
        
        Args:
            root: Tk根窗口
            screen_capture: 屏幕捕获实例
            ocr_engine: OCR引擎实例
            data_matcher: 数据匹配实例
        """
        self.root = root
        self.screen_capture = screen_capture
        self.ocr_engine = ocr_engine
        self.data_matcher = data_matcher
        
        # 设置窗口标题和大小
        self.root.title("崩铁货币战争策略助手")
        self.root.geometry("1200x800")
        
        # 标志位
        self.is_running = False
        self.thread = None
        
        # 创建UI组件
        self.create_widgets()
    
    def create_widgets(self):
        """创建UI组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 设置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 创建左侧控制面板
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 窗口选择
        ttk.Label(control_frame, text="游戏窗口:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.window_var = tk.StringVar()
        self.window_combobox = ttk.Combobox(control_frame, textvariable=self.window_var, width=30)
        self.window_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 刷新窗口列表按钮
        self.refresh_btn = ttk.Button(control_frame, text="刷新窗口列表", command=self.refresh_window_list)
        self.refresh_btn.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        
        # 启动/停止按钮
        self.toggle_btn = ttk.Button(control_frame, text="启动识别", command=self.toggle_recognition)
        self.toggle_btn.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 设置区域
        settings_frame = ttk.LabelFrame(control_frame, text="设置", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # OCR置信度阈值
        ttk.Label(settings_frame, text="OCR置信度阈值:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ocr_threshold_var = tk.DoubleVar(value=0.7)
        self.ocr_threshold_scale = ttk.Scale(settings_frame, from_=0.5, to=1.0, variable=self.ocr_threshold_var, orient=tk.HORIZONTAL)
        self.ocr_threshold_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.ocr_threshold_label = ttk.Label(settings_frame, text="0.7")
        self.ocr_threshold_label.grid(row=0, column=2, sticky=tk.W, pady=5)
        self.ocr_threshold_scale.bind("<Motion>", self.update_ocr_threshold_label)
        
        # 匹配阈值
        ttk.Label(settings_frame, text="匹配阈值:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.match_threshold_var = tk.DoubleVar(value=0.6)
        self.match_threshold_scale = ttk.Scale(settings_frame, from_=0.1, to=1.0, variable=self.match_threshold_var, orient=tk.HORIZONTAL)
        self.match_threshold_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.match_threshold_label = ttk.Label(settings_frame, text="0.6")
        self.match_threshold_label.grid(row=1, column=2, sticky=tk.W, pady=5)
        self.match_threshold_scale.bind("<Motion>", self.update_match_threshold_label)
        
        # 创建右侧显示区域
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 图像显示区域
        image_frame = ttk.LabelFrame(display_frame, text="游戏画面", padding="5")
        image_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # 图像标签
        self.image_label = ttk.Label(image_frame)
        self.image_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        image_frame.columnconfigure(0, weight=1)
        image_frame.rowconfigure(0, weight=1)
        
        # 识别结果和策略建议区域
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.columnconfigure(1, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # OCR识别结果
        ocr_frame = ttk.LabelFrame(results_frame, text="OCR识别结果", padding="5")
        ocr_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        results_frame.rowconfigure(0, weight=1)
        
        self.ocr_text = scrolledtext.ScrolledText(ocr_frame, width=40, height=15)
        self.ocr_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        ocr_frame.columnconfigure(0, weight=1)
        ocr_frame.rowconfigure(0, weight=1)
        
        # 策略建议
        strategy_frame = ttk.LabelFrame(results_frame, text="策略建议", padding="5")
        strategy_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.strategy_text = scrolledtext.ScrolledText(strategy_frame, width=40, height=15)
        self.strategy_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        strategy_frame.columnconfigure(0, weight=1)
        strategy_frame.rowconfigure(0, weight=1)
        
        # 刷新窗口列表
        self.refresh_window_list()
    
    def refresh_window_list(self):
        """刷新窗口列表"""
        try:
            windows = self.screen_capture.get_window_list()
            self.window_combobox['values'] = windows
            if windows:
                self.window_var.set(windows[0])
        except Exception as e:
            print(f"刷新窗口列表失败: {e}")
    
    def update_ocr_threshold_label(self, event):
        """更新OCR置信度阈值标签"""
        value = round(self.ocr_threshold_var.get(), 2)
        self.ocr_threshold_label.config(text=str(value))
    
    def update_match_threshold_label(self, event):
        """更新匹配阈值标签"""
        value = round(self.match_threshold_var.get(), 2)
        self.match_threshold_label.config(text=str(value))
    
    def toggle_recognition(self):
        """切换识别状态"""
        if self.is_running:
            # 停止识别
            self.is_running = False
            self.toggle_btn.config(text="启动识别")
            # 移除join()调用，避免主线程等待子线程导致卡死
        else:
            # 启动识别
            self.is_running = True
            self.toggle_btn.config(text="停止识别")
            # 使用守护线程，确保程序退出时子线程能自动结束
            self.thread = threading.Thread(target=self.recognition_loop, daemon=True)
            self.thread.start()
    
    def recognition_loop(self):
        """识别循环"""
        while self.is_running:
            try:
                # 捕获屏幕
                screenshot = self.screen_capture.capture_window(self.window_var.get())
                if screenshot:
                    # 更新图像显示
                    self.update_image(screenshot)
                    
                    # OCR识别
                    ocr_results = self.ocr_engine.recognize_text(screenshot)
                    
                    # 更新OCR结果
                    self.update_ocr_results(ocr_results)
                    
                    # 匹配策略
                    strategies = self.data_matcher.match_strategy(ocr_results, min_score=self.ocr_threshold_var.get())
                    
                    # 更新策略建议
                    self.update_strategies(strategies)
            except Exception as e:
                print(f"识别循环错误: {e}")
            
            # 控制识别频率
            time.sleep(0.5)
    
    def update_image(self, image):
        """更新图像显示"""
        try:
            # 调整图像大小以适应显示区域
            width = 600
            height = int(image.height * (width / image.width))
            resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
            
            # 转换为PhotoImage
            photo = ImageTk.PhotoImage(resized_image)
            
            # 更新图像标签
            self.image_label.config(image=photo)
            self.image_label.image = photo  # 保持引用，防止被垃圾回收
        except Exception as e:
            print(f"更新图像失败: {e}")
    
    def update_ocr_results(self, ocr_results):
        """更新OCR识别结果"""
        try:
            self.ocr_text.delete(1.0, tk.END)
            for result in ocr_results:
                text = result["text"]
                score = round(result["score"], 2)
                self.ocr_text.insert(tk.END, f"{text} (置信度: {score})\n")
        except Exception as e:
            print(f"更新OCR结果失败: {e}")
    
    def update_strategies(self, strategies):
        """更新策略建议"""
        try:
            self.strategy_text.delete(1.0, tk.END)
            if strategies:
                for i, strategy in enumerate(strategies, 1):
                    self.strategy_text.insert(tk.END, f"策略{i}:\n")
                    #self.strategy_text.insert(tk.END, f"  类别: {strategy['类别']}\n")
                    self.strategy_text.insert(tk.END, f"  名称: {strategy['名称']}\n")
                    self.strategy_text.insert(tk.END, f"  效果: {strategy['效果']}\n")
                    self.strategy_text.insert(tk.END, f"  策略建议: {strategy['推荐']}\n\n")
            else:
                self.strategy_text.insert(tk.END, "未匹配到相关策略")
        except Exception as e:
            print(f"更新策略建议失败: {e}")
