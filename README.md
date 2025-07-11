# AutoPageAudit_BrowserUse

基於 `browser-use` 的瀏覽器自動化代理 API 服務

## 功能特色

- 🚀 使用 `browser-use` 進行智能瀏覽器自動化
- ☁️ 使用 Azure OpenAI 服務
- 🐳 Docker 容器化部署，最小化環境配置
- 🔌 RESTful API 介面，方便整合
- 🎯 支援複雜的瀏覽器任務執行
- 🛡️ **強化反檢測功能** - 避免被 reCAPTCHA 阻擋
- 🤖 **人類行為模擬** - 模擬真實用戶操作
- 🌐 **代理支援** - 支援住宅代理輪換
- 🔄 **自動重試機制** - 智能處理失敗情況

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

**基本任務執行：**
```bash
curl -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{"task": "Compare the price of gpt-4o and DeepSeek-V3"}'
```

**使用反檢測功能：**
```bash
curl -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{
       "task": "搜尋最新的 iPhone 價格並比較不同電商",
       "use_stealth": true,
       "headless": false,
       "delay_range": [2, 5],
       "max_retries": 3
     }'
```



## API 文檔

啟動服務後，您可以在 http://localhost:8080/docs 查看自動生成的 API 文檔。

### 📚 詳細文檔

