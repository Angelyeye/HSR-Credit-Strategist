#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据匹配模块
"""

import os
import pandas as pd
import re


class DataMatcher:
    """数据匹配类"""
    
    def __init__(self, strategy_data_path):
        """初始化数据匹配器
        
        Args:
            strategy_data_path: 策略数据CSV路径
        """
        self.strategy_data_path = strategy_data_path
        self.strategy_data = None
        self.keyword_index = {}
        self.load_strategy_data()
    
    def load_strategy_data(self):
        """加载策略数据"""
        try:
            # 尝试使用不同编码读取CSV文件
            encodings = ['utf-8', 'gbk', 'gb2312', 'ansi']
            
            for encoding in encodings:
                try:
                    # 读取CSV文件
                    self.strategy_data = pd.read_csv(
                        self.strategy_data_path,
                        encoding=encoding,
                        header=None,
                        skiprows=1,  # 跳过表头
                        usecols=[0, 1, 2, 3]  # 只读取前4列
                    )
                    
                    # 检查数据是否正确加载
                    if not self.strategy_data.empty:
                        print(f"使用编码{encoding}成功加载策略数据")
                        break
                except Exception as e:
                    print(f"使用编码{encoding}读取CSV失败: {e}")
            
            if self.strategy_data is None or self.strategy_data.empty:
                print("无法加载策略数据")
                return
            
            # 设置列名
            self.strategy_data.columns = ['类别', '名称', '效果', '推荐']
            
            # 构建关键词索引
            self.build_keyword_index()
            
            print(f"策略数据加载成功，共{len(self.strategy_data)}条记录")
        except Exception as e:
            print(f"加载策略数据失败: {e}")
            self.strategy_data = None
    
    def build_keyword_index(self):
        """构建关键词索引"""
        if self.strategy_data is None:
            return
        
        # 清空索引
        self.keyword_index.clear()
        
        # 遍历每条策略数据
        for index, row in self.strategy_data.iterrows():
            # 提取关键词
            keywords = []
            
            # 将完整策略名称作为重要关键词
            if pd.notna(row['名称']):
                name = str(row['名称'])
                keywords.append(name)  # 完整名称作为一级关键词
                
                # 从名称中提取中文关键词作为二级关键词
                # name_words = re.findall(r'[\u4e00-\u9fa5]+', name)
                # keywords.extend(name_words)
            
            # 从效果中提取关键词作为三级关键词
            # if pd.notna(row['效果']):
            #     effect = str(row['效果'])
            #     effect_words = re.findall(r'[\u4e00-\u9fa5]+', effect)
            #     keywords.extend(effect_words)
            
            # 添加到索引
            for keyword in keywords:
                if keyword not in self.keyword_index:
                    self.keyword_index[keyword] = []
                self.keyword_index[keyword].append(index)
    
    def match_strategy(self, ocr_results, min_score=0.75):
        """匹配策略
        
        Args:
            ocr_results: OCR识别结果，格式为[{"text": "文本内容", "score": 置信度}, ...]
            min_score: 最低匹配分数
            
        Returns:
            list: 匹配到的策略，格式为[{"类别": "类别", "名称": "名称", "效果": "效果", "推荐": "推荐"}, ...]
        """
        if self.strategy_data is None:
            return []
        
        # 过滤低置信度的OCR结果
        filtered_results = [r for r in ocr_results if r["score"] >= min_score]
        if not filtered_results:
            return []
        
        # 提取识别到的文本和置信度
        recognized_text = "".join([r["text"] for r in filtered_results])
        
        # 创建OCR识别结果的关键词集合
        ocr_keywords = set()
        for result in filtered_results:
            text = result["text"]
            # 添加完整文本作为关键词
            ocr_keywords.add(text)
            
            # 提取中文关键词
            chinese_text = ''.join(re.findall(r'[\u4e00-\u9fa5]+', text))
            
            # 提取所有可能的四字及以上中文短语作为关键词
            # 因为所有词条名称至少有四个字
            for i in range(len(chinese_text) - 3):
                for j in range(i + 4, len(chinese_text) + 1):
                    phrase = chinese_text[i:j]
                    ocr_keywords.add(phrase)
            
            # 提取所有可能的中文单词（单字）
            ocr_keywords.update(list(chinese_text))
        
        # 计算每个策略的匹配分数
        strategy_scores = {}
        
        # 遍历每条策略数据
        for index, row in self.strategy_data.iterrows():
            score = 0.0
            
            # 获取策略名称
            if pd.notna(row['名称']):
                strategy_name = str(row['名称'])
                
                # 完整名称匹配（最高权重）
                if strategy_name in recognized_text:
                    score += 10.0
                
                # 名称关键词匹配（中等权重）
                name_words = re.findall(r'[\u4e00-\u9fa5]+', strategy_name)
                for word in name_words:
                    if word in ocr_keywords:
                        score += 5.0
            
            # 获取策略效果
            # if pd.notna(row['效果']):
            #     strategy_effect = str(row['效果'])
                
            #     # 效果关键词匹配（低权重）
            #     effect_words = re.findall(r'[\u4e00-\u9fa5]+', strategy_effect)
            #     for word in effect_words:
            #         if word in ocr_keywords:
            #             score += 2.0
            
            # 只有分数大于0的策略才被认为是匹配的
            if score > 0:
                strategy_scores[index] = score
        
        # 按分数降序排序
        sorted_indices = sorted(strategy_scores.keys(), key=lambda x: strategy_scores[x], reverse=True)
        
        # 获取匹配的策略
        matched_strategies = []
        for index in sorted_indices:
            row = self.strategy_data.loc[index]
            matched_strategies.append({
                "类别": row["类别"],
                "名称": row["名称"],
                "效果": row["效果"],
                "推荐": row["推荐"]
            })
        
        return matched_strategies
    
    def fuzzy_match(self, ocr_results, threshold=0.6):
        """模糊匹配策略
        
        Args:
            ocr_results: OCR识别结果
            threshold: 模糊匹配阈值
            
        Returns:
            list: 匹配到的策略
        """
        if self.strategy_data is None:
            return []
        
        # 过滤低置信度的OCR结果
        filtered_results = [r for r in ocr_results if r["score"] >= 0.75]
        if not filtered_results:
            return []
        
        # 提取识别到的文本
        recognized_text = "".join([r["text"] for r in filtered_results])
        
        # 计算每条策略与识别文本的相似度
        matched_strategies = []
        
        for index, row in self.strategy_data.iterrows():
            # 构建策略文本
            strategy_text = ""
            for column in ['名称', '效果']:
                if pd.notna(row[column]):
                    strategy_text += str(row[column])
            
            # 计算相似度
            similarity = self.calculate_similarity(recognized_text, strategy_text)
            
            if similarity >= threshold:
                matched_strategies.append({
                    "类别": row["类别"],
                    "名称": row["名称"],
                    "效果": row["效果"],
                    "推荐": row["推荐"],
                    "相似度": similarity
                })
        
        # 按相似度排序
        matched_strategies.sort(key=lambda x: x["相似度"], reverse=True)
        
        # 移除相似度字段
        for strategy in matched_strategies:
            del strategy["相似度"]
        
        return matched_strategies
    
    def calculate_similarity(self, text1, text2):
        """计算文本相似度（简单的Jaccard相似度）
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            float: 相似度，范围0-1
        """
        # 提取中文词语
        words1 = set(re.findall(r'[\u4e00-\u9fa5]+', text1))
        words2 = set(re.findall(r'[\u4e00-\u9fa5]+', text2))
        
        # 计算交集和并集
        intersection = words1 & words2
        union = words1 | words2
        
        # 计算Jaccard相似度
        if len(union) == 0:
            return 0.0
        
        return len(intersection) / len(union)
    
    def get_strategy_by_name(self, name):
        """根据名称获取策略
        
        Args:
            name: 策略名称
            
        Returns:
            dict: 策略信息，或None
        """
        if self.strategy_data is None:
            return None
        
        # 查找策略
        matched = self.strategy_data[self.strategy_data['名称'].str.contains(name, na=False)]
        
        if not matched.empty:
            row = matched.iloc[0]
            return {
                "类别": row["类别"],
                "名称": row["名称"],
                "效果": row["效果"],
                "推荐": row["推荐"]
            }
        
        return None
