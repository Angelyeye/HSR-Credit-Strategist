# 崩铁货币战争策略助手

## 项目概述

### 项目名称
崩铁货币战争策略助手（StarRail Currency War Strategy Assistant）

### 项目简介
崩铁货币战争策略助手是一款专为游戏《崩坏：星穹铁道》中的「货币战争」玩法设计的实时策略辅助工具。该工具通过OCR技术识别游戏画面中的中文词条，自动匹配最优策略建议，帮助玩家在游戏中取得更好的成绩。

### 主要功能
- **实时屏幕捕获**：自动查找并捕获游戏窗口画面
- **高精度OCR识别**：集成PaddleOCR引擎，实现高性能中文识别
- **智能策略匹配**：根据识别结果匹配最优策略建议
- **直观GUI界面**：实时显示游戏画面、识别结果和策略建议
- **灵活配置选项**：支持调整置信度阈值、匹配阈值等参数

### 项目特点
- **高效性能**：采用C++推理库的PaddleOCR-json，性能优于Python原生库
- **实时响应**：识别延迟低，策略建议实时更新
- **易于使用**：直观的GUI界面，操作简单
- **可扩展性**：模块化设计，便于后续功能扩展
- **跨平台兼容**：支持Windows系统
- **AI辅助开发**：主要依靠字节跳动出品的Trae的solo模式编写

### 开发工具
本项目主要依靠**字节跳动出品的Trae**的solo模式编写，Trae是一款强大的AI编程助手，能够帮助开发者快速高效地完成代码开发工作。

欢迎大家使用并提出宝贵意见！

## 环境要求与安装步骤

### 环境要求
- **操作系统**：Windows 10/11
- **Python版本**：Python 3.8+
- **游戏**：《崩坏：星穹铁道》

### 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/your-username/starrail-currency-war-assistant.git
cd starrail-currency-war-assistant
```

#### 2. 安装依赖
```bash
pip install -r requirements.txt
```

#### 3. 配置PaddleOCR引擎
- 从 [PaddleOCR-json Releases](https://github.com/hiroi-sora/PaddleOCR-json/releases) 下载Windows版本的OCR引擎
- 解压到项目目录下，确保路径结构为：`PaddleOCR-json_v1.4.1_windows_x64/PaddleOCR-json_v1.4.1/PaddleOCR-json.exe`

#### 4. 准备策略数据
- 确保项目目录下存在 `货币战争策略数据.csv` 文件
- 该文件包含游戏中的各种策略数据，用于匹配识别结果

## 使用指南

### 基本操作

1. **启动游戏**：确保《崩坏：星穹铁道》正在运行，并进入「货币战争」玩法

2. **运行策略助手**：
```bash
python main.py
```

3. **选择游戏窗口**：
   - 在GUI界面的「游戏窗口」下拉菜单中选择游戏窗口
   - 点击「刷新窗口列表」按钮更新窗口列表

4. **启动识别**：
   - 点击「启动识别」按钮开始实时识别
   - 程序将自动捕获游戏画面，识别中文词条，并匹配策略建议

5. **查看结果**：
   - 右侧「游戏画面」区域显示实时捕获的游戏画面
   - 「OCR识别结果」区域显示识别到的中文词条及置信度
   - 「策略建议」区域显示匹配到的策略建议

6. **停止识别**：
   - 点击「停止识别」按钮停止实时识别

### 配置选项

- **OCR置信度阈值**：调整OCR识别结果的置信度过滤阈值
- **匹配阈值**：调整策略匹配的相似度阈值

### 常用命令

```bash
# 启动程序
python main.py

# 安装依赖
pip install -r requirements.txt

# 生成依赖列表
pip freeze > requirements.txt
```

## 项目结构说明

```
starrail-currency-war-assistant/
├── main.py                 # 主程序入口
├── screen_capture.py       # 屏幕捕获模块
├── ocr_engine.py           # OCR引擎模块
├── data_matcher.py         # 数据匹配模块
├── gui.py                  # GUI界面模块
├── 货币战争策略数据.csv       # 策略数据文件
├── PaddleOCR-json_v1.4.1_windows_x64/  # PaddleOCR引擎目录
├── PaddleOCR-json-main/    # PaddleOCR API目录
├── requirements.txt        # 项目依赖
└── README.md               # 项目说明文档
```

### 主要文件功能

| 文件名称 | 功能描述 |
|---------|---------|
| main.py | 主程序入口，负责初始化各个模块和启动GUI |
| screen_capture.py | 实现游戏窗口查找和屏幕捕获功能 |
| ocr_engine.py | 集成PaddleOCR API，实现图像预处理和文本识别 |
| data_matcher.py | 解析策略数据，构建匹配索引，实现匹配算法 |
| gui.py | 设计GUI界面，实现实时画面显示和策略建议展示 |
| 货币战争策略数据.csv | 存储游戏中的各种策略数据 |

## 贡献指南

### 代码提交规范

1. **提交信息格式**：
   ```
   <类型>: <描述>
   
   <详细说明>
   ```
   
   类型包括：
   - feat: 新功能
   - fix: 修复bug
   - docs: 文档更新
   - style: 代码格式调整
   - refactor: 代码重构
   - test: 测试用例更新
   - chore: 构建过程或辅助工具变动

2. **代码风格**：
   - 遵循PEP 8编码规范
   - 使用4个空格缩进
   - 变量命名使用小写字母和下划线
   - 类名使用驼峰命名法

### 分支管理策略

- **main**：主分支，用于发布稳定版本
- **develop**：开发分支，用于集成新功能
- **feature/**：功能分支，用于开发新功能
- **bugfix/**：bug修复分支，用于修复bug

### PR流程

1. Fork项目到个人仓库
2. 创建功能分支
3. 提交代码
4. 创建Pull Request
5. 等待代码审查
6. 合并到develop分支

## 许可证信息

本项目采用MIT许可证，详见LICENSE文件。

## 联系方式及致谢

### 联系方式

- **项目地址**：https://github.com/your-username/starrail-currency-war-assistant
- **Issues**：https://github.com/your-username/starrail-currency-war-assistant/issues

### 致谢

- 感谢 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 提供的OCR技术支持
- 感谢 [PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json) 提供的高效OCR API
- 感谢所有为项目做出贡献的开发者

## 更新日志

### v1.0.0 (2025-12-01)
- 初始版本发布
- 实现实时屏幕捕获功能
- 集成PaddleOCR引擎
- 实现策略匹配算法
- 设计GUI界面

## 常见问题

### Q: 程序无法找到游戏窗口怎么办？
A: 确保游戏正在运行，并且窗口标题包含「星穹铁道」字样，然后点击「刷新窗口列表」按钮。

### Q: OCR识别精度不高怎么办？
A: 可以尝试调整「OCR置信度阈值」滑块，降低阈值可以提高识别率，但可能会增加误识别。

### Q: 策略匹配不准确怎么办？
A: 可以尝试调整「匹配阈值」滑块，降低阈值可以提高匹配率，但可能会匹配到不相关的策略。

### Q: 程序运行时出现卡顿怎么办？
A: 可以尝试关闭其他占用资源较多的程序，或者降低游戏画面分辨率。

## 免责声明

本工具仅用于学习和研究目的，请勿用于任何商业用途。使用本工具可能违反游戏的用户协议，请谨慎使用。本项目作者不承担任何因使用本工具而产生的法律责任。