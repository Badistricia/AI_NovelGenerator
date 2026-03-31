import os
from langchain_openai import OpenAIEmbeddings
import requests

api_key = "sk-00ec79c73d32409e83e9fee3b58d58bb"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# Test 1: Using LangChain OpenAIEmbeddings
try:
    print("Testing LangChain OpenAIEmbeddings...")
    emb = OpenAIEmbeddings(
        openai_api_key=api_key,
        openai_api_base=base_url,
        model="text-embedding-v4"
    )
    res = emb.embed_query("测试文本")
    print("Langchain response OK, len:", len(res))
except Exception as e:
    print("Langchain Exception:", e)

# Test 2: Raw requests
try:
    print("\nTesting raw requests...")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "text-embedding-v4",
        "input": "测试文本"
    }
    resp = requests.post(f"{base_url}/embeddings", headers=headers, json=payload)
    print("Raw requests status:", resp.status_code)
    print("Raw requests response:", resp.text)
except Exception as e:
    print("Raw Exception:", e)
