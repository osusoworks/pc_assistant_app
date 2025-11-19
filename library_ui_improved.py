#!/usr/bin/env python3
"""
改善されたライブラリUI - お気に入り一覧ウィンドウ
より使いやすく、視覚的に魅力的なお気に入り管理UI
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
from typing import List, Dict, Optional
from simple_library import SimpleLibrary
import datetime


class ImprovedLibraryUI:
    """改善されたお気に入り一覧ウィンドウ"""
    
    def __init__(self, parent_window: Optional[tk.Tk] = None):
        """初期化"""
        self.parent_window = parent_window
        self.window: Optional[tk.Toplevel] = None
        self.library = SimpleLibrary()
        self.favorites_tree: Optional[ttk.Treeview] = None
        self.detail_text: Optional[tk.Text] = None
        self.search_var: Optional[tk.StringVar] = None
        
        # スタイル設定
        self.colors = {
            'primary': '#4ECDC4',
            'secondary': '#45B7B8',
            'accent': '#F6AD55',
            'success': '#68D391',
            'warning': '#F6E05E',
            'error': '#FC8181',
            'text': '#2D3748',
            'bg': '#F7FAFC',
            'card': '#FFFFFF'
        }
        
        print("改善されたライブラリUIが初期化されました")
    
    def show_favorites_window(self):
        """お気に入り一覧ウィンドウを表示"""
        try:
            if self.window and self.window.winfo_exists():
                self.window.lift()
                self.window.focus_force()
                return
            
            self._create_window()
            self._setup_styles()
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
        
        self.window.title("📚 お気に入り管理 - SENPAI")
        self.window.geometry("1000x700")
        self.window.resizable(True, True)
        self.window.configure(bg=self.colors['bg'])
        
        # アイコン設定（可能な場合）
        try:
            self.window.iconname("SENPAI")
        except:
            pass
        
        if self.parent_window:
            self.window.transient(self.parent_window)
            # 中央に配置
            self.window.geometry("+%d+%d" % (
                self.parent_window.winfo_rootx() + 100,
                self.parent_window.winfo_rooty() + 50
            ))
    
    def _setup_styles(self):
        """スタイルを設定"""
        style = ttk.Style()
        
        # カスタムスタイルを定義
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       foreground=self.colors['text'],
                       background=self.colors['bg'])
        
        style.configure('Subtitle.TLabel',
                       font=('Arial', 10),
                       foreground=self.colors['text'],
                       background=self.colors['bg'])
        
        style.configure('Primary.TButton',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Success.TButton',
                       font=('Arial', 10))
        
        style.configure('Warning.TButton',
                       font=('Arial', 10))
    
    def _create_widgets(self):
        """ウィジェットを作成"""
        # メインフレーム
        main_frame = tk.Frame(self.window, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # ヘッダー部分
        self._create_header(main_frame)
        
        # 検索・フィルター部分
        self._create_search_section(main_frame)
        
        # メインコンテンツ部分
        self._create_content_section(main_frame)
        
        # フッター部分
        self._create_footer(main_frame)
    
    def _create_header(self, parent):
        """ヘッダー部分を作成"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # タイトル
        title_label = ttk.Label(header_frame, text="📚 お気に入り管理", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # 統計情報
        self.stats_label = ttk.Label(header_frame, text="", style='Subtitle.TLabel')
        self.stats_label.pack(side=tk.RIGHT)
    
    def _create_search_section(self, parent):
        """検索・フィルター部分を作成"""
        search_frame = tk.Frame(parent, bg=self.colors['card'], relief=tk.RAISED, bd=1)
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        search_inner = tk.Frame(search_frame, bg=self.colors['card'])
        search_inner.pack(fill=tk.X, padx=15, pady=10)
        
        # 検索ラベル
        search_label = ttk.Label(search_inner, text="🔍 検索・フィルター", 
                                font=('Arial', 11, 'bold'),
                                background=self.colors['card'])
        search_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 検索入力フレーム
        search_input_frame = tk.Frame(search_inner, bg=self.colors['card'])
        search_input_frame.pack(fill=tk.X)
        
        # 検索入力
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_input_frame, textvariable=self.search_var, 
                                font=('Arial', 10), width=40)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind('<KeyRelease>', self._on_search)
        
        # 検索ボタン
        search_button = ttk.Button(search_input_frame, text="🔍 検索", 
                                  command=self._on_search, style='Primary.TButton')
        search_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # クリアボタン
        clear_button = ttk.Button(search_input_frame, text="🗑️ クリア", 
                                 command=self._clear_search)
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 更新ボタン
        refresh_button = ttk.Button(search_input_frame, text="🔄 更新", 
                                   command=self._load_favorites, style='Success.TButton')
        refresh_button.pack(side=tk.RIGHT)
    
    def _create_content_section(self, parent):
        """メインコンテンツ部分を作成"""
        content_frame = tk.Frame(parent, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左側：お気に入り一覧（Treeview使用）
        left_frame = tk.Frame(content_frame, bg=self.colors['card'], relief=tk.RAISED, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self._create_favorites_list(left_frame)
        
        # 右側：詳細表示
        right_frame = tk.Frame(content_frame, bg=self.colors['card'], relief=tk.RAISED, bd=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self._create_detail_view(right_frame)
    
    def _create_favorites_list(self, parent):
        """お気に入り一覧を作成"""
        # ヘッダー
        list_header = tk.Frame(parent, bg=self.colors['card'])
        list_header.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        ttk.Label(list_header, text="📋 お気に入り一覧", 
                 font=('Arial', 11, 'bold'),
                 background=self.colors['card']).pack(side=tk.LEFT)
        
        # Treeviewフレーム
        tree_frame = tk.Frame(parent, bg=self.colors['card'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Treeview作成
        columns = ('tag', 'question', 'date')
        self.favorites_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # カラムヘッダー設定
        self.favorites_tree.heading('tag', text='🏷️ タグ')
        self.favorites_tree.heading('question', text='❓ 質問')
        self.favorites_tree.heading('date', text='📅 作成日')
        
        # カラム幅設定
        self.favorites_tree.column('tag', width=100, minwidth=80)
        self.favorites_tree.column('question', width=250, minwidth=200)
        self.favorites_tree.column('date', width=120, minwidth=100)
        
        # スクロールバー
        tree_scrollbar_v = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.favorites_tree.yview)
        tree_scrollbar_h = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.favorites_tree.xview)
        self.favorites_tree.configure(yscrollcommand=tree_scrollbar_v.set, xscrollcommand=tree_scrollbar_h.set)
        
        # 配置
        self.favorites_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
        
        # イベントバインド
        self.favorites_tree.bind('<<TreeviewSelect>>', self._on_select_favorite)
        self.favorites_tree.bind('<Double-1>', self._on_double_click)
        
        # 操作ボタンフレーム
        button_frame = tk.Frame(parent, bg=self.colors['card'])
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 削除ボタン
        delete_button = ttk.Button(button_frame, text="🗑️ 削除", 
                                  command=self._delete_selected_favorite,
                                  style='Warning.TButton')
        delete_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # エクスポートボタン（将来の機能）
        export_button = ttk.Button(button_frame, text="📤 エクスポート", 
                                  command=self._export_favorites,
                                  state=tk.DISABLED)
        export_button.pack(side=tk.LEFT, padx=(0, 5))
    
    def _create_detail_view(self, parent):
        """詳細表示部分を作成"""
        # ヘッダー
        detail_header = tk.Frame(parent, bg=self.colors['card'])
        detail_header.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        ttk.Label(detail_header, text="📄 詳細情報", 
                 font=('Arial', 11, 'bold'),
                 background=self.colors['card']).pack(side=tk.LEFT)
        
        # 詳細テキストフレーム
        detail_frame = tk.Frame(parent, bg=self.colors['card'])
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # テキストウィジェット
        self.detail_text = tk.Text(detail_frame, wrap=tk.WORD, font=('Arial', 10), 
                                  state=tk.DISABLED, bg='#FAFAFA', relief=tk.SUNKEN, bd=1)
        self.detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # スクロールバー
        detail_scrollbar = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL, command=self.detail_text.yview)
        detail_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.detail_text.configure(yscrollcommand=detail_scrollbar.set)
        
        # 詳細操作ボタン
        detail_button_frame = tk.Frame(parent, bg=self.colors['card'])
        detail_button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # コピーボタン
        copy_button = ttk.Button(detail_button_frame, text="📋 回答をコピー", 
                                command=self._copy_answer)
        copy_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 編集ボタン（将来の機能）
        edit_button = ttk.Button(detail_button_frame, text="✏️ 編集", 
                                command=self._edit_favorite,
                                state=tk.DISABLED)
        edit_button.pack(side=tk.LEFT)
    
    def _create_footer(self, parent):
        """フッター部分を作成"""
        footer_frame = tk.Frame(parent, bg=self.colors['bg'])
        footer_frame.pack(fill=tk.X, pady=(15, 0))
        
        # 左側：統計情報詳細
        self.detail_stats_label = ttk.Label(footer_frame, text="", style='Subtitle.TLabel')
        self.detail_stats_label.pack(side=tk.LEFT)
        
        # 右側：閉じるボタン
        close_button = ttk.Button(footer_frame, text="❌ 閉じる", 
                                 command=self._close_window,
                                 style='Primary.TButton')
        close_button.pack(side=tk.RIGHT)
    
    def _load_favorites(self):
        """お気に入り一覧を読み込み"""
        try:
            # Treeviewをクリア
            if self.favorites_tree:
                for item in self.favorites_tree.get_children():
                    self.favorites_tree.delete(item)
            
            # お気に入りを取得
            favorites = self.library.get_favorites_list()
            
            # Treeviewに追加
            for favorite in favorites:
                created_at = favorite.get('created_at', '')[:16].replace('T', ' ')
                tag = favorite.get('tag', '未分類')
                question = favorite.get('question', '質問なし')
                
                # 質問を短縮表示
                display_question = question[:50] + "..." if len(question) > 50 else question
                
                item_id = self.favorites_tree.insert('', tk.END, 
                                                    values=(tag, display_question, created_at))
                # 元のデータをitemに関連付け
                self.favorites_tree.set(item_id, 'full_data', favorite['id'])
            
            # 統計情報を更新
            count = len(favorites)
            self.stats_label.config(text=f"📊 総数: {count}件")
            
            # タグ別統計
            tag_stats = {}
            for favorite in favorites:
                tag = favorite.get('tag', '未分類')
                tag_stats[tag] = tag_stats.get(tag, 0) + 1
            
            if tag_stats:
                top_tags = sorted(tag_stats.items(), key=lambda x: x[1], reverse=True)[:3]
                tag_info = " | ".join([f"{tag}: {count}件" for tag, count in top_tags])
                self.detail_stats_label.config(text=f"人気タグ: {tag_info}")
            
            # 詳細をクリア
            self._clear_detail()
            
            print(f"お気に入り一覧を読み込みました: {count}件")
            
        except Exception as e:
            print(f"お気に入り読み込みエラー: {e}")
            messagebox.showerror("エラー", f"お気に入りの読み込みに失敗しました: {e}")
    
    def _on_search(self, event=None):
        """検索処理"""
        try:
            search_text = self.search_var.get().lower()
            
            # Treeviewをクリア
            for item in self.favorites_tree.get_children():
                self.favorites_tree.delete(item)
            
            # 全お気に入りを取得
            all_favorites = self.library.get_favorites_list()
            
            # フィルタリングして表示
            filtered_count = 0
            for favorite in all_favorites:
                question = favorite.get('question', '').lower()
                tag = favorite.get('tag', '').lower()
                
                if not search_text or search_text in question or search_text in tag:
                    created_at = favorite.get('created_at', '')[:16].replace('T', ' ')
                    tag_display = favorite.get('tag', '未分類')
                    question_display = favorite.get('question', '質問なし')
                    
                    # 質問を短縮表示
                    display_question = question_display[:50] + "..." if len(question_display) > 50 else question_display
                    
                    item_id = self.favorites_tree.insert('', tk.END, 
                                                        values=(tag_display, display_question, created_at))
                    self.favorites_tree.set(item_id, 'full_data', favorite['id'])
                    filtered_count += 1
            
            # 統計情報を更新
            total_count = len(all_favorites)
            if search_text:
                self.stats_label.config(text=f"📊 検索結果: {filtered_count}件 / 総数: {total_count}件")
            else:
                self.stats_label.config(text=f"📊 総数: {total_count}件")
                
        except Exception as e:
            print(f"検索エラー: {e}")
    
    def _clear_search(self):
        """検索をクリア"""
        if self.search_var:
            self.search_var.set("")
            self._load_favorites()
    
    def _on_select_favorite(self, event):
        """お気に入り選択時の処理"""
        try:
            selection = self.favorites_tree.selection()
            if not selection:
                return
            
            # 選択されたアイテムのIDを取得
            item = selection[0]
            favorite_id = self.favorites_tree.set(item, 'full_data')
            
            if favorite_id:
                self._show_favorite_detail(favorite_id)
                
        except Exception as e:
            print(f"お気に入り選択エラー: {e}")
    
    def _on_double_click(self, event):
        """ダブルクリック時の処理"""
        # 現在は選択時と同じ処理
        self._on_select_favorite(event)
    
    def _show_favorite_detail(self, favorite_id: str):
        """お気に入りの詳細を表示"""
        try:
            favorite = self.library.get_favorite(favorite_id)
            if not favorite:
                self._clear_detail()
                return
            
            # 詳細テキストを更新
            self.detail_text.config(state=tk.NORMAL)
            self.detail_text.delete(1.0, tk.END)
            
            # スタイル付きで詳細情報を構築
            self.detail_text.insert(tk.END, "📝 質問\\n", "header")
            self.detail_text.insert(tk.END, f"{favorite.get('question', '質問なし')}\\n\\n", "content")
            
            self.detail_text.insert(tk.END, "💡 回答\\n", "header")
            self.detail_text.insert(tk.END, f"{favorite.get('answer', '回答なし')}\\n\\n", "content")
            
            self.detail_text.insert(tk.END, "🏷️ タグ\\n", "header")
            self.detail_text.insert(tk.END, f"{favorite.get('tag', '未分類')}\\n\\n", "tag")
            
            self.detail_text.insert(tk.END, "📅 作成日時\\n", "header")
            created_at = favorite.get('created_at', '不明')[:19].replace('T', ' ')
            self.detail_text.insert(tk.END, f"{created_at}\\n\\n", "content")
            
            if favorite.get('screenshot_path'):
                self.detail_text.insert(tk.END, "📷 スクリーンショット\\n", "header")
                self.detail_text.insert(tk.END, f"{favorite['screenshot_path']}\\n", "path")
            
            # テキストスタイルを設定
            self.detail_text.tag_configure("header", font=('Arial', 10, 'bold'), foreground='#2D3748')
            self.detail_text.tag_configure("content", font=('Arial', 10), foreground='#4A5568')
            self.detail_text.tag_configure("tag", font=('Arial', 10), foreground='#38B2AC', background='#E6FFFA')
            self.detail_text.tag_configure("path", font=('Arial', 9), foreground='#718096', style='italic')
            
            self.detail_text.config(state=tk.DISABLED)
            
            # 現在選択中のお気に入りを保存（コピー機能用）
            self.current_favorite = favorite
            
        except Exception as e:
            print(f"詳細表示エラー: {e}")
            self._clear_detail()
    
    def _clear_detail(self):
        """詳細表示をクリア"""
        try:
            if self.detail_text:
                self.detail_text.config(state=tk.NORMAL)
                self.detail_text.delete(1.0, tk.END)
                self.detail_text.insert(1.0, "お気に入りを選択してください\\n\\n左側の一覧から項目を選択すると、詳細情報がここに表示されます。")
                self.detail_text.config(state=tk.DISABLED)
                
            self.current_favorite = None
        except Exception as e:
            print(f"詳細クリアエラー: {e}")
    
    def _delete_selected_favorite(self):
        """選択されたお気に入りを削除"""
        try:
            selection = self.favorites_tree.selection()
            if not selection:
                messagebox.showwarning("警告", "削除するお気に入りを選択してください")
                return
            
            # 削除確認
            item = selection[0]
            values = self.favorites_tree.item(item)['values']
            question = values[1] if len(values) > 1 else "選択された項目"
            
            result = messagebox.askyesno(
                "削除確認", 
                f"以下のお気に入りを削除しますか？\\n\\n質問: {question}\\n\\n⚠️ この操作は取り消せません。"
            )
            if not result:
                return
            
            # 選択されたお気に入りIDを取得
            favorite_id = self.favorites_tree.set(item, 'full_data')
            
            if favorite_id:
                # 削除実行
                if self.library.delete_favorite(favorite_id):
                    messagebox.showinfo("成功", "お気に入りを削除しました")
                    # 一覧を再読み込み
                    self._load_favorites()
                else:
                    messagebox.showerror("エラー", "お気に入りの削除に失敗しました")
                    
        except Exception as e:
            print(f"お気に入り削除エラー: {e}")
            messagebox.showerror("エラー", f"お気に入りの削除に失敗しました: {e}")
    
    def _copy_answer(self):
        """回答をクリップボードにコピー"""
        try:
            if hasattr(self, 'current_favorite') and self.current_favorite:
                answer = self.current_favorite.get('answer', '')
                if answer:
                    self.window.clipboard_clear()
                    self.window.clipboard_append(answer)
                    messagebox.showinfo("成功", "回答をクリップボードにコピーしました")
                else:
                    messagebox.showwarning("警告", "コピーする回答がありません")
            else:
                messagebox.showwarning("警告", "お気に入りを選択してください")
        except Exception as e:
            print(f"コピーエラー: {e}")
            messagebox.showerror("エラー", f"コピーに失敗しました: {e}")
    
    def _export_favorites(self):
        """お気に入りをエクスポート（将来の機能）"""
        messagebox.showinfo("情報", "エクスポート機能は今後のバージョンで実装予定です")
    
    def _edit_favorite(self):
        """お気に入りを編集（将来の機能）"""
        messagebox.showinfo("情報", "編集機能は今後のバージョンで実装予定です")
    
    def _close_window(self):
        """ウィンドウを閉じる"""
        try:
            if self.window:
                self.window.destroy()
                self.window = None
                print("改善されたお気に入りウィンドウを閉じました")
        except Exception as e:
            print(f"ウィンドウ終了エラー: {e}")


class ImprovedFavoriteSaveDialog:
    """改善されたお気に入り保存ダイアログ"""
    
    def __init__(self, parent_window: tk.Tk, question: str, answer: str):
        self.parent_window = parent_window
        self.question = question
        self.answer = answer
        self.result = None
        self.dialog: Optional[tk.Toplevel] = None
        
        # よく使われるタグの候補
        self.tag_suggestions = [
            "ボタンクリック", "ファイル操作", "設定変更", "ショートカット",
            "テキスト入力", "メニュー操作", "ウィンドウ操作", "検索",
            "コピー・貼り付け", "保存", "印刷", "その他"
        ]
    
    def show_dialog(self) -> Optional[str]:
        """ダイアログを表示してタグを取得"""
        try:
            self.dialog = tk.Toplevel(self.parent_window)
            self.dialog.title("⭐ お気に入りに保存")
            self.dialog.geometry("500x400")
            self.dialog.resizable(False, False)
            self.dialog.transient(self.parent_window)
            self.dialog.grab_set()
            self.dialog.configure(bg='#F7FAFC')
            
            # 中央に配置
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
        main_frame = tk.Frame(self.dialog, bg='#F7FAFC')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # タイトル
        title_label = tk.Label(main_frame, text="⭐ お気に入りに保存", 
                              font=('Arial', 14, 'bold'),
                              bg='#F7FAFC', fg='#2D3748')
        title_label.pack(pady=(0, 20))
        
        # 質問プレビュー
        question_frame = tk.LabelFrame(main_frame, text="📝 質問", 
                                      font=('Arial', 10, 'bold'),
                                      bg='#F7FAFC', fg='#2D3748')
        question_frame.pack(fill=tk.X, pady=(0, 15))
        
        question_text = tk.Text(question_frame, height=4, wrap=tk.WORD, 
                               state=tk.DISABLED, font=('Arial', 9),
                               bg='#FAFAFA', relief=tk.SUNKEN, bd=1)
        question_text.pack(fill=tk.X, padx=10, pady=10)
        question_text.config(state=tk.NORMAL)
        question_text.insert(1.0, self.question)
        question_text.config(state=tk.DISABLED)
        
        # タグ入力セクション
        tag_frame = tk.LabelFrame(main_frame, text="🏷️ タグ（分類用）", 
                                 font=('Arial', 10, 'bold'),
                                 bg='#F7FAFC', fg='#2D3748')
        tag_frame.pack(fill=tk.X, pady=(0, 15))
        
        # タグ入力
        tag_input_frame = tk.Frame(tag_frame, bg='#F7FAFC')
        tag_input_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.tag_var = tk.StringVar()
        self.tag_entry = tk.Entry(tag_input_frame, textvariable=self.tag_var, 
                                 font=('Arial', 11), relief=tk.SUNKEN, bd=1)
        self.tag_entry.pack(fill=tk.X)
        self.tag_entry.focus_set()
        
        # タグ候補ボタン
        suggestions_label = tk.Label(tag_frame, text="💡 よく使われるタグ:", 
                                   font=('Arial', 9),
                                   bg='#F7FAFC', fg='#4A5568')
        suggestions_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # タグ候補ボタンフレーム
        suggestions_frame = tk.Frame(tag_frame, bg='#F7FAFC')
        suggestions_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # タグ候補ボタンを3列で配置
        for i, tag in enumerate(self.tag_suggestions):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(suggestions_frame, text=tag, 
                           font=('Arial', 8),
                           bg='#E2E8F0', fg='#2D3748',
                           relief=tk.RAISED, bd=1,
                           command=lambda t=tag: self._select_tag(t))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
        
        # 列の重みを設定
        for i in range(3):
            suggestions_frame.columnconfigure(i, weight=1)
        
        # 例
        example_label = tk.Label(tag_frame, 
                               text="💭 例: ボタンクリック, ファイル操作, 設定変更", 
                               font=('Arial', 8),
                               bg='#F7FAFC', fg='#718096')
        example_label.pack(padx=10, pady=(0, 10))
        
        # ボタンフレーム
        button_frame = tk.Frame(main_frame, bg='#F7FAFC')
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # キャンセルボタン
        cancel_button = tk.Button(button_frame, text="❌ キャンセル", 
                                 font=('Arial', 10),
                                 bg='#FC8181', fg='white',
                                 relief=tk.RAISED, bd=2,
                                 command=self._cancel)
        cancel_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 保存ボタン
        save_button = tk.Button(button_frame, text="⭐ 保存", 
                               font=('Arial', 10, 'bold'),
                               bg='#68D391', fg='white',
                               relief=tk.RAISED, bd=2,
                               command=self._save)
        save_button.pack(side=tk.RIGHT)
        
        # キーバインド
        self.dialog.bind('<Return>', lambda e: self._save())
        self.dialog.bind('<Escape>', lambda e: self._cancel())
    
    def _select_tag(self, tag: str):
        """タグ候補を選択"""
        self.tag_var.set(tag)
        self.tag_entry.focus_set()
    
    def _save(self):
        """保存処理"""
        tag = self.tag_var.get().strip()
        if not tag:
            messagebox.showwarning("警告", "タグを入力してください")
            return
        
        self.result = tag
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
    
    library_ui = ImprovedLibraryUI(root)
    
    test_button = tk.Button(root, text="📚 改善されたお気に入り一覧を開く", 
                           command=library_ui.show_favorites_window)
    test_button.pack(pady=50)
    
    root.mainloop()
