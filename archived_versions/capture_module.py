#!/usr/bin/env python3
"""
画面キャプチャモジュール
"""

import os
import time
from datetime import datetime
from typing import Callable, Optional
from PIL import ImageGrab
from pynput import keyboard


class CaptureModule:
    """画面キャプチャとホットキー監視を担当するモジュール"""
    
    def __init__(self, callback: Callable[[str], None]):
        """
        初期化
        
        Args:
            callback: スクリーンショット撮影時に呼び出されるコールバック関数
        """
        self.callback = callback
        self.listener: Optional[keyboard.GlobalHotKeys] = None
        self.screenshots_dir = "/tmp/pc_assistant_screenshots"
        
        # スクリーンショット保存ディレクトリを作成
        os.makedirs(self.screenshots_dir, exist_ok=True)
    
    def start(self):
        """ホットキー監視を開始"""
        try:
            # Ctrl+Alt+S のホットキーを設定
            hotkeys = {
                '<ctrl>+<alt>+s': self.take_screenshot
            }
            
            self.listener = keyboard.GlobalHotKeys(hotkeys)
            self.listener.start()
            
            print("ホットキー監視を開始しました (Ctrl+Alt+S)")
            
        except Exception as e:
            print(f"ホットキー監視の開始に失敗しました: {e}")
    
    def stop(self):
        """ホットキー監視を停止"""
        if self.listener:
            self.listener.stop()
            self.listener = None
            print("ホットキー監視を停止しました")
    
    def take_screenshot(self):
        """スクリーンショットを撮影"""
        try:
            print("スクリーンショットを撮影中...")
            
            # 現在時刻でファイル名を生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            
            # スクリーンショットを撮影
            screenshot = ImageGrab.grab()
            screenshot.save(filepath)
            
            print(f"スクリーンショットを保存しました: {filepath}")
            
            # コールバックを呼び出し
            if self.callback:
                self.callback(filepath)
                
        except Exception as e:
            print(f"スクリーンショット撮影エラー: {e}")
    
    def take_screenshot_region(self, x1: int, y1: int, x2: int, y2: int) -> str:
        """
        指定された領域のスクリーンショットを撮影
        
        Args:
            x1, y1: 左上座標
            x2, y2: 右下座標
            
        Returns:
            撮影されたスクリーンショットのファイルパス
        """
        try:
            # 現在時刻でファイル名を生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_region_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            
            # 指定領域のスクリーンショットを撮影
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            screenshot.save(filepath)
            
            print(f"領域スクリーンショットを保存しました: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"領域スクリーンショット撮影エラー: {e}")
            return ""
    
    def cleanup_old_screenshots(self, max_age_hours: int = 24):
        """
        古いスクリーンショットファイルを削除
        
        Args:
            max_age_hours: 保持する最大時間（時間）
        """
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for filename in os.listdir(self.screenshots_dir):
                filepath = os.path.join(self.screenshots_dir, filename)
                
                if os.path.isfile(filepath):
                    file_age = current_time - os.path.getmtime(filepath)
                    
                    if file_age > max_age_seconds:
                        os.remove(filepath)
                        print(f"古いスクリーンショットを削除しました: {filename}")
                        
        except Exception as e:
            print(f"スクリーンショット削除エラー: {e}")


# テスト用のメイン関数
if __name__ == "__main__":
    def test_callback(filepath):
        print(f"テスト: スクリーンショットが撮影されました - {filepath}")
    
    # テスト実行
    capture = CaptureModule(test_callback)
    capture.start()
    
    print("Ctrl+Alt+S を押してスクリーンショットをテストしてください")
    print("Ctrl+C で終了します")
    
    try:
        # メインスレッドを維持
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nテストを終了します")
        capture.stop()
