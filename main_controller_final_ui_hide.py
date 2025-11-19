#!/usr/bin/env python3
"""
PC操作支援アプリケーション - メインコントローラー（UI非表示対応版）
スクリーンショット撮影時にアプリUIを自動的に非表示にする
"""

import os
import sys
import threading
import time
import json
from typing import Optional, Dict, Any

# UI非表示対応版モジュールをインポート
from capture_module_ui_aware import CaptureModuleUIAware
from speech_module import SpeechModule
from ui_module_hide_aware import UIModuleHideAware
from ai_module_improved import AIModuleImproved
from overlay_module_improved import OverlayModuleImproved


class MainControllerFinalUIHide:
    """メインコントローラークラス（UI非表示対応版）"""
    
    def __init__(self):
        """初期化"""
        self.running = False
        self.current_screenshot = None
        self.auto_screenshot_enabled = True
        
        # UIモジュールを最初に初期化
        self.ui_module = UIModuleHideAware(
            self.on_text_question, 
            self.on_app_close,
            self.on_manual_screenshot_request,
            self.on_auto_screenshot_toggle
        )
        
        # UI非表示対応版キャプチャモジュールを初期化
        self.capture_module = CaptureModuleUIAware(self.on_screenshot_captured)
        
        # UI表示/非表示のコールバックを設定
        self.capture_module.set_ui_callbacks(
            self.ui_module.hide_ui,
            self.ui_module.show_ui
        )
        
        # その他のモジュールを初期化
        self.speech_module = SpeechModule(self.on_speech_recognized)
        self.ai_module = AIModuleImproved()
        self.overlay_module = OverlayModuleImproved()
        
        print("PC操作支援アプリケーション（UI非表示対応版）が初期化されました")
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
        print(f"UI非表示機能: 有効")
        print(f"改良版オーバーレイ: 有効")
        
        if hotkey_available:
            print("Ctrl+Alt+S でUI非表示スクリーンショットを撮影できます")
        
        print("質問時に自動的にUIを非表示にしてスクリーンショットを撮影します")
    
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
        
        print("UI非表示対応版アプリケーションが開始されました")
    
    def stop(self):
        """アプリケーションを停止"""
        self.running = False
        
        print("🔄 シンプル矢印・永続表示版アプリケーションを終了しています...")
        
        # 矢印を非表示（終了時）
        self.overlay_module.hide()
        print("🔄 矢印を非表示にしました")
        
        # 各モジュールを停止
        self.capture_module.stop()
        self.speech_module.stop()
        
        print("✅ シンプル矢印・永続表示版アプリケーションが停止されました")
    
    def on_manual_screenshot_request(self):
        """手動スクリーンショット撮影が要求された時"""
        # 既存の矢印を非表示（手動スクリーンショットのため）
        self.overlay_module.hide()
        
        # UI非表示でスクリーンショットを撮影
        filepath = self.capture_module.take_screenshot_with_ui_hide()
        if filepath:
            self.ui_module.set_status("UI非表示スクリーンショット撮影完了")
        else:
            self.ui_module.set_status("スクリーンショット撮影に失敗しました")
    
    def on_auto_screenshot_toggle(self, enabled: bool):
        """自動スクリーンショット機能のON/OFF切り替え"""
        self.auto_screenshot_enabled = enabled
        status = "有効" if enabled else "無効"
        print(f"自動スクリーンショット機能: {status}")
        self.ui_module.set_status(f"自動スクリーンショット: {status}")
    
    def on_screenshot_captured(self, screenshot_path: str):
        """スクリーンショットが撮影された時のコールバック"""
        self.current_screenshot = screenshot_path
        print(f"UI非表示スクリーンショットが撮影されました: {screenshot_path}")
        
        # UIに通知
        if hasattr(self, '_auto_screenshot_in_progress') and self._auto_screenshot_in_progress:
            # 自動撮影の場合は簡潔な通知
            self.ui_module.set_status("UI非表示スクリーンショット撮影完了")
        else:
            # 手動撮影の場合は明確な通知
            self.ui_module.set_status("UI非表示スクリーンショット撮影完了")
    
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
        """質問を処理（UI非表示自動スクリーンショット付き）"""
        if not question.strip():
            self.ui_module.set_answer("質問を入力してください。")
            return
        
        # 自動スクリーンショットが有効な場合、UI非表示でスクリーンショットを撮影
        if self.auto_screenshot_enabled:
            self.ui_module.set_status("UI非表示でスクリーンショット撮影中...")
            
            # 自動撮影フラグを設定
            self._auto_screenshot_in_progress = True
            
            # UI非表示でスクリーンショットを撮影
            filepath = self.capture_module.take_screenshot_with_ui_hide()
            
            # フラグをリセット
            self._auto_screenshot_in_progress = False
            
            if filepath:
                self.on_screenshot_captured(filepath)
                print(f"質問に対してUI非表示スクリーンショットを撮影: {filepath}")
            else:
                self.ui_module.set_answer("UI非表示スクリーンショットの撮影に失敗しました。\\n\\n手動で撮影してください。")
                return
        
        # 既存の質問処理を実行
        self.process_question(question)
    
    def process_question(self, question: str):
        """質問を処理（強化版AI解析）"""
        if not self.current_screenshot:
            self.ui_module.set_answer("スクリーンショットが撮影されていません。\\n\\n自動スクリーンショットが無効になっている可能性があります。\\n手動で📷ボタンを押してUI非表示スクリーンショットを撮影してください。")
            return
        
        # AI機能が利用できない場合
        if not os.getenv('OPENAI_API_KEY'):
            self.ui_module.set_answer("AI解析機能が利用できません。\\n\\nOpenAI APIキーが設定されていません。\\n\\n設定方法:\\nexport OPENAI_API_KEY='your-api-key-here'")
            return
        
        # UIに処理中を表示
        self.ui_module.set_status("AI が純粋なPC画面を解析中...")
        self.ui_module.set_answer("AI が純粋なPC操作画面を詳細に解析しています...\\n\\n✨ UIが写り込まない純粋な画面を解析\\n🎯 座標精度が向上\\n🔍 信頼度評価システム\\n\\nしばらくお待ちください。")
        
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
                
                # 回答にUI非表示機能の効果を追加
                answer += "\n\n✨ UI非表示機能により、純粋なPC操作画面を解析しました。"
                
                # 回答に座標情報を追加
                if coordinates and isinstance(coordinates, dict):
                    x = coordinates.get('x')
                    y = coordinates.get('y')
                    if x is not None and y is not None:
                        answer += f"\n\n🎯 操作指示:\n"
                        answer += f"座標: ({x}, {y})\n"
                        answer += f"信頼度: {confidence}\n"
                        answer += f"要素: {element_description}"
                        
                        # 座標変換情報を追加（デバッグ用）
                        if 'coordinate_conversion' in result:
                            conv_info = result['coordinate_conversion']
                            answer += f"\n\n📊 座標変換詳細:\n"
                            answer += f"元座標: ({conv_info.get('original_x')}, {conv_info.get('original_y')})\n"
                            answer += f"画像サイズ: {conv_info.get('image_size')}\n"
                            answer += f"画面サイズ: {conv_info.get('screen_size')}\n"
                            answer += f"変換比率: x={conv_info.get('scale_x', 1.0):.3f}, y={conv_info.get('scale_y', 1.0):.3f}"
                        
                        if confidence == 'low':
                            answer += "\n\n⚠️ 注意: 座標の精度が低い可能性があります。手動で確認してください。"
                        elif confidence == 'high':
                            answer += "\n\n✅ 高精度: UI非表示により正確な座標を特定できました。"
                
                self.ui_module.set_answer(answer)
                
                # 座標情報があれば改良された矢印を表示
                if coordinates and isinstance(coordinates, dict):
                    x = coordinates.get('x')
                    y = coordinates.get('y')
                    if x is not None and y is not None:
                        try:
                            # 座標の詳細ログ出力
                            print(f"\n=== 座標表示詳細ログ ===")
                            print(f"AI解析結果座標: ({x}, {y})")
                            print(f"信頼度: {confidence}")
                            print(f"要素説明: {element_description}")
                            
                            if 'coordinate_conversion' in result:
                                conv_info = result['coordinate_conversion']
                                print(f"座標変換情報:")
                                print(f"  元座標: ({conv_info.get('original_x')}, {conv_info.get('original_y')})")
                                print(f"  画像サイズ: {conv_info.get('image_size')}")
                                print(f"  画面サイズ: {conv_info.get('screen_size')}")
                                print(f"  変換比率: x={conv_info.get('scale_x', 1.0):.3f}, y={conv_info.get('scale_y', 1.0):.3f}")
                            
                            # 信頼度に応じて表示方法を変更
                            if confidence == 'high':
                                # 高信頼度: 通常の矢印
                                print(f"高精度矢印を表示中: 画面座標({x}, {y})")
                                self.overlay_module.show_arrow(int(x), int(y), 80)
                                print(f"✅ 高精度矢印表示完了")
                            elif confidence == 'medium':
                                # 中信頼度: 方向指定矢印
                                print(f"方向指定矢印を表示中: 画面座標({x}, {y})")
                                self.overlay_module.show_pointing_arrow(int(x), int(y), 70)
                                print(f"✅ 方向指定矢印表示完了")
                            else:
                                # 低信頼度: ハイライト表示
                                margin = 50
                                x1, y1 = int(x) - margin, int(y) - margin
                                x2, y2 = int(x) + margin, int(y) + margin
                                print(f"ハイライト表示中: 画面座標({x1}, {y1}) - ({x2}, {y2})")
                                self.overlay_module.show_highlight_area(x1, y1, x2, y2)
                                print(f"✅ ハイライト表示完了")
                            
                            print(f"========================\n")
                            
                            # 表示時間を信頼度に応じて調整
                            display_time = 15.0 if confidence == 'high' else 10.0
                            threading.Timer(display_time, self.overlay_module.hide).start()
                            
                        except Exception as e:
                            print(f"❌ 矢印表示エラー: {e}")
                            import traceback
                            traceback.print_exc()
                
                self.ui_module.set_status("UI非表示解析完了")
            else:
                self.ui_module.set_answer("AI解析でエラーが発生しました。\\n\\n以下をご確認ください:\\n- インターネット接続\\n- OpenAI APIキーの有効性\\n- 画像ファイルの存在\\n- 画像の品質")
                self.ui_module.set_status("エラー")
                
        except Exception as e:
            print(f"AI解析エラー: {e}")
            error_message = f"エラーが発生しました: {str(e)}\\n\\n考えられる原因:\\n- ネットワーク接続の問題\\n- APIキーの問題\\n- 画像ファイルの問題\\n- API制限に達した可能性"
            self.ui_module.set_answer(error_message)
            self.ui_module.set_status("エラー")


def main():
    """メイン関数"""
    try:
        # メインコントローラーを作成
        controller = MainControllerFinalUIHide()
        
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
