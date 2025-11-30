#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
屏幕捕获模块
"""

from PIL import Image, ImageGrab
import win32gui


class ScreenCapture:
    """屏幕捕获类"""
    
    def __init__(self):
        """初始化"""
        self.game_window = None
        self.capture_region = None
        self.window_handles = {}
    
    def enum_windows_callback(self, hwnd, extra):
        """枚举窗口回调函数"""
        # 检查窗口是否可见
        if win32gui.IsWindowVisible(hwnd):
            # 获取窗口标题
            title = win32gui.GetWindowText(hwnd)
            if title:
                self.window_handles[title] = hwnd
    
    def find_game_window(self, exe_name="StarRail.exe"):
        """查找游戏窗口
        
        Args:
            exe_name: 游戏进程名称
            
        Returns:
            bool: 是否找到游戏窗口
        """
        try:
            # 枚举所有窗口
            self.window_handles.clear()
            win32gui.EnumWindows(self.enum_windows_callback, None)
            
            # 查找包含游戏名称的窗口
            for title, hwnd in self.window_handles.items():
                if "星穹铁道" in title:
                    # 获取窗口位置和大小
                    rect = win32gui.GetWindowRect(hwnd)
                    self.game_window = {
                        "hwnd": hwnd,
                        "title": title,
                        "top": rect[1],
                        "left": rect[0],
                        "width": rect[2] - rect[0],
                        "height": rect[3] - rect[1]
                    }
                    self.capture_region = {
                        "top": self.game_window["top"],
                        "left": self.game_window["left"],
                        "width": self.game_window["width"],
                        "height": self.game_window["height"]
                    }
                    return True
            
            return False
        except Exception as e:
            print(f"查找游戏窗口失败: {e}")
            return False
    
    def set_capture_region(self, region):
        """设置捕获区域
        
        Args:
            region: 捕获区域，格式为(top, left, width, height)
        """
        self.capture_region = {
            "top": region[0],
            "left": region[1],
            "width": region[2],
            "height": region[3]
        }
    
    def capture_screen(self):
        """捕获屏幕
        
        Returns:
            PIL.Image: 捕获的图像
        """
        try:
            if not self.capture_region:
                # 如果没有设置捕获区域，捕获整个屏幕
                img = ImageGrab.grab()
            else:
                # 捕获指定区域
                bbox = (
                    self.capture_region["left"],
                    self.capture_region["top"],
                    self.capture_region["left"] + self.capture_region["width"],
                    self.capture_region["top"] + self.capture_region["height"]
                )
                img = ImageGrab.grab(bbox)
            
            return img
        except Exception as e:
            print(f"捕获屏幕失败: {e}")
            return None
    
    def capture_window(self, window_title=None):
        """捕获指定窗口
        
        Args:
            window_title: 窗口标题
            
        Returns:
            PIL.Image: 捕获的图像
        """
        try:
            if window_title:
                # 查找指定标题的窗口
                self.window_handles.clear()
                win32gui.EnumWindows(self.enum_windows_callback, None)
                
                if window_title in self.window_handles:
                    hwnd = self.window_handles[window_title]
                    # 获取窗口位置和大小
                    rect = win32gui.GetWindowRect(hwnd)
                    self.capture_region = {
                        "top": rect[1],
                        "left": rect[0],
                        "width": rect[2] - rect[0],
                        "height": rect[3] - rect[1]
                    }
            elif not self.capture_region:
                # 如果没有设置捕获区域，查找游戏窗口
                if not self.find_game_window():
                    # 如果找不到游戏窗口，捕获整个屏幕
                    self.capture_region = None
            
            # 捕获屏幕
            return self.capture_screen()
        except Exception as e:
            print(f"捕获窗口失败: {e}")
            return None
    
    def get_window_list(self):
        """获取所有窗口列表
        
        Returns:
            list: 窗口标题列表
        """
        try:
            # 枚举所有窗口
            self.window_handles.clear()
            win32gui.EnumWindows(self.enum_windows_callback, None)
            
            # 返回窗口标题列表
            return list(self.window_handles.keys())
        except Exception as e:
            print(f"获取窗口列表失败: {e}")
            return []
