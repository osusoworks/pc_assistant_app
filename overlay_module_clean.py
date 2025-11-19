#!/usr/bin/env python3
"""
SENPAI クリーン矢印オーバーレイモジュール
影除去と先端の三角形修正を行った改善版
"""

import tkinter as tk
import math
import threading
import time
from typing import Tuple, Optional


class CleanOverlayModule:
    """クリーン矢印オーバーレイモジュールクラス"""
    
    def __init__(self):
        """初期化"""
        self.overlay_window = None
        self.canvas = None
        self.arrow_items = []
        self.is_visible = False
        
        # 矢印のデザイン仕様
        self.arrow_color = "#FF4444"  # 鮮やかな赤
        self.arrow_width = 3          # 線幅
        self.arrow_length = 60        # 全長
        self.shaft_length = 40        # 軸線の長さ
        self.head_length = 20         # 三角形部分の長さ
        self.head_width = 16          # 三角形の幅
        
        print("クリーン矢印オーバーレイモジュールが初期化されました")
    
    def _create_overlay_window(self):
        """オーバーレイウィンドウを作成"""
        if self.overlay_window is not None:
            return
        
        try:
            # トップレベルウィンドウを作成
            self.overlay_window = tk.Toplevel()
            
            # ウィンドウ設定
            self.overlay_window.title("SENPAI Overlay")
            self.overlay_window.attributes('-topmost', True)  # 最前面
            self.overlay_window.attributes('-transparentcolor', 'white')  # 透明色
            self.overlay_window.overrideredirect(True)  # ウィンドウ装飾を除去
            
            # 画面全体をカバー
            screen_width = self.overlay_window.winfo_screenwidth()
            screen_height = self.overlay_window.winfo_screenheight()
            self.overlay_window.geometry(f"{screen_width}x{screen_height}+0+0")
            
            # キャンバスを作成
            self.canvas = tk.Canvas(
                self.overlay_window,
                width=screen_width,
                height=screen_height,
                bg='white',  # 透明色として設定
                highlightthickness=0
            )
            self.canvas.pack(fill=tk.BOTH, expand=True)
            
            # 初期状態では非表示
            self.overlay_window.withdraw()
            
            print(f"オーバーレイウィンドウを作成: {screen_width}x{screen_height}")
            
        except Exception as e:
            print(f"オーバーレイウィンドウ作成エラー: {e}")
            self.overlay_window = None
            self.canvas = None
    
    def _calculate_arrow_points(self, x: float, y: float, angle: float = 0) -> Tuple[list, list]:
        """
        矢印の座標を計算
        
        Args:
            x: 矢印の開始点X座標
            y: 矢印の開始点Y座標
            angle: 矢印の角度（ラジアン）
        
        Returns:
            (軸線座標, 三角形座標)
        """
        # 角度の計算
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        # 軸線の座標
        shaft_end_x = x + self.shaft_length * cos_a
        shaft_end_y = y + self.shaft_length * sin_a
        shaft_coords = [x, y, shaft_end_x, shaft_end_y]
        
        # 三角形の頂点（矢印の先端）
        head_tip_x = x + self.arrow_length * cos_a
        head_tip_y = y + self.arrow_length * sin_a
        
        # 三角形の基部（軸線の終端から垂直方向に展開）
        perp_cos = math.cos(angle + math.pi / 2)  # 垂直方向
        perp_sin = math.sin(angle + math.pi / 2)
        
        half_width = self.head_width / 2
        head_left_x = shaft_end_x + half_width * perp_cos
        head_left_y = shaft_end_y + half_width * perp_sin
        head_right_x = shaft_end_x - half_width * perp_cos
        head_right_y = shaft_end_y - half_width * perp_sin
        
        # 三角形の座標（時計回り）
        head_coords = [
            head_tip_x, head_tip_y,    # 先端
            head_left_x, head_left_y,  # 左基部
            head_right_x, head_right_y # 右基部
        ]
        
        return shaft_coords, head_coords
    
    def show_arrow(self, x: int, y: int, angle: float = 0):
        """
        矢印を表示
        
        Args:
            x: 矢印の開始点X座標
            y: 矢印の開始点Y座標
            angle: 矢印の角度（度数法、デフォルトは右向き）
        """
        try:
            # オーバーレイウィンドウを作成（未作成の場合）
            if self.overlay_window is None:
                self._create_overlay_window()
            
            if self.canvas is None:
                print("❌ キャンバスが利用できません")
                return
            
            # 角度を度数法からラジアンに変換
            angle_rad = math.radians(angle)
            
            # 既存の矢印をクリア
            self.clear_arrows()
            
            # 矢印の座標を計算
            shaft_coords, head_coords = self._calculate_arrow_points(x, y, angle_rad)
            
            print(f"矢印表示: 座標({x}, {y}), 角度{angle}度")
            print(f"軸線座標: {shaft_coords}")
            print(f"三角形座標: {head_coords}")
            
            # 軸線を描画（影なし、クリーンな線）
            shaft_item = self.canvas.create_line(
                shaft_coords,
                fill=self.arrow_color,
                width=self.arrow_width,
                smooth=True,
                capstyle=tk.ROUND
            )
            self.arrow_items.append(shaft_item)
            
            # 三角形を描画（影なし、塗りつぶし）
            head_item = self.canvas.create_polygon(
                head_coords,
                fill=self.arrow_color,
                outline=self.arrow_color,
                width=1,
                smooth=True
            )
            self.arrow_items.append(head_item)
            
            # オーバーレイを表示
            self.overlay_window.deiconify()
            self.overlay_window.lift()
            self.is_visible = True
            
            print(f"✅ クリーン矢印を表示しました（影なし、改善された先端）")
            
        except Exception as e:
            print(f"❌ 矢印表示エラー: {e}")
    
    def show_arrow_to_element(self, element_x: int, element_y: int, 
                            element_width: int = 50, element_height: int = 30):
        """
        要素に向かって矢印を表示
        
        Args:
            element_x: 要素のX座標
            element_y: 要素のY座標
            element_width: 要素の幅
            element_height: 要素の高さ
        """
        # 要素の中心座標
        center_x = element_x + element_width // 2
        center_y = element_y + element_height // 2
        
        # 矢印の開始点（要素の左側から指すように配置）
        arrow_start_x = element_x - self.arrow_length - 20
        arrow_start_y = center_y
        
        # 要素の中心に向かう角度を計算
        dx = center_x - arrow_start_x
        dy = center_y - arrow_start_y
        angle = math.degrees(math.atan2(dy, dx))
        
        # 矢印を表示
        self.show_arrow(arrow_start_x, arrow_start_y, angle)
    
    def clear_arrows(self):
        """矢印をクリア"""
        try:
            if self.canvas and self.arrow_items:
                for item in self.arrow_items:
                    self.canvas.delete(item)
                self.arrow_items.clear()
                print("矢印をクリアしました")
        except Exception as e:
            print(f"矢印クリアエラー: {e}")
    
    def hide(self):
        """オーバーレイを非表示"""
        try:
            if self.overlay_window:
                self.overlay_window.withdraw()
                self.is_visible = False
                print("🔄 オーバーレイを非表示にしました")
        except Exception as e:
            print(f"オーバーレイ非表示エラー: {e}")
    
    def show(self):
        """オーバーレイを表示"""
        try:
            if self.overlay_window:
                self.overlay_window.deiconify()
                self.overlay_window.lift()
                self.is_visible = True
                print("🔄 オーバーレイを表示しました")
        except Exception as e:
            print(f"オーバーレイ表示エラー: {e}")
    
    def hide_overlay(self):
        """オーバーレイを非表示（互換性のため）"""
        self.hide()
    
    def show_overlay(self):
        """オーバーレイを表示（互換性のため）"""
        self.show()
    
    def auto_hide_after_delay(self, delay_seconds: int = 10):
        """指定秒後に自動的に非表示"""
        def hide_after_delay():
            time.sleep(delay_seconds)
            if self.is_visible:
                self.hide()
                print(f"{delay_seconds}秒後に矢印を自動非表示にしました")
        
        threading.Thread(target=hide_after_delay, daemon=True).start()
    
    def destroy(self):
        """オーバーレイを破棄"""
        try:
            if self.overlay_window:
                self.overlay_window.destroy()
                self.overlay_window = None
                self.canvas = None
                self.arrow_items.clear()
                self.is_visible = False
                print("オーバーレイを破棄しました")
        except Exception as e:
            print(f"オーバーレイ破棄エラー: {e}")
    
    def get_screen_info(self) -> dict:
        """画面情報を取得"""
        try:
            if self.overlay_window is None:
                # 一時的なウィンドウで画面情報を取得
                temp_window = tk.Tk()
                temp_window.withdraw()
                
                screen_info = {
                    'width': temp_window.winfo_screenwidth(),
                    'height': temp_window.winfo_screenheight(),
                    'dpi_x': temp_window.winfo_fpixels('1i'),
                    'dpi_y': temp_window.winfo_fpixels('1i')
                }
                
                temp_window.destroy()
                return screen_info
            else:
                return {
                    'width': self.overlay_window.winfo_screenwidth(),
                    'height': self.overlay_window.winfo_screenheight(),
                    'dpi_x': self.overlay_window.winfo_fpixels('1i'),
                    'dpi_y': self.overlay_window.winfo_fpixels('1i')
                }
        except Exception as e:
            print(f"画面情報取得エラー: {e}")
            return {'width': 1920, 'height': 1080, 'dpi_x': 96, 'dpi_y': 96}


