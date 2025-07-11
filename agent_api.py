from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from browser_use.llm import ChatAzureOpenAI
from browser_use import Agent
from dotenv import load_dotenv
import asyncio
import random
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
    use_stealth: bool = True  # 是否使用隱身模式
    use_proxy: bool = False  # 是否使用代理
    headless: bool = False  # 是否使用無頭模式
    delay_range: tuple = (1, 3)  # 動作間延遲範圍（秒）
    max_retries: int = 3  # 最大重試次數

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
    """
    print(f"接收到任務: {request.task}")
    print(f"配置: 隱身={request.use_stealth}, 代理={request.use_proxy}, 無頭={request.headless}")
    
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
            
            return {
                "status": "success", 
                "task": request.task, 
                "result": result,
                "attempt": attempt + 1,
                "config_used": {
                    "stealth": request.use_stealth,
                    "proxy": request.use_proxy,
                    "headless": request.headless
                }
            }
            
        except Exception as e:
            print(f"第 {attempt + 1} 次嘗試失敗: {e}")
            
            if attempt < request.max_retries - 1:
                # 重試前等待更長時間
                wait_time = (attempt + 1) * 5  # 5, 10, 15 秒
                print(f"等待 {wait_time} 秒後重試...")
                await asyncio.sleep(wait_time)
            else:
                return {
                    "status": "error", 
                    "message": str(e),
                    "attempts": request.max_retries,
                    "suggestion": "建議檢查網路連線、代理設定或增加延遲時間"
                }



# 如果您想直接運行這個 API 檔案
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080) 