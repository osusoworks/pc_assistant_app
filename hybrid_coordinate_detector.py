"""
ハイブリッド座標検出器
複数のアプローチを組み合わせて、最高精度の座標検出を実現
"""

from typing import Dict, Optional
from relative_coordinate_module import RelativeCoordinateModule
from ocr_text_matching_module import OCRTextMatchingModule
from coordinate_verification_module import CoordinateVerificationModule
from user_feedback_module import UserFeedbackModule


class HybridCoordinateDetector:
    """ハイブリッド方式で座標を検出するメインモジュール"""
    
    def __init__(self, ai_module=None):
        """
        初期化
        
        Args:
            ai_module: AI解析モジュール（AIModuleImproved）
        """
        self.ai_module = ai_module
        
        # 各モジュールを初期化
        self.relative_module = RelativeCoordinateModule(ai_module)
        self.ocr_module = OCRTextMatchingModule(ai_module)
        self.verification_module = CoordinateVerificationModule()
        self.feedback_module = UserFeedbackModule()
        
        print("✅ ハイブリッド座標検出器を初期化しました")
    
    def detect_coordinates(self, screenshot_path: str, question: str) -> Optional[Dict]:
        """
        ハイブリッド方式で座標を検出
        
        Args:
            screenshot_path: スクリーンショットのパス
            question: ユーザーの質問
        
        Returns:
            {
                'x': int,  # 座標X
                'y': int,  # 座標Y
                'confidence': str,  # 信頼度
                'method': str,  # 使用した方式
                'verified': bool  # 検証済みかどうか
            }
        """
        print("\n" + "="*60)
        print("🎯 ハイブリッド座標検出を開始")
        print("="*60)
        
        # ステップ1: 要素タイプ判定
        element_type = self._determine_element_type(question)
        print(f"要素タイプ: {element_type}")
        
        # ステップ2: 座標取得
        result = None
        
        if element_type == 'text':
            # テキスト要素の場合は、OCR方式を試す
            print("\n📝 OCR方式で座標を検出します")
            result = self.ocr_module.detect(screenshot_path, question)
            
            if not result:
                print("OCR方式で検出できませんでした。相対座標方式にフォールバックします")
                result = self.relative_module.detect(screenshot_path, question)
        else:
            # 非テキスト要素の場合は、相対座標方式を使用
            print("\n🖼️ 相対座標方式で座標を検出します")
            result = self.relative_module.detect(screenshot_path, question)
        
        if not result:
            print("❌ 座標の検出に失敗しました")
            return None
        
        print(f"\n✅ 座標を検出: ({result['x']}, {result['y']})")
        print(f"方式: {result.get('method', 'unknown')}")
        print(f"信頼度: {result.get('confidence', 'unknown')}")
        
        # ステップ3: 検証（信頼度が低い・中の場合）
        if result['confidence'] in ['low', 'medium']:
            print("\n🔍 信頼度が低いため、マルチステップ検証を実行します")
            result = self.verification_module.verify(screenshot_path, result, question)
        else:
            print("\n✅ 信頼度が高いため、検証をスキップします")
            result['verified'] = True
        
        # ステップ4: ユーザーフィードバック（将来的な機能）
        # 現在は自動的にフィードバックデータを保存
        result = self.feedback_module.get_user_confirmation(result)
        
        print("\n" + "="*60)
        print(f"🎯 最終座標: ({result['x']}, {result['y']})")
        print(f"信頼度: {result['confidence']}")
        print(f"検証済み: {result.get('verified', False)}")
        print("="*60 + "\n")
        
        return result
    
    def _determine_element_type(self, question: str) -> str:
        """
        要素タイプを判定
        
        Args:
            question: ユーザーの質問
        
        Returns:
            要素タイプ ('text', 'icon', 'other')
        """
        # キーワードベースの簡易判定
        text_keywords = [
            'ボタン', 'メニュー', 'リンク', 'テキスト', '項目', 
            'タブ', 'ラベル', '文字', '名前', 'タイトル',
            'button', 'menu', 'link', 'text', 'label'
        ]
        
        icon_keywords = [
            'アイコン', '画像', 'ロゴ', 'マーク', 'シンボル',
            'icon', 'image', 'logo', 'symbol'
        ]
        
        question_lower = question.lower()
        
        # テキストキーワードをチェック
        for keyword in text_keywords:
            if keyword in question_lower:
                return 'text'
        
        # アイコンキーワードをチェック
        for keyword in icon_keywords:
            if keyword in question_lower:
                return 'icon'
        
        # デフォルトは非テキスト要素として扱う
        # （相対座標方式の方が汎用性が高いため）
        return 'other'
    
    def get_statistics(self) -> Dict:
        """
        統計情報を取得
        
        Returns:
            統計情報
        """
        return self.feedback_module.get_feedback_statistics()

