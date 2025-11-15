import json
import requests
import asyncio
import re
import base64
import os
import sys
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, UploadFile, File,HTTPException

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录（web_demo 的父目录）
project_root = os.path.dirname(script_dir) if os.path.basename(script_dir) == "web_demo" else script_dir

# 添加 web_demo 目录到 Python 路径，以便导入 voiceapi
web_demo_dir = script_dir if os.path.basename(script_dir) == "web_demo" else os.path.join(project_root, "web_demo")
if web_demo_dir not in sys.path:
    sys.path.insert(0, web_demo_dir)

# 静态文件目录
static_dir = os.path.join(script_dir, "static")
if not os.path.exists(static_dir):
    # 如果在项目根目录运行，尝试 web_demo/static
    static_dir = os.path.join(project_root, "web_demo", "static")

app = FastAPI()

# 挂载静态文件
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 导入 LLM 模块
try:
    from voiceapi.llm import llm_stream
    USE_REAL_LLM = True
    print("✅ 已启用真实大模型服务")
except ImportError as e:
    print(f"⚠️  无法导入 LLM 模块: {e}")
    print("⚠️  将使用模拟回答")
    USE_REAL_LLM = False

# 导入 TTS 模块
USE_REAL_TTS = False
TTSEngineManager = None
try:
    from voiceapi.tts import get_audio as tts_get_audio, TTSEngineManager
    USE_REAL_TTS = True
    print("✅ TTS 模块已导入")
except ImportError as e:
    print(f"⚠️  无法导入 TTS 模块: {e}")
    print("⚠️  将使用模拟语音（固定音频文件）")

# 初始化 TTS 引擎（如果需要）
if USE_REAL_TTS:
    try:
        # 检查模型目录
        models_root = None
        possible_models_dirs = [
            os.path.join(project_root, 'models'),
            os.path.join(script_dir, 'models'),
            os.path.join(project_root, 'web_demo', 'models'),
            './models',
            '../models',
            'web_demo/models'
        ]
        
        for d in possible_models_dirs:
            if os.path.isdir(d):
                models_root = d
                break
        
        if models_root and os.path.exists(os.path.join(models_root, 'sherpa-onnx-vits-zh-ll')):
            # 创建简单的参数对象
            class TTSArgs:
                def __init__(self):
                    self.models_root = models_root
                    self.tts_provider = 'cpu'
                    self.tts_model = 'sherpa-onnx-vits-zh-ll'
                    self.threads = 2
            
            tts_args = TTSArgs()
            TTSEngineManager.initialize(args=tts_args)
            print("✅ TTS 模型已初始化")
        else:
            print("⚠️  TTS 模型未找到，将使用模拟语音")
            print(f"   请下载 TTS 模型到: {models_root or 'models/'} 目录")
            USE_REAL_TTS = False
    except Exception as e:
        print(f"⚠️  TTS 初始化失败: {e}")
        print("⚠️  将使用模拟语音")
        USE_REAL_TTS = False

async def get_audio(text_cache, voice_speed, voice_id):
    """获取音频（真实 TTS 或模拟）"""
    if not text_cache or len(text_cache.strip()) == 0:
        return ""
        
    if USE_REAL_TTS and TTSEngineManager:
        try:
            # 使用真实 TTS
            # 处理 voice_id：可能是数字字符串、数字、或空字符串
            if voice_id == "" or voice_id is None:
                voice_id_int = 0
            elif isinstance(voice_id, str):
                try:
                    voice_id_int = int(voice_id) if voice_id.isdigit() else 0
                except:
                    voice_id_int = 0
            else:
                voice_id_int = int(voice_id) if voice_id else 0
            
            # 处理 voice_speed：可能是数字字符串、数字、或空字符串
            if voice_speed == "" or voice_speed is None:
                voice_speed_float = 1.0
            elif isinstance(voice_speed, str):
                try:
                    voice_speed_float = float(voice_speed) if voice_speed else 1.0
                except:
                    voice_speed_float = 1.0
            else:
                voice_speed_float = float(voice_speed) if voice_speed else 1.0
            
            print(f"TTS 生成: text={text_cache[:20]}..., voice_id={voice_id_int}, speed={voice_speed_float}")
            base64_string = await tts_get_audio(text_cache, voice_speed=voice_speed_float, voice_id=voice_id_int)
            return base64_string
        except Exception as e:
            import traceback
            print(f"❌ TTS 生成失败: {e}")
            traceback.print_exc()
            #  fallback 到模拟音频
            pass
    
    # 使用模拟音频（fallback）
    print("⚠️  使用模拟音频（固定音频文件）")
    audio_path = os.path.join(static_dir, "common", "test.wav")
    with open(audio_path, "rb") as audio_file:
        audio_value = audio_file.read()
    base64_string = base64.b64encode(audio_value).decode('utf-8')
    return base64_string

