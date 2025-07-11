# Webhook 回調功能使用指南

AutoPageAudit_BrowserUse 現在支援 webhook 回調功能，讓您可以在瀏覽器自動化任務完成後，自動將結果推送到指定的 URL。

## 功能特點

- ✅ 支援任務完成後自動回調
- ✅ 包含成功和失敗兩種狀態的回調
- ✅ 可配置回調超時時間和重試次數
- ✅ 指數退避重試機制
- ✅ 詳細的回調日誌

## API 參數

### 新增的回調參數

```json
{
  "task": "您的自動化任務",
  "callback_url": "https://your-server.com/webhook",  // 可選：回調URL
  "callback_timeout": 30,                            // 可選：回調超時時間（預設30秒）
  "callback_retries": 3,                             // 可選：回調重試次數（預設3次）
  "use_stealth": true,
  "headless": false
}
```

## 使用示例

### 1. 基本回調使用

```bash
curl -X POST "http://localhost:8080/api/run-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "打開 google.com 並搜尋天氣",
    "callback_url": "https://your-server.com/webhook/browser-task",
    "use_stealth": true,
    "headless": false
  }'
```

### 2. 自定義回調配置

```bash
curl -X POST "http://localhost:8080/api/run-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "登入網站並抓取資料",
    "callback_url": "https://your-server.com/api/browser-callback",
    "callback_timeout": 60,
    "callback_retries": 5,
    "use_stealth": true,
    "max_retries": 2
  }'
```

### 3. 無回調模式（與之前相同）

```bash
curl -X POST "http://localhost:8080/api/run-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "瀏覽購物網站",
    "use_stealth": true
  }'
```

## 回調數據格式

### 成功回調

當任務成功完成時，會發送以下格式的數據到您的回調 URL：

```json
{
  "status": "success",
  "task": "打開 google.com 並搜尋天氣",
  "result": [
    {
      "url": "https://www.google.com/search?q=天氣",
      "title": "天氣 - Google 搜尋",
      "screenshot": "base64_encoded_screenshot_data...",
      "interacted_element": "搜尋框",
      "metadata": {
        "execution_time": 5.2,
        "actions_performed": 3
      }
    }
  ],
  "attempt": 1,
  "config_used": {
    "stealth": true,
    "proxy": false,
    "headless": false
  },
  "timestamp": 1704649200.123
}
```

### 失敗回調

當任務失敗時，會發送錯誤訊息：

```json
{
  "status": "error",
  "message": "網頁載入超時",
  "attempts": 3,
  "suggestion": "建議檢查網路連線、代理設定或增加延遲時間",
  "timestamp": 1704649200.123
}
```

## 回調伺服器實作範例

### Node.js Express 範例

```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.post('/webhook/browser-task', (req, res) => {
  const { status, task, result, timestamp } = req.body;
  
  console.log(`任務狀態: ${status}`);
  console.log(`任務內容: ${task}`);
  console.log(`完成時間: ${new Date(timestamp * 1000)}`);
  
  if (status === 'success') {
    console.log(`結果數量: ${result.length}`);
    // 處理成功結果
    result.forEach((step, index) => {
      console.log(`步驟 ${index + 1}: ${step.url}`);
      // 可以將 screenshot base64 數據儲存為圖片
      // fs.writeFileSync(`screenshot_${index}.png`, Buffer.from(step.screenshot, 'base64'));
    });
  } else {
    console.log(`錯誤訊息: ${req.body.message}`);
    // 處理錯誤情況
  }
  
  res.status(200).json({ received: true });
});

app.listen(3000, () => {
  console.log('回調伺服器運行在 http://localhost:3000');
});
```

### Python Flask 範例

```python
from flask import Flask, request, jsonify
import base64
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/webhook/browser-task', methods=['POST'])
def browser_task_callback():
    data = request.get_json()
    
    status = data.get('status')
    task = data.get('task')
    timestamp = data.get('timestamp')
    
    print(f"任務狀態: {status}")
    print(f"任務內容: {task}")
    print(f"完成時間: {datetime.fromtimestamp(timestamp)}")
    
    if status == 'success':
        result = data.get('result', [])
        print(f"結果數量: {len(result)}")
        
        for i, step in enumerate(result):
            print(f"步驟 {i+1}: {step.get('url')}")
            
            # 儲存截圖
            if 'screenshot' in step:
                screenshot_data = base64.b64decode(step['screenshot'])
                with open(f'screenshot_{i}.png', 'wb') as f:
                    f.write(screenshot_data)
    else:
        print(f"錯誤訊息: {data.get('message')}")
    
    return jsonify({"received": True})

if __name__ == '__main__':
    app.run(port=3000)
```

## 安全建議

1. **驗證回調來源**：檢查請求的 User-Agent 為 `AutoPageAudit-BrowserUse/2.0.0`
2. **使用 HTTPS**：確保回調 URL 使用安全連線
3. **API 金鑰驗證**：在回調 URL 中加入驗證參數或標頭
4. **限制回調頻率**：避免短時間內大量回調請求

## 故障排除

### 回調失敗的常見原因

1. **網路連線問題**：檢查伺服器網路狀態
2. **URL 無法訪問**：確認回調 URL 可正常訪問
3. **超時設定過短**：增加 `callback_timeout` 值
4. **伺服器回應錯誤**：確保回調伺服器回傳 200 狀態碼

### 調試技巧

1. 查看 AutoPageAudit 服務日誌
2. 使用測試工具（如 ngrok）建立臨時回調端點
3. 檢查防火牆設定

```bash
# 使用 ngrok 建立測試端點
ngrok http 3000
# 使用產生的 URL 作為 callback_url
```

## 整合範例

### 與資料庫整合

```python
import sqlite3
from datetime import datetime

def save_result_to_db(data):
    conn = sqlite3.connect('browser_results.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO browser_tasks (task, status, result, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (
        data['task'],
        data['status'], 
        json.dumps(data.get('result', {})),
        datetime.fromtimestamp(data['timestamp'])
    ))
    
    conn.commit()
    conn.close()
```

### 與消息隊列整合

```python
import pika
import json

def send_to_queue(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='browser_results')
    channel.basic_publish(
        exchange='',
        routing_key='browser_results',
        body=json.dumps(data)
    )
    
    connection.close()
```

## 最佳實踐

1. **冪等性設計**：確保重複回調不會造成問題
2. **異步處理**：使用背景任務處理回調數據
3. **監控和警報**：設置回調失敗的監控機制
4. **數據驗證**：驗證回調數據的完整性和格式
5. **錯誤處理**：優雅處理各種錯誤情況

這樣您就可以建立一個完整的瀏覽器自動化工作流程，從任務提交到結果處理都能自動化完成！ 