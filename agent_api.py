from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
import os
from browser_use.llm import ChatAzureOpenAI
from browser_use import Agent
from dotenv import load_dotenv
import asyncio
import random
import httpx
import json
from typing import Optional
from stealth_config import StealthConfig, HumanBehavior, get_enhanced_config

# 在 API 啟動時讀取一次 .env
load_dotenv()

# 初始化 Azure OpenAI LLM 模型
# 建議在全域範圍初始化一次，避免每次請求都重新建立
llm = ChatAzureOpenAI(
    model="gpt-4.1",
)

# 建立 FastAPI app
app = FastAPI(
    title="Browser Use Agent API",
    description="透過 API 調用 browser-use 代理來執行瀏覽器自動化任務（帶反檢測功能）",
    version="2.0.0"
)

# 定義 API 請求的資料結構
class AgentTaskRequest(BaseModel):
    task: str
    callback_url: Optional[str] = Field(None, description="任務完成後回調的URL")
    use_stealth: bool = True  # 是否使用隱身模式
    use_proxy: bool = False  # 是否使用代理
    headless: bool = False  # 是否使用無頭模式
    delay_range: tuple = (1, 3)  # 動作間延遲範圍（秒）
    max_retries: int = 3  # 最大重試次數
    callback_timeout: int = Field(30, description="回調請求超時時間（秒）")
    callback_retries: int = Field(3, description="回調重試次數")

async def send_callback(callback_url: str, data: dict, timeout: int = 30, max_retries: int = 3):
    """
    發送回調請求到指定URL
    
    Args:
        callback_url: 回調URL
        data: 要發送的數據
        timeout: 請求超時時間
        max_retries: 最大重試次數
    """
    if not callback_url:
        return
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "AutoPageAudit-BrowserUse/2.0.0"
    }
    
    for attempt in range(max_retries):
        try:
            print(f"發送回調到 {callback_url} (第 {attempt + 1} 次嘗試)")
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    callback_url,
                    json=data,
                    headers=headers
                )
                
                print(f"回調響應狀態: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"回調成功發送到 {callback_url}")
                    return True
                else:
                    print(f"回調失敗，狀態碼: {response.status_code}, 響應: {response.text}")
                    
        except httpx.TimeoutException:
            print(f"回調超時 (第 {attempt + 1} 次嘗試)")
        except Exception as e:
            print(f"回調發送失敗 (第 {attempt + 1} 次嘗試): {e}")
        
        if attempt < max_retries - 1:
            # 指數退避重試
            wait_time = (2 ** attempt) * 2  # 2, 4, 8 秒
            print(f"等待 {wait_time} 秒後重試回調...")
            await asyncio.sleep(wait_time)
    
    print(f"回調最終失敗，已重試 {max_retries} 次")
    return False

async def setup_stealth_environment():
    """設置隱身環境"""
    # 添加啟動前的隨機延遲
    await HumanBehavior.random_delay(0.5, 2.0)
    
    # 模擬人類行為 - 隨機等待
    await HumanBehavior.random_mouse_movement()

@app.get("/")
async def root():
    """
    健康檢查端點
    """
    return {
        "message": "Browser Use Agent API 正在運行", 
        "status": "healthy",
        "features": ["反檢測配置", "代理支援", "人類行為模擬"]
    }

@app.post("/api/run-agent")
async def run_agent_task(request: AgentTaskRequest):
    """
    接收一個高階任務，並驅動 browser-use agent 來完成它。
    包含完整的反檢測和reCAPTCHA避免功能。
    任務完成後會自動回調到指定URL（如果提供）。
    """
    print(f"接收到任務: {request.task}")
    print(f"配置: 隱身={request.use_stealth}, 代理={request.use_proxy}, 無頭={request.headless}")
    if request.callback_url:
        print(f"回調URL: {request.callback_url}")
    
    response_data = None
    
    for attempt in range(request.max_retries):
        try:
            print(f"嘗試執行任務 (第 {attempt + 1} 次)")
            
            # 設置隱身環境
            if request.use_stealth:
                await setup_stealth_environment()
            
            # 獲取增強配置
            browser_config = get_enhanced_config(
                use_proxy=request.use_proxy,
                headless=request.headless
            )
            
            print(f"使用瀏覽器配置: {browser_config}")
            
            agent = Agent(
                task=request.task,
                llm=llm,
                use_vision=True,
                browser_config=browser_config
            )
            
            # 添加執行前延遲
            if request.use_stealth:
                await HumanBehavior.random_delay(
                    request.delay_range[0], 
                    request.delay_range[1]
                )
            
            result = await agent.run()
            print(f"任務完成，結果: {result}")
            
            response_data = {
                "status": "success", 
                "task": request.task, 
                "result": result,
                "attempt": attempt + 1,
                "config_used": {
                    "stealth": request.use_stealth,
                    "proxy": request.use_proxy,
                    "headless": request.headless
                },
                "timestamp": asyncio.get_event_loop().time()
            }
            
            # 發送回調（如果有指定URL）
            if request.callback_url:
                asyncio.create_task(send_callback(
                    request.callback_url, 
                    response_data,
                    request.callback_timeout,
                    request.callback_retries
                ))
            
            return response_data
            
        except Exception as e:
            print(f"第 {attempt + 1} 次嘗試失敗: {e}")
            
            if attempt < request.max_retries - 1:
                # 重試前等待更長時間
                wait_time = (attempt + 1) * 5  # 5, 10, 15 秒
                print(f"等待 {wait_time} 秒後重試...")
                await asyncio.sleep(wait_time)
            else:
                response_data = {
                    "status": "error", 
                    "message": str(e),
                    "attempts": request.max_retries,
                    "suggestion": "建議檢查網路連線、代理設定或增加延遲時間",
                    "timestamp": asyncio.get_event_loop().time()
                }
                
                # 發送錯誤回調（如果有指定URL）
                if request.callback_url:
                    asyncio.create_task(send_callback(
                        request.callback_url, 
                        response_data,
                        request.callback_timeout,
                        request.callback_retries
                    ))
                
                return response_data



# 如果您想直接運行這個 API 檔案
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080) 