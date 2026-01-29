# ASIN/OE 链接打开工具

## 功能概述

该工具用于批量打开 ASIN 或 OE 链接，支持多个国家的 Amazon 和 eBay 网站。用户可以在输入框中输入多个 ASIN 或 OE 编号，并选择目标站点，工具会自动打开相应的链接。

## 主要功能

### 1. 输入 ASIN/OE 编号

用户可以在输入框中输入多个 ASIN 或 OE 编号，编号之间可以用换行符或逗号分隔。

### 2. 选择目标站点

用户可以从下拉菜单中选择目标站点，支持以下站点：
- 英国
- 德国
- 意大利
- 法国
- 西班牙

### 3. 打开链接

点击"打开链接"按钮后，工具会逐个打开输入的 ASIN 或 OE 编号对应的链接。支持以下情况：
- 如果编号以 `B0` 开头且长度为 10，则认为是 ASIN，打开 Amazon 链接。
- 如果编号是 12 位数字且目标站点为英国或德国，则认为是 eBay itemid，打开 eBay 链接。
- 其他情况则认为是 OE 编号，打开 Amazon 搜索链接。

### 4. 停止打开链接

用户可以按下 `ESC` 键来停止打开链接，工具会弹出提示框告知用户已停止操作。

## 详细说明

### 输入处理

- 获取输入框中的文本，按换行符或逗号分隔成多个编号。
- 去除空白项并去除前后空白字符。
- 如果输入的编号超过 10 个，弹出警告提示框。

### 站点选择

- 用户可以从下拉菜单中选择默认站点。
- 支持的站点包括英国、德国、意大利、法国和西班牙。

### 链接生成

- 根据用户选择的站点和编号类型，生成相应的链接并打开。
- 支持按下 `ESC` 键停止打开链接。

### 国家前缀处理

- 检查编号是否有国家前缀（例如 `[UK]`）。
- 根据国家前缀选择相应的站点。

### 链接类型判断

- 如果编号以 `B0` 开头且长度为 10，则认为是 ASIN，生成 Amazon 链接。
- 如果编号是 12 位数字且目标站点为英国或德国，则认为是 eBay itemid，生成 eBay 链接。
- 其他情况则认为是 OE 编号，生成 Amazon 搜索链接。

## 界面元素

- 主窗口：用于显示工具界面。
- 输入框：用于输入多个 ASIN 或 OE 编号。
- 站点选择下拉菜单：用于选择目标站点。
- 打开链接按钮：用于开始批量打开链接。
- 停止操作：按下 `ESC` 键停止打开链接。

## 使用方法

### 运行 Python 脚本
1. 确保已安装 Python 3.11+
2. 运行 `python ASIN-OE-Opener.py`

### 使用 macOS 可执行文件
1. 从 GitHub Releases 下载最新版本
2. 选择适合的格式：
   - **单文件可执行文件**: 下载 `ASIN-OE-Opener`，运行 `chmod +x ASIN-OE-Opener && ./ASIN-OE-Opener`
   - **应用程序包**: 下载 `ASIN-OE-Opener.app.zip`，解压后双击运行
   - **DMG 安装包**: 下载 `ASIN-OE-Opener.dmg`，拖拽安装到 Applications

### 工具使用步骤
1. 在输入框中输入多个 ASIN 或 OE 编号，编号之间用换行符或逗号分隔。
2. 从下拉菜单中选择目标站点。
3. 点击"打开链接"按钮，工具会逐个打开输入的编号对应的链接。
4. 如果需要停止操作，按下 `ESC` 键。

## macOS 构建

### 自动构建 (GitHub Actions)
项目配置了 GitHub Actions 工作流，自动构建适用于 macOS（包括 M 系列 Apple Silicon）的可执行文件。

**触发构建**：
1. 推送版本标签：`git tag v1.0.0 && git push origin v1.0.0`
2. 手动触发：在 GitHub Actions 页面点击 "Run workflow"

**构建产物**：
- 单文件可执行文件 (Universal Binary)
- 应用程序包 (.app)
- DMG 安装包

### 手动构建
```bash
# 安装依赖
pip install pyinstaller

# 构建通用二进制
pyinstaller --name="ASIN-OE-Opener" --windowed --onefile --target-arch=universal2 ASIN-OE-Opener.py
```

## 系统要求

- **Python 版本**: 3.11+ (运行源代码)
- **macOS**: 10.15+ (运行可执行文件)
- **架构支持**: Intel x86_64 和 Apple Silicon arm64

## 文件说明

- `ASIN-OE-Opener.py` - 主程序源代码
- `requirements.txt` - Python 依赖
- `.github/workflows/release-macos.yml` - GitHub Actions 工作流
- `RELEASE_MACOS.md` - 详细的 macOS 发布指南
- `pyinstaller_macos.spec` - PyInstaller 配置文件