import os
from openai import OpenAI

# 豆包（火山引擎）配置
# 优先使用环境变量，如果没有则使用默认密钥
api_key = os.getenv('ARK_API_KEY') or "54f5bb90-9d1d-4b8d-bc3d-952d658d2372"
base_url = "https://ark.cn-beijing.volces.com/api/v3"
model_name = "doubao-seed-1-6-251015"

llm_client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)


def llm_stream(prompt, system_prompt=None):
    if not system_prompt:
        system_prompt = "你是人工智能助手"
    # 强制要求不生成表情符号（因为TTS无法朗读）
    system_prompt += "\n\n【重要】你的回复将被语音合成，请不要使用任何表情符号（emoji）、特殊符号或颜文字。"
    stream = llm_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )
    return stream
