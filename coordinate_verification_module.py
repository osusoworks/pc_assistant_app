"""
座標検証モジュール
座標の妥当性をチェックし、マルチステップ検証で精度を向上
"""

import time
import json
from typing import Dict, Optional
from PIL import ImageGrab, ImageDraw
import os
from openai import OpenAI


class CoordinateVerificationModule:
    """座標を検証するモジュール"""
    
    def __init__(self):
        """初期化"""
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    def verify(self, screenshot_path: str, result: Dict, question: str) -> Dict:
        """
        座標を検証
        
        Args:
            screenshot_path: 元のスクリーンショット
            result: 検証対象の座標結果
            question: ユーザーの質問
        
        Returns:
            検証・修正された座標結果
        """
        print("=== 座標を検証 ===")
        
        x, y = result['x'], result['y']
        
        # ステップ1: 座標の妥当性チェック
        if not self._is_valid_coordinate(x, y):
            print(f"警告: 座標が画面外または不正です: ({x}, {y})")
            result['confidence'] = 'low'
            result['verified'] = False
            return result
        
        print(f"検証対象座標: ({x}, {y})")
        
        # ステップ2: 部分画像を撮影
        region_screenshot_path = self._capture_region(x, y)
        
        if not region_screenshot_path:
            print("部分画像の撮影に失敗しました")
            result['verified'] = False
            return result
        
        # ステップ3: AIに検証させる
        verification_result = self._verify_with_ai(
            region_screenshot_path,
            question,
            x,
            y
        )
        
        # ステップ4: 検証結果に基づいて座標を修正
        if verification_result['is_correct']:
            print("✅ 座標は正しいと判定されました")
            result['confidence'] = 'high'
            result['verified'] = True
        else:
            # 座標を修正
            offset_x = verification_result.get('offset_x', 0)
            offset_y = verification_result.get('offset_y', 0)
            
            result['x'] += offset_x
            result['y'] += offset_y
            result['confidence'] = verification_result.get('confidence', 'medium')
            result['verified'] = True
            result['correction_applied'] = True
            
            print(f"🔧 座標を修正: ({x}, {y}) → ({result['x']}, {result['y']})")
            print(f"修正理由: {verification_result.get('reason', '')}")
        
        return result
    
    def _is_valid_coordinate(self, x: int, y: int) -> bool:
        """
        座標の妥当性をチェック
        
        Args:
            x: X座標
            y: Y座標
        
        Returns:
            座標が有効かどうか
        """
        try:
            import tkinter as tk
            
            root = tk.Tk()
            root.withdraw()
            
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            
            root.destroy()
            
            # 画面内かチェック
            if x < 0 or x >= screen_width or y < 0 or y >= screen_height:
                return False
            
            # 画面端に近すぎないかチェック（警告のみ）
            margin = 5
            if x < margin or x > screen_width - margin or y < margin or y > screen_height - margin:
                print(f"警告: 座標が画面端に近すぎます: ({x}, {y})")
            
            return True
        
        except Exception as e:
            print(f"座標妥当性チェックエラー: {e}")
            # エラーの場合は有効とみなす
            return True
    
    def _capture_region(self, x: int, y: int, size: int = 200) -> Optional[str]:
        """
        指定座標周辺の部分画像を撮影
        
        Args:
            x: 中心X座標
            y: 中心Y座標
            size: 領域のサイズ（デフォルト200x200）
        
        Returns:
            部分画像のファイルパス
        """
        try:
            half_size = size // 2
            bbox = (x - half_size, y - half_size, x + half_size, y + half_size)
            
            region = ImageGrab.grab(bbox=bbox)
            
            # 中心に十字線を描画
            draw = ImageDraw.Draw(region)
            draw.line([(half_size - 10, half_size), (half_size + 10, half_size)], fill='red', width=2)
            draw.line([(half_size, half_size - 10), (half_size, half_size + 10)], fill='red', width=2)
            
            region_path = f"/tmp/region_{int(time.time())}.png"
            region.save(region_path)
            
            print(f"部分画像を保存: {region_path}")
            
            return region_path
        
        except Exception as e:
            print(f"部分画像撮影エラー: {e}")
            return None
    
    def _verify_with_ai(self, region_path: str, question: str, x: int, y: int) -> Dict:
        """
        AIで座標を検証
        
        Args:
            region_path: 部分画像のパス
            question: ユーザーの質問
            x: 現在のX座標
            y: 現在のY座標
        
        Returns:
            {
                'is_correct': bool,
                'confidence': str,
                'offset_x': int,
                'offset_y': int,
                'reason': str
            }
        """
        print("AIで座標を検証中...")
        
        try:
            import base64
            
            # 画像をBase64エンコード
            with open(region_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            prompt = f"""
この画像の中心（赤い十字線の位置）は、ユーザーの質問に該当する要素を正しく指していますか？

ユーザーの質問: {question}
現在の座標: ({x}, {y})

画像は200x200ピクセルで、中心が現在の座標位置です。

以下のJSON形式で回答してください：
{{
    "is_correct": true/false,
    "confidence": "high|medium|low",
    "offset_x": 修正X座標（ピクセル、正しい場合は0、右方向が正）,
    "offset_y": 修正Y座標（ピクセル、正しい場合は0、下方向が正）,
    "reason": "判断理由"
}}

重要:
- 赤い十字線が要素の中心を指している場合は is_correct: true
- ずれている場合は、正しい位置までのオフセット（ピクセル数）を返してください
- オフセットは -100 から +100 の範囲内で返してください
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            print(f"AI検証結果: {result}")
            
            return result
        
        except Exception as e:
            print(f"AI検証エラー: {e}")
            import traceback
            traceback.print_exc()
            
            # エラーの場合は、座標は正しいとみなす
            return {
                'is_correct': True,
                'confidence': 'medium',
                'offset_x': 0,
                'offset_y': 0,
                'reason': '検証失敗'
            }

