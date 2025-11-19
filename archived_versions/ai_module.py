#!/usr/bin/env python3
"""
AI解析モジュール
"""

import os
import base64
import json
from typing import Dict, Any, Optional
from openai import OpenAI


class AIModule:
    """AI解析を担当するモジュール"""
    
    def __init__(self):
        """初期化"""
        # OpenAI APIキーを環境変数から取得
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY環境変数が設定されていません")
        
        # OpenAIクライアントを初期化
        self.client = OpenAI()
        
        print("AI解析モジュールが初期化されました")
    
    def analyze_screenshot(self, image_path: str, question: str) -> Optional[Dict[str, Any]]:
        """
        スクリーンショットを解析して質問に回答
        
        Args:
            image_path: スクリーンショットのファイルパス
            question: ユーザーの質問
            
        Returns:
            解析結果の辞書（answer, coordinatesを含む）
        """
        try:
            # 画像をBase64エンコード
            image_base64 = self._encode_image(image_path)
            if not image_base64:
                return None
            
            # プロンプトを構築
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(question)
            
            # OpenAI APIを呼び出し
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # レスポンスを解析
            result = self._parse_response(response)
            return result
            
        except Exception as e:
            print(f"AI解析エラー: {e}")
            return None
    
    def _encode_image(self, image_path: str) -> Optional[str]:
        """画像をBase64エンコード"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"画像エンコードエラー: {e}")
            return None
    
    def _build_system_prompt(self) -> str:
        """システムプロンプトを構築"""
        return """あなたはPC操作支援AIアシスタントです。ユーザーが提供するスクリーンショットを分析し、質問に対して適切な回答を提供してください。

以下の形式でJSONレスポンスを返してください：

{
    "answer": "ユーザーの質問に対する詳細で分かりやすい回答",
    "coordinates": {
        "x": クリックすべき場所のX座標（ピクセル）,
        "y": クリックすべき場所のY座標（ピクセル）
    }
}

重要な指示：
1. 回答は日本語で、初心者にも分かりやすく説明してください
2. 操作手順がある場合は、ステップバイステップで説明してください
3. クリックすべき場所がある場合は、正確な座標を提供してください
4. 座標が特定できない場合は、coordinatesをnullにしてください
5. 画面上の要素（ボタン、メニュー、アイコンなど）を正確に識別してください
6. セキュリティに関わる操作の場合は、注意喚起を含めてください"""
    
    def _build_user_prompt(self, question: str) -> str:
        """ユーザープロンプトを構築"""
        return f"""スクリーンショットを分析して、以下の質問に回答してください：

質問: {question}

画面上の要素を詳しく分析し、質問に対する適切な回答と、必要に応じて操作すべき場所の座標を提供してください。"""
    
    def _parse_response(self, response) -> Optional[Dict[str, Any]]:
        """APIレスポンスを解析"""
        try:
            content = response.choices[0].message.content
            
            # JSONレスポンスを解析
            if content.startswith('```json'):
                # マークダウンのコードブロックを除去
                content = content.replace('```json', '').replace('```', '').strip()
            
            result = json.loads(content)
            
            # 必要なフィールドを確認
            if 'answer' not in result:
                result['answer'] = content  # JSONでない場合はそのまま回答として使用
            
            return result
            
        except json.JSONDecodeError:
            # JSONでない場合は、テキストをそのまま回答として使用
            content = response.choices[0].message.content
            return {
                'answer': content,
                'coordinates': None
            }
        except Exception as e:
            print(f"レスポンス解析エラー: {e}")
            return None
    
    def analyze_with_gemini(self, image_path: str, question: str) -> Optional[Dict[str, Any]]:
        """
        Gemini APIを使用した解析（将来の拡張用）
        
        Args:
            image_path: スクリーンショットのファイルパス
            question: ユーザーの質問
            
        Returns:
            解析結果の辞書
        """
        # TODO: Gemini APIの実装
        print("Gemini API解析は未実装です")
        return None
    
    def get_available_models(self) -> list:
        """利用可能なモデル一覧を取得"""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data if 'gpt-4' in model.id]
        except Exception as e:
            print(f"モデル一覧取得エラー: {e}")
            return []


# テスト用のメイン関数
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("使用方法: python ai_module.py <画像パス> <質問>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    question = sys.argv[2]
    
    # テスト実行
    try:
        ai = AIModule()
        result = ai.analyze_screenshot(image_path, question)
        
        if result:
            print("=== AI解析結果 ===")
            print(f"回答: {result.get('answer', 'N/A')}")
            
            coordinates = result.get('coordinates')
            if coordinates:
                print(f"座標: ({coordinates['x']}, {coordinates['y']})")
            else:
                print("座標: なし")
        else:
            print("解析に失敗しました")
            
    except Exception as e:
        print(f"テストエラー: {e}")
        sys.exit(1)
