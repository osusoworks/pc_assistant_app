#!/usr/bin/env python3
"""
ライブラリUI - お気に入り一覧ウィンドウ（修正版）
シンプルなtkinterベースのお気に入り管理UI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Optional
from simple_library import SimpleLibrary


class LibraryUI:
    """お気に入り一覧ウィンドウ"""
    
    def __init__(self, parent_window: Optional[tk.Tk] = None):
        """初期化"""
        self.parent_window = parent_window
        self.window: Optional[tk.Toplevel] = None
        self.library = SimpleLibrary()
        self.favorites_listbox: Optional[tk.Listbox] = None
        self.detail_text: Optional[tk.Text] = None
        
        print("ライブラリUIが初期化されました")
    
    def show_favorites_window(self):
        """お気に入り一覧ウィンドウを表示"""
        try:
            if self.window and self.window.winfo_exists():
                self.window.lift()
                self.window.focus_force()
                return
            
            self._create_window()
            self._create_widgets()
            self._load_favorites()
            
        except Exception as e:
            print(f"お気に入りウィンドウ表示エラー: {e}")
            messagebox.showerror("エラー", f"お気に入りウィンドウの表示に失敗しました: {e}")
    
    def _create_window(self):
        """ウィンドウを作成"""
        if self.parent_window:
            self.window = tk.Toplevel(self.parent_window)
        else:
            self.window = tk.Toplevel()
        
        self.window.title("📚 お気に入り一覧 - SENPAI")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        if self.parent_window:
            self.window.transient(self.parent_window)
            self.window.grab_set()
    
    def _create_widgets(self):
        """ウィジェットを作成"""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # タイトル
        title_label = ttk.Label(main_frame, text="📚 お気に入り一覧", font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # 上部フレーム
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 検索フレーム
        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(search_frame, text="🔍 検索:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.search_entry.bind('<KeyRelease>', self._on_search)
        
        # 更新ボタン
        refresh_button = ttk.Button(top_frame, text="🔄 更新", command=self._load_favorites)
        refresh_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # メインコンテンツフレーム
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左側：一覧
        left_frame = ttk.LabelFrame(content_frame, text="お気に入り一覧")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.favorites_listbox = tk.Listbox(listbox_frame, font=('Arial', 10))
        self.favorites_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.favorites_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.favorites_listbox.yview)
        
        self.favorites_listbox.bind('<<ListboxSelect>>', self._on_select_favorite)
        
        # 削除ボタン
        delete_button = ttk.Button(left_frame, text="🗑️ 削除", command=self._delete_selected_favorite)
        delete_button.pack(padx=5, pady=(0, 5))
        
        # 右側：詳細
        right_frame = ttk.LabelFrame(content_frame, text="詳細")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        detail_frame = ttk.Frame(right_frame)
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.detail_text = tk.Text(detail_frame, wrap=tk.WORD, font=('Arial', 10), state=tk.DISABLED)
        self.detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        detail_scrollbar = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL)
        detail_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.detail_text.config(yscrollcommand=detail_scrollbar.set)
        detail_scrollbar.config(command=self.detail_text.yview)
        
        # 下部フレーム
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.stats_label = ttk.Label(bottom_frame, text="")
        self.stats_label.pack(side=tk.LEFT)
        
        close_button = ttk.Button(bottom_frame, text="❌ 閉じる", command=self._close_window)
        close_button.pack(side=tk.RIGHT)
    
    def _load_favorites(self):
        """お気に入り一覧を読み込み"""
        try:
            if self.favorites_listbox:
                self.favorites_listbox.delete(0, tk.END)
            
            favorites = self.library.get_favorites_list()
            
            for favorite in favorites:
                created_at = favorite.get('created_at', '')[:16].replace('T', ' ')
                tag = favorite.get('tag', '未分類')
                question = favorite.get('question', '質問なし')
                
                display_text = f"[{tag}] {question} ({created_at})"
                self.favorites_listbox.insert(tk.END, display_text)
            
            count = len(favorites)
            self.stats_label.config(text=f"📊 総数: {count}件")
            self._clear_detail()
            
            print(f"お気に入り一覧を読み込みました: {count}件")
            
        except Exception as e:
            print(f"お気に入り読み込みエラー: {e}")
            messagebox.showerror("エラー", f"お気に入りの読み込みに失敗しました: {e}")
    
    def _on_search(self, event):
        """検索処理"""
        try:
            search_text = self.search_var.get().lower()
            all_favorites = self.library.get_favorites_list()
            
            self.favorites_listbox.delete(0, tk.END)
            
            filtered_count = 0
            for favorite in all_favorites:
                question = favorite.get('question', '').lower()
                tag = favorite.get('tag', '').lower()
                
                if search_text in question or search_text in tag:
                    created_at = favorite.get('created_at', '')[:16].replace('T', ' ')
                    tag_display = favorite.get('tag', '未分類')
                    question_display = favorite.get('question', '質問なし')
                    
                    display_text = f"[{tag_display}] {question_display} ({created_at})"
                    self.favorites_listbox.insert(tk.END, display_text)
                    filtered_count += 1
            
            total_count = len(all_favorites)
            if search_text:
                self.stats_label.config(text=f"📊 検索結果: {filtered_count}件 / 総数: {total_count}件")
            else:
                self.stats_label.config(text=f"📊 総数: {total_count}件")
                
        except Exception as e:
            print(f"検索エラー: {e}")
    
    def _on_select_favorite(self, event):
        """お気に入り選択時の処理"""
        try:
            selection = self.favorites_listbox.curselection()
            if not selection:
                return
            
            index = selection[0]
            search_text = self.search_var.get().lower()
            
            if search_text:
                all_favorites = self.library.get_favorites_list()
                filtered_favorites = []
                for favorite in all_favorites:
                    question = favorite.get('question', '').lower()
                    tag = favorite.get('tag', '').lower()
                    if search_text in question or search_text in tag:
                        filtered_favorites.append(favorite)
                favorites = filtered_favorites
            else:
                favorites = self.library.get_favorites_list()
            
            if index < len(favorites):
                favorite_id = favorites[index]['id']
                self._show_favorite_detail(favorite_id)
                
        except Exception as e:
            print(f"お気に入り選択エラー: {e}")
    
    def _show_favorite_detail(self, favorite_id: str):
        """お気に入りの詳細を表示"""
        try:
            favorite = self.library.get_favorite(favorite_id)
            if not favorite:
                self._clear_detail()
                return
            
            self.detail_text.config(state=tk.NORMAL)
            self.detail_text.delete(1.0, tk.END)
            
            detail_lines = []
            detail_lines.append("📝 質問:")
            detail_lines.append(favorite.get('question', '質問なし'))
            detail_lines.append("")
            detail_lines.append("💡 回答:")
            detail_lines.append(favorite.get('answer', '回答なし'))
            detail_lines.append("")
            detail_lines.append(f"🏷️ タグ: {favorite.get('tag', '未分類')}")
            detail_lines.append(f"📅 作成日時: {favorite.get('created_at', '不明')[:19].replace('T', ' ')}")
            
            if favorite.get('screenshot_path'):
                detail_lines.append(f"📷 スクリーンショット: {favorite['screenshot_path']}")
            
            detail_text = "\\n".join(detail_lines)
            self.detail_text.insert(1.0, detail_text)
            self.detail_text.config(state=tk.DISABLED)
            
        except Exception as e:
            print(f"詳細表示エラー: {e}")
            self._clear_detail()
    
    def _clear_detail(self):
        """詳細表示をクリア"""
        try:
            if self.detail_text:
                self.detail_text.config(state=tk.NORMAL)
                self.detail_text.delete(1.0, tk.END)
                self.detail_text.insert(1.0, "お気に入りを選択してください")
                self.detail_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"詳細クリアエラー: {e}")
    
    def _delete_selected_favorite(self):
        """選択されたお気に入りを削除"""
        try:
            selection = self.favorites_listbox.curselection()
            if not selection:
                messagebox.showwarning("警告", "削除するお気に入りを選択してください")
                return
            
            result = messagebox.askyesno("削除確認", "選択されたお気に入りを削除しますか？\\n\\nこの操作は取り消せません。")
            if not result:
                return
            
            index = selection[0]
            search_text = self.search_var.get().lower()
            
            if search_text:
                all_favorites = self.library.get_favorites_list()
                filtered_favorites = []
                for favorite in all_favorites:
                    question = favorite.get('question', '').lower()
                    tag = favorite.get('tag', '').lower()
                    if search_text in question or search_text in tag:
                        filtered_favorites.append(favorite)
                favorites = filtered_favorites
            else:
                favorites = self.library.get_favorites_list()
            
            if index < len(favorites):
                favorite_id = favorites[index]['id']
                
                if self.library.delete_favorite(favorite_id):
                    messagebox.showinfo("成功", "お気に入りを削除しました")
                    self._load_favorites()
                else:
                    messagebox.showerror("エラー", "お気に入りの削除に失敗しました")
                    
        except Exception as e:
            print(f"お気に入り削除エラー: {e}")
            messagebox.showerror("エラー", f"お気に入りの削除に失敗しました: {e}")
    
    def _close_window(self):
        """ウィンドウを閉じる"""
        try:
            if self.window:
                self.window.destroy()
                self.window = None
                print("お気に入りウィンドウを閉じました")
        except Exception as e:
            print(f"ウィンドウ終了エラー: {e}")


class FavoriteSaveDialog:
    """お気に入り保存ダイアログ"""
    
    def __init__(self, parent_window: tk.Tk, question: str, answer: str):
        self.parent_window = parent_window
        self.question = question
        self.answer = answer
        self.result = None
        self.dialog: Optional[tk.Toplevel] = None
    
    def show_dialog(self) -> Optional[str]:
        """ダイアログを表示してタグを取得"""
        try:
            self.dialog = tk.Toplevel(self.parent_window)
            self.dialog.title("⭐ お気に入りに保存")
            self.dialog.geometry("400x300")
            self.dialog.resizable(False, False)
            self.dialog.transient(self.parent_window)
            self.dialog.grab_set()
            
            self.dialog.geometry("+%d+%d" % (
                self.parent_window.winfo_rootx() + 50,
                self.parent_window.winfo_rooty() + 50
            ))
            
            self._create_dialog_widgets()
            self.dialog.wait_window()
            
            return self.result
            
        except Exception as e:
            print(f"お気に入り保存ダイアログエラー: {e}")
            return None
    
    def _create_dialog_widgets(self):
        """ダイアログのウィジェットを作成"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # タイトル
        title_label = ttk.Label(main_frame, text="⭐ お気に入りに保存", font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # 質問プレビュー
        question_frame = ttk.LabelFrame(main_frame, text="質問")
        question_frame.pack(fill=tk.X, pady=(0, 10))
        
        question_text = tk.Text(question_frame, height=3, wrap=tk.WORD, state=tk.DISABLED, font=('Arial', 9))
        question_text.pack(fill=tk.X, padx=5, pady=5)
        question_text.config(state=tk.NORMAL)
        question_text.insert(1.0, self.question)
        question_text.config(state=tk.DISABLED)
        
        # タグ入力
        tag_frame = ttk.LabelFrame(main_frame, text="タグ（分類用）")
        tag_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.tag_var = tk.StringVar()
        tag_entry = ttk.Entry(tag_frame, textvariable=self.tag_var, font=('Arial', 10))
        tag_entry.pack(fill=tk.X, padx=5, pady=5)
        tag_entry.focus_set()
        
        example_label = ttk.Label(tag_frame, text="例: ボタンクリック, ファイル操作, 設定変更", font=('Arial', 8), foreground='gray')
        example_label.pack(padx=5, pady=(0, 5))
        
        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        cancel_button = ttk.Button(button_frame, text="❌ キャンセル", command=self._cancel)
        cancel_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        save_button = ttk.Button(button_frame, text="⭐ 保存", command=self._save)
        save_button.pack(side=tk.RIGHT)
        
        self.dialog.bind('<Return>', lambda e: self._save())
        self.dialog.bind('<Escape>', lambda e: self._cancel())
    
    def _save(self):
        """保存処理"""
        self.result = self.tag_var.get().strip()
        if self.dialog:
            self.dialog.destroy()
    
    def _cancel(self):
        """キャンセル処理"""
        self.result = None
        if self.dialog:
            self.dialog.destroy()


if __name__ == "__main__":
    # テスト用
    root = tk.Tk()
    root.title("テスト")
    root.geometry("300x200")
    
    library_ui = LibraryUI(root)
    
    test_button = ttk.Button(root, text="📚 お気に入り一覧を開く", command=library_ui.show_favorites_window)
    test_button.pack(pady=50)
    
    root.mainloop()
