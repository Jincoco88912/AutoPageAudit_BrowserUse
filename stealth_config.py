"""
瀏覽器反檢測配置模組
用於躲避 Google reCAPTCHA 和其他反機器人檢測
"""

import random
import asyncio
from typing import Dict, List
import os

class StealthConfig:
    """瀏覽器隱身配置類"""
    
    @staticmethod
    def get_random_user_agent() -> str:
        """獲取隨機 User-Agent"""
        user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Safari/605.1.15"
        ]
        return random.choice(user_agents)
    
    @staticmethod
    def get_stealth_args() -> List[str]:
        """獲取隱身瀏覽器參數"""
        return [
            '--no-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-dev-shm-usage',
            '--disable-extensions-file-access-check',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-gpu',
            '--no-first-run',
            '--no-default-browser-check',
            '--no-pings',
            '--password-store=basic',
            '--use-mock-keychain',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-field-trial-config',
            '--disable-features=TranslateUI',
            '--disable-ipc-flooding-protection',
            '--enable-features=NetworkService,NetworkServiceLogging',
            '--force-color-profile=srgb',
            '--metrics-recording-only',
            '--use-fake-device-for-media-stream',
            '--use-fake-ui-for-media-stream',
            '--mute-audio',
            f'--user-agent={StealthConfig.get_random_user_agent()}'
        ]
    
    @staticmethod
    def get_browser_config(headless: bool = False) -> Dict:
        """獲取完整的瀏覽器配置"""
        return {
            'headless': headless,
            'args': StealthConfig.get_stealth_args(),
            'slow_mo': random.randint(50, 150),  # 隨機慢速模式
            'viewport': {'width': 1920, 'height': 1080},
            'locale': 'zh-TW',
            'timezone_id': 'Asia/Taipei',
            'permissions': ['geolocation'],
            'geolocation': {'latitude': 25.0330, 'longitude': 121.5654},  # 台北座標
            'extra_http_headers': {
                'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Upgrade-Insecure-Requests': '1'
            }
        }

class HumanBehavior:
    """模擬人類行為的工具類"""
    
    @staticmethod
    async def random_delay(min_seconds: float = 0.5, max_seconds: float = 2.0):
        """隨機延遲"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)
    
    @staticmethod
    async def human_type_delay():
        """模擬人類打字延遲"""
        await asyncio.sleep(random.uniform(0.05, 0.15))
    
    @staticmethod
    async def random_mouse_movement():
        """隨機鼠標移動延遲"""
        await asyncio.sleep(random.uniform(0.1, 0.3))
    
    @staticmethod
    def get_random_viewport():
        """獲取隨機視窗大小"""
        viewports = [
            {'width': 1920, 'height': 1080},
            {'width': 1366, 'height': 768},
            {'width': 1440, 'height': 900},
            {'width': 1536, 'height': 864},
            {'width': 1280, 'height': 720}
        ]
        return random.choice(viewports)

class ProxyConfig:
    """代理配置類"""
    
    @staticmethod
    def get_proxy_config(proxy_url: str = None) -> Dict:
        """獲取代理配置"""
        if proxy_url:
            return {
                'server': proxy_url,
                'bypass': 'localhost,127.0.0.1'
            }
        return {}
    
    @staticmethod
    def get_residential_proxies() -> List[str]:
        """獲取住宅代理列表（需要您自己的代理服務）"""
        # 這裡您需要添加自己的代理服務器
        # 例如從環境變數讀取
        proxy_list = os.getenv('PROXY_LIST', '').split(',')
        return [proxy.strip() for proxy in proxy_list if proxy.strip()]

# 使用範例
def get_enhanced_config(use_proxy: bool = False, headless: bool = False) -> Dict:
    """獲取增強的配置"""
    config = StealthConfig.get_browser_config(headless=headless)
    
    if use_proxy:
        proxies = ProxyConfig.get_residential_proxies()
        if proxies:
            proxy_url = random.choice(proxies)
            config['proxy'] = ProxyConfig.get_proxy_config(proxy_url)
    
    # 添加隨機視窗大小
    config['viewport'] = HumanBehavior.get_random_viewport()
    
    return config 