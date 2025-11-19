"""
OCRテキストマッチングモジュール
OCRでテキストを抽出し、AIでマッチングして座標を取得
"""

import json
from typing import Dict, List, Optional
from PIL import Image


class OCRTextMatchingModule:
    """OCR方式で座標を検出するモジュール"""
    
    def __init__(self, ai_module=None):
        """
        初期化
        
        Args:
            ai_module: AI解析モジュール（AIModuleImproved）
        """
        self.ai_module = ai_module
    
    def detect(self, screenshot_path: str, question: str) -> Optional[Dict]:
        """
        OCR方式で座標を検出
        
        Args:
            screenshot_path: スクリーンショットのパス
            question: ユーザーの質問
        
        Returns:
            {
                'x': int,  # 座標X
                'y': int,  # 座標Y
                'confidence': str,  # 信頼度
                'matched_text': str,  # マッチしたテキスト
                'ocr_confidence': float,  # OCR信頼度
                'method': str  # 使用した方式
            }
        """
        print("=== OCR方式で座標を検出 ===")
        
        # OCRでテキストを抽出
        text_elements = self._extract_text_with_ocr(screenshot_path)
        
        if not text_elements:
            print("OCRでテキストが検出されませんでした")
            return None
        
        print(f"OCRで{len(text_elements)}個のテキスト要素を検出")
        
        # AIにテキストを特定させる
        matched_element = self._match_text_with_ai(text_elements, question)
        
        if not matched_element:
            print("マッチするテキストが見つかりませんでした")
            return None
        
        print(f"マッチしたテキスト: '{matched_element['text']}'")
        print(f"OCR信頼度: {matched_element['confidence']}")
        
        # テキストの中心座標を計算
        center_x = matched_element['x'] + matched_element['width'] // 2
        center_y = matched_element['y'] + matched_element['height'] // 2
        
        print(f"テキスト座標: ({center_x}, {center_y})")
        
        return {
            'x': center_x,
            'y': center_y,
            'confidence': self._calculate_confidence(matched_element),
            'matched_text': matched_element['text'],
            'ocr_confidence': matched_element['confidence'],
            'method': 'ocr_text_matching'
        }
    
    def _extract_text_with_ocr(self, screenshot_path: str) -> List[Dict]:
        """
        OCRでテキストを抽出
        
        Args:
            screenshot_path: スクリーンショットのパス
        
        Returns:
            テキスト要素のリスト
            [
                {
                    'text': str,
                    'x': int,
                    'y': int,
                    'width': int,
                    'height': int,
                    'confidence': float
                },
                ...
            ]
        """
        try:
            import pytesseract
            
            image = Image.open(screenshot_path)
            
            # 日本語と英語の両方を認識
            # Tesseractがインストールされていない場合はエラー
            try:
                ocr_data = pytesseract.image_to_data(
                    image,
                    lang='jpn+eng',
                    output_type=pytesseract.Output.DICT
                )
            except pytesseract.TesseractNotFoundError:
                print("Tesseractがインストールされていません。英語のみで認識します。")
                ocr_data = pytesseract.image_to_data(
                    image,
                    output_type=pytesseract.Output.DICT
                )
            
            # テキスト要素のリストを作成
            text_elements = []
            for i in range(len(ocr_data['text'])):
                text = ocr_data['text'][i].strip()
                confidence = ocr_data['conf'][i]
                
                # 信頼度30以上のテキストのみを抽出
                if text and confidence > 30:
                    text_elements.append({
                        'text': text,
                        'x': ocr_data['left'][i],
                        'y': ocr_data['top'][i],
                        'width': ocr_data['width'][i],
                        'height': ocr_data['height'][i],
                        'confidence': confidence
                    })
            
            return text_elements
        
        except ImportError:
            print("pytesseractがインストールされていません")
            return []
        
        except Exception as e:
            print(f"OCRエラー: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _match_text_with_ai(self, text_elements: List[Dict], question: str) -> Optional[Dict]:
        """
        AIでテキストをマッチング
        
        Args:
            text_elements: テキスト要素のリスト
            question: ユーザーの質問
        
        Returns:
            マッチしたテキスト要素
        """
        if not self.ai_module:
            print("AI解析モジュールが設定されていません")
            return None
        
        # テキスト要素のリストを整形
        text_list = []
        for i, elem in enumerate(text_elements):
            text_list.append(
                f"{i}: '{elem['text']}' (位置: {elem['x']}, {elem['y']}, 信頼度: {elem['confidence']:.1f})"
            )
        
        # テキストリストが長すぎる場合は、上位100個に制限
        if len(text_list) > 100:
            print(f"テキスト要素が多すぎるため、上位100個に制限します")
            text_elements = text_elements[:100]
            text_list = text_list[:100]
        
        prompt = f"""
以下のテキスト要素リストから、ユーザーの質問に最も関連するテキストを特定してください。

テキスト要素リスト:
{chr(10).join(text_list)}

ユーザーの質問: {question}

以下のJSON形式で回答してください：
{{
    "element_index": 該当するテキストのインデックス（整数）,
    "confidence": "high|medium|low",
    "reason": "選択理由"
}}

重要:
- element_indexは必ず整数で返してください
- リストにあるインデックス（0から{len(text_elements)-1}）の範囲内で返してください
"""
        
        # AIで解析
        try:
            # AIモジュールに専用メソッドがない場合は、通常のanalyze_screenshotを使用
            # ただし、画像ではなくテキストベースの解析なので、プロンプトのみで処理
            
            # 一時的な解決策: OpenAI APIを直接呼び出し
            import os
            from openai import OpenAI
            
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            if result and 'element_index' in result:
                index = result['element_index']
                
                if 0 <= index < len(text_elements):
                    matched_element = text_elements[index].copy()
                    matched_element['ai_confidence'] = result['confidence']
                    matched_element['reason'] = result.get('reason', '')
                    
                    print(f"AIマッチング結果: インデックス{index}, 信頼度: {result['confidence']}")
                    print(f"理由: {result.get('reason', '')}")
                    
                    return matched_element
                else:
                    print(f"AIが返したインデックスが範囲外です: {index}")
            else:
                print("AIの応答にelement_indexが含まれていません")
        
        except Exception as e:
            print(f"AIマッチングエラー: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    def _calculate_confidence(self, matched_element: Dict) -> str:
        """
        総合的な信頼度を計算
        
        Args:
            matched_element: マッチしたテキスト要素
        
        Returns:
            信頼度 ('high', 'medium', 'low')
        """
        ocr_confidence = matched_element['confidence']
        ai_confidence = matched_element.get('ai_confidence', 'medium')
        
        # OCR信頼度とAI信頼度を組み合わせて判定
        if ocr_confidence >= 80 and ai_confidence == 'high':
            return 'high'
        elif ocr_confidence >= 60 and ai_confidence in ['high', 'medium']:
            return 'medium'
        else:
            return 'low'

