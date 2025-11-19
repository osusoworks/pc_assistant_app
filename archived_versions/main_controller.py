#!/usr/bin/env python3
"""
PC操作支援アプリケーション - メインコントローラー
"""

import os
import sys
import threading
import time
import json
from typing import Optional, Dict, Any

# 各モジュールをインポート
from capture_module import CaptureModule
from speech_module import SpeechModule
from ui_module import UIModule
from ai_module import AIModule
from overlay_module import OverlayModule


class MainController:
    """メインコントローラークラス"""
    
    def __init__(self):
        """初期化"""
        self.running = False
        self.current_screenshot = None
        
        # 各モジュールを初期化
        self.capture_module = CaptureModule(self.on_screenshot_captured)
        self.speech_module = SpeechModule(self.on_speech_recognized)
        self.ui_module = UIModule(self.on_text_question, self.on_app_close)
        self.ai_module = AIModule()
        self.overlay_module = OverlayModule()
        
        print("PC操作支援アプリケーションが初期化されました")
        print("Ctrl+Alt+S でスクリーンショットを撮影できます")
    
    def start(self):
        """アプリケーションを開始"""
        self.running = True
        
        # キャプチャモジュールを開始（ホットキー監視）
        self.capture_module.start()
        
        # 音声認識モジュールを開始
        self.speech_module.start()
        
        # UIを表示
        self.ui_module.show()
        
        print("アプリケーションが開始されました")
    
    def stop(self):
        """アプリケーションを停止"""
        self.running = False
        
        # 各モジュールを停止
        self.capture_module.stop()
        self.speech_module.stop()
        self.overlay_module.hide()
        
        print("アプリケーションが停止されました")
    
    def on_screenshot_captured(self, screenshot_path: str):
        """スクリーンショットが撮影された時のコールバック"""
        self.current_screenshot = screenshot_path
        print(f"スクリーンショットが撮影されました: {screenshot_path}")
        
        # UIに通知
        self.ui_module.set_status("スクリーンショットが撮影されました。質問をどうぞ。")
    
    def on_speech_recognized(self, text: str):
        """音声が認識された時のコールバック"""
        print(f"音声認識結果: {text}")
        
        # UIに音声認識結果を表示
        self.ui_module.set_question_text(text)
        
        # 質問を処理
        self.process_question(text)
    
    def on_text_question(self, text: str):
        """テキスト質問が入力された時のコールバック"""
        print(f"テキスト質問: {text}")
        self.process_question(text)
    
    def on_app_close(self):
        """アプリケーション終了時のコールバック"""
        self.stop()
        sys.exit(0)
    
    def process_question(self, question: str):
        """質問を処理"""
        if not self.current_screenshot:
            self.ui_module.set_answer("まず Ctrl+Alt+S でスクリーンショットを撮影してください。")
            return
        
        if not question.strip():
            self.ui_module.set_answer("質問を入力してください。")
            return
        
        # UIに処理中を表示
        self.ui_module.set_status("AI が画面を解析中...")
        
        # 別スレッドでAI解析を実行（UIをブロックしないため）
        threading.Thread(
            target=self._analyze_with_ai,
            args=(question,),
            daemon=True
        ).start()
    
    def _analyze_with_ai(self, question: str):
        """AI解析を実行（別スレッド）"""
        try:
            # AI解析を実行
            result = self.ai_module.analyze_screenshot(self.current_screenshot, question)
            
            if result:
                # 回答をUIに表示
                self.ui_module.set_answer(result.get('answer', '回答を生成できませんでした。'))
                
                # 座標情報があれば矢印を表示
                coordinates = result.get('coordinates')
                if coordinates:
                    self.overlay_module.show_arrow(coordinates['x'], coordinates['y'])
                    # 5秒後に矢印を非表示
                    threading.Timer(5.0, self.overlay_module.hide).start()
                
                self.ui_module.set_status("解析完了")
            else:
                self.ui_module.set_answer("AI解析でエラーが発生しました。")
                self.ui_module.set_status("エラー")
                
        except Exception as e:
            print(f"AI解析エラー: {e}")
            self.ui_module.set_answer(f"エラーが発生しました: {str(e)}")
            self.ui_module.set_status("エラー")


def main():
    """メイン関数"""
    try:
        # メインコントローラーを作成
        controller = MainController()
        
        # アプリケーションを開始
        controller.start()
        
        # UIのメインループを実行
        controller.ui_module.run()
        
    except KeyboardInterrupt:
        print("\nアプリケーションを終了します...")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        if 'controller' in locals():
            controller.stop()


if __name__ == "__main__":
    main()
