#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据匹配模块
"""

import os
import pandas as pd
import re


class AhoCorasickNode:
    """AC自动机节点"""
    
    def __init__(self):
        """初始化节点"""
        self.children = {}  # 子节点
        self.fail = None     # 失败指针
        self.output = []     # 输出列表，存储匹配到的模式串索引


class AhoCorasick:
    """AC自动机"""
    
    def __init__(self):
        """初始化AC自动机"""
        self.root = AhoCorasickNode()
    
    def add_pattern(self, pattern, index):
        """添加模式串
        
        Args:
            pattern: 模式串
            index: 模式串对应的索引
        """
        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = AhoCorasickNode()
            node = node.children[char]
        node.output.append(index)
    
    def build_fail_links(self):
        """构建失败指针"""
        from collections import deque
        
        queue = deque()
        
        # 初始化根节点的所有子节点的失败指针为根节点
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)
        
        # BFS构建失败指针
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                queue.append(child)
                
                # 查找当前节点的失败指针
                fail_node = current.fail
                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail
                
                if fail_node is None:
                    child.fail = self.root
                else:
                    child.fail = fail_node.children[char]
                    # 合并输出列表
                    child.output.extend(child.fail.output)
    
    def search(self, text):
        """搜索文本中的模式串
        
        Args:
            text: 待搜索文本
            
        Returns:
            list: 匹配到的模式串索引列表
        """
        matched_indices = set()
        node = self.root
        
        for char in text:
            # 沿着失败指针查找匹配的节点
            while node is not None and char not in node.children:
                node = node.fail
            
            if node is None:
                node = self.root
                continue
            
            node = node.children[char]
            
            # 收集匹配结果
            if node.output:
                matched_indices.update(node.output)
        
        return list(matched_indices)


class DataMatcher:
    """数据匹配类"""
    
    def __init__(self, strategy_data_path):
        """初始化数据匹配器
        
        Args:
            strategy_data_path: 策略数据CSV路径
        """
        self.strategy_data_path = strategy_data_path
        self.strategy_data = None
        self.ac_automaton = None
        self.pattern_index_map = {}  # 模式串到索引的映射
        self.index_pattern_map = {}  # 索引到模式串的映射
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
        """构建AC自动机索引"""
        if self.strategy_data is None:
            return
        
        # 创建AC自动机实例
        self.ac_automaton = AhoCorasick()
        
        # 重置映射
        self.pattern_index_map.clear()
        self.index_pattern_map.clear()
        
        # 遍历每条策略数据
        for index, row in self.strategy_data.iterrows():
            # 将完整策略名称作为模式串
            if pd.notna(row['名称']):
                name = str(row['名称'])
                # 只添加4个汉字及以上的名称
                if len(name) >= 4:
                    # 添加到AC自动机
                    self.ac_automaton.add_pattern(name, index)
                    # 更新映射
                    self.pattern_index_map[name] = index
                    self.index_pattern_map[index] = name
        
        # 构建失败指针
        self.ac_automaton.build_fail_links()
    
    def match_strategy(self, ocr_results, min_score=0.75):
        """匹配策略
        
        Args:
            ocr_results: OCR识别结果，格式为[{"text": "文本内容", "score": 置信度}, ...]
            min_score: 最低匹配分数
            
        Returns:
            list: 匹配到的策略，格式为[{"类别": "类别", "名称": "名称", "效果": "效果", "推荐": "推荐"}, ...]
        """
        if self.strategy_data is None or self.ac_automaton is None:
            return []
        
        # 过滤低置信度的OCR结果
        filtered_results = [r for r in ocr_results if r["score"] >= min_score]
        if not filtered_results:
            return []
        
        # 提取识别到的文本
        recognized_text = "".join([r["text"] for r in filtered_results])
        
        # 使用AC自动机搜索匹配的策略
        matched_indices = self.ac_automaton.search(recognized_text)
        
        # 如果没有匹配到结果，尝试提取中文文本后再次匹配
        if not matched_indices:
            # 提取中文文本
            chinese_text = ''.join(re.findall(r'[\u4e00-\u9fa5]+', recognized_text))
            # 再次搜索
            matched_indices = self.ac_automaton.search(chinese_text)
        
        # 如果仍然没有匹配到结果，返回空列表
        if not matched_indices:
            return []
        
        # 计算每个策略的匹配分数
        strategy_scores = {}
        
        # 遍历匹配到的索引
        for index in matched_indices:
            # 获取策略名称
            strategy_name = self.index_pattern_map.get(index, "")
            if not strategy_name:
                continue
            
            # 计算匹配分数
            score = 0.0
            
            # 检查完整名称匹配
            if strategy_name in recognized_text:
                score += 10.0
            
            # 检查在中文文本中的匹配
            chinese_text = ''.join(re.findall(r'[\u4e00-\u9fa5]+', recognized_text))
            if strategy_name in chinese_text:
                score += 8.0
            
            # 检查在OCR结果中的匹配
            # 暂时注释掉OCR置信度参与匹配的逻辑
            # for result in filtered_results:
            #     if strategy_name in result["text"]:
            #         # 结合OCR置信度计算分数
            #         score += 5.0 * result["score"]
            
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
