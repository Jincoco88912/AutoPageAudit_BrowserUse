# AutoPageAudit_BrowserUse

基於 `browser-use` 的瀏覽器自動化代理 API 服務

## 功能特色

- 🚀 使用 `browser-use` 進行智能瀏覽器自動化
- ☁️ 使用 Azure OpenAI 服務
- 🐳 Docker 容器化部署，最小化環境配置
- 🔌 RESTful API 介面，方便整合
- 🎯 支援複雜的瀏覽器任務執行

## 快速開始

### 1. 設定環境變數

請參考 `env-setup.md` 文件的詳細說明，創建 `.env` 檔案並填入您的 Azure OpenAI 配置：

```bash
# 在專案根目錄創建 .env 檔案（官方格式）
cat > .env << 'EOF'
AZURE_OPENAI_ENDPOINT=https://wilso-m9kz12x4-eastus2.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=49jOyexfFzonOJE7pretv76J14tGT4cLwdPENhe0GRZr9g2hiDGjJQQJ99BDACHYHv6XJ3w3AAAAACOGjTH2
EOF
```

### 2. 驗證設置（可選但建議）

運行測試腳本來檢查設置是否正確：

```bash
python test-setup.py
```

### 3. 使用 Docker Compose 啟動服務

```bash
# 建構並啟動服務
docker-compose up --build

# 或在背景執行
docker-compose up -d --build
```

### 4. 測試 API

服務啟動後，您可以透過以下方式測試：

#### 健康檢查
```bash
curl http://localhost:8080/
```

#### 執行瀏覽器任務
```bash
curl -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{"task": "Compare the price of gpt-4o and DeepSeek-V3"}'
```

## API 文檔

啟動服務後，您可以在 http://localhost:8080/docs 查看自動生成的 API 文檔。

## 本地開發

如果您想在本地環境開發（不使用 Docker）：

### 1. 安裝依賴
```bash
# 使用 uv（推薦）
pip install uv
uv pip install -r requirements.txt

# 或使用 pip
pip install -r requirements.txt
```

### 2. 安裝 Playwright 瀏覽器
```bash
playwright install --with-deps
```

### 3. 執行基礎代理示例
```bash
python agent.py
```

### 4. 執行 API 服務
```bash
python agent_api.py
```

## 專案結構

```
AutoPageAudit_BrowserUse/
├── Dockerfile              # Docker 容器配置
├── docker-compose.yml      # Docker Compose 服務配置
├── requirements.txt        # Python 依賴
├── agent_api.py           # FastAPI API 服務
├── test-setup.py          # 設置驗證腳本
└── README.md              # 專案說明
```

## 注意事項

- 本專案需要 Python 3.11+
- Docker 容器會自動安裝 Playwright 及其瀏覽器依賴
- 建議分配足夠的共享記憶體（shm_size: 2gb）以確保瀏覽器穩定運行
- 確保您的 Azure OpenAI 服務有足夠的配額

## 故障排除

### 如果遇到 Playwright 安裝問題
```bash
# 重新安裝 Playwright 瀏覽器
playwright install --with-deps chromium
```

### 如果容器啟動失敗
```bash
# 查看容器日誌
docker-compose logs browser_agent

# 重新建構容器
docker-compose down
docker-compose up --build
``` 