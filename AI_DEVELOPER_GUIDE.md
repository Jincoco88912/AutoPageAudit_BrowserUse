# 🤖 AI开发者专用 - 浏览器自动化API指南

## 🎯 快速开始
这是一个**已部署在生产环境**的浏览器自动化API，可以执行任何网页操作任务。

### 核心API
```
POST https://browser-use.jincoco.site/api/run-agent
```

### 最简单的调用
```bash
curl -X POST https://browser-use.jincoco.site/api/run-agent \
  -H "Content-Type: application/json" \
  -d '{"task": "你的任务描述"}'
```

## 📋 参数说明

### 必需参数
- `task` (string): 任务描述，支持中英文，例如：
  - "访问淘宝首页并搜索iPhone"
  - "打开百度并截图"
  - "访问某网站并获取所有链接"

### 可选参数
- `callback_url` (string): 任务完成后回调的URL
- `use_stealth` (boolean): 反检测模式，访问复杂网站时建议开启
- `headless` (boolean): false=可视化调试，true=后台运行
- `max_retries` (integer): 重试次数，默认3次

## 🚀 实际使用案例

### 案例1: 网站截图
```json
{
  "task": "访问 https://www.apple.com 并截图首页"
}
```

### 案例2: 搜索操作
```json
{
  "task": "在Google搜索'人工智能最新发展'并获取前5个结果的标题",
  "use_stealth": true
}
```

### 案例3: 带回调的任务
```json
{
  "task": "访问京东首页，搜索'笔记本电脑'，获取商品列表",
  "callback_url": "https://你的服务器/webhook/callback",
  "use_stealth": true,
  "headless": false
}
```

## 📤 响应格式

### 成功时返回
```json
{
  "task_id": "1234.567890123",
  "status": "success", 
  "result": [/* 操作步骤和截图 */],
  "timestamp": 1234567890.123
}
```

### 失败时返回
```json
{
  "error": "任务失败原因",
  "suggestions": ["解决建议1", "建议2"]
}
```

## 🔔 Webhook回调 (可选)

如果提供了`callback_url`，任务完成后会POST发送结果到你的URL：

```json
{
  "status": "success",
  "task": "原始任务描述", 
  "result": [/* 详细执行结果 */],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 💡 AI开发建议

1. **任务描述要具体**: "访问XX网站并YY操作" 比 "帮我处理网站" 效果更好
2. **复杂任务分步**: 把复杂操作拆分成多个简单任务
3. **开启反检测**: 遇到现代网站时设置 `"use_stealth": true`
4. **使用回调**: 长任务建议使用webhook而不是同步等待
5. **调试模式**: 开发时设置 `"headless": false` 查看执行过程

## ⚡ 快速集成代码

### Python
```python
import requests

def browser_task(task_description, callback_url=None):
    payload = {
        "task": task_description,
        "use_stealth": True,
        "headless": False
    }
    if callback_url:
        payload["callback_url"] = callback_url
    
    response = requests.post(
        "https://browser-use.jincoco.site/api/run-agent",
        json=payload
    )
    return response.json()

# 使用示例
result = browser_task("访问百度首页并搜索'机器学习'")
print(result)
```

### Node.js
```javascript
async function browserTask(taskDescription, callbackUrl = null) {
  const payload = {
    task: taskDescription,
    use_stealth: true,
    headless: false
  };
  
  if (callbackUrl) payload.callback_url = callbackUrl;
  
  const response = await fetch('https://browser-use.jincoco.site/api/run-agent', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  
  return await response.json();
}

// 使用示例
const result = await browserTask("访问淘宝搜索iPhone并获取前10个商品");
console.log(result);
```

## 🎯 系统特性

✅ **已在生产环境稳定运行**  
✅ **支持反检测和验证码处理**  
✅ **智能重试机制**  
✅ **完整的错误处理和日志**  
✅ **支持复杂交互操作**  
✅ **自动截图和结果记录**  

## 🔗 相关资源
- 完整文档: `API_USAGE_GUIDE.md`
- GitHub: https://github.com/Jincoco88912/AutoPageAudit_BrowserUse
- 测试用例: 雄狮旅游网站已验证通过

---
**直接开始使用，无需复杂配置！** 🚀 