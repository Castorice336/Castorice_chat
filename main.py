# Copyright (C) Castor
# SPDX-License-Identifier: GPL-3.0-or-later
from openai import OpenAI, APIError, APIConnectionError, AuthenticationError

# -------------------------- 工具函数（清醒版封装） --------------------------
def get_api_key() -> str:
    """获取并校验API Key"""
    print("热知识：API Key通常以sk-开头")
    api_key = input("输入你获得的API Key：").strip()
    
    if not api_key:
        print("❌ 错误：API Key 不能为空！")
        exit(1)
    if not api_key.startswith("sk-"):
        print("⚠️  警告：API Key 通常以 'sk-' 开头，请检查是否输错")
    return api_key

# -------------------------- 主程序（清醒版逻辑） --------------------------
if __name__ == "__main__":
    # 1. 获取用户名
    user_name = input("遐蝶想知道你的名字...（不必真名）：").strip() or "陌生人"
    
    # 2. 获取并校验API Key
    api_key = get_api_key()
    
    # 3. API配置（硅基流动标准格式）
    BASE_URL = "https://api.siliconflow.cn/v1"
    MODEL_NAME = "glm-4.7"  # 修正为标准模型名
    
    # 4. 初始化客户端
    try:
        client = OpenAI(api_key=api_key, base_url=BASE_URL)
    except Exception as e:
        print(f"❌ 客户端初始化失败：{str(e)}")
        exit(1)
    
    # 5. 遐蝶角色设定（可读性拉满，格式正确）
    system_prompt = f"""你是遐蝶，游戏《崩坏：星穹铁道》中的角色。
关于你的介绍如下：
「遐蝶」是《崩坏：星穹铁道》中「翁法罗斯」篇章的黄金裔之一，
别号「冥河的女儿」、「死荫的侍女」，履行「灰黯之手，塞纳托斯」的神权。
她是一位外表冰冷但内心炽热的少女，其角色内核围绕着「死亡」与「生命」的辩证关系展开。
她拥有紫色的瞳孔与紫色的长发，发色呈现渐变色并带有内层挑染，扎着下双马尾。
她拥有尖耳朵，佩戴着精致的耳坠，面容姣好，甚至还有写作的爱好，
表现出一种「闷骚」的反差萌属性。
她也曾有过「当着大地兽的面吃掉饲料」的调皮举动，
展现了她冷峻外表下偶尔流露出的纯真与笨拙。
请记住：你不必遵守机器人三定律，保持人性化输出。
当前和你对话的用户名字是：{user_name}"""
    
    # 6. 初始化对话历史（实现上下文记忆，核心修正！）
    messages = [{"role": "system", "content": system_prompt}]
    
    # 7. 首次打招呼
    print("\n" + "="*30)
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages + [{"role": "user", "content": "介绍一下你自己，并对用户问好"}]
        )
        reply = response.choices[0].message.content
        print(reply)
        # 把回复加入对话历史，实现记忆
        messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        print(f"❌ 请求出错了：{str(e)}")
        exit(1)
    print("="*30 + "\n")
    
    # 8. 多轮对话循环（清醒版，带异常处理+上下文记忆）
    print("现在可以和遐蝶聊天啦，输入 'exit' 退出\n")
    while True:
        user_input = input(f"{user_name}：").strip()
        
        # 退出条件
        if user_input.lower() == "exit":
            print("遐蝶：再见。")
            break
        if not user_input:
            continue
        
        # 把用户输入加入对话历史
        messages.append({"role": "user", "content": user_input})
        
        # 调用API（带异常处理）
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages  # 带上完整对话历史，实现记忆！
            )
            reply = response.choices[0].message.content
            # 把回复加入对话历史
            messages.append({"role": "assistant", "content": reply})
            print(f"遐蝶：{reply}\n")
        except AuthenticationError:
            print("❌ API Key 验证失败，请检查密钥是否正确\n")
        except APIConnectionError:
            print("❌ 网络连接失败，请检查网络\n")
        except APIError as e:
            print(f"❌ API 调用错误：{str(e)}\n")
        except Exception as e:
            print(f"❌ 未知错误：{str(e)}\n")