def llm_answer(prompt):
    """获取大模型回答（如果可用）"""
    if USE_REAL_LLM:
        # 使用真实大模型
        try:
            answer = ""
            stream = llm_stream(prompt)
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    answer += chunk.choices[0].delta.content
            return answer if answer else "抱歉，大模型没有返回回答。"
        except Exception as e:
            print(f"❌ 大模型调用失败: {e}")
            return f"大模型调用失败: {str(e)}"
    else:
        # 模拟大模型的回答
        answer = "我会重复三遍来模仿大模型的回答，我会重复三遍来模仿大模型的回答，我会重复三遍来模仿大模型的回答。"
        return answer

def split_sentence(sentence, min_length=10):
    # 定义包括小括号在内的主要标点符号
    punctuations = r'[。？！；…，、()（）]'
    # 使用正则表达式切分句子，保留标点符号
    parts = re.split(f'({punctuations})', sentence)
    parts = [p for p in parts if p]  # 移除空字符串
    sentences = []
    current = ''
    for part in parts:
        if current:
            # 如果当前片段加上新片段长度超过最小长度，则将当前片段添加到结果中
            if len(current) + len(part) >= min_length:
                sentences.append(current + part)
                current = ''
            else:
                current += part
        else:
            current = part
    # 将剩余的片段添加到结果中
    if len(current) >= 2:
        sentences.append(current)
    return sentences

PUNCTUATION_SET = {
    '，', " ", '。', '！', '？', '；', '：', '、', '（', '）', '【', '】', '“', '”',
    ',', '.', '!', '?', ';', ':', '(', ')', '[', ']', '"', "'"
}

