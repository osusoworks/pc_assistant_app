#!/usr/bin/env python3
"""
オーバーレイモジュール - 画面上への矢印表示
"""

import tkinter as tk
import math
import threading
from typing import Optional


class OverlayModule:
    """画面オーバーレイを担当するモジュール"""
    
    def __init__(self):
        """初期化"""
        self.overlay_window: Optional[tk.Toplevel] = None
        self.canvas: Optional[tk.Canvas] = None
        self.arrow_items = []
        
        print("オーバーレイモジュールが初期化されました")
    
    def show_arrow(self, x: int, y: int, size: int = 50):
        """
        指定された座標に赤い矢印を表示
        
        Args:
            x: X座標
            y: Y座標
            size: 矢印のサイズ
        """
        try:
            # メインスレッドで実行されることを確認
            if threading.current_thread() != threading.main_thread():
                # メインスレッドで実行するようにスケジュール
                tk._default_root.after(0, lambda: self.show_arrow(x, y, size))
                return
            
            # 既存のオーバーレイがあれば削除
            self.hide()
            
            # 新しいオーバーレイウィンドウを作成
            self._create_overlay_window()
            
            # 矢印を描画
            self._draw_arrow(x, y, size)
            
            print(f"矢印を表示しました: ({x}, {y})")
            
        except Exception as e:
            print(f"矢印表示エラー: {e}")
    
    def _create_overlay_window(self):
        """オーバーレイウィンドウを作成"""
        # ルートウィンドウが存在しない場合は作成
        if not tk._default_root:
            root = tk.Tk()
            root.withdraw()  # 非表示にする
        
        # オーバーレイウィンドウを作成
        self.overlay_window = tk.Toplevel()
        
        # ウィンドウの設定
        self.overlay_window.attributes('-topmost', True)  # 最前面に表示
        self.overlay_window.attributes('-transparentcolor', 'black')  # 黒を透明に
        self.overlay_window.overrideredirect(True)  # ウィンドウの枠を削除
        
        # 画面全体をカバー
        screen_width = self.overlay_window.winfo_screenwidth()
        screen_height = self.overlay_window.winfo_screenheight()
        self.overlay_window.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # キャンバスを作成
        self.canvas = tk.Canvas(
            self.overlay_window,
            width=screen_width,
            height=screen_height,
            bg='black',  # 透明色として黒を使用
            highlightthickness=0
        )
        self.canvas.pack()
        
        # クリックイベントを透過させる（Linux環境では制限あり）
        try:
            # Windowsの場合の設定
            self.overlay_window.wm_attributes('-transparentcolor', 'black')
        except:
            pass
    
    def _draw_arrow(self, x: int, y: int, size: int):
        """矢印を描画"""
        if not self.canvas:
            return
        
        # 矢印の色
        arrow_color = '#FF0000'  # 赤色
        outline_color = '#FFFFFF'  # 白色の縁取り
        
        # 矢印の形状を計算（下向きの矢印）
        arrow_points = self._calculate_arrow_points(x, y, size)
        
        # 縁取り付きの矢印を描画
        # 外側（縁取り）
        outline_arrow = self.canvas.create_polygon(
            arrow_points,
            fill=outline_color,
            outline=outline_color,
            width=3
        )
        
        # 内側（メイン）
        main_arrow = self.canvas.create_polygon(
            arrow_points,
            fill=arrow_color,
            outline=arrow_color,
            width=1
        )
        
        # 矢印アイテムを記録
        self.arrow_items = [outline_arrow, main_arrow]
        
        # パルス効果を追加
        self._add_pulse_effect(x, y, size)
    
    def _calculate_arrow_points(self, x: int, y: int, size: int) -> list:
        """矢印の座標点を計算"""
        # 下向きの矢印の形状
        half_size = size // 2
        quarter_size = size // 4
        
        points = [
            x, y - size,  # 上の頂点
            x - quarter_size, y - half_size,  # 左上
            x - quarter_size, y - quarter_size,  # 左中
            x - half_size, y - quarter_size,  # 左下
            x, y,  # 下の頂点
            x + half_size, y - quarter_size,  # 右下
            x + quarter_size, y - quarter_size,  # 右中
            x + quarter_size, y - half_size,  # 右上
        ]
        
        return points
    
    def _add_pulse_effect(self, x: int, y: int, size: int):
        """パルス効果を追加"""
        if not self.canvas:
            return
        
        # パルス用の円を描画
        pulse_radius = size // 2
        
        pulse_circle = self.canvas.create_oval(
            x - pulse_radius, y - pulse_radius,
            x + pulse_radius, y + pulse_radius,
            outline='#FF0000',
            width=2,
            fill=''
        )
        
        self.arrow_items.append(pulse_circle)
        
        # アニメーション効果
        self._animate_pulse(pulse_circle, x, y, pulse_radius)
    
    def _animate_pulse(self, item, x: int, y: int, initial_radius: int):
        """パルスアニメーション"""
        def pulse_step(step=0):
            if not self.canvas or step > 20:
                return
            
            try:
                # 半径を徐々に大きくする
                radius = initial_radius + (step * 3)
                alpha = max(0, 255 - (step * 12))  # 透明度を下げる
                
                # 円のサイズを更新
                self.canvas.coords(
                    item,
                    x - radius, y - radius,
                    x + radius, y + radius
                )
                
                # 次のステップをスケジュール
                self.overlay_window.after(100, lambda: pulse_step(step + 1))
                
            except:
                pass  # ウィンドウが閉じられた場合
        
        pulse_step()
    
    def hide(self):
        """オーバーレイを非表示"""
        try:
            if self.overlay_window:
                self.overlay_window.destroy()
                self.overlay_window = None
                self.canvas = None
                self.arrow_items = []
                
                print("オーバーレイを非表示にしました")
                
        except Exception as e:
            print(f"オーバーレイ非表示エラー: {e}")
    
    def show_multiple_arrows(self, coordinates_list: list):
        """
        複数の矢印を表示
        
        Args:
            coordinates_list: [(x1, y1), (x2, y2), ...] の座標リスト
        """
        try:
            # 既存のオーバーレイがあれば削除
            self.hide()
            
            # 新しいオーバーレイウィンドウを作成
            self._create_overlay_window()
            
            # 各座標に矢印を描画
            for i, (x, y) in enumerate(coordinates_list):
                self._draw_arrow(x, y, 40)  # 少し小さめのサイズ
                
                # 番号を表示
                number_text = self.canvas.create_text(
                    x, y + 60,
                    text=str(i + 1),
                    font=('Arial', 16, 'bold'),
                    fill='#FF0000',
                    anchor='center'
                )
                self.arrow_items.append(number_text)
            
            print(f"複数の矢印を表示しました: {len(coordinates_list)}個")
            
        except Exception as e:
            print(f"複数矢印表示エラー: {e}")
    
    def show_highlight_area(self, x1: int, y1: int, x2: int, y2: int):
        """
        指定された領域をハイライト表示
        
        Args:
            x1, y1: 左上座標
            x2, y2: 右下座標
        """
        try:
            # 既存のオーバーレイがあれば削除
            self.hide()
            
            # 新しいオーバーレイウィンドウを作成
            self._create_overlay_window()
            
            # ハイライト矩形を描画
            highlight_rect = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline='#FF0000',
                width=3,
                fill='',
                dash=(10, 5)  # 破線
            )
            
            self.arrow_items.append(highlight_rect)
            
            print(f"領域をハイライトしました: ({x1}, {y1}) - ({x2}, {y2})")
            
        except Exception as e:
            print(f"ハイライト表示エラー: {e}")


# テスト用のメイン関数
if __name__ == "__main__":
    import time
    
    # テスト実行
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示
    
    overlay = OverlayModule()
    
    print("オーバーレイテストを開始します")
    
    # 画面中央に矢印を表示
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    overlay.show_arrow(center_x, center_y, 60)
    
    print(f"画面中央 ({center_x}, {center_y}) に矢印を表示しました")
    print("5秒後に非表示になります")
    
    # 5秒後に非表示
    root.after(5000, overlay.hide)
    
    # 7秒後に複数矢印のテスト
    def test_multiple():
        coords = [
            (center_x - 100, center_y - 100),
            (center_x + 100, center_y - 100),
            (center_x, center_y + 100)
        ]
        overlay.show_multiple_arrows(coords)
        print("複数矢印を表示しました")
        
        # 5秒後に非表示
        root.after(5000, overlay.hide)
    
    root.after(7000, test_multiple)
    
    # メインループを実行
    root.mainloop()
