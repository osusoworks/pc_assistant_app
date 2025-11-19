#!/usr/bin/env python3
"""
PC操作支援アプリケーション - 実行スクリプト
"""

import os
import sys
import signal
from main_controller import MainController


def setup_environment():
    """環境設定を確認"""
    # OpenAI APIキーの確認
    if not os.getenv('OPENAI_API_KEY'):
        print("エラー: OPENAI_API_KEY環境変数が設定されていません")
        print("以下のコマンドで設定してください:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    # 必要なディレクトリを作成
    temp_dir = "/tmp/pc_assistant_screenshots"
    os.makedirs(temp_dir, exist_ok=True)
    
    return True


def signal_handler(signum, frame):
    """シグナルハンドラ（Ctrl+C対応）"""
    print("\nアプリケーションを終了します...")
    sys.exit(0)


def main():
    """メイン関数"""
    print("=" * 50)
    print("PC操作支援アプリケーション")
    print("=" * 50)
    
    # 環境設定を確認
    if not setup_environment():
        sys.exit(1)
    
    # シグナルハンドラを設定
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        print("アプリケーションを初期化中...")
        
        # メインコントローラーを作成
        controller = MainController()
        
        print("アプリケーションを開始します...")
        print()
        print("使用方法:")
        print("1. Ctrl+Alt+S でスクリーンショットを撮影")
        print("2. 音声またはテキストで質問を入力")
        print("3. AIが画面を解析して回答・操作指示を表示")
        print()
        print("終了するには、UIの「終了」ボタンを押すか、Ctrl+C を押してください")
        print()
        
        # アプリケーションを開始
        controller.start()
        
        # UIのメインループを実行
        controller.ui_module.run()
        
    except KeyboardInterrupt:
        print("\nユーザーによって中断されました")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("アプリケーションを終了しています...")
        if 'controller' in locals():
            controller.stop()
        print("終了しました")


if __name__ == "__main__":
    main()
