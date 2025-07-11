# AutoPageAudit_BrowserUse API 使用指南

## 🚀 概述
这是一个基于 Azure OpenAI 和 browser-use 的智能浏览器自动化API，支持网页爬取、自动化操作和 webhook 回调功能。

## 📡 API 端点
```
POST https://browser-use.jincoco.site/api/run-agent
```

## 🔧 请求参数

### 基本参数
| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| `task` | string | ✅ | 要执行的任务描述（中文或英文） |
| `callback_url` | string | ❌ | 任务完成后的回调URL |

### 配置参数
| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `use_stealth` | boolean | `false` | 启用反检测模式 |
| `headless` | boolean | `true` | 无头模式（false=可视化） |
| `max_retries` | integer | `3` | 最大重试次数 |
| `delay_range` | array | `[1, 3]` | 操作间延迟范围（秒） |

### Webhook 参数
| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `callback_url` | string | `null` | 回调URL地址 |
| `callback_timeout` | integer | `30` | 回调超时时间（秒） |
| `callback_retries` | integer | `3` | 回调重试次数 |

## 📝 请求示例

### 基本用法
```bash
curl -X POST https://browser-use.jincoco.site/api/run-agent \
  -H "Content-Type: application/json" \
  -d '{
    "task": "访问 https://example.com 并获取页面标题"
  }'
```

### 完整配置示例
```bash
curl -X POST https://browser-use.jincoco.site/api/run-agent \
  -H "Content-Type: application/json" \
  -d '{
    "task": "前往雄獅旅遊網站 https://www.liontravel.com/category/zh-tw/index 並瀏覽首頁，確認頁面正常",
    "callback_url": "https://your-webhook-url.com/callback",
    "callback_timeout": 30,
    "callback_retries": 3,
    "use_stealth": true,
    "headless": false,
    "max_retries": 2,
    "delay_range": [1, 3]
  }'
```

### JavaScript/Node.js 示例
```javascript
const response = await fetch('https://browser-use.jincoco.site/api/run-agent', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    task: "访问淘宝网站并搜索iPhone",
    callback_url: "https://your-webhook-url.com/callback",
    use_stealth: true,
    headless: false
  })
});

const result = await response.json();
console.log(result);
```

### Python 示例
```python
import requests

url = "https://browser-use.jincoco.site/api/run-agent"
payload = {
    "task": "打开百度搜索页面并搜索'人工智能'",
    "callback_url": "https://your-webhook-url.com/callback",
    "use_stealth": True,
    "headless": False,
    "max_retries": 2
}

response = requests.post(url, json=payload)
result = response.json()
print(result)
```

## 📤 响应格式

### 成功响应
```json
{
  "task_id": "1234.567890123",
  "status": "success",
  "message": "任务执行成功",
  "result": [
    {
      "action": "goto",
      "url": "https://example.com",
      "screenshot": "base64_encoded_image..."
    }
  ],
  "attempt": 1,
  "config_used": {
    "stealth": true,
    "proxy": false,
    "headless": false
  },
  "timestamp": 1234567890.123
}
```

### 错误响应
```json
{
  "error": "任务执行失败",
  "message": "详细错误信息",
  "attempts": 3,
  "suggestions": ["建议1", "建议2"],
  "timestamp": 1234567890.123
}
```

## 🔔 Webhook 回调

如果提供了 `callback_url`，任务完成后会自动发送POST请求到指定URL。

### 成功回调数据
```json
{
  "status": "success",
  "task": "用户提交的任务描述",
  "result": [
    {
      "action": "操作类型",
      "details": "操作详情",
      "screenshot": "base64截图"
    }
  ],
  "attempt": 1,
  "config_used": {
    "stealth": true,
    "proxy": false,
    "headless": false
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 失败回调数据
```json
{
  "status": "error",
  "message": "错误详情",
  "attempts": 3,
  "suggestions": ["建议解决方案"],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🎯 任务类型示例

### 网页访问
```json
{
  "task": "访问 https://www.google.com 并截图"
}
```

### 搜索操作
```json
{
  "task": "在百度搜索'机器学习'并查看前3个结果"
}
```

### 表单填写
```json
{
  "task": "访问注册页面，填写用户名'testuser'和邮箱'test@example.com'"
}
```

### 数据抓取
```json
{
  "task": "访问新闻网站首页，获取所有新闻标题"
}
```

## ⚠️ 注意事项

1. **任务描述要清晰**: 详细描述要执行的操作
2. **Webhook URL**: 确保回调URL可以接收POST请求
3. **反检测模式**: 访问反爬虫网站时建议启用 `use_stealth: true`
4. **超时设置**: 复杂任务可能需要更长执行时间
5. **重试机制**: 系统会自动重试失败的任务

## 🛠️ 调试建议

1. **可视化调试**: 设置 `headless: false` 查看浏览器操作过程
2. **日志分析**: 检查响应中的错误信息和建议
3. **分步执行**: 复杂任务建议拆分为多个简单步骤
4. **网络环境**: 确保服务器网络能正常访问目标网站

## 📞 技术支持

- 项目地址: https://github.com/Jincoco88912/AutoPageAudit_BrowserUse
- 问题反馈: 通过GitHub Issues提交
- 功能特点: 智能反检测、reCAPTCHA解决、webhook回调

---

**这个API已经在生产环境中稳定运行，支持各种网页自动化任务！** 🚀 