# 使用官方 Python 3.11 映像，因為 browser-use 要求 3.11+
FROM python:3.11-slim-bookworm

# 設定工作目錄
WORKDIR /app

# 更新包管理器並安裝系統級依賴
RUN apt-get update && apt-get install -y \
    # 基礎工具
    curl \
    wget \
    gnupg \
    unzip \
    # 瀏覽器相關依賴
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libgtk-3-0 \
    libgbm-dev \
    libasound2 \
    # X11 和顯示相關
    xvfb \
    x11vnc \
    fluxbox \
    # 字體支持
    fonts-liberation \
    fonts-noto-color-emoji \
    # 清理緩存
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安裝 uv (遵循官方指南的作法)
RUN pip install uv

# 複製 requirements.txt 並安裝依賴
# 這樣可以利用 Docker 的 layer cache，只有在 requirements.txt 變更時才重新安裝
COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

# [!!] 關鍵步驟: 安裝 Playwright 的瀏覽器和作業系統級依賴
# --with-deps 會自動安裝所有需要的系統函式庫，在 Docker 中至關重要
RUN playwright install --with-deps chromium

# 設置 X11 虛擬顯示
ENV DISPLAY=:99
ENV SCREEN_WIDTH=1920
ENV SCREEN_HEIGHT=1080

# 複製您應用程式的所有程式碼到容器中
COPY . .

# 直接啟動服務，不使用啟動腳本
CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 & sleep 3 && uvicorn agent_api:app --host 0.0.0.0 --port 8080"] 