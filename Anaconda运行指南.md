# DH_live 项目 Anaconda 运行指南

## ⚠️ 快速故障排除

### 1. mediapipe 安装错误

**如果您遇到 `ERROR: No matching distribution found for mediapipe` 错误：**

1. **检查 Python 版本**（必须是 3.8-3.11）：
   ```bash
   python --version
   ```

2. **如果版本不对，重新创建环境**：
   ```bash
   conda deactivate
   conda remove -n dh_live --all
   conda create -n dh_live python=3.9
   conda activate dh_live
   ```

3. **单独安装 mediapipe**：
   ```bash
   pip install mediapipe==0.10.9
   ```

### 2. sys.excepthook 错误

**如果运行 `python app.py` 时遇到 `Error in sys.excepthook` 错误：**

**原因**：缺少必要的模型文件（checkpoint目录）

**解决方案**：
1. **创建checkpoint目录**：
   ```bash
   mkdir checkpoint
   mkdir checkpoint/lstm
   mkdir checkpoint/DINet_mini
   ```

2. **下载必要模型**：
   - 访问项目官方页面或GitHub releases下载模型文件
   - 将模型文件放置到对应目录：
     - `checkpoint/lstm/lstm_model_epoch_325.pkl`
     - `checkpoint/DINet_mini/epoch_40.pth`

3. **验证模型文件**：
   ```bash
   # 检查文件是否存在
   ls checkpoint/lstm/lstm_model_epoch_325.pkl
   ls checkpoint/DINet_mini/epoch_40.pth
   ```

4. **如果仍有错误**，检查依赖是否完整安装：
   ```bash
   pip list | grep torch
   pip list | grep mediapipe
   pip list | grep gradio
   ```

---

## 项目简介

DH_live 是一个实时数字人直播系统，提供全网最快的2D视频数字人解决方案。本项目主要维护 DH_live_mini 版本，具有极低的算力需求（仅39 Mflops），可在任何设备上实时运行。

## 系统要求

### 硬件要求
- **CPU**: 2核4G以上（推荐4核8G）
- **GPU**: 可选（支持CPU推理）
- **存储**: 至少5GB可用空间
- **内存**: 最低4GB（推荐8GB以上）

### 软件要求
- **操作系统**: Windows 10/11, Linux, macOS
- **Anaconda**: 最新版本
- **Python**: 3.8-3.11（推荐3.11）

## 环境配置

### 1. 安装 Anaconda

