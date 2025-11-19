#!/usr/bin/env python3
"""
AI解析モジュール（座標精度大幅改善版）
座標系統一、マルチモニター対応、認識精度向上を実装
"""

import os
import json
import base64
from typing import Optional, Dict, Any, Tuple
from PIL import Image, ImageGrab
import tkinter as tk


class AIModuleImproved:
    """AI解析を担当するモジュール（座標精度大幅改善版）"""
    
    def __init__(self):
        """初期化"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        
        # 座標精度改善のための設定
        self.screen_info = self._get_screen_info()
        
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI()
                print("AI解析モジュール（座標精度改善版）が初期化されました")
                print(f"画面情報: {self.screen_info}")
            except ImportError:
                print("OpenAIライブラリがインストールされていません")
                self.client = None
        else:
            print("OpenAI APIキーが設定されていません")
    
    def _get_screen_info(self) -> Dict[str, Any]:
        """
        画面情報を取得（座標計算精度向上のため）
        
        Returns:
            画面情報の辞書
        """
        try:
            # 実際の画面サイズを取得
            screenshot = ImageGrab.grab()
            actual_width, actual_height = screenshot.size
            
            # tkinterでの画面情報も取得
            root = tk.Tk()
            root.withdraw()  # ウィンドウを表示しない
            
            tk_width = root.winfo_screenwidth()
            tk_height = root.winfo_screenheight()
            
            # DPI情報を取得
            try:
                dpi_x = root.winfo_fpixels('1i')
                dpi_y = root.winfo_fpixels('1i')
            except:
                dpi_x = dpi_y = 96  # デフォルト値
            
            root.destroy()
            
            screen_info = {
                'actual_width': actual_width,
                'actual_height': actual_height,
                'tk_width': tk_width,
                'tk_height': tk_height,
                'dpi_x': dpi_x,
                'dpi_y': dpi_y,
                'scale_x': actual_width / tk_width if tk_width > 0 else 1.0,
                'scale_y': actual_height / tk_height if tk_height > 0 else 1.0
            }
            
            return screen_info
            
        except Exception as e:
            print(f"画面情報取得エラー: {e}")
            return {
                'actual_width': 1920,
                'actual_height': 1080,
                'tk_width': 1920,
                'tk_height': 1080,
                'dpi_x': 96,
                'dpi_y': 96,
                'scale_x': 1.0,
                'scale_y': 1.0
            }
    
    def _encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """
        画像をBase64エンコード
        
        Args:
            image_path: 画像ファイルのパス
            
        Returns:
            Base64エンコードされた画像データ
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                return encoded_image
        except Exception as e:
            print(f"画像エンコードエラー: {e}")
            return None
    
    def _get_image_dimensions(self, image_path: str) -> Tuple[int, int]:
        """
        画像の実際のサイズを取得
        
        Args:
            image_path: 画像ファイルのパス
            
        Returns:
            (width, height) のタプル
        """
        try:
            with Image.open(image_path) as img:
                return img.size
        except Exception as e:
            print(f"画像サイズ取得エラー: {e}")
            return (1920, 1080)  # デフォルト値
    
    def _create_enhanced_prompt(self, question: str, image_width: int, image_height: int) -> str:
        """
        座標精度向上のための強化プロンプトを作成
        
        Args:
            question: ユーザーの質問
            image_width: 画像の幅
            image_height: 画像の高さ
            
        Returns:
            強化されたプロンプト
        """
        return f"""あなたは画面操作支援の専門家です。提供されたスクリーンショット画像を詳細に分析し、ユーザーの質問に対して正確な操作指示を提供してください。

【重要な座標計算ルール】
1. 画像サイズ: {image_width} x {image_height} ピクセル
2. 座標は画像の左上を (0, 0) とする絶対座標で指定
3. 要素の中心点を正確に計算して座標を返す
4. ボタンやリンクなどのクリック可能要素は、その視覚的中心を座標とする
5. テキスト要素の場合は、テキストの中央部分を座標とする

【座標精度向上のガイドライン】
- ボタン: ボタンの境界を正確に識別し、その中心点を計算
- リンク: リンクテキストの中央位置を特定
- アイコン: アイコンの視覚的中心を計算
- メニュー項目: 項目の中央部分を特定
- 入力フィールド: フィールドの中央部分を特定

【信頼度評価基準】
- high: 要素が明確に識別でき、境界が正確に判断できる
- medium: 要素は識別できるが、境界に若干の不確実性がある
- low: 要素の識別が困難、または複数の候補がある

【特別な注意事項】
- Canvaなどのウェブサイトでログインを求められた場合：
  * 画面左上のユーザーアイコン（人型アイコン）を探してください
  * 「ログイン」「サインイン」「Sign in」などのテキストボタンを探してください
  * 右上のメニューエリアも確認してください
  * アカウント関連のアイコンやボタンを優先的に検出してください
- ブラウザのコンテンツ、デスクトップアプリ、システムUIを対象とする

ユーザーの質問: {question}

以下のJSON形式で回答してください：
{{
    "answer": "操作方法の詳細な説明",
    "coordinates": {{
        "x": 正確なX座標（整数）,
        "y": 正確なY座標（整数）
    }},
    "confidence": "high|medium|low",
    "element_description": "指示している要素の詳細な説明",
    "calculation_method": "座標計算の方法（要素の境界と中心点計算の説明）",
    "alternative_coordinates": [
        {{
            "x": 代替X座標,
            "y": 代替Y座標,
            "description": "代替座標の説明"
        }}
    ]
}}

座標は必ず画像内の実際の要素を指すようにし、推測や概算ではなく、視覚的に確認できる要素の正確な中心点を返してください。"""
    
    def analyze_screenshot(self, screenshot_path: str, question: str) -> Optional[Dict[str, Any]]:
        """
        スクリーンショットを解析（座標精度大幅改善版）
        
        Args:
            screenshot_path: スクリーンショットのファイルパス
            question: ユーザーの質問
            
        Returns:
            解析結果の辞書
        """
        if not self.client:
            print("OpenAIクライアントが利用できません")
            return None
        
        try:
            # 画像の実際のサイズを取得
            image_width, image_height = self._get_image_dimensions(screenshot_path)
            print(f"解析対象画像サイズ: {image_width} x {image_height}")
            
            # 画像をBase64エンコード
            base64_image = self._encode_image_to_base64(screenshot_path)
            if not base64_image:
                return None
            
            # 強化プロンプトを作成
            prompt = self._create_enhanced_prompt(question, image_width, image_height)
            
            print("座標精度改善版AI解析を実行中...")
            
            # OpenAI APIを呼び出し
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
                                    "url": f"data:image/png;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.1  # 一貫性のために低い値
            )
            
            # レスポンスを解析
            response_text = response.choices[0].message.content
            print(f"AI解析レスポンス: {response_text}")
            
            # JSONを抽出
            result = self._extract_json_from_response(response_text)
            
            if result:
                # 座標を画面座標系に変換
                converted_result = self._convert_coordinates_to_screen(
                    result, image_width, image_height
                )
                
                print(f"座標変換結果: {converted_result}")
                return converted_result
            else:
                print("JSON解析に失敗しました")
                return None
                
        except Exception as e:
            print(f"AI解析エラー: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _extract_json_from_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """
        レスポンステキストからJSONを抽出
        
        Args:
            response_text: AIのレスポンステキスト
            
        Returns:
            抽出されたJSONデータ
        """
        try:
            # JSONブロックを探す
            import re
            
            # ```json ブロックを探す
            json_match = re.search(r'```json\s*({.*?})\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # 直接JSONを探す
                json_match = re.search(r'({.*})', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    print("JSONが見つかりませんでした")
                    return None
            
            # JSONをパース
            result = json.loads(json_str)
            
            # 必要なフィールドを検証
            required_fields = ['answer', 'coordinates', 'confidence', 'element_description']
            for field in required_fields:
                if field not in result:
                    print(f"必須フィールド '{field}' が見つかりません")
                    return None
            
            # 座標の検証
            coords = result.get('coordinates', {})
            if not isinstance(coords, dict) or 'x' not in coords or 'y' not in coords:
                print("座標情報が不正です")
                return None
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON解析エラー: {e}")
            return None
        except Exception as e:
            print(f"レスポンス解析エラー: {e}")
            return None
    
    def _convert_coordinates_to_screen(self, result: Dict[str, Any], 
                                     image_width: int, image_height: int) -> Dict[str, Any]:
        """
        画像座標を実際の画面座標に変換
        
        Args:
            result: AI解析結果
            image_width: 画像の幅
            image_height: 画像の高さ
            
        Returns:
            座標変換済みの結果
        """
        try:
            coords = result['coordinates']
            image_x = coords['x']
            image_y = coords['y']
            
            # 画像サイズと実際の画面サイズの比率を計算
            screen_width = self.screen_info['actual_width']
            screen_height = self.screen_info['actual_height']
            
            # 座標を実際の画面座標に変換
            if image_width > 0 and image_height > 0:
                scale_x = screen_width / image_width
                scale_y = screen_height / image_height
                
                screen_x = int(image_x * scale_x)
                screen_y = int(image_y * scale_y)
            else:
                # フォールバック: そのまま使用
                screen_x = image_x
                screen_y = image_y
            
            # 画面境界内に制限
            screen_x = max(0, min(screen_x, screen_width - 1))
            screen_y = max(0, min(screen_y, screen_height - 1))
            
            # 結果を更新
            result['coordinates'] = {
                'x': screen_x,
                'y': screen_y
            }
            
            # 変換情報を追加
            result['coordinate_conversion'] = {
                'original_x': image_x,
                'original_y': image_y,
                'image_size': f"{image_width}x{image_height}",
                'screen_size': f"{screen_width}x{screen_height}",
                'scale_x': scale_x,
                'scale_y': scale_y
            }
            
            # 代替座標も変換
            if 'alternative_coordinates' in result:
                converted_alternatives = []
                for alt in result['alternative_coordinates']:
                    if 'x' in alt and 'y' in alt:
                        alt_screen_x = int(alt['x'] * scale_x)
                        alt_screen_y = int(alt['y'] * scale_y)
                        
                        # 境界内に制限
                        alt_screen_x = max(0, min(alt_screen_x, screen_width - 1))
                        alt_screen_y = max(0, min(alt_screen_y, screen_height - 1))
                        
                        converted_alt = {
                            'x': alt_screen_x,
                            'y': alt_screen_y,
                            'description': alt.get('description', '')
                        }
                        converted_alternatives.append(converted_alt)
                
                result['alternative_coordinates'] = converted_alternatives
            
            print(f"座標変換: ({image_x}, {image_y}) -> ({screen_x}, {screen_y})")
            print(f"変換比率: x={scale_x:.3f}, y={scale_y:.3f}")
            
            return result
            
        except Exception as e:
            print(f"座標変換エラー: {e}")
            return result

    # 後方互換性のためのメソッド
    def _encode_image(self, image_path: str) -> Optional[str]:
        """画像をBase64エンコード（後方互換性）"""
        return self._encode_image_to_base64(image_path)
    
    def _get_image_size(self, image_path: str) -> tuple:
        """画像のサイズを取得（後方互換性）"""
        return self._get_image_dimensions(image_path)


# テスト用のメイン関数
if __name__ == "__main__":
    import sys
    
    # テスト実行
    ai_module = AIModuleImproved()
    
    print("座標精度改善版AI解析モジュールのテストを開始します")
    print(f"画面情報: {ai_module.screen_info}")
    
    if ai_module.client:
        print("✅ OpenAIクライアント: 利用可能")
    else:
        print("❌ OpenAIクライアント: 利用不可")
        print("   OPENAI_API_KEY環境変数を設定してください")
    
    # 座標変換のテスト
    test_result = {
        'answer': 'テスト回答',
        'coordinates': {'x': 960, 'y': 540},
        'confidence': 'high',
        'element_description': 'テスト要素'
    }
    
    converted = ai_module._convert_coordinates_to_screen(test_result, 1920, 1080)
    print(f"座標変換テスト: {converted}")
    
    print("テスト完了")
