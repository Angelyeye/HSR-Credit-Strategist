#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试匹配逻辑
"""

from data_matcher import DataMatcher


def test_matcher():
    """测试匹配逻辑"""
    # 创建数据匹配实例
    dm = DataMatcher('货币战争策略数据.csv')
    
    # 测试案例："送复仇心切"匹配"复仇心切"
    ocr_results = [
        {'text': '送复仇心切', 'score': 0.78}
    ]
    
    # 调用匹配方法
    strategies = dm.match_strategy(ocr_results)
    
    # 打印结果
    print('测试案例："送复仇心切"匹配"复仇心切"')
    print('匹配到的策略：')
    for i, s in enumerate(strategies, 1):
        print(f'策略{i}:')
        print(f'  类别: {s["类别"]}')
        print(f'  名称: {s["名称"]}')
        print(f'  效果: {s["效果"]}')
        print(f'  推荐: {s["推荐"]}')
        print()
    
    # 测试案例：多个识别结果
    ocr_results2 = [
        {'text': '战个痛快', 'score': 1.0},
        {'text': '应激反应', 'score': 1.0},
        {'text': '第三位面强化', 'score': 0.99},
        {'text': '送复仇心切', 'score': 0.78}
    ]
    
    strategies2 = dm.match_strategy(ocr_results2)
    
    print('\n测试案例：多个识别结果')
    print('匹配到的策略：')
    for i, s in enumerate(strategies2, 1):
        print(f'策略{i}:')
        print(f'  类别: {s["类别"]}')
        print(f'  名称: {s["名称"]}')
        print(f'  效果: {s["效果"]}')
        print(f'  推荐: {s["推荐"]}')
        print()


if __name__ == '__main__':
    test_matcher()