如果尚未安装 Anaconda，请从 [官方网站](https://www.anaconda.com/products/distribution) 下载并安装。

### 2. 创建虚拟环境

**重要提示：** mediapipe 对 Python 版本有严格要求，建议使用 Python 3.8-3.11 版本。

打开 Anaconda Prompt 或终端，执行以下命令：

```bash
# 创建名为 dh_live 的虚拟环境，使用 Python 3.11
conda create -n dh_live python=3.11

# 激活虚拟环境
conda activate dh_live

# 验证 Python 版本
python --version
```

### 3. 安装 PyTorch

根据您的系统配置选择合适的 PyTorch 版本：

#### GPU 版本（推荐，如果有NVIDIA显卡）
```bash
# CUDA 12.4 版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# 或者 CUDA 11.8 版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### CPU 版本（无GPU或测试环境）
```bash
pip install torch torchvision torchaudio
```

### 4. 安装 mediapipe（重要步骤）

由于 mediapipe 的兼容性问题，需要单独安装：

```bash
# 方法1：使用 pip 安装（推荐）
pip install mediapipe

# 如果上述方法失败，尝试指定版本
pip install mediapipe==0.10.9

# 方法2：如果仍然失败，尝试从 conda-forge 安装
conda install -c conda-forge mediapipe
```

### 5. 安装项目依赖

```bash
# 先单独安装可能有问题的包
pip install kaldi_native_fbank
pip install scikit-learn
pip install tqdm
pip install pyglm
pip install glfw
pip install PyOpenGL
pip install gradio
pip install sherpa-onnx

# 最后安装完整依赖（如果上述步骤成功）
pip install -r requirements.txt

# 如果遇到网络问题，可以使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 依赖包说明
- `kaldi_native_fbank`: 音频特征提取
- `mediapipe`: 人脸检测和面部网格
- `tqdm`: 进度条显示
- `scikit-learn`: 机器学习工具
- `pyglm`: OpenGL数学库
- `glfw`: OpenGL窗口管理
- `PyOpenGL`: Python OpenGL绑定
- `gradio`: Web界面框架
- `sherpa-onnx`: 语音识别和合成

## 模型文件下载

### 1. 下载预训练模型

从以下链接下载模型文件：
- **百度网盘**: [https://pan.baidu.com/s/1jH3WrIAfwI3U5awtnt9KPQ?pwd=ynd7](https://pan.baidu.com/s/1jH3WrIAfwI3U5awtnt9KPQ?pwd=ynd7)
- **Google Drive**: [https://drive.google.com/drive/folders/1az5WEWOFmh0_yrF3I9DEyctMyjPolo8V?usp=sharing](https://drive.google.com/drive/folders/1az5WEWOFmh0_yrF3I9DEyctMyjPolo8V?usp=sharing)

### 2. 解压模型文件

将下载的模型文件解压到项目根目录下的 `checkpoint` 文件夹中：

```
DH_live/
├── checkpoint/
│   ├── DINet_mini/
│   │   └── epoch_40.pth
│   └── lstm/
│       └── lstm_model_epoch_325.pkl
```

### 3. 下载ASR和TTS模型（可选）

如果需要使用实时语音对话功能，需要下载额外的模型：

```bash
# 创建模型目录
mkdir -p web_demo/models

# 下载ASR模型（中英双语）
wget -P web_demo/models/ https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20.tar.bz2
tar -xf web_demo/models/sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20.tar.bz2 -C web_demo/models/

# 下载TTS模型（中文）
wget -P web_demo/models/ https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-zh-ll.tar.bz2
tar -xf web_demo/models/vits-zh-ll.tar.bz2 -C web_demo/models/
```

## 项目运行

### 运行前检查

**⚠️ 重要：运行前请确保模型文件已下载**

#### 方法一：使用自动检查脚本（推荐）

```bash
# 运行环境检查脚本
python check_environment.py
```

该脚本会自动检查：
- Python版本兼容性
- 项目文件结构完整性  
- 依赖包安装情况
- 模型文件存在性

#### 方法二：手动检查

```bash
# 检查模型文件是否存在
ls checkpoint/lstm/lstm_model_epoch_325.pkl
ls checkpoint/DINet_mini/epoch_40.pth

# Windows用户使用dir命令
dir checkpoint\lstm\lstm_model_epoch_325.pkl
dir checkpoint\DINet_mini\epoch_40.pth

# 如果文件不存在，请参考下方"模型文件缺失问题"部分下载
```

### 方式一：使用 Gradio 界面（推荐新手）

```bash
# 确保在项目根目录下
cd D:\work\DH_live

# 2. 激活虚拟环境（环境已经创建好了）
conda activate dh_live

# 3. 验证 Python 版本
python --version

# 4. 安装 PyTorch（CPU 版本）
pip install torch torchvision torchaudio

# 5. 安装 mediapipe
pip install mediapipe==0.10.9

# 6. 安装其他依赖
pip install -r requirements.txt

# 7. 检查环境
python check_environment.py

# 8. 运行项目
python app.py
```

**如果出现错误**：
- `sys.excepthook` 错误 → 检查模型文件是否存在
- 依赖错误 → 重新安装requirements.txt
- 端口占用 → 更换端口或关闭占用进程

启动后，浏览器会自动打开 Gradio 界面，您可以通过可视化界面完成以下操作：
1. 上传静默视频进行预处理
2. 上传音频文件生成数字人视频
3. 启动Web服务

### 方式二：命令行运行

#### 1. 数据准备

```bash
# 处理视频数据（以 video_data/000002/video.mp4 为例）
python data_preparation_mini.py video_data/000002/video.mp4 video_data/000002

# 生成Web资源
python data_preparation_web.py video_data/000002
```

#### 2. 生成数字人视频

```bash
# 使用音频文件生成视频（仅Windows支持）
python demo_mini.py video_data/000002/assets video_data/audio1.wav output.mp4
```

**注意**: 音频文件必须是单通道16kHz的WAV格式。

#### 3. 启动Web服务

```bash
# 基础Web演示
python web_demo/server.py

# 实时语音对话服务（需要配置ASR/TTS）
python web_demo/server_realtime.py
```

启动后访问：
- 基础演示: [http://localhost:8888/static/MiniLive.html](http://localhost:8888/static/MiniLive.html)
- 实时对话: [http://localhost:8888/static/MiniLive_RealTime.html](http://localhost:8888/static/MiniLive_RealTime.html)

## 常见问题解决

### 1. 依赖安装问题

**问题：** `ERROR: No matching distribution found for mediapipe`
**解决方案：**
```bash
# 1. 检查 Python 版本（必须是 3.8-3.11）
python --version

# 2. 如果版本不对，重新创建环境
conda deactivate
conda remove -n dh_live --all
conda create -n dh_live python=3.11
conda activate dh_live

# 3. 单独安装 mediapipe
pip install mediapipe==0.10.9

# 4. 如果仍然失败，尝试不同的安装源
pip install mediapipe -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

**问题：** `kaldi_native_fbank` 安装失败
**解决方案：**
```bash
# 使用预编译版本
pip install kaldi_native_fbank --only-binary=all

# 或者跳过该依赖（如果不使用语音功能）
pip install --ignore-installed kaldi_native_fbank
```

**其他依赖问题：**
```bash
# 如果 pip 安装失败，尝试使用 conda
conda install opencv-python numpy scipy

# 如果网络问题，使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 2. 模型文件缺失问题

**错误现象**：
- 运行时出现 `sys.excepthook` 错误
- 提示找不到模型文件
- FileNotFoundError: checkpoint/xxx.pkl

**解决方案**：

1. **创建必要目录**：
```bash
# Windows
mkdir checkpoint
mkdir checkpoint\lstm
mkdir checkpoint\DINet_mini

# Linux/Mac
mkdir -p checkpoint/lstm
mkdir -p checkpoint/DINet_mini
```

2. **下载模型文件**：

**方法1：从官方渠道下载**
- 访问 [项目官网](https://www.matesx.com) 下载完整模型包
- 或从 GitHub Releases 页面下载

**方法2：使用百度网盘等分享链接**
- 通常项目README中会提供网盘链接
- 下载后解压到项目根目录

**方法3：联系项目维护者**
- 关注公众号"Mates数字生命"获取下载链接

3. **验证模型文件完整性**：
```bash
# 检查必要文件是否存在
ls -la checkpoint/lstm/lstm_model_epoch_325.pkl
ls -la checkpoint/DINet_mini/epoch_40.pth

# 检查文件大小（模型文件通常较大）
du -h checkpoint/
```

4. **模型文件说明**：
- `lstm_model_epoch_325.pkl`: 音频特征提取模型（约50-100MB）
- `epoch_40.pth`: 数字人生成模型（约100-500MB）
- 如果文件过小（<10MB），可能下载不完整

**注意事项**：
- 模型文件较大，下载时间可能较长
- 确保网络稳定，避免下载中断
- 某些模型可能需要特定的PyTorch版本

### 2. CUDA 相关问题

```bash
# 检查CUDA是否可用
python -c "import torch; print(torch.cuda.is_available())"

# 如果CUDA不可用，安装CPU版本
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio
```

### 3. MediaPipe 安装问题

```bash
# 如果 MediaPipe 安装失败
pip install mediapipe --no-deps
pip install opencv-python numpy protobuf
```

### 4. OpenGL 相关问题

在某些系统上可能遇到 OpenGL 问题：

```bash
# Linux 系统
sudo apt-get install freeglut3-dev

# macOS 系统
brew install glfw
```

### 5. 内存不足问题

如果遇到内存不足，可以：
- 减少批处理大小
- 使用较小的视频分辨率
- 关闭其他占用内存的程序

## Python 版本兼容性指南

### 1. 支持的 Python 版本

| Python 版本 | mediapipe 支持 | kaldi_native_fbank 支持 | 推荐程度 |
|-------------|----------------|-------------------------|----------|
| Python 3.8  | ✅ 支持        | ✅ 支持                  | ⭐⭐⭐     |
| Python 3.9  | ✅ 支持        | ✅ 支持                  | ⭐⭐⭐⭐⭐ |
| Python 3.10 | ✅ 支持        | ✅ 支持                  | ⭐⭐⭐⭐   |
| Python 3.11 | ✅ 支持        | ✅ 支持                  | ⭐⭐⭐⭐   |
| Python 3.12 | ❌ 不支持      | ⚠️ 部分支持              | ❌        |
| Python 3.13 | ❌ 不支持      | ❌ 不支持                | ❌        |

### 2. 版本检查和切换

```bash
# 检查当前 Python 版本
python --version

# 如果版本不兼容，重新创建环境
conda deactivate
conda remove -n dh_live --all
conda create -n dh_live python=3.9
conda activate dh_live
```

## 性能优化建议

### 1. GPU 加速
- 确保安装了正确的 CUDA 版本
- 使用 GPU 版本的 PyTorch
- 监控 GPU 使用率

### 2. CPU 优化
- 设置合适的线程数：`export OMP_NUM_THREADS=4`
- 使用 Intel MKL 加速（如果是 Intel CPU）

### 3. 内存优化
- 及时释放不需要的变量
- 使用较小的批处理大小
- 定期清理缓存

## 项目结构说明

```
DH_live/
├── app.py                    # Gradio 主界面
├── demo_mini.py             # 命令行推理接口
├── data_preparation_mini.py  # 视频预处理
├── data_preparation_web.py   # Web资源准备
├── requirements.txt         # 依赖列表
├── checkpoint/              # 模型文件目录
├── talkingface/            # 核心算法模块
├── mini_live/              # 渲染模块
├── web_demo/               # Web服务模块
├── video_data/             # 视频数据目录
└── data/                   # 配置数据
```

## 进阶配置

### 1. 自定义形象

1. 准备5-30秒的静默视频（嘴巴保持闭合或微张）
2. 使用 `data_preparation_mini.py` 处理视频
3. 使用 `data_preparation_web.py` 生成Web资源
4. 替换 `web_demo/static/assets` 目录下的文件

### 2. 语音配置

编辑 `web_demo/voiceapi/` 目录下的配置文件：
- `asr.py`: 语音识别配置
- `tts.py`: 语音合成配置
- `llm.py`: 大语言模型配置

### 3. API 集成

项目提供 RESTful API 接口，支持：
- 文本输入对话
- 语音输入对话
- 流式响应
- 自定义音色和语速

## 商业化部署

### 1. 授权说明
- 项目采用 MIT 许可证
- 商业使用需要去除 logo：访问 [授权页面](https://www.matesx.com/authorized.html)
- 上传 `combined_data.json.gz` 文件获取授权

### 2. 生产环境部署
- 使用 Docker 容器化部署
- 配置负载均衡
- 设置监控和日志
- 优化网络和存储

## 故障排除流程

```
遇到问题？按以下流程排查：

1. 运行环境检查脚本
   python check_environment.py
   ↓
2. 检查Python版本
   是否为3.8-3.11？
   ↓ 否 → 重新安装Python或创建新环境
   ↓ 是
3. 检查依赖包
   是否全部安装？
   ↓ 否 → pip install -r requirements.txt
   ↓ 是  
4. 检查模型文件
   checkpoint目录是否存在？
   ↓ 否 → 下载模型文件
   ↓ 是
5. 运行项目
   python app.py
   ↓
6. 仍有问题？
   → 查看下方技术支持
```

## 技术支持

- **官方网站**: [matesx.com](https://matesx.com)
- **GitHub**: [https://github.com/kleinlee/DH_live](https://github.com/kleinlee/DH_live)
- **微信群**: 添加好友备注"进群"
- **QQ群**: 见项目README

**如果您在使用过程中遇到问题：**

1. **查看日志**：检查终端输出的错误信息
2. **运行检查脚本**：`python check_environment.py`
3. **检查环境**：确认Python版本和依赖包
4. **重新安装**：删除环境重新创建
5. **联系支持**：提交详细的错误信息和检查脚本输出

**提交问题时请包含**：
- 操作系统版本
- Python版本
- 错误信息截图
- `check_environment.py` 的输出结果

## 更新日志

- **2025-01-26**: 最小化网页资源包，gzip资源小于2MB
- **2025-02-09**: 增加ASR入口、一键切换形象
- **2025-02-27**: 优化渲染、去除参照视频
- **2025-03-11**: 增加CPU支持
- **2025-04-09**: 增加iOS17长视频支持
- **2025-04-25**: 增加完整实时对话服务

---

**注意**: 本文档基于项目当前版本编写，如遇到问题请参考最新的官方文档或联系技术支持。