- **[反檢測和 reCAPTCHA 解決方案指南](ANTI_DETECTION_GUIDE.md)** - 詳細的反檢測配置和使用指南
- **[API 文檔](http://localhost:8080/docs)** - 自動生成的 API 文檔（服務啟動後可用）

## 📊 API 回應格式

### ✅ 成功執行時的回應結構

```json
{
  "status": "success",
  "task": "您提交的原始任務描述",
  "result": {
    "screenshot": "iVBORw0KGgo...（Base64 編碼的PNG截圖）",
    "interacted_element": [
      {
        "tag_name": "input",
        "xpath": "html/body/div/input",
        "attributes": {
          "class": "search-box",
          "placeholder": "請輸入搜尋關鍵字"
        }
      }
    ],
    "url": "https://example.com/search",
    "title": "搜尋結果頁面",
    "metadata": {
      "step_start_time": 1752197349.6582184,
      "step_end_time": 1752197359.6553552,
      "step_number": 13
    }
  },
  "attempt": 1,
  "config_used": {
    "stealth": true,
    "proxy": false,
    "headless": false
  }
}
```

### ❌ 失敗時的回應結構

```json
{
  "status": "error",
  "message": "具體錯誤訊息",
  "attempts": 3,
  "suggestion": "建議檢查網路連線、代理設定或增加延遲時間"
}
```

### 📋 欄位說明

| 欄位 | 類型 | 說明 |
|------|------|------|
| `status` | string | 執行狀態：`"success"` 或 `"error"` |
| `task` | string | 您提交的原始任務描述 |
| `result` | object | AI 代理的執行結果（詳見下表） |
| `attempt` | number | 成功的嘗試次數（1-3） |
| `config_used` | object | 實際使用的配置參數 |

### 🎯 Result 陣列詳細說明

`result` 是一個**陣列**，包含 AI 執行過程中每個步驟的詳細記錄：

| 欄位 | 類型 | 說明 |
|------|------|------|
| `result[i].screenshot` | string | 該步驟的頁面截圖 Base64 編碼（PNG 格式） |
| `result[i].interacted_element` | array | 該步驟中互動的頁面元素詳情 |
| `result[i].url` | string | 該步驟中的頁面 URL |
| `result[i].title` | string | 該步驟中的頁面標題 |
| `result[i].metadata` | object | 該步驟的執行時間和步驟編號 |

**重要：** 陣列中的每個物件代表一個執行步驟，包含該步驟的完整狀態快照。

### 💡 實際使用範例

#### 範例 1：搜尋任務

**請求：**
```bash
curl -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{
       "task": "在雄獅旅遊搜尋大阪旅遊行程",
       "use_stealth": true
     }'
```

**回應：**
```json
{
  "status": "success",
  "task": "在雄獅旅遊搜尋大阪旅遊行程",
  "result": {
    "screenshot": "iVBORw0KGgo...（完整的頁面截圖）",
    "interacted_element": [
      {
        "tag_name": "input",
        "attributes": {
          "class": "search-input",
          "placeholder": "請輸入目的地"
        }
      }
    ],
    "url": "https://travel.liontravel.com/search?Keywords=大阪",
    "title": "旅遊行程搜尋| 雄獅旅遊",
    "metadata": {
      "step_number": 13,
      "step_start_time": 1752197349.66,
      "step_end_time": 1752197359.66
    }
  },
  "attempt": 1,
  "config_used": {
    "stealth": true,
    "proxy": false,
    "headless": false
  }
}
```

#### 範例 2：多頁面操作任務

**請求：**
```bash
curl -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{
       "task": "在 momo 購物網搜尋 iPhone 15，然後點擊第一個商品查看詳細資訊",
       "use_stealth": true,
       "delay_range": [2, 4]
     }'
```

**回應：**
```json
{
  "status": "success",
  "task": "在 momo 購物網搜尋 iPhone 15，然後點擊第一個商品查看詳細資訊",
  "result": [
    {
      "screenshot": "iVBORw0KGgo...（momo首頁截圖）",
      "interacted_element": [null],
      "url": "https://www.momoshop.com.tw",
      "title": "momo購物網",
      "metadata": {
        "step_start_time": 1752197825.123,
        "step_end_time": 1752197827.456,
        "step_number": 1
      }
    },
    {
      "screenshot": "iVBORw0KGgo...（輸入搜尋關鍵字後的截圖）",
      "interacted_element": [
        {
          "tag_name": "input",
          "xpath": "html/body/div[1]/header/div/div[2]/div/input",
          "attributes": {
            "class": "searchTextBox",
            "placeholder": "搜尋商品"
          }
        }
      ],
      "url": "https://www.momoshop.com.tw",
      "title": "momo購物網",
      "metadata": {
        "step_start_time": 1752197827.456,
        "step_end_time": 1752197829.789,
        "step_number": 2
      }
    },
    {
      "screenshot": "iVBORw0KGgo...（搜尋結果頁面截圖）",
      "interacted_element": [
        {
          "tag_name": "button",
          "xpath": "html/body/div[1]/header/div/div[2]/div/button",
          "attributes": {
            "class": "searchBtn",
            "type": "submit"
          }
        }
      ],
      "url": "https://www.momoshop.com.tw/search/searchShop.jsp?keyword=iPhone%2015",
      "title": "iPhone 15 - momo購物網",
      "metadata": {
        "step_start_time": 1752197829.789,
        "step_end_time": 1752197833.012,
        "step_number": 3
      }
    },
    {
      "screenshot": "iVBORw0KGgo...（商品詳細頁面截圖）",
      "interacted_element": [
        {
          "tag_name": "a",
          "xpath": "html/body/div[3]/div[2]/div[1]/ul/li[1]/div/div[2]/h3/a",
          "attributes": {
            "class": "goodsName",
            "href": "/goods/GoodsDetail.jsp?i_code=10963583"
          }
        }
      ],
      "url": "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=10963583",
      "title": "Apple iPhone 15 128GB 藍色 - momo購物網",
      "metadata": {
        "step_start_time": 1752197833.012,
        "step_end_time": 1752197841.456,
        "step_number": 4
      }
    }
  ],
  "attempt": 1,
  "config_used": {
    "stealth": true,
    "proxy": false,
    "headless": false
  }
}
```

#### 範例 3：遇到錯誤

**回應：**
```json
{
  "status": "error",
  "message": "Connection timeout after 30 seconds",
  "attempts": 3,
  "suggestion": "建議檢查網路連線、代理設定或增加延遲時間"
}
```

### 🖼️ 如何查看截圖

截圖以 Base64 格式編碼，您可以：

1. **使用線上工具**：將 Base64 字串貼到 https://base64.guru/converter/decode/image
2. **直接在瀏覽器查看**：
   ```html
   <img src="data:image/png;base64,您的Base64字串" />
   ```
3. **使用命令行**：
   ```bash
   echo "您的Base64字串" | base64 -d > screenshot.png
   ```

### 📈 提取特定資訊

```bash
# 檢查執行狀態
curl -s -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{"task": "您的任務"}' | jq -r '.status'

# 取得最終步驟的 URL
curl -s -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{"task": "您的任務"}' | jq -r '.result[-1].url'

# 取得最終步驟的頁面標題
curl -s -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{"task": "您的任務"}' | jq -r '.result[-1].title'

# 取得所有步驟的 URL
curl -s -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{"task": "您的任務"}' | jq -r '.result[].url'

# 計算總執行步驟數
curl -s -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{"task": "您的任務"}' | jq '.result | length'

# 取得第一步的截圖（儲存為檔案）
curl -s -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{"task": "您的任務"}' | jq -r '.result[0].screenshot' | base64 -d > step1.png
```

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

### 🛡️ 反檢測功能說明

- **預設啟用隱身模式**：自動隱藏瀏覽器自動化特徵
- **建議使用有頭模式**：`headless: false` 可大幅提高成功率
- **代理支援**：可配置住宅代理避免 IP 封鎖
- **合規使用**：請遵守目標網站的使用條款和相關法規

詳細配置請參考 [反檢測指南](ANTI_DETECTION_GUIDE.md)。

## 🔄 Webhook 回調功能

AutoPageAudit_BrowserUse 支援 webhook 回調功能，讓您可以在瀏覽器任務完成後自動接收結果。

### 快速使用

```bash
curl -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{
       "task": "搜尋商品資訊",
       "callback_url": "https://your-server.com/webhook",
       "use_stealth": true
     }'
```

### 新增參數

| 參數 | 類型 | 說明 | 預設值 |
|------|------|------|--------|
| `callback_url` | string | 任務完成後回調的 URL | `null` |
| `callback_timeout` | int | 回調請求超時時間（秒） | `30` |
| `callback_retries` | int | 回調重試次數 | `3` |

### 回調數據格式

**成功時：**
```json
{
  "status": "success",
  "task": "您的任務描述",
  "result": [...],  // 完整的執行結果陣列
  "timestamp": 1704649200.123
}
```

**失敗時：**
```json
{
  "status": "error", 
  "message": "錯誤原因",
  "attempts": 3,
  "timestamp": 1704649200.123
}
```

### 回調伺服器範例

#### Node.js Express
```javascript
app.post('/webhook', (req, res) => {
  const { status, result } = req.body;
  console.log(`任務狀態: ${status}`);
  if (status === 'success') {
    // 處理成功結果
    result.forEach(step => console.log(step.url));
  }
  res.json({ received: true });
});
```

#### Python Flask
```python
@app.route('/webhook', methods=['POST'])
def handle_callback():
    data = request.get_json()
    print(f"任務狀態: {data['status']}")
    if data['status'] == 'success':
        # 處理成功結果
        for step in data['result']:
            print(step['url'])
    return {"received": True}
```

### 🔗 詳細說明

完整的 webhook 功能說明、安全建議和整合範例請參考：
📋 **[Webhook 回調功能使用指南](webhook_example.md)**

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