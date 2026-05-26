# ok-script
* ok-script 是基于图像识别技术, 纯Python实现的, 支持Windows窗口和模拟器的自动化测试框架。
* 框架包含UI, 截图, 输入, 设备控制, OCR, 模板匹配, 框框Debug浮层, 基于Github Action的测试, 打包, 升级/降级。
* 基于开发一个工业级的自动化软件仅需几百行代码。

## 优势

1. 纯Python实现, 免费开源, 依赖库均为开源方案
2. 支持pip install任何第三方库, 可以方便整合yolo等框架
3. 一套代码即可支持Windows安卓模拟器/ADB连接的虚拟机, Windows客户端游戏
4. 自适应分辨率
5. 使用coco管理图片匹配素材, 仅需一个分辨率下的截图就, 支持不同分辨率自适应
6. 可打包离线/在线安装setup.exe, 支持通过Pip/Git国内镜像在线增量更新. 在线安装包仅3M
7. 支持Github Action一键构建
8. 支持多语言国际化

## [使用基于ok-script的按键精灵, 快速学习和开始](https://github.com/ok-oldking/ok-py)

**API列表, 脚本录制**
![image_scripting](docs/ok_py/image_scripting.png)

**支持多种截图以及交互方式**
![image_screenshot](docs/ok_py/image_capture.png)

**标注管理 (Template Matching)**
![image_template](docs/ok_py/image_template.png)
![image_markup](docs/ok_py/image_markup.png)

### 使用 推荐使用Python 3.12

* 在你的项目中通过pip依赖使用
```commandline
pip install ok-script
```

* 编译国际化文件
```commandline
compile_i18n.cmd
```

## Web 部署（前端静态托管）

当前仓库主要是 Windows/PySide 桌面端代码，不包含现成的前端构建产物目录。  
已提供最小 Web 托管入口（`python -m ok_web`），可用于部署你已有的前端产物。

### 1) 依赖拆分

* 桌面端/完整开发依赖：`requirements-desktop.txt`
* Web 部署依赖：`requirements-web.txt`（仅标准库，无 GUI/Windows 依赖）

### 2) 放置前端产物

默认静态目录为 `web/`（仓库内已放置占位 `index.html`）。  
你也可以通过环境变量或参数指定其他目录。

### 3) 启动服务（默认端口 10086）

```commandline
python -m ok_web
```

可选参数：

```commandline
python -m ok_web --host 0.0.0.0 --port 10086 --static-dir web
```

环境变量覆盖：

* `PORT` 或 `WEB_PORT`：覆盖端口（默认 `10086`）
* `WEB_STATIC_DIR`：覆盖静态目录（默认 `web`）

### 4) 健康检查

* `GET /health` -> `{"status": "ok"}`
* `GET /` -> 返回 `index.html`

### 5) 反向代理建议

建议由 Nginx/Caddy 反向代理到 `http://127.0.0.1:10086`，并在代理层处理 HTTPS、域名和缓存策略。

## 文档和示例代码

* [游戏自动化入门](docs/intro_to_automation/README.md)
  - [1、基本原理：计算机如何“玩”游戏](docs/intro_to_automation/README.md#一基本原理计算机如何玩游戏)
    - [核心循环：三步走](docs/intro_to_automation/README.md#核心循环三步走)
    - [图像分析：从像素到决策](docs/intro_to_automation/README.md#图像分析从像素到决策)
        - [传统图色算法 (OpenCV 库)](docs/intro_to_automation/README.md#1-传统图色算法-opencv-库)
        - [神经网络推理 (Inference)](docs/intro_to_automation/README.md#2-神经网络推理-inference)
    - [2、编程语言选择](docs/intro_to_automation/README.md#二编程语言选择)
        - [常用库概览](docs/intro_to_automation/README.md#常用库概览)
    - [3、开发工具](docs/intro_to_automation/README.md#三开发工具)
* [快速开始](docs/quick_start/README.md)
* [API文档](docs/api_doc/README.md)
  - [Box](docs/api_doc/README.md#box)
  - [BaseTask](docs/api_doc/README.md#basetask)
    - [截图 (Screenshot)](docs/api_doc/README.md#截图-screenshot)
    - [输入 (Input)](docs/api_doc/README.md#输入-input)
    - [OCR](docs/api_doc/README.md#ocr)
    - [找图 (Image finding)](docs/api_doc/README.md#找图-image-finding)
* [进阶使用](docs/after_quick_start/README.md)
  - [1. 模板匹配 (Template Matching)](docs/after_quick_start/README.md#1-模板匹配-template-matching)
  - [2. 多语言国际化 (i18n)](docs/after_quick_start/README.md#2-多语言国际化-i18n)
  - [3. 自动化测试](docs/after_quick_start/README.md#3-自动化测试)
  - [4. 使用 GitHub Action 自动化打包与发布](docs/after_quick_start/README.md#4-使用-github-action-自动化打包与发布)
* 开发者群: 938132715
* pip [https://pypi.org/project/ok-script](https://pypi.org/project/ok-script)


## 使用ok-script的项目：

* 鸣潮 [https://github.com/ok-oldking/ok-wuthering-wave](https://github.com/ok-oldking/ok-wuthering-waves)
* 原神(不在维护,
  但是后台过剧情可用) [https://github.com/ok-oldking/ok-genshin-impact](https://github.com/ok-oldking/ok-genshin-impact)
* 少前2 [https://github.com/ok-oldking/ok-gf2](https://github.com/ok-oldking/ok-gf2)
* 星铁 [https://github.com/Shasnow/ok-starrailassistant](https://github.com/Shasnow/ok-starrailassistant)
* 星痕共鸣 [https://github.com/Sanheiii/ok-star-resonance](https://github.com/Sanheiii/ok-star-resonance)
* 二重螺旋 [https://github.com/BnanZ0/ok-duet-night-abyss](https://github.com/BnanZ0/ok-duet-night-abyss)
* 白荆回廊(停止更新) [https://github.com/ok-oldking/ok-baijing](https://github.com/ok-oldking/ok-baijing)
* 终末地 [https://github.com/AliceJump/ok-end-field](https://github.com/AliceJump/ok-end-field)
* 异环 [https://github.com/BnanZ0/ok-nte](https://github.com/BnanZ0/ok-nte)
