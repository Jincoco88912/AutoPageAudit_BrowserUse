# 反檢測和 reCAPTCHA 解決方案指南

## 概述

本指南介紹如何使用增強的反檢測功能來避免被 Google reCAPTCHA 和其他反機器人系統阻擋。

## 🚀 快速開始

### 1. 基本反檢測配置

```bash
# 使用隱身模式執行任務
curl -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{
       "task": "搜尋最新的 iPhone 價格",
       "use_stealth": true,
       "headless": false,
       "delay_range": [2, 5]
     }'
```



## 📋 配置選項

### API 參數說明

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `use_stealth` | boolean | true | 啟用隱身模式 |
| `use_proxy` | boolean | false | 使用代理服務器 |
| `headless` | boolean | false | 無頭模式（建議設為 false） |
| `delay_range` | tuple | [1, 3] | 動作間延遲範圍（秒） |
| `max_retries` | int | 3 | 最大重試次數 |

### 環境變數配置

在 `.env` 文件中添加以下配置：

```bash
# Azure OpenAI 配置
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_api_key

# 代理配置（可選）
PROXY_LIST=proxy1:port,proxy2:port,proxy3:port
```

## 🛡️ 反檢測策略

### 1. 瀏覽器指紋偽裝

- **User-Agent 輪換**: 自動輪換真實的瀏覽器 User-Agent
- **視窗大小隨機化**: 隨機設置瀏覽器視窗大小
- **地理位置偽裝**: 設置台北地理座標
- **時區設置**: 設置為台北時區

### 2. 行為模擬

- **滑鼠移動**: 模擬自然的滑鼠移動軌跡
- **隨機延遲**: 在動作間添加人性化延遲
- **頁面滾動**: 模擬人類閱讀行為
- **打字延遲**: 模擬真實的打字速度

### 3. 瀏覽器屬性隱藏

- **WebDriver 屬性移除**: 隱藏自動化控制標識
- **Chrome 擴展模擬**: 添加真實的 Chrome 擴展屬性
- **Navigator 屬性修改**: 修改瀏覽器導航器屬性

## 🔧 reCAPTCHA 處理方法

### 方法 1: 等待和重試（推薦）

```python
# 自動重試並等待驗證碼消失
{
  "task": "your_task",
  "use_stealth": true,
  "max_retries": 5,
  "delay_range": [3, 8]
}
```

### 方法 2: 人類行為模擬

系統會自動：
- 檢測 reCAPTCHA 存在
- 模擬滑鼠移動和頁面滾動
- 簡單的頁面互動
- 等待並重新檢測驗證碼狀態

## 🌐 代理配置

### 住宅代理設置

1. 在 `.env` 文件中設置代理列表：
```bash
PROXY_LIST=residential_proxy1:port,residential_proxy2:port
```

2. 啟用代理：
```json
{
  "task": "your_task",
  "use_proxy": true,
  "use_stealth": true
}
```

### 代理輪換

系統會自動：
- 隨機選擇代理服務器
- 在重試時切換代理
- 檢測代理健康狀態

## 📊 效果監控

### 測試反檢測效果

您可以通過訪問檢測網站來測試反檢測效果：

```bash
# 測試基本反檢測
curl -X POST "http://localhost:8080/api/run-agent" \
     -H "Content-Type: application/json" \
     -d '{
       "task": "訪問 https://bot.sannysoft.com/ 並報告檢測結果",
       "use_stealth": true,
       "headless": false
     }'
```

**常用檢測網站：**
1. **Bot Detection Test**: https://bot.sannysoft.com/
2. **Headless Browser Test**: https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html
3. **Are You Headless**: https://arh.antoinevastel.com/bots/areyouheadless



## 🎯 最佳實踐

### 1. 任務設計

- **避免過於頻繁的請求**: 在請求間添加適當延遲
- **分散任務時間**: 避免在同一時間大量執行任務
- **使用自然語言**: 任務描述要像人類會做的事情

### 2. 配置優化

```json
{
  "task": "搜尋並比較三個電商網站的 iPhone 價格",
  "use_stealth": true,
  "use_proxy": false,
  "headless": false,
  "delay_range": [3, 7],
  "max_retries": 3
}
```

### 3. 錯誤處理

當遇到 reCAPTCHA 時：
1. 系統會自動重試
2. 增加延遲時間
3. 切換代理（如果已配置）
4. 模擬人類行為

## ⚠️ 注意事項

### 法律合規

- **遵守網站條款**: 確保您的使用符合目標網站的使用條款
- **請求頻率**: 不要過度頻繁地請求同一網站
- **資料使用**: 遵守相關的資料保護法規

### 技術限制

- **100% 成功率不保證**: 某些高級反機器人系統仍可能檢測到自動化
- **效能影響**: 隱身模式會增加延遲和資源使用
- **代理品質**: 代理服務器品質直接影響成功率

### 建議策略

1. **漸進式增強**: 從基本隱身開始，逐步添加更多功能
2. **監控和調整**: 根據實際效果調整參數
3. **備用方案**: 準備多種處理策略

## 🔍 故障排除

### 常見問題

**Q: 仍然被檢測為機器人**
A: 
- 確保 `headless: false`
- 增加 `delay_range` 值
- 嘗試使用住宅代理

**Q: 驗證碼無法自動解決**
A:
- 增加重試次數和延遲時間
- 使用住宅代理
- 檢查任務設計是否過於頻繁

**Q: 效能較慢**
A:
- 這是正常的，隱身模式會增加延遲
- 可以調整 `delay_range` 來平衡效能和成功率

### 日誌分析

檢查容器日誌：
```bash
docker-compose logs browser_agent
```

查找關鍵訊息：
- "檢測到 reCAPTCHA"
- "使用隱身配置"
- "代理連接狀態"

## 📈 效能優化建議

1. **選擇合適的代理**: 使用高品質的住宅代理
2. **優化延遲設置**: 根據目標網站調整延遲
3. **監控成功率**: 定期測試和調整配置
4. **使用快取**: 避免重複請求相同資料

---

*本指南會隨著技術發展持續更新。如有問題，請參考項目文檔或提交 Issue。* 