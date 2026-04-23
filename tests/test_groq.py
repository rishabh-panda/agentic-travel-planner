import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

def test_groq():
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("ERROR: GROQ_API_KEY not found")
        return False
    
    # Groq's verified working models from API
    working_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "qwen/qwen3-32b",
        "openai/gpt-oss-20b",
        "groq/compound-mini"
    ]
    
    for model in working_models:
        try:
            print(f"Testing model: {model}")
            llm = ChatGroq(
                model=model,
                temperature=0.3,
                api_key=api_key,
                timeout=30
            )
            
            response = llm.invoke([HumanMessage(content="Say 'Hello from Groq!' in one sentence.")])
            print(f"SUCCESS with {model}: {response.content}")
            return model
            
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue
    
    print("ERROR: No working models found")
    return None

if __name__ == "__main__":
    working_model = test_groq()
    if working_model:
        print(f"\n✓ Recommended model to use: {working_model}")