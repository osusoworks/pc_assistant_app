#!/usr/bin/env python3
"""
UIモジュール - ユーザーインターフェース
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Callable, Optional
import threading


class UIModule:
    """ユーザーインターフェースを担当するモジュール"""
    
    def __init__(self, question_callback: Callable[[str], None], 
                 close_callback: Callable[[], None]):
        """
        初期化
        
        Args:
            question_callback: 質問が送信された時のコールバック
            close_callback: アプリケーション終了時のコールバック
        """
        self.question_callback = question_callback
        self.close_callback = close_callback
        
        # メインウィンドウを作成
        self.root = tk.Tk()
        self.root.title("AI HELP")
        self.root.geometry("400x500")
        self.root.resizable(True, True)
        
        # ウィンドウを常に最前面に表示
        self.root.attributes('-topmost', True)
        
        # 終了時のイベントハンドラを設定
        self.root.protocol("WM_DELETE_WINDOW", self.close_callback)
        
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
        
        # ステータス表示
        status_frame = tk.Frame(main_frame, bg='#4ECDC4')
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            status_frame,
            text="Right Shift キーで音声入力:",
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
        
        # 質問送信ボタン
        self.send_button = tk.Button(
            main_frame,
            text="質問する",
            font=('Arial', 12, 'bold'),
            bg='#FF9F43',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self._send_question
        )
        self.send_button.pack(pady=(0, 10))
        
        # 回答表示エリア
        answer_label = tk.Label(
            main_frame,
            text="音声中:",
            font=('Arial', 10),
            bg='#4ECDC4',
            fg='white'
        )
        answer_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 回答表示テキストエリア
        self.answer_text = scrolledtext.ScrolledText(
            main_frame,
            height=12,
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
        
        # ボタンフレーム
        button_frame = tk.Frame(main_frame, bg='#4ECDC4')
        button_frame.pack(fill=tk.X)
        
        # クリアボタン
        clear_button = tk.Button(
            button_frame,
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
            button_frame,
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
        # テスト用の回答を設定
        ui.set_answer(f"テスト回答: {question}に対する回答です。")
    
    def test_close_callback():
        print("テスト: アプリケーションを終了します")
        import sys
        sys.exit(0)
    
    # テスト実行
    ui = UIModule(test_question_callback, test_close_callback)
    ui.show()
    
    print("UIテストを開始しました")
    ui.run()
