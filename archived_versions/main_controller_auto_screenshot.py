#!/usr/bin/env python3
"""
PC操作支援アプリケーション - メインコントローラー（自動スクリーンショット版）
"""

import os
import sys
import threading
import time
import json
from typing import Optional, Dict, Any

# 改良版モジュールをインポート
from capture_module_improved import CaptureModuleImproved
from speech_module import SpeechModule
from ui_module_auto_screenshot import UIModuleAutoScreenshot
from ai_module import AIModule
from overlay_module import OverlayModule


class MainControllerAutoScreenshot:
    """メインコントローラークラス（自動スクリーンショット版）"""
    
    def __init__(self):
        """初期化"""
        self.running = False
        self.current_screenshot = None
        self.auto_screenshot_enabled = True
        
        # 各モジュールを初期化
        self.capture_module = CaptureModuleImproved(self.on_screenshot_captured)
        self.speech_module = SpeechModule(self.on_speech_recognized)
        self.ui_module = UIModuleAutoScreenshot(
            self.on_text_question, 
            self.on_app_close,
            self.on_manual_screenshot_request,
            self.on_auto_screenshot_toggle
        )
        self.ai_module = AIModule()
        self.overlay_module = OverlayModule()
        
        print("PC操作支援アプリケーション（自動スクリーンショット版）が初期化されました")
        self._check_module_availability()
    
    def _check_module_availability(self):
        """各モジュールの利用可能性をチェック"""
        # ホットキー機能の確認
        hotkey_available = self.capture_module.is_hotkey_available()
        self.ui_module.set_function_status('hotkey', hotkey_available)
        
        # 音声認識機能の確認
        speech_available = self.speech_module.microphone is not None
        self.ui_module.set_function_status('speech', speech_available)
        
        # AI機能の確認
        ai_available = os.getenv('OPENAI_API_KEY') is not None
        self.ui_module.set_function_status('ai', ai_available)
        
        # 利用可能な機能を報告
        print(f"ホットキー機能: {'利用可能' if hotkey_available else '利用不可'}")
        print(f"音声認識機能: {'利用可能' if speech_available else '利用不可'}")
        print(f"AI解析機能: {'利用可能' if ai_available else '利用不可'}")
        print(f"自動スクリーンショット: 有効")
        
        if hotkey_available:
            print("Ctrl+Alt+S でスクリーンショットを撮影できます")
        
        print("質問時に自動的にスクリーンショットを撮影します")
    
    def start(self):
        """アプリケーションを開始"""
        self.running = True
        
        # キャプチャモジュールを開始（ホットキー監視）
        self.capture_module.start()
        
        # 音声認識モジュールを開始（利用可能な場合のみ）
        if self.speech_module.microphone:
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
    
    def on_manual_screenshot_request(self):
        """手動スクリーンショット撮影が要求された時"""
        filepath = self.capture_module.take_screenshot()
        if filepath:
            self.on_screenshot_captured(filepath)
            self.ui_module.set_status("手動スクリーンショット撮影完了")
    
    def on_auto_screenshot_toggle(self, enabled: bool):
        """自動スクリーンショット機能のON/OFF切り替え"""
        self.auto_screenshot_enabled = enabled
        status = "有効" if enabled else "無効"
        print(f"自動スクリーンショット機能: {status}")
        self.ui_module.set_status(f"自動スクリーンショット: {status}")
    
    def on_screenshot_captured(self, screenshot_path: str):
        """スクリーンショットが撮影された時のコールバック"""
        self.current_screenshot = screenshot_path
        print(f"スクリーンショットが撮影されました: {screenshot_path}")
        
        # UIに通知（自動撮影の場合は控えめに）
        if hasattr(self, '_auto_screenshot_in_progress') and self._auto_screenshot_in_progress:
            # 自動撮影の場合は簡潔な通知
            pass
        else:
            # 手動撮影の場合は明確な通知
            self.ui_module.set_status("スクリーンショット撮影完了")
    
    def on_speech_recognized(self, text: str):
        """音声が認識された時のコールバック"""
        print(f"音声認識結果: {text}")
        
        # UIに音声認識結果を表示
        self.ui_module.set_question_text(text)
        
        # 質問を処理（自動スクリーンショット付き）
        self.process_question_with_auto_screenshot(text)
    
    def on_text_question(self, text: str):
        """テキスト質問が入力された時のコールバック"""
        print(f"テキスト質問: {text}")
        self.process_question_with_auto_screenshot(text)
    
    def on_app_close(self):
        """アプリケーション終了時のコールバック"""
        self.stop()
        sys.exit(0)
    
    def process_question_with_auto_screenshot(self, question: str):
        """質問を処理（自動スクリーンショット付き）"""
        if not question.strip():
            self.ui_module.set_answer("質問を入力してください。")
            return
        
        # 自動スクリーンショットが有効な場合、まずスクリーンショットを撮影
        if self.auto_screenshot_enabled:
            self.ui_module.set_status("スクリーンショット撮影中...")
            
            # 自動撮影フラグを設定
            self._auto_screenshot_in_progress = True
            
            # スクリーンショットを撮影
            filepath = self.capture_module.take_screenshot()
            
            # フラグをリセット
            self._auto_screenshot_in_progress = False
            
            if filepath:
                self.on_screenshot_captured(filepath)
                print(f"質問に対して自動スクリーンショットを撮影: {filepath}")
            else:
                self.ui_module.set_answer("スクリーンショットの撮影に失敗しました。手動で撮影してください。")
                return
        
        # 既存の質問処理を実行
        self.process_question(question)
    
    def process_question(self, question: str):
        """質問を処理"""
        if not self.current_screenshot:
            self.ui_module.set_answer("スクリーンショットが撮影されていません。\\n\\n自動スクリーンショットが無効になっている可能性があります。\\n手動で📷ボタンを押してスクリーンショットを撮影してください。")
            return
        
        # AI機能が利用できない場合
        if not os.getenv('OPENAI_API_KEY'):
            self.ui_module.set_answer("AI解析機能が利用できません。\\n\\nOpenAI APIキーが設定されていません。\\n\\n設定方法:\\nexport OPENAI_API_KEY='your-api-key-here'")
            return
        
        # UIに処理中を表示
        self.ui_module.set_status("AI が画面を解析中...")
        self.ui_module.set_answer("AI が画面を解析しています...\\n\\nしばらくお待ちください。")
        
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
                answer = result.get('answer', '回答を生成できませんでした。')
                self.ui_module.set_answer(answer)
                
                # 座標情報があれば矢印を表示
                coordinates = result.get('coordinates')
                if coordinates and isinstance(coordinates, dict):
                    x = coordinates.get('x')
                    y = coordinates.get('y')
                    if x is not None and y is not None:
                        try:
                            self.overlay_module.show_arrow(int(x), int(y))
                            # 10秒後に矢印を非表示
                            threading.Timer(10.0, self.overlay_module.hide).start()
                            print(f"操作指示矢印を表示しました: ({x}, {y})")
                        except Exception as e:
                            print(f"矢印表示エラー: {e}")
                
                self.ui_module.set_status("解析完了")
            else:
                self.ui_module.set_answer("AI解析でエラーが発生しました。\\n\\n以下をご確認ください:\\n- インターネット接続\\n- OpenAI APIキーの有効性\\n- 画像ファイルの存在")
                self.ui_module.set_status("エラー")
                
        except Exception as e:
            print(f"AI解析エラー: {e}")
            error_message = f"エラーが発生しました: {str(e)}\\n\\n考えられる原因:\\n- ネットワーク接続の問題\\n- APIキーの問題\\n- 画像ファイルの問題"
            self.ui_module.set_answer(error_message)
            self.ui_module.set_status("エラー")


def main():
    """メイン関数"""
    try:
        # メインコントローラーを作成
        controller = MainControllerAutoScreenshot()
        
        # アプリケーションを開始
        controller.start()
        
        # UIのメインループを実行
        controller.ui_module.run()
        
    except KeyboardInterrupt:
        print("\\nアプリケーションを終了します...")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'controller' in locals():
            controller.stop()


if __name__ == "__main__":
    main()
