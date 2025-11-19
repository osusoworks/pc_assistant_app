#!/usr/bin/env python3
"""
PC操作支援アプリケーション - UI非表示対応版実行スクリプト
スクリーンショット撮影時にアプリUIを自動的に非表示にする
"""

import os
import sys
import signal
from main_controller_final_ui_hide import MainControllerFinalUIHide


def setup_environment():
    """環境設定を確認"""
    print("UI非表示対応版環境設定を確認中...")
    
    # OpenAI APIキーの確認
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  警告: OPENAI_API_KEY環境変数が設定されていません")
        print("   AI解析機能を使用するには、以下のコマンドで設定してください:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print()
        print("   APIキーなしでも基本機能（UI非表示スクリーンショット撮影）は利用できます。")
    else:
        print("✅ OpenAI APIキーが設定されています")
    
    # 必要なディレクトリを作成
    temp_dir = "/tmp/pc_assistant_screenshots"
    os.makedirs(temp_dir, exist_ok=True)
    print(f"✅ スクリーンショット保存ディレクトリ: {temp_dir}")
    
    # 依存関係の確認
    missing_modules = []
    
    try:
        import tkinter
        print("✅ tkinter: 利用可能")
    except ImportError:
        missing_modules.append("python3-tk")
    
    try:
        from PIL import ImageGrab, Image
        print("✅ PIL (Pillow): 利用可能")
    except ImportError:
        missing_modules.append("pillow")
    
    try:
        import speech_recognition
        print("✅ SpeechRecognition: 利用可能")
    except ImportError:
        missing_modules.append("speechrecognition")
    
    try:
        import pyaudio
        print("✅ PyAudio: 利用可能")
    except ImportError:
        missing_modules.append("pyaudio")
    
    try:
        import openai
        print("✅ OpenAI: 利用可能")
    except ImportError:
        missing_modules.append("openai")
    
    try:
        from pynput import keyboard
        print("✅ pynput: 利用可能")
    except ImportError:
        print("⚠️  pynput: 利用不可（ホットキー機能が制限されます）")
    
    if missing_modules:
        print(f"❌ 不足しているモジュール: {', '.join(missing_modules)}")
        print("   以下のコマンドでインストールしてください:")
        print(f"   pip3 install {' '.join(missing_modules)}")
        return False
    
    return True


def signal_handler(signum, frame):
    """シグナルハンドラ（Ctrl+C対応）"""
    print("\\nアプリケーションを終了します...")
    sys.exit(0)


def print_ui_hide_usage_instructions():
    """UI非表示対応版使用方法を表示"""
    print()
    print("=" * 80)
    print("🎯 PC操作支援アプリケーション（UI非表示対応版）")
    print("=" * 80)
    print()
    print("🆕 UI非表示機能:")
    print("  ✨ スクリーンショット撮影時にアプリUIを自動的に非表示")
    print("  🖼️  純粋なPC操作画面のみをキャプチャ")
    print("  🎯 AIの解析精度が大幅向上")
    print("  🔄 撮影後にUIを自動復帰")
    print()
    print("❌ 解決された問題:")
    print("  - アプリのUIが写り込んでしまう問題")
    print("  - AIがアプリUIを誤認識する問題")
    print("  - 本来の操作対象が隠れてしまう問題")
    print("  - 画面が煩雑になる問題")
    print()
    print("📋 使用方法:")
    print("  1. ❓ 質問入力")
    print("     - テキストボックスに質問を入力")
    print("     - 「🚀 質問する（UI自動非表示）」ボタンをクリック")
    print("     - アプリUIが自動的に非表示になります")
    print("     - 純粋なPC操作画面をスクリーンショット撮影")
    print("     - UIが自動的に再表示されます")
    print()
    print("  2. 📷 手動スクリーンショット")
    print("     - 「📷 手動スクリーンショット（UI非表示）」ボタンをクリック")
    print("     - または Ctrl+Alt+S（利用可能な場合）")
    print("     - 同様にUI非表示で撮影")
    print()
    print("  3. 🤖 強化されたAI解析")
    print("     - 純粋なPC操作画面を解析")
    print("     - UIの写り込みによる誤認識を排除")
    print("     - より正確な座標と操作指示を提供")
    print()
    print("🎯 UI非表示機能の動作:")
    print("  1. 撮影開始 → アプリUIを一時的に非表示")
    print("  2. 画面キャプチャ → 純粋なPC操作画面のみ撮影")
    print("  3. 撮影完了 → アプリUIを自動復帰")
    print("  4. AI解析 → クリーンな画面で高精度解析")
    print()
    print("💡 質問例:")
    print("  - 'この青いボタンをクリックしたいです'")
    print("  - '保存メニューはどこにありますか？'")
    print("  - 'エラーダイアログを閉じるにはどうすればいいですか？'")
    print("  - 'ファイルを開く方法を教えてください'")
    print("  - '設定画面に移動したいです'")
    print()
    print("✅ 改善された点:")
    print("  - UI写り込み: 完全に排除")
    print("  - 解析精度: 大幅向上")
    print("  - 座標精度: より正確")
    print("  - ユーザビリティ: 自動化で簡単")
    print()
    print("🔧 機能状態:")
    print("  - UI非表示機能: 有効")
    print("  - 自動スクリーンショット: デフォルトで有効")
    print("  - 改良版オーバーレイ: 有効")
    print("  - 座標精度向上: 有効")
    print("  - 信頼度評価: 有効")
    print("  - ホットキー: 環境により利用可否が決まります")
    print("  - 音声認識: マイクロフォンが必要です")
    print("  - AI解析: OpenAI APIキーが必要です")
    print()
    print("🚪 終了方法:")
    print("  - UIの「❌ 終了」ボタンをクリック")
    print("  - または Ctrl+C")
    print()


def main():
    """メイン関数"""
    # 使用方法を表示
    print_ui_hide_usage_instructions()
    
    # 環境設定を確認
    if not setup_environment():
        print()
        print("❌ 環境設定に問題があります。上記の指示に従って修正してください。")
        sys.exit(1)
    
    # シグナルハンドラを設定
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        print()
        print("🚀 UI非表示対応版アプリケーションを起動中...")
        print("   🎯 スクリーンショット時UI自動非表示機能")
        print("   🖼️  純粋なPC操作画面キャプチャ")
        print("   ✨ 改良されたオーバーレイシステム")
        print("   🎯 座標精度向上機能")
        
        # メインコントローラーを作成
        controller = MainControllerFinalUIHide()
        
        print("✅ UI非表示対応版初期化完了")
        print()
        print("📱 UIウィンドウが表示されます...")
        print("💡 質問を入力すると自動的にUIが非表示になり、")
        print("   純粋なPC操作画面をスクリーンショット撮影します")
        print("🎯 AIはクリーンな画面を解析し、より正確な操作指示を提供します")
        
        # アプリケーションを開始
        controller.start()
        
        # UIのメインループを実行
        controller.ui_module.run()
        
    except KeyboardInterrupt:
        print("\\n👋 ユーザーによって中断されました")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("🔧 トラブルシューティング:")
        print("  1. 依存関係が正しくインストールされているか確認")
        print("  2. OpenAI APIキーが正しく設定されているか確認")
        print("  3. ネットワーク接続を確認")
        print("  4. 画面解像度とディスプレイ設定を確認")
        print("  5. ウィンドウマネージャーの設定を確認")
        print("  6. README.mdのトラブルシューティング章を参照")
    finally:
        print("🔄 UI非表示対応版アプリケーションを終了しています...")
        if 'controller' in locals():
            controller.stop()
        print("✅ 終了しました")


if __name__ == "__main__":
    main()
