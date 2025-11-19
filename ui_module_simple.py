#!/usr/bin/env python3
"""
SENPAI シンプルUIモジュール
添付画像のデザインに準じたミニマルなユーザーインターフェース
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from typing import Optional, Callable


class SimpleUIModule:
    """シンプルUIモジュールクラス"""
    
    def __init__(self, 
                 question_callback: Optional[Callable[[str], None]] = None,
                 save_favorite_callback: Optional[Callable[[str, str], None]] = None,
                 show_library_callback: Optional[Callable[[], None]] = None):
        """
        初期化
        
        Args:
            question_callback: 質問送信時のコールバック
            save_favorite_callback: お気に入り保存時のコールバック
            show_library_callback: お気に入り一覧表示時のコールバック
        """
        self.question_callback = question_callback
        self.save_favorite_callback = save_favorite_callback
        self.show_library_callback = show_library_callback
        
        # UI状態管理
        self.current_question = ""
        self.current_answer = ""
        self.input_mode = "text"  # "text" or "voice"
        
        # ウィンドウとウィジェット
        self.root = None
        self.question_text = None
        self.answer_text = None
        self.mode_button = None
        self.ask_button = None
        self.clear_button = None
        self.end_button = None
        
        # 初期化
        self._create_window()
        self._setup_styles()
        self._create_widgets()
        self._setup_bindings()
    
    def _create_window(self):
        """メインウィンドウを作成"""
        self.root = tk.Tk()
        self.root.title("SENPAI")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        self.root.configure(bg='#FFFFFF')
        
        # ウィンドウを中央に配置
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
        
        # 閉じるボタンのイベント設定
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
    
    def _setup_styles(self):
        """スタイルを設定"""
        style = ttk.Style()
        
        # ボタンスタイル
        style.configure(
            "Simple.TButton",
            background='#F5F5F5',
            foreground='#000000',
            borderwidth=1,
            relief='solid',
            font=('Yu Gothic UI', 11),
            padding=(12, 6)
        )
        
        # ボタンホバー効果
        style.map(
            "Simple.TButton",
            background=[
                ('active', '#EEEEEE'),
                ('pressed', '#E0E0E0')
            ]
        )
    
    def _create_widgets(self):
        """ウィジェットを作成"""
        # メインフレーム
        main_frame = tk.Frame(self.root, bg='#FFFFFF', padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # グリッド設定
        main_frame.grid_rowconfigure(1, weight=1)  # 質問エリア
        main_frame.grid_rowconfigure(3, weight=1)  # 回答エリア
        main_frame.grid_columnconfigure(0, weight=1)
        
        # 1. 質問入力エリア
        self.question_text = tk.Text(
            main_frame,
            height=6,
            font=('Yu Gothic UI', 11),
            bg='#FFFFFF',
            fg='#000000',
            relief='solid',
            borderwidth=1,
            highlightthickness=0,
            padx=8,
            pady=8,
            wrap=tk.WORD
        )
        self.question_text.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        
        # プレースホルダー設定
        self._set_placeholder(self.question_text, "質問を入力してください")
        
        # 2. 上部ボタンエリア
        top_button_frame = tk.Frame(main_frame, bg='#FFFFFF')
        top_button_frame.grid(row=2, column=0, sticky='e', pady=(0, 10))
        
        # 音声認識ボタン（マイクアイコン）
        self.mode_button = ttk.Button(
            top_button_frame,
            text="🎤 音声認識",
            style="Simple.TButton",
            command=self._toggle_input_mode,
            width=12
        )
        self.mode_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # 質問するボタン
        self.ask_button = ttk.Button(
            top_button_frame,
            text="質問する",
            style="Simple.TButton",
            command=self._send_question,
            width=10
        )
        self.ask_button.pack(side=tk.RIGHT)
        
        # 3. 回答表示エリア
        self.answer_text = tk.Text(
            main_frame,
            height=8,
            font=('Yu Gothic UI', 11),
            bg='#F9F9F9',
            fg='#000000',
            relief='solid',
            borderwidth=1,
            highlightthickness=0,
            padx=8,
            pady=8,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.answer_text.grid(row=3, column=0, sticky='ew', pady=(0, 10))
        
        # 初期メッセージ設定
        self._set_answer("考え中...")
        
        # 4. 下部ボタンエリア
        bottom_button_frame = tk.Frame(main_frame, bg='#FFFFFF')
        bottom_button_frame.grid(row=4, column=0, sticky='e')
        
        # 終了ボタン
        self.end_button = ttk.Button(
            bottom_button_frame,
            text="終了",
            style="Simple.TButton",
            command=self._on_window_close,
            width=8
        )
        self.end_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # クリアボタン
        self.clear_button = ttk.Button(
            bottom_button_frame,
            text="クリア",
            style="Simple.TButton",
            command=self._clear_all,
            width=8
        )
        self.clear_button.pack(side=tk.RIGHT)
    
    def _setup_bindings(self):
        """キーボードショートカットを設定"""
        # Ctrl+Enter で質問送信
        self.root.bind('<Control-Return>', lambda e: self._send_question())
        
        # Escape でクリア
        self.root.bind('<Escape>', lambda e: self._clear_all())
        
        # Ctrl+Q で終了
        self.root.bind('<Control-q>', lambda e: self._on_window_close())
        
        # 質問テキストエリアのフォーカスイベント
        self.question_text.bind('<FocusIn>', self._on_question_focus_in)
        self.question_text.bind('<FocusOut>', self._on_question_focus_out)
    
    def _set_placeholder(self, text_widget, placeholder):
        """プレースホルダーを設定"""
        text_widget.insert(1.0, placeholder)
        text_widget.configure(fg='#999999')
        text_widget.placeholder = placeholder
        text_widget.has_placeholder = True
    
    def _on_question_focus_in(self, event):
        """質問テキストエリアにフォーカスが入った時"""
        if hasattr(self.question_text, 'has_placeholder') and self.question_text.has_placeholder:
            self.question_text.delete(1.0, tk.END)
            self.question_text.configure(fg='#000000')
            self.question_text.has_placeholder = False
    
    def _on_question_focus_out(self, event):
        """質問テキストエリアからフォーカスが外れた時"""
        content = self.question_text.get(1.0, tk.END).strip()
        if not content:
            self._set_placeholder(self.question_text, "質問を入力してください")
    
    def _toggle_input_mode(self):
        """入力モードを切り替え"""
        if self.input_mode == "text":
            self.input_mode = "voice"
            self.mode_button.configure(text="🔴 音声入力中")
            messagebox.showinfo("入力モード", "音声入力モードに切り替えました")
        else:
            self.input_mode = "text"
            self.mode_button.configure(text="🎤 音声認識")
            messagebox.showinfo("入力モード", "テキスト入力モードに切り替えました")
    
    def _send_question(self):
        """質問を送信"""
        # プレースホルダーチェック
        if hasattr(self.question_text, 'has_placeholder') and self.question_text.has_placeholder:
            messagebox.showwarning("入力エラー", "質問を入力してください")
            return
        
        # 質問内容を取得
        question = self.question_text.get(1.0, tk.END).strip()
        if not question:
            messagebox.showwarning("入力エラー", "質問を入力してください")
            return
        
        # 質問を保存
        self.current_question = question
        
        # 回答エリアを処理中に設定
        self._set_answer("考え中...")
        
        # ボタンを無効化
        self.ask_button.configure(state=tk.DISABLED)
        
        # コールバック実行
        if self.question_callback:
            # 別スレッドで実行して UI をブロックしない
            threading.Thread(
                target=self._execute_question_callback,
                args=(question,),
                daemon=True
            ).start()
    
    def _execute_question_callback(self, question):
        """質問コールバックを実行"""
        try:
            if self.question_callback:
                self.question_callback(question)
        except Exception as e:
            print(f"質問処理エラー: {e}")
            self.root.after(0, lambda: self._set_answer(f"エラーが発生しました: {e}"))
        finally:
            # ボタンを有効化
            self.root.after(0, lambda: self.ask_button.configure(state=tk.NORMAL))
    
    def _clear_all(self):
        """すべてをクリア"""
        # 質問エリアをクリア
        self.question_text.delete(1.0, tk.END)
        self._set_placeholder(self.question_text, "質問を入力してください")
        
        # 回答エリアをクリア
        self._set_answer("考え中...")
        
        # 状態をリセット
        self.current_question = ""
        self.current_answer = ""
        
        print("画面をクリアしました")
    
    def _on_window_close(self):
        """ウィンドウを閉じる時の処理"""
        try:
            print("アプリケーション終了処理を開始...")
            self.root.quit()
            self.root.destroy()
            print("アプリケーション終了完了")
        except Exception as e:
            print(f"終了処理エラー: {e}")
    
    def _set_answer(self, answer: str):
        """回答を設定"""
        def update():
            self.answer_text.configure(state=tk.NORMAL)
            self.answer_text.delete(1.0, tk.END)
            self.answer_text.insert(1.0, answer)
            self.answer_text.configure(state=tk.DISABLED)
            
            # 現在の回答を保存
            self.current_answer = answer
        
        if threading.current_thread() == threading.main_thread():
            update()
        else:
            self.root.after(0, update)
    
    def set_status(self, status: str):
        """ステータスを設定（互換性のため）"""
        self._set_answer(status)
    
    def set_answer(self, answer: str):
        """回答を設定（外部インターフェース）"""
        self._set_answer(answer)
    
    def get_question(self) -> str:
        """現在の質問を取得"""
        return self.current_question
    
    def get_answer(self) -> str:
        """現在の回答を取得"""
        return self.current_answer
    
    def hide_ui(self):
        """UIを非表示にする"""
        if self.root:
            self.root.withdraw()
    
    def show_ui(self):
        """UIを表示する"""
        if self.root:
            self.root.deiconify()
            self.root.lift()
    
    def run(self):
        """UIメインループを開始"""
        try:
            print("シンプルUIを開始します...")
            self.root.mainloop()
        except Exception as e:
            print(f"UI実行エラー: {e}")
    
    def close(self):
        """UIを閉じる"""
        self._on_window_close()


def main():
    """テスト用メイン関数"""
    def test_question_callback(question):
        print(f"質問受信: {question}")
        # テスト用の回答
        import time
        time.sleep(2)  # 処理時間をシミュレート
        ui.set_answer(f"テスト回答: {question}に対する回答です。")
    
    # UIを作成
    ui = SimpleUIModule(question_callback=test_question_callback)
    
    # 実行
    ui.run()


if __name__ == "__main__":
    main()
