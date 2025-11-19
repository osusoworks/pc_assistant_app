"""
相対座標モジュール
アクティブウィンドウ内の相対座標を取得し、絶対座標に変換
"""

import time
from typing import Dict, Optional
from PIL import ImageGrab
import json


class RelativeCoordinateModule:
    """相対座標方式で座標を検出するモジュール"""
    
    def __init__(self, ai_module=None):
        """
        初期化
        
        Args:
            ai_module: AI解析モジュール（AIModuleImproved）
        """
        self.ai_module = ai_module
    
    def detect(self, screenshot_path: str, question: str) -> Optional[Dict]:
        """
        相対座標方式で座標を検出
        
        Args:
            screenshot_path: 元のスクリーンショットのパス
            question: ユーザーの質問
        
        Returns:
            {
                'x': int,  # 絶対座標X
                'y': int,  # 絶対座標Y
                'confidence': str,  # 信頼度
                'window_info': Dict,  # ウィンドウ情報
                'relative_coords': Dict,  # 相対座標
                'method': str  # 使用した方式
            }
        """
        print("=== 相対座標方式で座標を検出 ===")
        
        # アクティブウィンドウを取得
        window_info = self._get_active_window()
        
        if not window_info:
            print("アクティブウィンドウが取得できませんでした。全画面で処理します。")
            return self._fallback_to_fullscreen(screenshot_path, question)
        
        print(f"アクティブウィンドウ: {window_info['title']}")
        print(f"ウィンドウ位置: ({window_info['x']}, {window_info['y']})")
        print(f"ウィンドウサイズ: {window_info['width']} x {window_info['height']}")
        
        # ウィンドウ内のスクリーンショットを撮影
        window_screenshot_path = self._capture_window(window_info)
        
        if not window_screenshot_path:
            print("ウィンドウのスクリーンショット撮影に失敗しました")
            return self._fallback_to_fullscreen(screenshot_path, question)
        
        # AI解析（ウィンドウ内の相対座標を返す）
        prompt = self._create_relative_coordinate_prompt(
            question,
            window_info['width'],
            window_info['height']
        )
        
        if not self.ai_module:
            print("AI解析モジュールが設定されていません")
            return None
        
        result = self.ai_module.analyze_screenshot(window_screenshot_path, prompt)
        
        if not result or 'coordinates' not in result:
            print("AI解析で座標が取得できませんでした")
            return None
        
        # 相対座標を取得
        coordinates = result['coordinates']
        
        if not isinstance(coordinates, dict):
            print(f"座標が辞書形式ではありません: {type(coordinates)}")
            return None
        
        relative_x = coordinates.get('x')
        relative_y = coordinates.get('y')
        
        if relative_x is None or relative_y is None:
            print("座標にxまたはyが含まれていません")
            return None
        
        # 相対座標を絶対座標に変換
        absolute_x = window_info['x'] + relative_x
        absolute_y = window_info['y'] + relative_y
        
        print(f"相対座標: ({relative_x}, {relative_y})")
        print(f"絶対座標: ({absolute_x}, {absolute_y})")
        
        return {
            'x': absolute_x,
            'y': absolute_y,
            'confidence': result.get('confidence', 'medium'),
            'window_info': window_info,
            'relative_coords': {'x': relative_x, 'y': relative_y},
            'method': 'relative_coordinate'
        }
    
    def _get_active_window(self) -> Optional[Dict]:
        """
        アクティブウィンドウの情報を取得
        
        Returns:
            {
                'title': str,  # ウィンドウタイトル
                'x': int,  # ウィンドウ左上X座標
                'y': int,  # ウィンドウ左上Y座標
                'width': int,  # ウィンドウ幅
                'height': int  # ウィンドウ高さ
            }
        """
        try:
            import sys
            
            # Windows環境のみサポート
            if sys.platform != 'win32':
                print("pygetwindowはWindows環境でのみ使用可能です")
                return None
            
            import pygetwindow as gw
            
            active_window = gw.getActiveWindow()
            
            if active_window:
                # ウィンドウ情報を取得
                window_info = {
                    'title': active_window.title,
                    'x': active_window.left,
                    'y': active_window.top,
                    'width': active_window.width,
                    'height': active_window.height
                }
                
                # ウィンドウサイズが有効かチェック
                if window_info['width'] > 0 and window_info['height'] > 0:
                    return window_info
                else:
                    print(f"ウィンドウサイズが無効です: {window_info['width']} x {window_info['height']}")
            else:
                print("アクティブウィンドウが見つかりませんでした")
        
        except Exception as e:
            print(f"アクティブウィンドウ取得エラー: {e}")
        
        return None
    
    def _capture_window(self, window_info: Dict) -> Optional[str]:
        """
        ウィンドウ内のスクリーンショットを撮影
        
        Args:
            window_info: ウィンドウ情報
        
        Returns:
            スクリーンショットのファイルパス
        """
        try:
            bbox = (
                window_info['x'],
                window_info['y'],
                window_info['x'] + window_info['width'],
                window_info['y'] + window_info['height']
            )
            
            screenshot = ImageGrab.grab(bbox=bbox)
            
            screenshot_path = f"/tmp/window_screenshot_{int(time.time())}.png"
            screenshot.save(screenshot_path)
            
            print(f"ウィンドウのスクリーンショットを保存: {screenshot_path}")
            
            return screenshot_path
        
        except Exception as e:
            print(f"ウィンドウスクリーンショット撮影エラー: {e}")
            return None
    
    def _create_relative_coordinate_prompt(self, question: str, width: int, height: int) -> str:
        """
        相対座標取得用のAIプロンプトを作成
        
        Args:
            question: ユーザーの質問
            width: ウィンドウ幅
            height: ウィンドウ高さ
        
        Returns:
            AIプロンプト
        """
        prompt = f"""
この画像はアクティブウィンドウのスクリーンショットです。
画像サイズ: {width} x {height} ピクセル

ユーザーの質問: {question}

この画像内で、ユーザーの質問に該当する要素の位置を、ウィンドウ内の相対座標（左上を(0,0)とする）で返してください。

以下のJSON形式で回答してください：
{{
    "answer": "質問への回答",
    "coordinates": {{
        "x": X座標（整数、0から{width}の範囲）,
        "y": Y座標（整数、0から{height}の範囲）
    }},
    "confidence": "high|medium|low",
    "element_description": "要素の説明"
}}

重要:
- 座標は必ず整数で返してください
- 座標はウィンドウ内の相対座標です（画面全体ではありません）
- 要素の中心座標を返してください
"""
        return prompt
    
    def _fallback_to_fullscreen(self, screenshot_path: str, question: str) -> Optional[Dict]:
        """
        全画面での処理にフォールバック
        
        Args:
            screenshot_path: 元のスクリーンショットのパス
            question: ユーザーの質問
        
        Returns:
            座標結果（全画面座標）
        """
        print("全画面での処理にフォールバックします")
        
        if not self.ai_module:
            return None
        
        # 通常のAI解析を実行
        result = self.ai_module.analyze_screenshot(screenshot_path, question)
        
        if not result or 'coordinates' not in result:
            return None
        
        coordinates = result['coordinates']
        
        if not isinstance(coordinates, dict):
            return None
        
        x = coordinates.get('x')
        y = coordinates.get('y')
        
        if x is None or y is None:
            return None
        
        return {
            'x': x,
            'y': y,
            'confidence': result.get('confidence', 'medium'),
            'window_info': None,
            'relative_coords': None,
            'method': 'fullscreen_fallback'
        }

