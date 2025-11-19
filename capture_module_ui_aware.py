#!/usr/bin/env python3
"""
画面キャプチャモジュール（UI非表示対応版）
スクリーンショット撮影時にアプリUIを一時的に非表示にする
"""

import os
import time
import threading
from datetime import datetime
from typing import Optional, Callable
from PIL import ImageGrab


class CaptureModuleUIAware:
    """画面キャプチャを担当するモジュール（UI非表示対応版）"""
    
    def __init__(self, screenshot_callback: Callable[[str], None]):
        """
        初期化
        
        Args:
            screenshot_callback: スクリーンショット撮影完了時のコールバック
        """
        self.screenshot_callback = screenshot_callback
        self.hotkey_listener = None
        self.running = False
        self.ui_hide_callback = None
        self.ui_show_callback = None
        
        # スクリーンショット保存ディレクトリ
        self.screenshot_dir = "/tmp/pc_assistant_screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        print("UI非表示対応版キャプチャモジュールが初期化されました")
    
    def set_ui_callbacks(self, hide_callback: Callable[[], None], show_callback: Callable[[], None]):
        """
        UI表示/非表示のコールバックを設定
        
        Args:
            hide_callback: UI非表示のコールバック
            show_callback: UI表示のコールバック
        """
        self.ui_hide_callback = hide_callback
        self.ui_show_callback = show_callback
        print("UI表示制御コールバックが設定されました")
    
    def start(self):
        """キャプチャモジュールを開始（ホットキー監視）"""
        self.running = True
        
        try:
            from pynput import keyboard
            
            def on_hotkey():
                """ホットキーが押された時の処理"""
                if self.running:
                    print("ホットキー（Ctrl+Alt+S）が押されました")
                    self.take_screenshot_with_ui_hide()
            
            # ホットキーを設定
            self.hotkey_listener = keyboard.GlobalHotKeys({
                '<ctrl>+<alt>+s': on_hotkey
            })
            
            self.hotkey_listener.start()
            print("ホットキー監視を開始しました（Ctrl+Alt+S）")
            
        except ImportError:
            print("pynputが利用できません。ホットキー機能は無効です。")
        except Exception as e:
            print(f"ホットキー設定エラー: {e}")
    
    def stop(self):
        """キャプチャモジュールを停止"""
        self.running = False
        
        if self.hotkey_listener:
            try:
                self.hotkey_listener.stop()
                print("ホットキー監視を停止しました")
            except Exception as e:
                print(f"ホットキー停止エラー: {e}")
    
    def is_hotkey_available(self) -> bool:
        """ホットキー機能が利用可能かチェック"""
        try:
            from pynput import keyboard
            return True
        except ImportError:
            return False
    
    def take_screenshot_with_ui_hide(self) -> Optional[str]:
        """
        UI非表示でスクリーンショットを撮影
        
        Returns:
            撮影されたスクリーンショットのファイルパス
        """
        try:
            print("UI非表示スクリーンショット撮影を開始...")
            
            # 1. UIを非表示にする
            if self.ui_hide_callback:
                print("アプリUIを一時的に非表示にします...")
                self.ui_hide_callback()
                
                # UI非表示の完了を待つ
                time.sleep(0.5)
            
            # 2. スクリーンショットを撮影
            print("純粋なPC操作画面をキャプチャ中...")
            filepath = self._capture_screen()
            
            # 3. UIを再表示する
            if self.ui_show_callback:
                print("アプリUIを再表示します...")
                self.ui_show_callback()
            
            if filepath:
                print(f"UI非表示スクリーンショット撮影完了: {filepath}")
                
                # コールバックを呼び出し
                if self.screenshot_callback:
                    self.screenshot_callback(filepath)
                
                return filepath
            else:
                print("スクリーンショット撮影に失敗しました")
                return None
                
        except Exception as e:
            print(f"UI非表示スクリーンショット撮影エラー: {e}")
            
            # エラー時もUIを再表示
            if self.ui_show_callback:
                try:
                    self.ui_show_callback()
                except:
                    pass
            
            return None
    
    def take_screenshot(self) -> Optional[str]:
        """
        通常のスクリーンショット撮影（UI非表示なし）
        後方互換性のために残す
        
        Returns:
            撮影されたスクリーンショットのファイルパス
        """
        return self._capture_screen()
    
    def _capture_screen(self) -> Optional[str]:
        """
        実際の画面キャプチャ処理
        
        Returns:
            撮影されたスクリーンショットのファイルパス
        """
        try:
            # スクリーンショットを撮影
            screenshot = ImageGrab.grab()
            
            # ファイル名を生成（タイムスタンプ付き）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # ファイルに保存
            screenshot.save(filepath, "PNG")
            
            # ファイルサイズを確認
            file_size = os.path.getsize(filepath)
            print(f"スクリーンショット保存: {filepath} ({file_size} bytes)")
            
            return filepath
            
        except Exception as e:
            print(f"画面キャプチャエラー: {e}")
            return None
    
    def get_screen_size(self) -> tuple:
        """
        画面サイズを取得
        
        Returns:
            (width, height) のタプル
        """
        try:
            screenshot = ImageGrab.grab()
            return screenshot.size
        except Exception as e:
            print(f"画面サイズ取得エラー: {e}")
            return (1280, 1024)  # デフォルト値
    
    def cleanup_old_screenshots(self, keep_count: int = 10):
        """
        古いスクリーンショットファイルを削除
        
        Args:
            keep_count: 保持するファイル数
        """
        try:
            # スクリーンショットファイル一覧を取得
            files = []
            for filename in os.listdir(self.screenshot_dir):
                if filename.startswith("screenshot_") and filename.endswith(".png"):
                    filepath = os.path.join(self.screenshot_dir, filename)
                    files.append((filepath, os.path.getmtime(filepath)))
            
            # 作成時刻でソート（新しい順）
            files.sort(key=lambda x: x[1], reverse=True)
            
            # 古いファイルを削除
            for filepath, _ in files[keep_count:]:
                try:
                    os.remove(filepath)
                    print(f"古いスクリーンショットを削除: {filepath}")
                except Exception as e:
                    print(f"ファイル削除エラー: {e}")
                    
        except Exception as e:
            print(f"クリーンアップエラー: {e}")


# テスト用のメイン関数
if __name__ == "__main__":
    import sys
    
    def test_callback(filepath):
        print(f"テスト: スクリーンショットが撮影されました - {filepath}")
    
    def test_ui_hide():
        print("テスト: UIを非表示にしました")
    
    def test_ui_show():
        print("テスト: UIを再表示しました")
    
    # テスト実行
    capture = CaptureModuleUIAware(test_callback)
    capture.set_ui_callbacks(test_ui_hide, test_ui_show)
    
    print("UI非表示対応版キャプチャモジュールのテストを開始します")
    
    # 画面サイズをテスト
    screen_size = capture.get_screen_size()
    print(f"画面サイズ: {screen_size}")
    
    # UI非表示スクリーンショットをテスト
    print("\\nUI非表示スクリーンショットのテストを実行します...")
    filepath = capture.take_screenshot_with_ui_hide()
    
    if filepath:
        print(f"✅ テスト成功: {filepath}")
    else:
        print("❌ テスト失敗")
    
    # クリーンアップをテスト
    capture.cleanup_old_screenshots(5)
    
    print("テスト完了")
