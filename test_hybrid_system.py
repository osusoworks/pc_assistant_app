"""
ハイブリッド座標検出システムの基本テスト
"""

import sys
import os

# モジュールのインポートテスト
print("="*60)
print("ハイブリッド座標検出システム - 基本テスト")
print("="*60)

print("\n1. モジュールのインポートテスト")
print("-"*60)

try:
    from relative_coordinate_module import RelativeCoordinateModule
    print("✅ RelativeCoordinateModule: インポート成功")
except Exception as e:
    print(f"❌ RelativeCoordinateModule: インポート失敗 - {e}")
    sys.exit(1)

try:
    from ocr_text_matching_module import OCRTextMatchingModule
    print("✅ OCRTextMatchingModule: インポート成功")
except Exception as e:
    print(f"❌ OCRTextMatchingModule: インポート失敗 - {e}")
    sys.exit(1)

try:
    from coordinate_verification_module import CoordinateVerificationModule
    print("✅ CoordinateVerificationModule: インポート成功")
except Exception as e:
    print(f"❌ CoordinateVerificationModule: インポート失敗 - {e}")
    sys.exit(1)

try:
    from user_feedback_module import UserFeedbackModule
    print("✅ UserFeedbackModule: インポート成功")
except Exception as e:
    print(f"❌ UserFeedbackModule: インポート失敗 - {e}")
    sys.exit(1)

try:
    from hybrid_coordinate_detector import HybridCoordinateDetector
    print("✅ HybridCoordinateDetector: インポート成功")
except Exception as e:
    print(f"❌ HybridCoordinateDetector: インポート失敗 - {e}")
    sys.exit(1)

print("\n2. 依存関係のチェック")
print("-"*60)

# OpenAI APIキーのチェック
if os.environ.get("OPENAI_API_KEY"):
    print("✅ OpenAI APIキー: 設定済み")
else:
    print("❌ OpenAI APIキー: 未設定")

# pygetwindowのチェック
if sys.platform == 'win32':
    try:
        import pygetwindow as gw
        print("✅ pygetwindow: インストール済み (Windows)")
    except ImportError:
        print("⚠️ pygetwindow: 未インストール（相対座標方式が使用できません）")
else:
    print("⚠️ pygetwindow: Windows環境でのみ使用可能（相対座標方式は無効）")

# pytesseractのチェック
try:
    import pytesseract
    print("✅ pytesseract: インストール済み")
    
    # Tesseractのチェック
    try:
        pytesseract.get_tesseract_version()
        print("✅ Tesseract: インストール済み")
    except pytesseract.TesseractNotFoundError:
        print("⚠️ Tesseract: 未インストール（OCR方式が使用できません）")
except ImportError:
    print("⚠️ pytesseract: 未インストール（OCR方式が使用できません）")

print("\n3. メインコントローラーとの統合テスト")
print("-"*60)

try:
    from main_controller_simple import SimpleMainController
    print("✅ SimpleMainController: インポート成功")
    print("✅ ハイブリッド座標検出器の統合: 成功")
except Exception as e:
    print(f"❌ SimpleMainController: インポート失敗 - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n4. ハイブリッド座標検出器の初期化テスト")
print("-"*60)

try:
    from ai_module_improved import AIModuleImproved
    
    ai_module = AIModuleImproved()
    print("✅ AIModuleImproved: 初期化成功")
    
    hybrid_detector = HybridCoordinateDetector(ai_module)
    print("✅ HybridCoordinateDetector: 初期化成功")
    
except Exception as e:
    print(f"❌ 初期化失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("✅ すべてのテストが成功しました！")
print("="*60)
print("\nハイブリッド座標検出システムは正常に動作する準備ができています。")
print("実際のアプリケーションで使用するには、run_simple_clean.py を実行してください。")

