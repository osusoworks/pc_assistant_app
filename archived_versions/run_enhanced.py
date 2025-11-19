#!/usr/bin/env python3
"""
PC操作支援アプリケーション - 強化版実行スクリプト
改良されたオーバーレイと座標精度向上機能付き
"""

import os
import sys
import signal
from main_controller_enhanced import MainControllerEnhanced


def setup_environment():
    """環境設定を確認"""
    print("強化版環境設定を確認中...")
    
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


def print_enhanced_usage_instructions():
    """強化版使用方法を表示"""
    print()
    print("=" * 80)
    print("🚀 PC操作支援アプリケーション（強化版）")
    print("=" * 80)
    print()
    print("🆕 強化された機能:")
    print("  ✨ 改良されたシンプルな矢印デザイン")
    print("  🎯 座標精度の大幅向上")
    print("  🔍 信頼度評価システム")
    print("  📍 複数の表示モード（矢印/方向指定/ハイライト）")
    print("  🧠 強化されたAI解析プロンプト")
    print()
    print("📋 使用方法:")
    print("  1. ❓ 質問入力")
    print("     - テキストボックスに質問を入力")
    print("     - 「🚀 質問する（自動SS付き）」ボタンをクリック")
    print("     - 自動的にスクリーンショットが撮影されます")
    print()
    print("  2. 🤖 強化されたAI解析")
    print("     - 画面を詳細に解析して正確な座標を特定")
    print("     - 座標の信頼度を評価（High/Medium/Low）")
    print("     - 要素の詳細な説明を提供")
    print()
    print("  3. 🎯 改良された操作指示")
    print("     - 高信頼度: シンプルな赤い矢印で正確に指示")
    print("     - 中信頼度: 方向指定矢印で大まかな位置を指示")
    print("     - 低信頼度: ハイライト表示で範囲を指示")
    print()
    print("🎨 矢印デザインの改良:")
    print("  - 添付画像のようなシンプルで太い矢印")
    print("  - 影付きで視認性向上")
    print("  - 控えめなパルス効果")
    print("  - 白い縁取りで背景との区別を明確化")
    print()
    print("🎯 座標精度の向上:")
    print("  - 要素の中心点を正確に計算")
    print("  - 画像サイズを考慮した座標補正")
    print("  - 複数候補から最適な要素を選択")
    print("  - 信頼度に基づく表示方法の自動選択")
    print()
    print("💡 質問例:")
    print("  - 'この青いボタンをクリックしたいです'")
    print("  - '保存ボタンはどこにありますか？'")
    print("  - 'メニューを開くにはどうすればいいですか？'")
    print("  - 'このエラーを解決するには何をクリックすればいいですか？'")
    print("  - '設定画面に移動したいです'")
    print()
    print("🔧 機能状態:")
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
    print_enhanced_usage_instructions()
    
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
        print("🚀 強化版アプリケーションを起動中...")
        print("   ✨ 改良されたオーバーレイシステム")
        print("   🎯 座標精度向上機能")
        print("   🔍 信頼度評価システム")
        
        # メインコントローラーを作成
        controller = MainControllerEnhanced()
        
        print("✅ 強化版初期化完了")
        print()
        print("📱 UIウィンドウが表示されます...")
        print("💡 質問を入力すると自動的にスクリーンショットが撮影され、")
        print("   改良された矢印で正確な操作箇所を指示します")
        
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
        print("  5. README.mdのトラブルシューティング章を参照")
    finally:
        print("🔄 強化版アプリケーションを終了しています...")
        if 'controller' in locals():
            controller.stop()
        print("✅ 終了しました")


if __name__ == "__main__":
    main()
