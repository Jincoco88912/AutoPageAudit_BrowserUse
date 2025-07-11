"""
reCAPTCHA 和驗證碼處理模組
提供基礎的驗證碼檢測和處理策略
"""

import asyncio
import random
from typing import Dict, Any
from stealth_config import HumanBehavior

class CaptchaHandler:
    """驗證碼檢測和處理器"""
    
    async def detect_captcha(self, page) -> Dict[str, Any]:
        """檢測頁面中是否有驗證碼"""
        captcha_indicators = [
            # reCAPTCHA v2
            'iframe[src*="recaptcha"]',
            '.g-recaptcha',
            '#recaptcha',
            
            # reCAPTCHA v3
            '.grecaptcha-badge',
            
            # hCaptcha
            '.h-captcha',
            'iframe[src*="hcaptcha"]',
            
            # Cloudflare
            '.cf-browser-verification',
            '#cf-challenge-running',
            
            # 通用驗證碼指示器
            '[data-captcha]',
            '.captcha',
            '#captcha'
        ]
        
        detected_captchas = []
        
        for selector in captcha_indicators:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    detected_captchas.append({
                        'type': self._identify_captcha_type(selector),
                        'selector': selector,
                        'count': len(elements)
                    })
            except Exception as e:
                print(f"檢測驗證碼時出錯 {selector}: {e}")
        
        return {
            'has_captcha': len(detected_captchas) > 0,
            'captchas': detected_captchas
        }
    
    def _identify_captcha_type(self, selector: str) -> str:
        """識別驗證碼類型"""
        if 'recaptcha' in selector.lower():
            return 'reCAPTCHA'
        elif 'hcaptcha' in selector.lower():
            return 'hCaptcha'
        elif 'cf-' in selector.lower():
            return 'Cloudflare'
        else:
            return 'Generic'
    
    async def handle_recaptcha(self, page, method: str = 'wait_and_retry') -> bool:
        """處理 reCAPTCHA"""
        print("檢測到 reCAPTCHA，開始處理...")
        
        if method == 'wait_and_retry':
            return await self._wait_and_retry_strategy(page)
        elif method == 'human_simulation':
            return await self._human_simulation_strategy(page)
        else:
            return False
    
    async def _wait_and_retry_strategy(self, page) -> bool:
        """等待和重試策略"""
        print("使用等待和重試策略...")
        
        # 等待較長時間，希望驗證碼自動消失
        await asyncio.sleep(random.uniform(10, 20))
        
        # 重新整理頁面
        await page.reload(wait_until='networkidle')
        await HumanBehavior.random_delay(2, 5)
        
        # 檢查驗證碼是否還存在
        captcha_result = await self.detect_captcha(page)
        return not captcha_result['has_captcha']
    
    async def _human_simulation_strategy(self, page) -> bool:
        """人類行為模擬策略"""
        print("使用人類行為模擬策略...")
        
        try:
            # 模擬用戶行為 - 滾動頁面
            await page.evaluate("""
                () => {
                    window.scrollBy(0, Math.random() * 300);
                }
            """)
            await HumanBehavior.random_delay(1, 3)
            
            # 模擬滑鼠移動
            await page.mouse.move(
                random.randint(100, 800),
                random.randint(100, 600)
            )
            await HumanBehavior.random_delay(0.5, 2)
            
            # 簡單的頁面互動
            await page.evaluate("window.scrollTo(0, 0)")
            await HumanBehavior.random_delay(1, 2)
            
            # 等待後檢查驗證碼是否消失
            await asyncio.sleep(random.uniform(5, 10))
            captcha_result = await self.detect_captcha(page)
            return not captcha_result['has_captcha']
            
        except Exception as e:
            print(f"人類行為模擬失敗: {e}")
            return False

class CaptchaAvoider:
    """驗證碼避免器 - 預防性措施"""
    
    @staticmethod
    async def implement_evasion_tactics(page):
        """實施規避策略"""
        
        # 隱藏 webdriver 屬性
        await page.evaluate("""
            () => {
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // 移除 automation 相關屬性
                if (window.chrome && window.chrome.runtime && window.chrome.runtime.onConnect) {
                    delete window.chrome.runtime.onConnect;
                }
                
                // 修改 plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                // 修改 languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-TW', 'zh', 'en'],
                });
            }
        """)
        
        # 添加真實的 Chrome 擴展屬性
        await page.evaluate("""
            () => {
                if (!window.chrome) {
                    window.chrome = {};
                }
                if (!window.chrome.runtime) {
                    window.chrome.runtime = {
                        onConnect: undefined,
                        onMessage: undefined
                    };
                }
            }
        """)
    
    @staticmethod
    async def add_mouse_movements(page):
        """添加自然的滑鼠移動"""
        for _ in range(random.randint(3, 7)):
            x = random.randint(100, 1000)
            y = random.randint(100, 700)
            await page.mouse.move(x, y)
            await HumanBehavior.random_delay(0.1, 0.5)
    
    @staticmethod
    async def simulate_human_reading(page):
        """模擬人類閱讀行為"""
        # 隨機滾動，模擬閱讀
        for _ in range(random.randint(2, 5)):
            scroll_amount = random.randint(100, 400)
            await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            await HumanBehavior.random_delay(1, 3)
        
        # 滾回頂部
        await page.evaluate("window.scrollTo(0, 0)")
        await HumanBehavior.random_delay(1, 2) 