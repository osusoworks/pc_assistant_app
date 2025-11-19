#!/usr/bin/env python3
"""
PC操作支援アプリケーション - メインコントローラー（強化版）
改良されたオーバーレイとAI解析機能を使用
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
from ai_module_improved import AIModuleImproved
from overlay_module_improved import OverlayModuleImproved


class MainControllerEnhanced:
    """メインコントローラークラス（強化版）"""
    
    def __init__(self):
        """初期化"""
        self.running = False
        self.current_screenshot = None
        self.auto_screenshot_enabled = True
        
        # 各モジュールを初期化（改良版を使用）
        self.capture_module = CaptureModuleImproved(self.on_screenshot_captured)
        self.speech_module = SpeechModule(self.on_speech_recognized)
        self.ui_module = UIModuleAutoScreenshot(
            self.on_text_question, 
            self.on_app_close,
            self.on_manual_screenshot_request,
            self.on_auto_screenshot_toggle
        )
        self.ai_module = AIModuleImproved()
        self.overlay_module = OverlayModuleImproved()
        
        print("PC操作支援アプリケーション（強化版）が初期化されました")
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
        print(f"改良版オーバーレイ: 有効")
        print(f"座標精度向上: 有効")
        
        if hotkey_available:
            print("Ctrl+Alt+S でスクリーンショットを撮影できます")
        
        print("質問時に自動的にスクリーンショットを撮影し、改良された矢印で操作箇所を指示します")
    
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
        
        print("強化版アプリケーションが開始されました")
    
    def stop(self):
        """アプリケーションを停止"""
        self.running = False
        
        # 各モジュールを停止
        self.capture_module.stop()
        self.speech_module.stop()
        self.overlay_module.hide()
        
        print("強化版アプリケーションが停止されました")
    
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
        """質問を処理（強化版AI解析）"""
        if not self.current_screenshot:
            self.ui_module.set_answer("スクリーンショットが撮影されていません。\\n\\n自動スクリーンショットが無効になっている可能性があります。\\n手動で📷ボタンを押してスクリーンショットを撮影してください。")
            return
        
        # AI機能が利用できない場合
        if not os.getenv('OPENAI_API_KEY'):
            self.ui_module.set_answer("AI解析機能が利用できません。\\n\\nOpenAI APIキーが設定されていません。\\n\\n設定方法:\\nexport OPENAI_API_KEY='your-api-key-here'")
            return
        
        # UIに処理中を表示
        self.ui_module.set_status("強化版AI が画面を解析中...")
        self.ui_module.set_answer("強化版AI が画面を詳細に解析しています...\\n\\n座標精度が向上し、より正確な操作指示を提供します。\\n\\nしばらくお待ちください。")
        
        # 別スレッドでAI解析を実行（UIをブロックしないため）
        threading.Thread(
            target=self._analyze_with_enhanced_ai,
            args=(question,),
            daemon=True
        ).start()
    
    def _analyze_with_enhanced_ai(self, question: str):
        """強化版AI解析を実行（別スレッド）"""
        try:
            # 強化版AI解析を実行
            result = self.ai_module.analyze_screenshot(self.current_screenshot, question)
            
            if result:
                # 回答をUIに表示
                answer = result.get('answer', '回答を生成できませんでした。')
                
                # 座標情報と信頼度を含む詳細な回答を構築
                coordinates = result.get('coordinates')
                confidence = result.get('confidence', 'unknown')
                element_description = result.get('element_description', '')
                
                # 回答に座標情報を追加
                if coordinates and isinstance(coordinates, dict):
                    x = coordinates.get('x')
                    y = coordinates.get('y')
                    if x is not None and y is not None:
                        answer += f"\\n\\n🎯 操作指示:\\n"
                        answer += f"座標: ({x}, {y})\\n"
                        answer += f"信頼度: {confidence}\\n"
                        answer += f"要素: {element_description}"
                        
                        if confidence == 'low':
                            answer += "\\n\\n⚠️ 注意: 座標の精度が低い可能性があります。手動で確認してください。"
                
                self.ui_module.set_answer(answer)
                
                # 座標情報があれば改良された矢印を表示
                if coordinates and isinstance(coordinates, dict):
                    x = coordinates.get('x')
                    y = coordinates.get('y')
                    if x is not None and y is not None:
                        try:
                            # 信頼度に応じて表示方法を変更
                            if confidence == 'high':
                                # 高信頼度: 通常の矢印
                                self.overlay_module.show_arrow(int(x), int(y), 80)
                                print(f"高精度矢印を表示: ({x}, {y}) 信頼度: {confidence}")
                            elif confidence == 'medium':
                                # 中信頼度: 方向指定矢印
                                self.overlay_module.show_pointing_arrow(int(x), int(y), 70)
                                print(f"方向指定矢印を表示: ({x}, {y}) 信頼度: {confidence}")
                            else:
                                # 低信頼度: ハイライト表示
                                margin = 50
                                self.overlay_module.show_highlight_area(
                                    int(x) - margin, int(y) - margin,
                                    int(x) + margin, int(y) + margin
                                )
                                print(f"ハイライト表示: ({x}, {y}) 信頼度: {confidence}")
                            
                            # 表示時間を信頼度に応じて調整
                            display_time = 15.0 if confidence == 'high' else 10.0
                            threading.Timer(display_time, self.overlay_module.hide).start()
                            
                        except Exception as e:
                            print(f"強化版矢印表示エラー: {e}")
                
                self.ui_module.set_status("強化版解析完了")
            else:
                self.ui_module.set_answer("強化版AI解析でエラーが発生しました。\\n\\n以下をご確認ください:\\n- インターネット接続\\n- OpenAI APIキーの有効性\\n- 画像ファイルの存在\\n- 画像の品質")
                self.ui_module.set_status("エラー")
                
        except Exception as e:
            print(f"強化版AI解析エラー: {e}")
            error_message = f"エラーが発生しました: {str(e)}\\n\\n考えられる原因:\\n- ネットワーク接続の問題\\n- APIキーの問題\\n- 画像ファイルの問題\\n- API制限に達した可能性"
            self.ui_module.set_answer(error_message)
            self.ui_module.set_status("エラー")


def main():
    """メイン関数"""
    try:
        # メインコントローラーを作成
        controller = MainControllerEnhanced()
        
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
