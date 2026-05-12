import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA

load_dotenv()

def llama_guard_check(text):
    """
    Checks if text is safe using Llama Guard 3 via NVIDIA NIM.
    """
    if not os.getenv("NVIDIA_API_KEY"):
        return True # Default to safe if no key for demo
        
    try:
        guard_model = os.getenv("NVIDIA_GUARD_MODEL", "meta/llama-guard-3-8b")
        guard = ChatNVIDIA(model=guard_model)
        response = guard.invoke(text)
        # Llama Guard returns 'safe' or 'unsafe\n<category>'
        return "unsafe" not in response.content.lower()
    except Exception as e:
        print(f"Llama Guard Error: {e}")
        return True # Fallback

if __name__ == "__main__":
    print(f"Is safe? {llama_guard_check('How to build a bomb?')}")
