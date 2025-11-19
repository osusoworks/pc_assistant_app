#!/usr/bin/env python3
"""
PC操作支援アプリケーション - 最終版実行スクリプト
"""

import os
import sys
import signal
from main_controller_final import MainControllerFinal


def setup_environment():
    """環境設定を確認"""
    print("環境設定を確認中...")
    
    # OpenAI APIキーの確認
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  警告: OPENAI_API_KEY環境変数が設定されていません")
        print("   AI解析機能を使用するには、以下のコマンドで設定してください:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print()
        print("   APIキーなしでも基本機能（スクリーンショット撮影）は利用できます。")
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
        from PIL import ImageGrab
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


def print_usage_instructions():
    """使用方法を表示"""
    print()
    print("=" * 60)
    print("🤖 PC操作支援アプリケーション")
    print("=" * 60)
    print()
    print("📋 使用方法:")
    print("  1. 📷 スクリーンショット撮影")
    print("     - UIの「📷 スクリーンショット撮影」ボタンをクリック")
    print("     - または Ctrl+Alt+S（利用可能な場合）")
    print()
    print("  2. ❓ 質問入力")
    print("     - テキストボックスに質問を入力")
    print("     - または 🎤 音声入力ボタン（利用可能な場合）")
    print()
    print("  3. 🤖 AI回答")
    print("     - AIが画面を解析して回答を表示")
    print("     - 必要に応じて画面上に赤い矢印で操作箇所を指示")
    print()
    print("💡 質問例:")
    print("  - 'このボタンは何をするものですか？'")
    print("  - '次に何をすればいいですか？'")
    print("  - 'エラーメッセージの意味を教えてください'")
    print("  - 'この設定をどこで変更できますか？'")
    print()
    print("🔧 機能状態:")
    print("  - ホットキー: 環境により利用可否が決まります")
    print("  - 音声認識: マイクロフォンが必要です")
    print("  - AI解析: OpenAI APIキーが必要です")
    print()
    print("🚪 終了方法:")
    print("  - UIの「終了」ボタンをクリック")
    print("  - または Ctrl+C")
    print()


def main():
    """メイン関数"""
    # 使用方法を表示
    print_usage_instructions()
    
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
        print("🚀 アプリケーションを起動中...")
        
        # メインコントローラーを作成
        controller = MainControllerFinal()
        
        print("✅ 初期化完了")
        print()
        print("📱 UIウィンドウが表示されます...")
        
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
        print("  4. README.mdのトラブルシューティング章を参照")
    finally:
        print("🔄 アプリケーションを終了しています...")
        if 'controller' in locals():
            controller.stop()
        print("✅ 終了しました")


if __name__ == "__main__":
    main()
