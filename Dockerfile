# 使用官方 Python 3.11 映像，因為 browser-use 要求 3.11+
FROM python:3.11-slim-bookworm

# 設定工作目錄
WORKDIR /app

# 安裝 uv (遵循官方指南的作法)
RUN pip install uv

# 複製 requirements.txt 並安裝依賴
# 這樣可以利用 Docker 的 layer cache，只有在 requirements.txt 變更時才重新安裝
COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

# [!!] 關鍵步驟: 安裝 Playwright 的瀏覽器和作業系統級依賴
# --with-deps 會自動安裝所有需要的系統函式庫，在 Docker 中至關重要
RUN playwright install --with-deps

# 複製您應用程式的所有程式碼到容器中
COPY . .

# 容器啟動時改為啟動 uvicorn API 伺服器
CMD ["uvicorn", "agent_api:app", "--host", "0.0.0.0", "--port", "8080"] 