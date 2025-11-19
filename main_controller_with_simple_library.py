#!/usr/bin/env python3
"""
PC操作支援アプリケーション - メインコントローラー（シンプルライブラリ機能付き）
既存の安定版にシンプルなお気に入り機能を追加
"""

import os
import sys
import threading
import time
import json
from typing import Optional, Dict, Any
from tkinter import messagebox

# 既存の安定版モジュールをインポート
from capture_module_ui_aware import CaptureModuleUIAware
from speech_module import SpeechModule
from ui_module_hide_aware import UIModuleHideAware
from ai_module_improved import AIModuleImproved
from overlay_module_improved import OverlayModuleImproved

# 新しいライブラリ機能をインポート
from simple_library import SimpleLibrary
from library_ui_improved import ImprovedLibraryUI, ImprovedFavoriteSaveDialog


class MainControllerWithSimpleLibrary:
    """メインコントローラークラス（シンプルライブラリ機能付き）"""
    
    def __init__(self):
        """初期化"""
        self.running = False
        self.current_screenshot = None
        self.auto_screenshot_enabled = True
        
        print("=== SENPAI - PC操作ガイド（シンプルライブラリ機能付き） ===")
        print("シンプルライブラリ機能:")
        print("- ⭐ お気に入り保存でAI回答を保存")
        print("- 📚 お気に入り一覧で保存済み回答を管理")
        print("- 🏷️ タグ付けで分類・検索")
        print("- 🔍 シンプルな検索機能")
        print()
        
        # ライブラリ機能を初期化
        try:
            self.library = SimpleLibrary()
            self.library_ui = None  # 必要時に作成
            print("✅ シンプルライブラリ機能が初期化されました")
        except Exception as e:
            print(f"⚠️ ライブラリ機能初期化エラー: {e}")
            self.library = None
        
        # UIモジュールを最初に初期化（ライブラリコールバック付き）
        self.ui_module = UIModuleHideAware(
            self.on_text_question, 
            self.on_app_close,
            self.on_manual_screenshot_request,
            self.on_auto_screenshot_toggle,
            self.on_save_favorite,  # ライブラリ機能
            self.on_show_library    # ライブラリ機能
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
        
        # 機能状態を更新
        self._update_function_status()
        
        print("✅ 初期化完了！")
    
    def _update_function_status(self):
        """機能の有効/無効状態を更新"""
        try:
            # AI機能の状態
            ai_available = bool(os.getenv('OPENAI_API_KEY'))
            self.ui_module.set_function_status('ai', ai_available)
            
            # 音声認識機能の状態
            speech_available = self.speech_module.is_available()
            self.ui_module.set_function_status('speech', speech_available)
            
            # ホットキー機能の状態（環境依存）
            hotkey_available = False  # サンドボックス環境では無効
            self.ui_module.set_function_status('hotkey', hotkey_available)
            
        except Exception as e:
            print(f"機能状態更新エラー: {e}")
    
    def on_save_favorite(self, question: str, answer: str):
        """お気に入り保存処理"""
        try:
            if not self.library:
                messagebox.showerror("エラー", "ライブラリ機能が利用できません")
                return
            
            # 改善されたタグ入力ダイアログを表示
            dialog = ImprovedFavoriteSaveDialog(self.ui_module.root, question, answer)
            tag = dialog.show_dialog()
            
            if tag is not None:  # キャンセルされていない場合
                # お気に入りを保存
                success = self.library.save_favorite(
                    question=question,
                    answer=answer,
                    tag=tag,
                    screenshot_path=self.current_screenshot or ""
                )
                
                if success:
                    messagebox.showinfo("成功", f"お気に入りに保存しました！\\n\\nタグ: {tag}")
                    print(f"お気に入り保存成功: {tag}")
                else:
                    messagebox.showerror("エラー", "お気に入りの保存に失敗しました")
            
        except Exception as e:
            print(f"お気に入り保存エラー: {e}")
            messagebox.showerror("エラー", f"お気に入り保存中にエラーが発生しました: {e}")
    
    def on_show_library(self):
        """お気に入り一覧表示処理"""
        try:
            if not self.library:
                messagebox.showerror("エラー", "ライブラリ機能が利用できません")
                return
            
            # ライブラリUIを作成（初回のみ）
            if not self.library_ui:
                self.library_ui = ImprovedLibraryUI(self.ui_module.root)
            
            # お気に入り一覧ウィンドウを表示
            self.library_ui.show_favorites_window()
            
        except Exception as e:
            print(f"お気に入り一覧表示エラー: {e}")
            messagebox.showerror("エラー", f"お気に入り一覧の表示中にエラーが発生しました: {e}")
    
    def on_text_question(self, question: str):
        """テキスト質問が送信された時の処理"""
        if not question.strip():
            return
        
        print(f"=== 質問受信: {question} ===")
        
        # 自動スクリーンショットが有効な場合は撮影
        if self.auto_screenshot_enabled:
            print("UI非表示でスクリーンショット撮影中...")
            self.ui_module.set_status("UI非表示でスクリーンショット撮影中...")
            
            # UI非表示でスクリーンショット撮影
            screenshot_path = self.capture_module.take_screenshot_with_ui_hide()
            if screenshot_path:
                # スクリーンショット撮影成功時の処理はコールバックで実行される
                pass
            else:
                self.ui_module.set_status("スクリーンショット撮影失敗")
                self.ui_module.set_answer("スクリーンショットの撮影に失敗しました。\n\n再度お試しください。")
        else:
            # 既存のスクリーンショットがあるかチェック
            if self.current_screenshot and os.path.exists(self.current_screenshot):
                print(f"既存のスクリーンショットを使用: {self.current_screenshot}")
                self._process_question_with_screenshot(question, self.current_screenshot)
            else:
                print("スクリーンショットが必要です")
                self.ui_module.set_status("スクリーンショットを撮影してください")
                self.ui_module.set_answer("まずスクリーンショットを撮影してから質問してください。\\n\\n📷 手動スクリーンショットボタンをクリックするか、\\n🚀 質問ボタンで自動撮影を有効にしてください。")
    
    def on_speech_recognized(self, text: str):
        """音声認識結果を受信した時の処理"""
        print(f"音声認識結果: {text}")
        self.ui_module.question_text.delete(1.0, 'end')
        self.ui_module.question_text.insert(1.0, text)
        self.on_text_question(text)
    
    def on_manual_screenshot_request(self):
        """手動スクリーンショット撮影要求"""
        print("手動スクリーンショット撮影要求")
        self.ui_module.set_status("UI非表示でスクリーンショット撮影中...")
        
        # UI非表示でスクリーンショット撮影
        screenshot_path = self.capture_module.take_screenshot_with_ui_hide()
        if not screenshot_path:
            self.ui_module.set_status("スクリーンショット撮影失敗")
            self.ui_module.set_answer("スクリーンショットの撮影に失敗しました。\n\n再度お試しください。")
    
    def on_auto_screenshot_toggle(self, enabled: bool):
        """自動スクリーンショット切り替え"""
        self.auto_screenshot_enabled = enabled
        status = "有効" if enabled else "無効"
        print(f"自動スクリーンショット: {status}")
        self.ui_module.set_status(f"自動スクリーンショット: {status}")
    
    def on_screenshot_captured(self, screenshot_path: str):
        """スクリーンショット撮影完了時の処理"""
        self.current_screenshot = screenshot_path
        print(f"スクリーンショット撮影完了: {screenshot_path}")
        
        # 現在質問中の場合は処理を続行
        current_question = self.ui_module.current_question
        if current_question:
            self._process_question_with_screenshot(current_question, screenshot_path)
    
    def _process_question_with_screenshot(self, question: str, screenshot_path: str):
        """質問とスクリーンショットを使ってAI解析を実行"""
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
            args=(question, screenshot_path),
            daemon=True
        ).start()
    
    def _analyze_with_enhanced_ai(self, question: str, screenshot_path: str):
        """強化版AI解析を実行（別スレッド）"""
        try:
            # 強化版AI解析を実行
            result = self.ai_module.analyze_screenshot(screenshot_path, question)
            
            if result:
                # 回答をUIに表示
                answer = result.get('answer', '回答を生成できませんでした。')
                
                # 座標情報と信頼度を含む詳細な回答を構築
                coordinates = result.get('coordinates')
                confidence = result.get('confidence', 'unknown')
                element_description = result.get('element_description', '')
                
                # 回答にUI非表示機能の効果を追加
                answer += "\\n\\n✨ UI非表示機能により、純粋なPC操作画面を解析しました。"
                
                # 回答に座標情報を追加
                if coordinates and isinstance(coordinates, dict):
                    x = coordinates.get('x')
                    y = coordinates.get('y')
                    if x is not None and y is not None:
                        answer += f"\\n\\n🎯 操作指示:\\n"
                        answer += f"座標: ({x}, {y})\\n"
                        answer += f"信頼度: {confidence}\\n"
                        answer += f"要素: {element_description}"
                        
                        # 座標変換情報を追加（デバッグ用）
                        if 'coordinate_conversion' in result:
                            conv_info = result['coordinate_conversion']
                            answer += f"\\n\\n📊 座標変換詳細:\\n"
                            answer += f"元座標: ({conv_info.get('original_x')}, {conv_info.get('original_y')})\\n"
                            answer += f"変換座標: ({conv_info.get('converted_x')}, {conv_info.get('converted_y')})\\n"
                            answer += f"画面サイズ: {conv_info.get('screen_width')}x{conv_info.get('screen_height')}"
                        
                        # オーバーレイで矢印を表示
                        try:
                            print(f"矢印表示試行: 座標({x}, {y}), 信頼度: {confidence}")
                            self.overlay_module.show_arrow(x, y)  # sizeパラメータはデフォルト使用
                            answer += "\n\n🎯 画面上に矢印で操作箇所を表示しました。"
                            print("矢印表示成功")
                        except Exception as overlay_error:
                            print(f"オーバーレイ表示エラー: {overlay_error}")
                            import traceback
                            traceback.print_exc()
                            answer += "\n\n⚠️ 矢印表示でエラーが発生しましたが、座標は正確です。"
                
                # UIに回答を表示
                self.ui_module.set_answer(answer)
                self.ui_module.set_status("AI解析完了")
                
                print("AI解析完了")
                
            else:
                self.ui_module.set_answer("申し訳ありません。画像の解析に失敗しました。\\n\\n以下をお試しください:\\n- 別の質問で再度お試しください\\n- スクリーンショットを再撮影してください\\n- OpenAI APIキーが正しく設定されているか確認してください")
                self.ui_module.set_status("AI解析失敗")
                
        except Exception as e:
            print(f"AI解析エラー: {e}")
            self.ui_module.set_answer(f"AI解析中にエラーが発生しました: {e}\\n\\n以下をお試しください:\\n- ネットワーク接続を確認してください\\n- OpenAI APIキーが正しく設定されているか確認してください\\n- しばらく時間をおいて再度お試しください")
            self.ui_module.set_status("AI解析エラー")
    
    def on_app_close(self):
        """アプリケーション終了時の処理"""
        try:
            print("アプリケーション終了処理を開始...")
            self.running = False
            
            # オーバーレイを非表示
            try:
                self.overlay_module.hide()
                print("オーバーレイを非表示にしました")
            except Exception as e:
                print(f"オーバーレイ終了エラー: {e}")
            
            # ライブラリUIを閉じる
            try:
                if self.library_ui and self.library_ui.window:
                    self.library_ui._close_window()
                    print("ライブラリUIを閉じました")
            except Exception as e:
                print(f"ライブラリUI終了エラー: {e}")
            
            print("アプリケーション終了完了")
            
        except Exception as e:
            print(f"終了処理エラー: {e}")
    
    def run(self):
        """アプリケーション実行"""
        try:
            print("SENPAI - PC操作ガイド（シンプルライブラリ機能付き）を開始します")
            self.ui_module.set_status("準備完了")
            
            # UIメインループを開始
            self.ui_module.run()
            
        except KeyboardInterrupt:
            print("\\nキーボード割り込みを受信しました")
            self.on_app_close()
        except Exception as e:
            print(f"実行エラー: {e}")
            self.on_app_close()


def main():
    """メイン関数"""
    try:
        # 環境チェック
        print("=== 環境チェック ===")
        
        # OpenAI APIキー
        if os.getenv('OPENAI_API_KEY'):
            print("✅ OpenAI APIキーが設定されています")
        else:
            print("⚠️ OpenAI APIキーが設定されていません（AI機能が制限されます）")
        
        # スクリーンショット保存ディレクトリ
        screenshot_dir = "/tmp/pc_assistant_screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        print(f"✅ スクリーンショット保存ディレクトリ: {screenshot_dir}")
        
        print("=== アプリケーション開始 ===")
        
        # メインコントローラーを作成・実行
        controller = MainControllerWithSimpleLibrary()
        controller.run()
        
    except Exception as e:
        print(f"メイン関数エラー: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