def main():
    """テスト用メイン関数"""
    def test_overlay():
        # ルートウィンドウを作成（オーバーレイのため）
        root = tk.Tk()
        root.title("オーバーレイテスト")
        root.geometry("400x300")
        
        # オーバーレイモジュールを作成
        overlay = CleanOverlayModule()
        
        def show_test_arrow():
            # 画面中央に矢印を表示
            screen_info = overlay.get_screen_info()
            center_x = screen_info['width'] // 2 - 100
            center_y = screen_info['height'] // 2
            
            overlay.show_arrow(center_x, center_y, 0)  # 右向き矢印
            overlay.auto_hide_after_delay(5)  # 5秒後に自動非表示
        
        def show_angled_arrow():
            # 斜め矢印を表示
            screen_info = overlay.get_screen_info()
            x = screen_info['width'] // 2 - 150
            y = screen_info['height'] // 2 - 100
            
            overlay.show_arrow(x, y, 45)  # 45度の矢印
            overlay.auto_hide_after_delay(5)
        
        def hide_arrow():
            overlay.hide()
        
        # テストボタン
        tk.Button(root, text="右向き矢印表示", command=show_test_arrow).pack(pady=10)
        tk.Button(root, text="斜め矢印表示", command=show_angled_arrow).pack(pady=10)
        tk.Button(root, text="矢印非表示", command=hide_arrow).pack(pady=10)
        
        # 終了時の処理
        def on_closing():
            overlay.destroy()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("クリーン矢印オーバーレイのテストを開始...")
        print("- 影なし")
        print("- 改善された三角形の先端")
        print("- 鮮やかな赤色")
        
        root.mainloop()
    
    test_overlay()


if __name__ == "__main__":
    main()
