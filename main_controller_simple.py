#!/usr/bin/env python3
"""
SENPAI シンプル版メインコントローラー
シンプルUIと改善された矢印オーバーレイを統合
"""

import os
import threading
import time
from tkinter import messagebox
from typing import Optional

# 既存モジュールをインポート
from ui_module_simple import SimpleUIModule
from capture_module_ui_aware import CaptureModuleUIAware
from ai_module_improved import AIModuleImproved
from overlay_module_clean import CleanOverlayModule
from speech_module import SpeechModule
from hybrid_coordinate_detector import HybridCoordinateDetector

# ライブラリ機能をインポート
from simple_library import SimpleLibrary
from library_ui_improved import ImprovedLibraryUI, ImprovedFavoriteSaveDialog


class SimpleMainController:
    """シンプル版メインコントローラークラス"""
    
    def __init__(self):
        """初期化"""
        print("=== SENPAI - シンプル版PC操作ガイド ===")
        print("特徴:")
        print("- シンプルで洗練されたUI")
        print("- 影なしクリーン矢印")
        print("- 改善された三角形先端")
        print("- お気に入り機能付き")
        print()
        
        # モジュール初期化
        self.ui_module = None
        self.capture_module = None
        self.ai_module = None
        self.overlay_module = None
        self.speech_module = None
        self.library = None
        self.library_ui = None
        
        # 状態管理
        self.current_screenshot = None
        self.current_question = None
        
        # 画面スケール情報
        self.screen_scale_x = 1.0
        self.screen_scale_y = 1.0
        
        # 初期化実行
        self._initialize_modules()
    
    def _detect_screen_scale(self):
        """画面スケール情報を検出"""
        try:
            import tkinter as tk
            
            # 一時的なTkウィンドウを作成
            temp_root = tk.Tk()
            temp_root.withdraw()
            
            # Tkinterが認識する画面サイズ
            tk_width = temp_root.winfo_screenwidth()
            tk_height = temp_root.winfo_screenheight()
            
            # 実際の画面サイズ（AIモジュールから取得）
            if hasattr(self.ai_module, 'screen_info'):
                actual_width = self.ai_module.screen_info.get('actual_width', tk_width)
                actual_height = self.ai_module.screen_info.get('actual_height', tk_height)
            else:
                # AIモジュールから取得できない場合は、スクリーンショットから取得
                try:
                    from PIL import Image
                    import pyautogui
                    screenshot = pyautogui.screenshot()
                    actual_width = screenshot.width
                    actual_height = screenshot.height
                except:
                    actual_width = tk_width
                    actual_height = tk_height
            
            # スケール比率を計算
            self.screen_scale_x = actual_width / tk_width if tk_width > 0 else 1.0
            self.screen_scale_y = actual_height / tk_height if tk_height > 0 else 1.0
            
            print(f"画面情報: Tk={tk_width}x{tk_height}, 実際={actual_width}x{actual_height}, スケール={self.screen_scale_x:.2f}x{self.screen_scale_y:.2f}")
            
            temp_root.destroy()
            
        except Exception as e:
            print(f"画面スケール検出エラー: {e}")
            self.screen_scale_x = 1.0
            self.screen_scale_y = 1.0
    
    def _convert_coordinates_to_overlay(self, x: int, y: int) -> tuple:
        """
        AI解析座標をオーバーレイ座標に変換
        
        Args:
            x: AI解析座標X（実際の画面サイズ）
            y: AI解析座標Y（実際の画面サイズ）
        
        Returns:
            (overlay_x, overlay_y): オーバーレイ座標
        """
        overlay_x = int(x / self.screen_scale_x)
        overlay_y = int(y / self.screen_scale_y)
        
        print(f"座標変換: ({x}, {y}) -> ({overlay_x}, {overlay_y}) [スケール: {self.screen_scale_x:.2f}x{self.screen_scale_y:.2f}]")
        
        return (overlay_x, overlay_y)
    
    def _initialize_modules(self):
        """各モジュールを初期化"""
        try:
            print("初期化中...")
            
            # シンプルUIモジュールを初期化
            print("シンプルUIモジュール初期化中...")
            self.ui_module = SimpleUIModule(
                question_callback=self.on_text_question,
                save_favorite_callback=self.on_save_favorite,
                show_library_callback=self.on_show_library
            )
            
            # UI非表示対応版キャプチャモジュールを初期化
            print("キャプチャモジュール初期化中...")
            self.capture_module = CaptureModuleUIAware(self.on_screenshot_captured)
            
            # UI表示/非表示のコールバックを設定
            self.capture_module.set_ui_callbacks(
                self.ui_module.hide_ui,
                self.ui_module.show_ui
            )
            
            # その他のモジュールを初期化
            print("AIモジュール初期化中...")
            self.ai_module = AIModuleImproved()
            
            print("クリーン矢印オーバーレイモジュール初期化中...")
            self.overlay_module = CleanOverlayModule()
            
            print("音声モジュール初期化中...")
            self.speech_module = SpeechModule(self.on_speech_recognized)
            
            # ライブラリ機能を初期化
            print("ライブラリ管理モジュール初期化中...")
            self.library = SimpleLibrary()
            
            # ハイブリッド座標検出器を初期化
            print("ハイブリッド座標検出器初期化中...")
            self.hybrid_detector = HybridCoordinateDetector(self.ai_module)
            
            # 画面スケール情報を取得
            self._detect_screen_scale()
            
            # 機能状態を更新
            self._update_function_status()
            
            print(f"画面スケール: x={self.screen_scale_x:.2f}, y={self.screen_scale_y:.2f}")
            print("✅ 初期化完了!")
            
        except Exception as e:
            print(f"❌ 初期化エラー: {e}")
            messagebox.showerror("初期化エラー", f"アプリケーションの初期化に失敗しました: {e}")
    
    def _update_function_status(self):
        """機能の有効/無効状態を更新"""
        try:
            # AI機能の状態確認
            ai_available = bool(os.getenv('OPENAI_API_KEY'))
            print(f"AI機能: {'✅ 利用可能' if ai_available else '❌ APIキー未設定'}")
            
            # 音声認識機能の状態確認
            speech_available = self.speech_module.is_available()
            print(f"音声認識: {'✅ 利用可能' if speech_available else '❌ 利用不可'}")
            
            # ライブラリ機能の状態確認
            library_available = self.library is not None
            print(f"ライブラリ機能: {'✅ 利用可能' if library_available else '❌ 利用不可'}")
            
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
            messagebox.showerror("エラー", f"お気に入り一覧の表示に失敗しました: {e}")
    
    def on_text_question(self, question: str):
        """テキスト質問処理"""
        try:
            print(f"=== 質問受信: {question} ===")
            
            # ライブラリから回答を検索
            if self.library:
                print("ライブラリから回答を検索中...")
                library_result = self.library.search_favorites(question)
                
                if library_result:
                    print(f"ライブラリから回答を発見: {library_result['tag']}")
                    self.ui_module.set_answer(f"📚 ライブラリから回答\\n\\n{library_result['answer']}")
                    return
                else:
                    print("ライブラリに回答がないため、AI解析を実行します")
            
            # UI非表示でスクリーンショット撮影
            print("UI非表示でスクリーンショット撮影中...")
            self.ui_module.set_status("スクリーンショット撮影中...")
            
            # 別スレッドで撮影実行
            threading.Thread(
                target=self._capture_and_analyze,
                args=(question,),
                daemon=True
            ).start()
            
        except Exception as e:
            print(f"質問処理エラー: {e}")
            self.ui_module.set_answer(f"エラーが発生しました: {e}")
    
    def _capture_and_analyze(self, question: str):
        """スクリーンショット撮影とAI解析を実行"""
        try:
            # 現在の質問を保存
            self.current_question = question
            
            # スクリーンショット撮影
            screenshot_path = self.capture_module.take_screenshot_with_ui_hide()
            
            if screenshot_path:
                self.current_screenshot = screenshot_path
                print(f"スクリーンショット撮影完了: {screenshot_path}")
                
                # AI解析実行
                self.ui_module.set_status("AI解析中...")
                print("AI解析中...")
                
                analysis_result = self.ai_module.analyze_screenshot(screenshot_path, question)
                
                if analysis_result:
                    self._handle_ai_result(analysis_result)
                else:
                    self.ui_module.set_answer("AI解析に失敗しました")
            else:
                self.ui_module.set_answer("スクリーンショット撮影に失敗しました")
                
        except Exception as e:
            print(f"撮影・解析エラー: {e}")
            self.ui_module.set_answer(f"処理中にエラーが発生しました: {e}")
    
    def _handle_ai_result(self, result: dict):
        """AI解析結果を処理"""
        try:
            print("AI解析結果を処理中...")
            
            # 回答を表示
            answer = result.get('answer', 'AI解析結果を取得できませんでした')
            self.ui_module.set_answer(answer)
            
            # ハイブリッド方式で座標を検出
            hybrid_result = self.hybrid_detector.detect_coordinates(
                self.current_screenshot,
                self.current_question
            )
            
            if hybrid_result:
                x = hybrid_result['x']
                y = hybrid_result['y']
                confidence = hybrid_result['confidence']
                method = hybrid_result.get('method', 'unknown')
                
                print(f"ハイブリッド座標検出: ({x}, {y}), 信頼度: {confidence}, 方式: {method}")
                
                # 座標をオーバーレイ座標に変換
                overlay_x, overlay_y = self._convert_coordinates_to_overlay(x, y)
                
                # 矢印を表示
                self.overlay_module.show_arrow(overlay_x, overlay_y)
                
                # 10秒後に自動非表示
                self.overlay_module.auto_hide_after_delay(10)
                
                print("✅ ハイブリッド方式で矢印を表示しました")
            else:
                print("座標情報がないため矢印は表示しません")
            
        except Exception as e:
            print(f"AI結果処理エラー: {e}")
            self.ui_module.set_answer(f"結果処理中にエラーが発生しました: {e}")
    
    def on_screenshot_captured(self, screenshot_path: str):
        """スクリーンショット撮影完了時のコールバック"""
        print(f"スクリーンショット撮影完了: {screenshot_path}")
        self.current_screenshot = screenshot_path
    
    def on_speech_recognized(self, text: str):
        """音声認識結果のコールバック"""
        print(f"音声認識結果: {text}")
        # 音声認識結果をテキスト質問として処理
        self.on_text_question(text)
    
    def on_app_close(self):
        """アプリケーション終了処理"""
        try:
            print("アプリケーション終了処理を開始...")
            
            # オーバーレイを終了
            try:
                if self.overlay_module:
                    self.overlay_module.destroy()
                    print("オーバーレイを終了しました")
            except Exception as e:
                print(f"オーバーレイ終了エラー: {e}")
            
            # ライブラリUIを閉じる
            try:
                if self.library_ui and hasattr(self.library_ui, 'window') and self.library_ui.window:
                    self.library_ui.window.destroy()
                    print("ライブラリUIを閉じました")
            except Exception as e:
                print(f"ライブラリUI終了エラー: {e}")
            
            print("アプリケーション終了完了")
            
        except Exception as e:
            print(f"終了処理エラー: {e}")
    
    def run(self):
        """アプリケーション実行"""
        try:
            print("SENPAI - シンプル版PC操作ガイドを開始します")
            self.ui_module.set_status("準備完了")
            
            # 終了処理の設定
            self.ui_module.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
            
            # UIメインループを開始
            self.ui_module.run()
            
        except KeyboardInterrupt:
            print("\\nキーボード割り込みを受信しました")
            self.on_app_close()
        except Exception as e:
            print(f"実行エラー: {e}")
            self.on_app_close()
    
    def _on_window_close(self):
        """ウィンドウ閉じるボタンが押された時の処理"""
        self.on_app_close()
        if self.ui_module and self.ui_module.root:
            self.ui_module.root.quit()
            self.ui_module.root.destroy()


def main():
    """メイン関数"""
    try:
        # 環境チェック
        if not os.getenv('OPENAI_API_KEY'):
            print("⚠️  警告: OPENAI_API_KEY環境変数が設定されていません")
            print("   AI機能を使用するには、OpenAI APIキーを設定してください")
            print()
        
        # メインコントローラーを作成・実行
        controller = SimpleMainController()
        controller.run()
        
    except Exception as e:
        print(f"❌ アプリケーション実行エラー: {e}")
        messagebox.showerror("実行エラー", f"アプリケーションの実行に失敗しました: {e}")


if __name__ == "__main__":
    main()
