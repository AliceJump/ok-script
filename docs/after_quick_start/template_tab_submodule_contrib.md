# 模板 Tab 详细图文流程（含 submodule 贡献）

> 面向基于 `ok-script` 的模板项目维护者（项目中存在 `ok_templates/` 子仓库时）。

---

## 先理解结构

```text
ok_templates/  (子仓库: 标注原图 + coco JSON)
     │ Template Tab: Screenshot / Markup / Save
     ▼
assets/        (主仓库: 裁剪压缩后的模板产物)
     │ config.py / src/config.py 指向这里
     ▼
FeatureSet → BaseTask.find_feature/find_one → cv2.matchTemplate
```

**关键原则**：`ok_templates/` 是模板源码，`assets/` 是运行产物。改模板时先改源码，再导出到 `assets/`。

---

## 完整流程

### 1) Fork 两个仓库

1. Fork 主仓库（你的模板项目主仓库）。
2. Fork 模板源仓库（通常是 `ok_templates/` 对应的子仓库）。

### 2) Clone（含 submodule）

```bash
git clone --recursive https://github.com/你的账号/your-project.git
cd your-project
```

如已克隆但未初始化子模块：

```bash
git submodule update --init --recursive
```

### 3) 修改子仓库 remote 并签出分支

```bash
cd ok_templates
git remote set-url origin https://github.com/你的账号/your-template-repo.git
git checkout -b update-templates
```

### 4) 进入 Debug 模式进行模板维护（图文流程）

```bash
cd ..
python main_debug.py
```

在左侧模板 Tab 执行：

1. **Screenshot**：截图（建议使用高分辨率原图）。
2. **Markup**：框选目标元素并命名模板名（名称需与代码调用一致）。
3. **Save**：在弹窗中选择保存到本软件 `assets`。

> **重要**：只有在 `python main_debug.py` 下，模板 Tab 的 Save 弹窗里才有“保存到本软件 `assets`”选项。  
> `python main.py` 不用于模板素材维护导出。

### 5) 本地检查

```bash
cd ok_templates && git status      # 子仓库源码变更
cd .. && git diff assets/          # 主仓库产物更新
```

### 6) 推送子仓库并提 PR

```bash
cd ok_templates
git add .
git commit -m "feat: update template sources"
git push -u origin update-templates
```

先创建子仓库 PR（你的 fork → 上游模板源仓库），并等待合并。

### 7) 子仓库合并后，再更新主仓库

```bash
cd ok_templates
git fetch origin
git checkout main
git pull origin main
cd ..
python main_debug.py   # 再次通过模板 Tab Save 到 assets
git add ok_templates assets
git commit -m "feat: update templates and submodule"
git push -u origin update-templates
```

然后创建主仓库 PR（你的 fork → 上游主仓库）。

---

## 常见错误速查

| 错误 | 原因 | 解决 |
|------|------|------|
| `Permission denied` push 失败 | remote 仍指向上游 | `git remote set-url origin` 改到你的 fork |
| 子模块 `dirty` | 子仓库修改未提交 | `cd ok_templates && git status` |
| PR 里只有子模块指针变化、没有 `assets` 更新 | 没在 Debug 模式重新 Save | 重新 `python main_debug.py` → 模板 Tab Save 到 `assets` |
| `not found in featureDict` | 模板名不一致或未导出 | 检查命名并确认 `assets` 已更新 |