async def gen_stream(prompt, asr = False, voice_speed=None, voice_id=None):
    print("gen_stream", voice_speed, voice_id)
    if asr:
        chunk = {
            "prompt": prompt
        }
        yield f"{json.dumps(chunk)}\n"  # 使用换行符分隔 JSON 块

    if USE_REAL_LLM:
        # 使用真实大模型流式返回
        try:
            print("----- streaming request -----")
            stream = llm_stream(prompt)
            llm_answer_cache = ""
            
            for chunk in stream:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content or ""
                if not content:
                    continue
                    
                llm_answer_cache += content

                # 查找最近的标点符号位置（从后往前查找最近50个字符）
                search_end = len(llm_answer_cache)
                search_start = max(0, search_end - 50)
                punctuation_pos = -1
                for i in range(search_end - 1, search_start - 1, -1):
                    if llm_answer_cache[i] in PUNCTUATION_SET:
                        punctuation_pos = i
                        break
                
                # 如果找到标点符号且累积的文本足够长（至少15个字符）
                if punctuation_pos != -1 and punctuation_pos + 1 >= 15:
                    # 获取到标点符号为止的句子
                    first_sentence = llm_answer_cache[:punctuation_pos + 1]
                    # 剩余的文字
                    remaining_text = llm_answer_cache[punctuation_pos + 1:]
                    print("get_audio: ", first_sentence)
                    base64_string = await get_audio(first_sentence, voice_speed, voice_id)
                    chunk_data = {
                        "text": first_sentence,
                        "audio": base64_string,
                        "endpoint": False
                    }
                    # 更新缓存为剩余的文字
                    llm_answer_cache = remaining_text
                    yield f"{json.dumps(chunk_data)}\n"
                    await asyncio.sleep(0.2)
                # 如果累积的文本太长（超过60个字符）还没找到标点，强制输出一部分
                elif len(llm_answer_cache) >= 60:
                    # 输出前50个字符
                    first_sentence = llm_answer_cache[:50]
                    remaining_text = llm_answer_cache[50:]
                    print("get_audio (forced): ", first_sentence)
                    base64_string = await get_audio(first_sentence, voice_speed, voice_id)
                    chunk_data = {
                        "text": first_sentence,
                        "audio": base64_string,
                        "endpoint": False
                    }
                    llm_answer_cache = remaining_text
                    yield f"{json.dumps(chunk_data)}\n"
                    await asyncio.sleep(0.2)
            
            # 处理剩余的文字
            if llm_answer_cache and len(llm_answer_cache.strip()) > 0:
                print("get_audio (final): ", llm_answer_cache)
                base64_string = await get_audio(llm_answer_cache, voice_speed, voice_id)
                chunk_data = {
                    "text": llm_answer_cache,
                    "audio": base64_string,
                    "endpoint": True
                }
                yield f"{json.dumps(chunk_data)}\n"
        except Exception as e:
            import traceback
            print(f"❌ 大模型流式调用失败: {e}")
            traceback.print_exc()
            error_text = f"抱歉，大模型调用失败: {str(e)}"
            base64_string = await get_audio(error_text, voice_speed, voice_id)
            chunk_data = {
                "text": error_text,
                "audio": base64_string,
                "endpoint": True
            }
            yield f"{json.dumps(chunk_data)}\n"
    else:
        # 使用模拟回答（向后兼容）
        print("使用模拟回答")
        text_cache = llm_answer(prompt)
        sentences = split_sentence(text_cache)

        for index_, sub_text in enumerate(sentences):
            base64_string = await get_audio(sub_text, voice_speed, voice_id)
            # 生成 JSON 格式的数据块
            chunk_data = {
                "text": sub_text,
                "audio": base64_string,
                "endpoint": index_ == len(sentences)-1
            }
            yield f"{json.dumps(chunk_data)}\n"  # 使用换行符分隔 JSON 块
            await asyncio.sleep(0.2)  # 模拟异步延迟

# 处理 ASR 和 TTS 的端点
@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):
    # 模仿调用 ASR API 获取文本
    text = "语音已收到，这里只是模仿，真正对话需要您自己设置ASR服务。"
    # 调用 TTS 生成流式响应
    return StreamingResponse(gen_stream(text, asr=True), media_type="application/json")


async def call_asr_api(audio_data):
    # 调用ASR完成语音识别
    answer = "语音已收到，这里只是模仿，真正对话需要您自己设置ASR服务。"
    return answer

@app.post("/eb_stream")    # 前端调用的path
async def eb_stream(request: Request):
    try:
        body = await request.json()
        input_mode = body.get("input_mode")
        voice_speed = body.get("voice_speed")
        voice_id = body.get("voice_id")

        if input_mode == "audio":
            base64_audio = body.get("audio")
            # 解码 Base64 音频数据
            audio_data = base64.b64decode(base64_audio)
            # 这里可以添加对音频数据的处理逻辑
            prompt = await call_asr_api(audio_data)  # 假设 call_asr_api 可以处理音频数据
            return StreamingResponse(gen_stream(prompt, asr=True, voice_speed=voice_speed, voice_id=voice_id), media_type="application/json")
        elif input_mode == "text":
            prompt = body.get("prompt")
            return StreamingResponse(gen_stream(prompt, asr=False, voice_speed=voice_speed, voice_id=voice_id), media_type="application/json")
        else:
            raise HTTPException(status_code=400, detail="Invalid input mode")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 启动Uvicorn服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
