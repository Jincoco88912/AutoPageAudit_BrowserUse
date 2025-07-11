#!/usr/bin/env python3
"""
Webhook 回調功能測試腳本

此腳本創建一個簡單的測試服務器來接收回調，
然後發送測試請求到 AutoPageAudit API
"""

import asyncio
import json
import threading
import time
from flask import Flask, request, jsonify
import requests
import sys

# 創建測試 Flask 應用
app = Flask(__name__)

# 儲存接收到的回調數據
received_callbacks = []

@app.route('/test-webhook', methods=['POST'])
def test_webhook():
    """測試webhook端點"""
    data = request.get_json()
    print(f"\n🎯 收到回調！")
    print(f"狀態: {data.get('status')}")
    print(f"任務: {data.get('task')}")
    print(f"時間戳: {data.get('timestamp')}")
    
    if data.get('status') == 'success':
        result = data.get('result', [])
        print(f"結果步驟數: {len(result) if isinstance(result, list) else 1}")
        if isinstance(result, list) and result:
            print(f"最終URL: {result[-1].get('url', 'N/A')}")
        elif isinstance(result, dict):
            print(f"URL: {result.get('url', 'N/A')}")
    else:
        print(f"錯誤訊息: {data.get('message')}")
    
    # 儲存接收到的數據
    received_callbacks.append(data)
    
    return jsonify({"received": True, "status": "ok"})

@app.route('/health', methods=['GET'])
def health():
    """健康檢查端點"""
    return jsonify({"status": "healthy", "callbacks_received": len(received_callbacks)})

def run_flask_server():
    """在背景運行 Flask 服務器"""
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def test_webhook_functionality():
    """測試webhook功能"""
    print("🚀 啟動 Webhook 測試")
    
    # 在背景啟動 Flask 服務器
    flask_thread = threading.Thread(target=run_flask_server, daemon=True)
    flask_thread.start()
    
    # 等待服務器啟動
    print("⏳ 等待測試服務器啟動...")
    time.sleep(3)
    
    # 測試服務器是否正常運行
    try:
        response = requests.get('http://127.0.0.1:5000/health', timeout=5)
        print(f"✅ 測試服務器運行正常: {response.json()}")
    except Exception as e:
        print(f"❌ 測試服務器啟動失敗: {e}")
        return False
    
    # 發送測試請求到 AutoPageAudit API
    print("\n📤 發送測試請求到 AutoPageAudit API...")
    
    test_data = {
        "task": "打開 google.com 主頁",
        "callback_url": "http://127.0.0.1:5000/test-webhook",
        "callback_timeout": 30,
        "callback_retries": 2,
        "use_stealth": True,
        "headless": False,
        "max_retries": 1  # 減少重試次數以加快測試
    }
    
    try:
        # 發送 API 請求
        api_response = requests.post(
            'http://127.0.0.1:8080/api/run-agent',
            json=test_data,
            timeout=120  # 2分鐘超時
        )
        
        print(f"📥 API 回應狀態碼: {api_response.status_code}")
        
        if api_response.status_code == 200:
            response_data = api_response.json()
            print(f"✅ API 執行成功")
            print(f"任務狀態: {response_data.get('status')}")
            
            if response_data.get('status') == 'success':
                result = response_data.get('result')
                if isinstance(result, list):
                    print(f"執行步驟數: {len(result)}")
                else:
                    print("單步驟執行結果")
        else:
            print(f"❌ API 請求失敗: {api_response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ API 請求超時")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到 AutoPageAudit API，請確保服務正在運行")
        return False
    except Exception as e:
        print(f"❌ API 請求出錯: {e}")
        return False
    
    # 等待回調
    print("\n⏳ 等待 webhook 回調...")
    max_wait = 30  # 最多等待30秒
    wait_time = 0
    
    while wait_time < max_wait:
        if received_callbacks:
            print(f"🎉 成功接收到 {len(received_callbacks)} 個回調！")
            
            # 顯示回調詳情
            for i, callback in enumerate(received_callbacks):
                print(f"\n回調 {i+1}:")
                print(f"  狀態: {callback.get('status')}")
                print(f"  任務: {callback.get('task')}")
                if callback.get('status') == 'success':
                    result = callback.get('result')
                    if isinstance(result, list):
                        print(f"  步驟數: {len(result)}")
                        if result:
                            print(f"  最終URL: {result[-1].get('url', 'N/A')}")
                    elif isinstance(result, dict):
                        print(f"  URL: {result.get('url', 'N/A')}")
                
            return True
        
        time.sleep(1)
        wait_time += 1
        if wait_time % 5 == 0:
            print(f"  已等待 {wait_time} 秒...")
    
    print(f"⏰ 等待超時（{max_wait}秒），未收到回調")
    return False

def test_api_without_webhook():
    """測試不使用webhook的API請求"""
    print("\n🧪 測試無webhook模式...")
    
    test_data = {
        "task": "打開 google.com",
        "use_stealth": True,
        "headless": True,  # 使用無頭模式加快測試
        "max_retries": 1
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:8080/api/run-agent',
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 無webhook模式正常工作")
            print(f"狀態: {data.get('status')}")
            return True
        else:
            print(f"❌ 無webhook模式失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 無webhook測試失敗: {e}")
        return False

if __name__ == "__main__":
    print("🔧 AutoPageAudit Webhook 功能測試")
    print("=" * 50)
    
    # 檢查參數
    if len(sys.argv) > 1 and sys.argv[1] == "--no-webhook":
        # 只測試無webhook模式
        success = test_api_without_webhook()
    else:
        # 完整測試
        success = test_webhook_functionality()
        
        if success:
            print("\n🧪 額外測試：無webhook模式")
            test_api_without_webhook()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 測試完成！webhook功能正常工作")
    else:
        print("❌ 測試失敗，請檢查配置")
    
    print("\n💡 提示：")
    print("- 確保 AutoPageAudit API 在 http://127.0.0.1:8080 運行")
    print("- 確保網路連線正常")
    print("- 使用 --no-webhook 參數只測試基本API功能") 