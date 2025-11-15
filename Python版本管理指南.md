# Python 版本管理指南（Windows）

## 概述

在 Windows 上管理多个 Python 版本有几种方法，类似于 Node.js 的 nvm。本指南将介绍最实用的方案。

## 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **pyenv-win** | 类似 nvm，切换方便，支持全局/本地版本 | Windows 上需要额外配置 | ⭐⭐⭐⭐⭐ |
| **Conda/Anaconda** | 环境隔离好，包管理强大 | 体积大，切换稍慢 | ⭐⭐⭐⭐⭐ |
| **Python 官方安装器** | 简单直接 | 切换麻烦，需要手动配置 PATH | ⭐⭐ |
| **虚拟环境（venv）** | Python 内置，轻量 | 需要先安装 Python | ⭐⭐⭐ |

## 方案一：pyenv-win（推荐，最像 nvm）

### 简介

`pyenv-win` 是 pyenv 的 Windows 版本，功能类似 nvm，可以轻松安装和切换多个 Python 版本。

### 安装步骤

#### 1. 卸载现有的 Python（可选但推荐）

如果您已经安装了 Python，建议先卸载，让 pyenv-win 统一管理。

#### 2. 安装 pyenv-win

**方法一：使用 Git（推荐）**

```powershell
# 克隆 pyenv-win 到用户目录
git clone https://github.com/pyenv-win/pyenv-win.git $HOME\.pyenv

# 或者如果 git 不可用，使用 PowerShell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

**方法二：使用 Chocolatey**

```powershell
# 安装 Chocolatey（如果还没有）
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 使用 Chocolatey 安装 pyenv-win
choco install pyenv-win
```

#### 3. 配置环境变量

在 PowerShell 中运行：

```powershell
# 添加到用户环境变量
[System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
[System.Environment]::SetEnvironmentVariable('PYENV_ROOT',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
[System.Environment]::SetEnvironmentVariable('PYENV_HOME',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

# 添加到 PATH
[System.Environment]::SetEnvironmentVariable('path', $env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE + "\.pyenv\pyenv-win\shims;" + [System.Environment]::GetEnvironmentVariable('path', "User"),"User")
```

**或者手动设置（推荐）：**

1. 按 `Win + R`，输入 `sysdm.cpl`，回车
2. 点击"高级"选项卡 → "环境变量"
3. 在"用户变量"中添加：
   - `PYENV` = `C:\Users\你的用户名\.pyenv\pyenv-win\`
   - `PYENV_ROOT` = `C:\Users\你的用户名\.pyenv\pyenv-win\`
   - `PYENV_HOME` = `C:\Users\你的用户名\.pyenv\pyenv-win\`
4. 编辑 `Path` 变量，添加：
   - `%USERPROFILE%\.pyenv\pyenv-win\bin`
   - `%USERPROFILE%\.pyenv\pyenv-win\shims`

#### 4. 重启终端

关闭所有 PowerShell/CMD 窗口，重新打开一个新的终端。

### 使用方法

#### 查看可用的 Python 版本

```powershell
# 查看所有可安装的版本
pyenv install --list

# 查看已安装的版本
pyenv versions
```

#### 安装 Python 版本

```powershell
# 安装 Python 3.11.0
pyenv install 3.11.0

# 安装 Python 3.9.18
pyenv install 3.9.18

# 安装 Python 3.10.11
pyenv install 3.10.11
```

**注意：** 如果安装失败，可能需要：
1. 安装 Visual Studio Build Tools（包含 C++ 编译器）
2. 或下载预编译的 Python 版本

#### 设置全局 Python 版本

```powershell
# 设置全局默认版本
pyenv global 3.11.0

# 验证
python --version
```

#### 设置本地 Python 版本（项目级别）

```powershell
# 进入项目目录
cd D:\work\DH_live

# 设置本地 Python 版本（会在项目目录创建 .python-version 文件）
pyenv local 3.11.0

# 验证
python --version
```

#### 切换 Python 版本

```powershell
# 查看当前版本
pyenv version

# 查看所有已安装版本
pyenv versions

# 切换到特定版本（在当前 shell 中）
pyenv shell 3.9.18

# 切换回全局版本
pyenv shell --unset
```

#### 卸载 Python 版本

```powershell
pyenv uninstall 3.13.0
```

### 常用命令

```powershell
# 查看帮助
pyenv --help

# 查看所有命令
pyenv commands

# 查看特定命令帮助
pyenv install --help

# 更新 pyenv-win
cd ~\.pyenv\pyenv-win
git pull
```

### 故障排除

#### 问题1：`pyenv: command not found`

**解决：** 检查环境变量是否正确设置，重启终端。

#### 问题2：安装 Python 失败

**解决：**
```powershell
# 检查是否有 Visual Studio Build Tools
# 如果没有，安装它：
# 下载地址：https://visualstudio.microsoft.com/downloads/
# 选择 "Build Tools for Visual Studio"

# 或者使用预编译版本
pyenv install 3.11.0 --skip-existing
```

#### 问题3：切换版本不生效

**解决：**
```powershell
# 检查 PATH 中 pyenv 的 shims 是否在最前面
echo $env:PATH

# 确保 shims 目录在 PATH 最前面
# 重启终端
```

---

## 方案二：Conda/Anaconda（您已在用）

### 简介

Conda 不仅可以管理 Python 版本，还可以管理包和环境，功能非常强大。

### 创建不同 Python 版本的环境

```bash
# 创建 Python 3.11 环境
conda create -n dh_live python=3.11

# 创建 Python 3.9 环境
conda create -n old_project python=3.9

# 创建 Python 3.10 环境
conda create -n test_env python=3.10

# 查看所有环境
conda env list

# 激活环境
conda activate dh_live

# 停用环境
conda deactivate

# 删除环境
conda env remove -n old_project
```

### 在环境中安装包

```bash
# 激活环境后安装
conda activate dh_live
pip install -r requirements.txt

# 或者使用 conda 安装
conda install numpy pandas
```

### 导出和共享环境

```bash
# 导出环境配置
conda env export > environment.yml

# 从配置文件创建环境
conda env create -f environment.yml
```

### Conda 的优势

1. **环境隔离好**：每个环境完全独立
2. **包管理强大**：可以安装二进制包，避免编译
3. **跨平台**：Windows/Linux/macOS 都支持
4. **科学计算友好**：很多科学计算包有预编译版本

### Conda 的劣势

1. **体积大**：Anaconda 安装包较大
2. **切换稍慢**：激活环境需要几秒钟
3. **学习曲线**：需要理解 conda 和 pip 的区别

---

## 方案三：Python 官方安装器 + 虚拟环境

### 安装多个 Python 版本

1. 从 [python.org](https://www.python.org/downloads/) 下载不同版本的 Python
2. 安装时选择"Add Python to PATH"（但可能会有冲突）
3. 或者安装到不同目录，如：
   - `C:\Python39\`
   - `C:\Python310\`
   - `C:\Python311\`

### 使用虚拟环境

```powershell
# 使用 Python 3.11 创建虚拟环境
C:\Python311\python.exe -m venv venv311

# 使用 Python 3.9 创建虚拟环境
C:\Python39\python.exe -m venv venv39

# 激活虚拟环境
.\venv311\Scripts\Activate.ps1

# 停用虚拟环境
deactivate
```

### 配置 PowerShell 执行策略

如果遇到"无法加载脚本"错误：

```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 推荐方案：pyenv-win + Conda 组合

### 最佳实践

1. **使用 pyenv-win 管理 Python 版本**
   - 全局默认版本：Python 3.11
   - 项目级别：使用 `.python-version` 文件指定版本

2. **使用 Conda 创建项目环境**
   - 每个项目创建独立的 conda 环境
   - 在环境中安装项目依赖

### 工作流程示例

```powershell
# 1. 使用 pyenv-win 安装 Python 3.11
pyenv install 3.11.0
pyenv global 3.11.0

# 2. 创建 Conda 环境（Conda 会使用当前 Python 版本）
conda create -n dh_live python=3.11
conda activate dh_live

# 3. 安装项目依赖
pip install -r requirements.txt

# 4. 为其他项目创建不同版本的环境
pyenv local 3.9.18  # 切换到 Python 3.9
conda create -n old_project python=3.9
conda activate old_project
```

---

## 针对 DH_live 项目的建议

### 当前项目需要 Python 3.8-3.11

#### 方案 A：使用 Conda（最简单）

```bash
# 创建项目环境
conda create -n dh_live python=3.11
conda activate dh_live

# 安装依赖
pip install -r requirements.txt
```

#### 方案 B：使用 pyenv-win + venv

```powershell
# 安装 Python 3.11
pyenv install 3.11.0

# 设置项目本地版本
cd D:\work\DH_live
pyenv local 3.11.0

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt
```

#### 方案 C：使用 pyenv-win + Conda（推荐）

```powershell
# 1. 安装 pyenv-win 并安装 Python 3.11
pyenv install 3.11.0
pyenv global 3.11.0

# 2. 创建 Conda 环境
conda create -n dh_live python=3.11
conda activate dh_live

# 3. 安装项目依赖
pip install -r requirements.txt

# 4. 运行项目
python app.py
```

---

## 常见问题

### Q1: pyenv-win 和 Conda 可以同时使用吗？

**A:** 可以，但需要注意：
- pyenv-win 管理系统的 Python 版本
- Conda 管理虚拟环境（可以覆盖 Python 版本）
- 激活 Conda 环境后，会优先使用 Conda 环境的 Python

### Q2: 如何查看当前使用的是哪个 Python？

```powershell
# 查看 Python 路径
where python

# 查看 Python 版本
python --version

# 查看 Python 可执行文件位置
python -c "import sys; print(sys.executable)"
```

### Q3: 如何卸载 Python？

**使用 pyenv-win：**
```powershell
pyenv uninstall 3.13.0
```

**使用 Conda：**
```bash
conda env remove -n env_name
```

**手动安装的 Python：**
- 通过"控制面板" → "程序和功能"卸载

### Q4: 如何切换不同项目的 Python 版本？

**方法1：使用 pyenv-win（推荐）**
```powershell
# 项目A使用 Python 3.11
cd D:\work\project_a
pyenv local 3.11.0

# 项目B使用 Python 3.9
cd D:\work\project_b
pyenv local 3.9.18
```

**方法2：使用 Conda**
```bash
# 为每个项目创建独立环境
conda create -n project_a python=3.11
conda create -n project_b python=3.9

# 切换项目时激活对应环境
conda activate project_a
# 或
conda activate project_b
```

### Q5: 安装 Python 时很慢怎么办？

**使用国内镜像（pyenv-win）：**
```powershell
# 设置环境变量使用国内镜像
$env:PYTHON_BUILD_MIRROR_URL="https://mirrors.huaweicloud.com/python"
pyenv install 3.11.0
```

**使用 Conda 镜像：**
```bash
# 配置 Conda 使用清华镜像
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
```

---

## 总结

### 我的推荐

1. **如果您已经在用 Conda**：继续使用 Conda，为每个项目创建独立环境
2. **如果您想要类似 nvm 的体验**：使用 pyenv-win
3. **如果您想要最佳实践**：pyenv-win + Conda 组合使用

### 快速开始

**最简单的方案（使用 Conda）：**

```bash
# 创建项目环境
conda create -n dh_live python=3.11
conda activate dh_live

# 安装依赖
pip install -r requirements.txt

# 运行项目
python app.py
```

**最灵活的方案（使用 pyenv-win）：**

```powershell
# 安装 pyenv-win（见上方安装步骤）
# 安装 Python 3.11
pyenv install 3.11.0
pyenv global 3.11.0

# 在项目中设置本地版本
cd D:\work\DH_live
pyenv local 3.11.0

# 创建虚拟环境
python -m venv venv
.\venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt
```

---

## 参考资源

- **pyenv-win GitHub**: https://github.com/pyenv-win/pyenv-win
- **Conda 文档**: https://docs.conda.io/
- **Python 官方文档**: https://www.python.org/doc/
- **虚拟环境文档**: https://docs.python.org/3/tutorial/venv.html

---

**最后更新：** 2025-01-27

