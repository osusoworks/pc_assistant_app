#!/usr/bin/env python3
"""
SENPAI シンプル版実行ファイル
シンプルUIと改善された矢印オーバーレイ版
"""

import sys
import os
from tkinter import messagebox

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from main_controller_simple import SimpleMainController
except ImportError as e:
    print(f"❌ インポートエラー: {e}")
    print("必要なモジュールが見つかりません。")
    sys.exit(1)


def check_dependencies():
    """依存関係をチェック"""
    missing_modules = []
    
    # 必須モジュールのチェック
    required_modules = [
        'tkinter',
        'threading', 
        'time',
        'os',
        'json',
        'datetime',
        'math'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    # オプションモジュールのチェック
    optional_modules = {
        'PIL': 'Pillow (画像処理)',
        'requests': 'requests (HTTP通信)',
        'openai': 'openai (AI機能)'
    }
    
    missing_optional = []
    for module, description in optional_modules.items():
        try:
            __import__(module)
        except ImportError:
            missing_optional.append(f"{module} ({description})")
    
    # 結果表示
    if missing_modules:
        print(f"❌ 必須モジュールが不足しています: {', '.join(missing_modules)}")
        return False
    
    if missing_optional:
        print(f"⚠️  オプションモジュールが不足しています: {', '.join(missing_optional)}")
        print("   一部機能が制限される可能性があります")
    
    return True


def check_environment():
    """環境設定をチェック"""
    print("=== 環境チェック ===")
    
    # OpenAI APIキーのチェック
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ OpenAI APIキー: 設定済み")
    else:
        print("⚠️  OpenAI APIキー: 未設定")
        print("   AI機能を使用するには環境変数 OPENAI_API_KEY を設定してください")
    
    # 作業ディレクトリのチェック
    work_dir = os.path.expanduser("~/SENPAI")
    if os.path.exists(work_dir):
        print(f"✅ 作業ディレクトリ: {work_dir}")
    else:
        print(f"📁 作業ディレクトリを作成します: {work_dir}")
        try:
            os.makedirs(work_dir, exist_ok=True)
            print("✅ 作業ディレクトリ作成完了")
        except Exception as e:
            print(f"❌ 作業ディレクトリ作成失敗: {e}")
    
    # スクリーンショット保存ディレクトリのチェック
    screenshot_dir = "/tmp/pc_assistant_screenshots"
    try:
        os.makedirs(screenshot_dir, exist_ok=True)
        print(f"✅ スクリーンショットディレクトリ: {screenshot_dir}")
    except Exception as e:
        print(f"❌ スクリーンショットディレクトリ作成失敗: {e}")
    
    print()


def show_startup_info():
    """起動情報を表示"""
    print("=" * 60)
    print("🎯 SENPAI - シンプル版PC操作ガイド")
    print("=" * 60)
    print()
    print("📋 特徴:")
    print("  ✨ シンプルで洗練されたUI（添付画像準拠）")
    print("  🏹 影なしクリーン矢印（改善された先端）")
    print("  📚 お気に入り機能（質問・回答の保存）")
    print("  🤖 AI解析（OpenAI GPT-4）")
    print("  📷 UI非表示スクリーンショット")
    print("  🎤 音声認識対応")
    print()
    print("🎮 操作方法:")
    print("  1. 質問を入力して「質問する」ボタンをクリック")
    print("  2. AI解析結果と矢印が表示されます")
    print("  3. 有用な回答は「⭐ お気に入り保存」で保存")
    print("  4. 「📚 お気に入り一覧」で過去の回答を検索")
    print()
    print("⌨️  キーボードショートカット:")
    print("  Ctrl+Enter: 質問実行")
    print("  Escape: クリア")
    print("  Ctrl+Q: 終了")
    print()
    print("🔧 設定:")
    print(f"  OpenAI APIキー: {'✅ 設定済み' if os.getenv('OPENAI_API_KEY') else '❌ 未設定'}")
    print(f"  作業ディレクトリ: {os.path.expanduser('~/SENPAI')}")
    print()


def main():
    """メイン関数"""
    try:
        # 起動情報表示
        show_startup_info()
        
        # 依存関係チェック
        if not check_dependencies():
            print("❌ 依存関係の問題により起動できません")
            input("Enterキーを押して終了...")
            return 1
        
        # 環境チェック
        check_environment()
        
        # APIキー未設定の警告
        if not os.getenv('OPENAI_API_KEY'):
            print("⚠️  注意: OpenAI APIキーが設定されていません")
            print("   AI機能を使用するには、以下のコマンドでAPIキーを設定してください:")
            print()
            print("   Windows:")
            print("   set OPENAI_API_KEY=your_api_key_here")
            print()
            print("   Linux/Mac:")
            print("   export OPENAI_API_KEY=your_api_key_here")
            print()
            
            # 続行確認
            try:
                response = input("APIキー未設定でも続行しますか？ (y/N): ").strip().lower()
                if response not in ['y', 'yes']:
                    print("アプリケーションを終了します")
                    return 0
            except KeyboardInterrupt:
                print("\\nアプリケーションを終了します")
                return 0
        
        print("🚀 アプリケーションを起動中...")
        print()
        
        # メインコントローラーを作成・実行
        controller = SimpleMainController()
        controller.run()
        
        return 0
        
    except KeyboardInterrupt:
        print("\\n⏹️  ユーザーによって中断されました")
        return 0
    except Exception as e:
        print(f"❌ 予期しないエラーが発生しました: {e}")
        
        # エラーの詳細をファイルに保存
        try:
            import traceback
            error_file = os.path.expanduser("~/SENPAI/error_log.txt")
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write(f"SENPAI エラーログ\\n")
                f.write(f"発生時刻: {time.strftime('%Y-%m-%d %H:%M:%S')}\\n")
                f.write(f"エラー: {e}\\n\\n")
                f.write("詳細:\\n")
                f.write(traceback.format_exc())
            
            print(f"📝 エラーログを保存しました: {error_file}")
        except:
            pass
        
        # GUI環境でエラーダイアログを表示
        try:
            messagebox.showerror(
                "エラー", 
                f"アプリケーションでエラーが発生しました:\\n\\n{e}\\n\\n"
                f"詳細はエラーログを確認してください。"
            )
        except:
            pass
        
        return 1


if __name__ == "__main__":
    import time
    exit_code = main()
    
    # 終了メッセージ
    if exit_code == 0:
        print("👋 SENPAI を終了しました。お疲れさまでした！")
    else:
        print("❌ エラーにより終了しました")
        input("Enterキーを押して終了...")
    
    sys.exit(exit_code)
