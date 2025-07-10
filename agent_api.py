from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from browser_use.llm import ChatAzureOpenAI
from browser_use import Agent
from dotenv import load_dotenv

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
    description="透過 API 調用 browser-use 代理來執行瀏覽器自動化任務",
    version="1.0.0"
)

# 定義 API 請求的資料結構
class AgentTaskRequest(BaseModel):
    task: str

@app.get("/")
async def root():
    """
    健康檢查端點
    """
    return {"message": "Browser Use Agent API 正在運行", "status": "healthy"}

@app.post("/api/run-agent")
async def run_agent_task(request: AgentTaskRequest):
    """
    接收一個高階任務，並驅動 browser-use agent 來完成它。
    """
    print(f"接收到任務: {request.task}")
    try:
        agent = Agent(
            task=request.task,
            llm=llm,
            use_vision=True,
        )
        result = await agent.run()
        print(f"任務完成，結果: {result}")
        return {"status": "success", "task": request.task, "result": result}
    except Exception as e:
        print(f"任務執行失敗: {e}")
        return {"status": "error", "message": str(e)}

# 如果您想直接運行這個 API 檔案
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080) 