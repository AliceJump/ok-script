# 贡献指南

> 面向 ok-oldking/ok-script 贡献者。
>
> ok-script 是一个基于图像识别技术的纯 Python 自动化测试框架。
> 支持 Windows 窗口和模拟器，包含 UI、截图、输入、设备控制、OCR、模板匹配等功能。

---

## 项目架构

`
ok/                   核心框架代码
  ├── alas/           调度/任务管理
  ├── capture/        截图模块
  ├── cli.py          命令行入口
  ├── device/         设备控制
  ├── feature/        特征/模板匹配
  ├── gui/            GUI 界面
  ├── ocr/            OCR 文字识别
  ├── task/           任务系统
  ├── update/         更新机制
  └── util/           工具函数
docs/                 文档
  ├── quick_start/    快速开始
  ├── api_doc/        API 文档
  ├── after_quick_start/  进阶使用
  └── intro_to_automation/ 游戏自动化入门
tests/                测试
`

---

## 贡献方式

### Fork & Clone

`ash
git clone https://github.com/你的账号/ok-script.git
cd ok-script
`

### 安装开发环境

`ash
pip install -e .
`

### 运行测试

`ash
pytest
`

### 提交 PR

1. 创建功能分支：git checkout -b feat/your-feature
2. 修改代码并确保测试通过
3. 推送并创建 PR → ok-oldking/ok-script

---

## 开发注意事项

- 框架核心代码位于 ok/ 包下，**不是** src/
- GUI 代码在 ok/gui/ 中，使用纯 Python 实现
- 国际化字符串在 ok/gui/i18n/ 中管理
- 请保持向后兼容性，影响其他 ok-* 项目的改动需在 PR 中说明

---

## 速查

`ash
# Fork 后 clone
git clone https://github.com/你的账号/ok-script.git
cd ok-script

# 安装
pip install -e .

# 运行测试
pytest

# 提交 PR
git checkout -b feat/your-feature
git add . && git commit -m "feat: description"
git push -u origin feat/your-feature
# GitHub → PR → ok-oldking/ok-script
`

