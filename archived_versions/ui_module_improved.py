#!/usr/bin/env python3
"""
UIモジュール（改良版）- スクリーンショットボタン追加
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Callable, Optional
import threading


class UIModuleImproved:
    """ユーザーインターフェースを担当するモジュール（改良版）"""
    
    def __init__(self, question_callback: Callable[[str], None], 
                 close_callback: Callable[[], None],
                 screenshot_callback: Callable[[], None]):
        """
        初期化
        
        Args:
            question_callback: 質問が送信された時のコールバック
            close_callback: アプリケーション終了時のコールバック
            screenshot_callback: スクリーンショット撮影時のコールバック
        """
        self.question_callback = question_callback
        self.close_callback = close_callback
        self.screenshot_callback = screenshot_callback
        
        # メインウィンドウを作成
        self.root = tk.Tk()
        self.root.title("AI HELP")
        self.root.geometry("400x550")
        self.root.resizable(True, True)
        
        # ウィンドウを常に最前面に表示
        self.root.attributes('-topmost', True)
        
        # 終了時のイベントハンドラを設定
        self.root.protocol("WM_DELETE_WINDOW", self.close_callback)
        
        # 機能の有効/無効状態
        self.hotkey_available = False
        self.speech_available = False
        self.ai_available = False
        
        # UIコンポーネントを作成
        self._create_widgets()
        
        # 初期状態を設定
        self.set_status("待機中")
    
    def _create_widgets(self):
        """UIコンポーネントを作成"""
        # メインフレーム
        main_frame = tk.Frame(self.root, bg='#4ECDC4')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # タイトル
        title_label = tk.Label(
            main_frame, 
            text="AI HELP", 
            font=('Arial', 16, 'bold'),
            bg='#4ECDC4',
            fg='white'
        )
        title_label.pack(pady=(0, 10))
        
        # スクリーンショット撮影フレーム
        screenshot_frame = tk.Frame(main_frame, bg='#4ECDC4')
        screenshot_frame.pack(fill=tk.X, pady=(0, 10))
        
        # スクリーンショット撮影ボタン
        self.screenshot_button = tk.Button(
            screenshot_frame,
            text="📷 スクリーンショット撮影",
            font=('Arial', 12, 'bold'),
            bg='#2ECC71',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self._take_screenshot
        )
        self.screenshot_button.pack(side=tk.LEFT)
        
        # ホットキー表示ラベル
        self.hotkey_label = tk.Label(
            screenshot_frame,
            text="(Ctrl+Alt+S)",
            font=('Arial', 9),
            bg='#4ECDC4',
            fg='white'
        )
        self.hotkey_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # ステータス表示
        status_frame = tk.Frame(main_frame, bg='#4ECDC4')
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            status_frame,
            text="ステータス:",
            font=('Arial', 10),
            bg='#4ECDC4',
            fg='white'
        ).pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            status_frame,
            text="待機中",
            font=('Arial', 10),
            bg='#B0B0B0',
            fg='black',
            padx=10,
            pady=2
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # 機能状態表示フレーム
        function_frame = tk.Frame(main_frame, bg='#4ECDC4')
        function_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 機能状態ラベル
        self.function_labels = {}
        
        functions = [
            ('hotkey', 'ホットキー'),
            ('speech', '音声認識'),
            ('ai', 'AI解析')
        ]
        
        for i, (key, name) in enumerate(functions):
            label = tk.Label(
                function_frame,
                text=f"{name}: ❌",
                font=('Arial', 8),
                bg='#4ECDC4',
                fg='white'
            )
            label.grid(row=0, column=i, padx=5, sticky='w')
            self.function_labels[key] = label
        
        # 質問入力フレーム
        input_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=1)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 質問入力テキストボックス
        self.question_text = tk.Text(
            input_frame,
            height=3,
            font=('Arial', 11),
            wrap=tk.WORD,
            bg='white',
            fg='black',
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.question_text.pack(fill=tk.BOTH, expand=True)
        self.question_text.insert(tk.END, "質問を入力してください")
        self.question_text.bind('<FocusIn>', self._on_question_focus_in)
        self.question_text.bind('<FocusOut>', self._on_question_focus_out)
        
        # ボタンフレーム
        button_frame = tk.Frame(main_frame, bg='#4ECDC4')
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 質問送信ボタン
        self.send_button = tk.Button(
            button_frame,
            text="質問する",
            font=('Arial', 12, 'bold'),
            bg='#FF9F43',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self._send_question
        )
        self.send_button.pack(side=tk.LEFT)
        
        # 音声入力ボタン
        self.voice_button = tk.Button(
            button_frame,
            text="🎤 音声入力",
            font=('Arial', 11),
            bg='#9B59B6',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=10,
            command=self._voice_input,
            state=tk.DISABLED
        )
        self.voice_button.pack(side=tk.RIGHT)
        
        # 回答表示エリア
        answer_label = tk.Label(
            main_frame,
            text="AI回答:",
            font=('Arial', 10),
            bg='#4ECDC4',
            fg='white'
        )
        answer_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 回答表示テキストエリア
        self.answer_text = scrolledtext.ScrolledText(
            main_frame,
            height=10,
            font=('Arial', 11),
            wrap=tk.WORD,
            bg='white',
            fg='black',
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.answer_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 下部ボタンフレーム
        bottom_button_frame = tk.Frame(main_frame, bg='#4ECDC4')
        bottom_button_frame.pack(fill=tk.X)
        
        # クリアボタン
        clear_button = tk.Button(
            bottom_button_frame,
            text="クリア",
            font=('Arial', 11),
            bg='#5A67D8',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self._clear_all
        )
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 終了ボタン
        exit_button = tk.Button(
            bottom_button_frame,
            text="終了",
            font=('Arial', 11),
            bg='#E53E3E',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.close_callback
        )
        exit_button.pack(side=tk.RIGHT)
    
    def _take_screenshot(self):
        """スクリーンショット撮影ボタンが押された時"""
        if self.screenshot_callback:
            self.screenshot_callback()
    
    def _voice_input(self):
        """音声入力ボタンが押された時"""
        # TODO: 音声入力機能の実装
        self.set_status("音声入力機能は準備中です")
    
    def _on_question_focus_in(self, event):
        """質問テキストボックスにフォーカスが入った時"""
        if self.question_text.get(1.0, tk.END).strip() == "質問を入力してください":
            self.question_text.delete(1.0, tk.END)
            self.question_text.config(fg='black')
    
    def _on_question_focus_out(self, event):
        """質問テキストボックスからフォーカスが外れた時"""
        if not self.question_text.get(1.0, tk.END).strip():
            self.question_text.insert(1.0, "質問を入力してください")
            self.question_text.config(fg='gray')
    
    def _send_question(self):
        """質問を送信"""
        question = self.question_text.get(1.0, tk.END).strip()
        
        if question and question != "質問を入力してください":
            # コールバックを呼び出し
            if self.question_callback:
                self.question_callback(question)
            
            # 質問テキストをクリア
            self.question_text.delete(1.0, tk.END)
            self.question_text.insert(1.0, "質問を入力してください")
            self.question_text.config(fg='gray')
    
    def _clear_all(self):
        """すべてをクリア"""
        # 質問テキストをクリア
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(1.0, "質問を入力してください")
        self.question_text.config(fg='gray')
        
        # 回答テキストをクリア
        self.answer_text.config(state=tk.NORMAL)
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.config(state=tk.DISABLED)
        
        # ステータスをリセット
        self.set_status("待機中")
    
    def show(self):
        """ウィンドウを表示"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def hide(self):
        """ウィンドウを非表示"""
        self.root.withdraw()
    
    def run(self):
        """UIのメインループを実行"""
        self.root.mainloop()
    
    def set_status(self, status: str):
        """ステータスを設定"""
        def update():
            self.status_label.config(text=status)
        
        if threading.current_thread() == threading.main_thread():
            update()
        else:
            self.root.after(0, update)
    
    def set_function_status(self, function: str, available: bool):
        """機能の有効/無効状態を設定"""
        def update():
            if function in self.function_labels:
                status_text = "✅" if available else "❌"
                current_text = self.function_labels[function].cget('text')
                new_text = current_text.split(':')[0] + f": {status_text}"
                self.function_labels[function].config(text=new_text)
            
            # 音声ボタンの状態を更新
            if function == 'speech':
                self.speech_available = available
                self.voice_button.config(
                    state=tk.NORMAL if available else tk.DISABLED
                )
            
            # ホットキーラベルの表示を更新
            if function == 'hotkey':
                self.hotkey_available = available
                self.hotkey_label.config(
                    fg='white' if available else 'gray'
                )
        
        if threading.current_thread() == threading.main_thread():
            update()
        else:
            self.root.after(0, update)
    
    def set_question_text(self, text: str):
        """質問テキストを設定"""
        def update():
            self.question_text.delete(1.0, tk.END)
            self.question_text.insert(1.0, text)
            self.question_text.config(fg='black')
        
        if threading.current_thread() == threading.main_thread():
            update()
        else:
            self.root.after(0, update)
    
    def set_answer(self, answer: str):
        """回答を設定"""
        def update():
            self.answer_text.config(state=tk.NORMAL)
            self.answer_text.delete(1.0, tk.END)
            self.answer_text.insert(1.0, answer)
            self.answer_text.config(state=tk.DISABLED)
        
        if threading.current_thread() == threading.main_thread():
            update()
        else:
            self.root.after(0, update)
    
    def append_answer(self, text: str):
        """回答に追記"""
        def update():
            self.answer_text.config(state=tk.NORMAL)
            self.answer_text.insert(tk.END, text)
            self.answer_text.see(tk.END)
            self.answer_text.config(state=tk.DISABLED)
        
        if threading.current_thread() == threading.main_thread():
            update()
        else:
            self.root.after(0, update)


# テスト用のメイン関数
if __name__ == "__main__":
    def test_question_callback(question):
        print(f"テスト: 質問が送信されました - {question}")
        ui.set_answer(f"テスト回答: {question}に対する回答です。")
    
    def test_close_callback():
        print("テスト: アプリケーションを終了します")
        import sys
        sys.exit(0)
    
    def test_screenshot_callback():
        print("テスト: スクリーンショット撮影が要求されました")
        ui.set_status("スクリーンショットを撮影しました")
    
    # テスト実行
    ui = UIModuleImproved(test_question_callback, test_close_callback, test_screenshot_callback)
    
    # 機能状態をテスト
    ui.set_function_status('hotkey', True)
    ui.set_function_status('speech', False)
    ui.set_function_status('ai', True)
    
    ui.show()
    
    print("改良版UIテストを開始しました")
    ui.run()
