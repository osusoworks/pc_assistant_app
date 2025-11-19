#!/usr/bin/env python3
"""
オーバーレイモジュール（シンプル矢印・永続表示版）
ゲームチュートリアル風のシンプルな矢印デザインと永続表示機能を実装
"""

import tkinter as tk
import math
import threading
from typing import Optional, Tuple, Dict, Any
from PIL import ImageGrab


class OverlayModuleImproved:
    """画面オーバーレイを担当するモジュール（シンプル矢印・永続表示版）"""
    
    def __init__(self):
        """初期化"""
        self.overlay_window: Optional[tk.Toplevel] = None
        self.canvas: Optional[tk.Canvas] = None
        self.arrow_items = []
        
        # 座標精度改善のための画面情報を取得
        self.screen_info = self._get_screen_info()
        
        print("シンプル矢印・永続表示版オーバーレイモジュールが初期化されました")
        print(f"画面情報: {self.screen_info}")
    
    def _get_screen_info(self) -> Dict[str, Any]:
        """
        画面情報を取得（座標計算精度向上のため）
        
        Returns:
            画面情報の辞書
        """
        try:
            # 実際の画面サイズを取得
            screenshot = ImageGrab.grab()
            actual_width, actual_height = screenshot.size
            
            # tkinterでの画面情報も取得
            root = tk.Tk()
            root.withdraw()  # ウィンドウを表示しない
            
            tk_width = root.winfo_screenwidth()
            tk_height = root.winfo_screenheight()
            
            # DPI情報を取得
            try:
                dpi_x = root.winfo_fpixels('1i')
                dpi_y = root.winfo_fpixels('1i')
            except:
                dpi_x = dpi_y = 96  # デフォルト値
            
            root.destroy()
            
            screen_info = {
                'actual_width': actual_width,
                'actual_height': actual_height,
                'tk_width': tk_width,
                'tk_height': tk_height,
                'dpi_x': dpi_x,
                'dpi_y': dpi_y,
                'scale_x': actual_width / tk_width if tk_width > 0 else 1.0,
                'scale_y': actual_height / tk_height if tk_height > 0 else 1.0
            }
            
            return screen_info
            
        except Exception as e:
            print(f"画面情報取得エラー: {e}")
            return {
                'actual_width': 1920,
                'actual_height': 1080,
                'tk_width': 1920,
                'tk_height': 1080,
                'dpi_x': 96,
                'dpi_y': 96,
                'scale_x': 1.0,
                'scale_y': 1.0
            }
    
    def _convert_screen_to_tk_coordinates(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """
        実際の画面座標をtkinter座標系に変換
        
        Args:
            screen_x: 実際の画面X座標
            screen_y: 実際の画面Y座標
            
        Returns:
            (tk_x, tk_y) のタプル
        """
        try:
            scale_x = self.screen_info['scale_x']
            scale_y = self.screen_info['scale_y']
            
            # 逆変換（画面座標 → tkinter座標）
            tk_x = int(screen_x / scale_x)
            tk_y = int(screen_y / scale_y)
            
            # 境界チェック
            tk_width = self.screen_info['tk_width']
            tk_height = self.screen_info['tk_height']
            
            tk_x = max(0, min(tk_x, tk_width - 1))
            tk_y = max(0, min(tk_y, tk_height - 1))
            
            print(f"座標変換: 画面({screen_x}, {screen_y}) -> tkinter({tk_x}, {tk_y})")
            return tk_x, tk_y
            
        except Exception as e:
            print(f"座標変換エラー: {e}")
            return screen_x, screen_y  # フォールバック
    
    def show_arrow(self, x: int, y: int, size: int = 60):
        """
        指定された座標にシンプルな矢印を永続表示
        
        Args:
            x: X座標（実際の画面座標）
            y: Y座標（実際の画面座標）
            size: 矢印のサイズ
        """
        try:
            # メインスレッドで実行されることを確認
            if threading.current_thread() != threading.main_thread():
                if hasattr(tk, '_default_root') and tk._default_root:
                    tk._default_root.after(0, lambda: self.show_arrow(x, y, size))
                return
            
            print(f"シンプル矢印表示要求: 画面座標({x}, {y})")
            
            # 座標をtkinter座標系に変換
            tk_x, tk_y = self._convert_screen_to_tk_coordinates(x, y)
            
            # 既存のオーバーレイがあれば削除
            self.hide()
            
            # 新しいオーバーレイウィンドウを作成
            self._create_overlay_window()
            
            # シンプルな矢印を描画
            self._draw_simple_game_arrow(tk_x, tk_y, size)
            
            print(f"✅ シンプル矢印を永続表示: 画面({x}, {y}) -> tkinter({tk_x}, {tk_y})")
            print("💡 矢印は次の操作まで表示し続けます")
            
        except Exception as e:
            print(f"矢印表示エラー: {e}")
            import traceback
            traceback.print_exc()
    
    def show_pointing_arrow(self, x: int, y: int, size: int = 50):
        """
        方向指定矢印を永続表示（中信頼度用）
        
        Args:
            x: X座標（実際の画面座標）
            y: Y座標（実際の画面座標）
            size: 矢印のサイズ
        """
        try:
            # メインスレッドで実行されることを確認
            if threading.current_thread() != threading.main_thread():
                if hasattr(tk, '_default_root') and tk._default_root:
                    tk._default_root.after(0, lambda: self.show_pointing_arrow(x, y, size))
                return
            
            print(f"方向指定矢印表示要求: 画面座標({x}, {y})")
            
            # 座標をtkinter座標系に変換
            tk_x, tk_y = self._convert_screen_to_tk_coordinates(x, y)
            
            # 既存のオーバーレイがあれば削除
            self.hide()
            
            # 新しいオーバーレイウィンドウを作成
            self._create_overlay_window()
            
            # 方向指定矢印を描画
            self._draw_pointing_arrow(tk_x, tk_y, size)
            
            print(f"✅ 方向指定矢印を永続表示: 画面({x}, {y}) -> tkinter({tk_x}, {tk_y})")
            
        except Exception as e:
            print(f"方向指定矢印表示エラー: {e}")
    
    def show_highlight_area(self, x1: int, y1: int, x2: int, y2: int):
        """
        ハイライト表示を永続表示（低信頼度用）
        
        Args:
            x1: 左上X座標（実際の画面座標）
            y1: 左上Y座標（実際の画面座標）
            x2: 右下X座標（実際の画面座標）
            y2: 右下Y座標（実際の画面座標）
        """
        try:
            # メインスレッドで実行されることを確認
            if threading.current_thread() != threading.main_thread():
                if hasattr(tk, '_default_root') and tk._default_root:
                    tk._default_root.after(0, lambda: self.show_highlight_area(x1, y1, x2, y2))
                return
            
            print(f"ハイライト表示要求: 画面座標({x1}, {y1}) - ({x2}, {y2})")
            
            # 座標をtkinter座標系に変換
            tk_x1, tk_y1 = self._convert_screen_to_tk_coordinates(x1, y1)
            tk_x2, tk_y2 = self._convert_screen_to_tk_coordinates(x2, y2)
            
            # 既存のオーバーレイがあれば削除
            self.hide()
            
            # 新しいオーバーレイウィンドウを作成
            self._create_overlay_window()
            
            # ハイライト領域を描画
            self._draw_highlight_area(tk_x1, tk_y1, tk_x2, tk_y2)
            
            print(f"✅ ハイライトを永続表示: 画面({x1}, {y1})-({x2}, {y2}) -> tkinter({tk_x1}, {tk_y1})-({tk_x2}, {tk_y2})")
            
        except Exception as e:
            print(f"ハイライト表示エラー: {e}")
    
    def _create_overlay_window(self):
        """
        オーバーレイウィンドウを作成（座標精度改善版）
        """
        try:
            # ルートウィンドウが存在しない場合は作成
            if not hasattr(tk, '_default_root') or not tk._default_root:
                root = tk.Tk()
                root.withdraw()  # 非表示にする
            
            # オーバーレイウィンドウを作成
            self.overlay_window = tk.Toplevel()
            
            # ウィンドウの設定（座標精度向上のため）
            screen_width = self.screen_info['tk_width']
            screen_height = self.screen_info['tk_height']
            
            # フルスクリーンに設定
            self.overlay_window.geometry(f"{screen_width}x{screen_height}+0+0")
            
            # ウィンドウを透明にし、最前面に表示
            self.overlay_window.attributes('-topmost', True)
            self.overlay_window.attributes('-transparentcolor', 'white')
            self.overlay_window.overrideredirect(True)  # ウィンドウ装飾を削除
            
            # クリックを透過させる（Linux環境では制限あり）
            try:
                self.overlay_window.wm_attributes('-type', 'dock')
            except:
                pass  # 環境によっては対応していない
            
            # キャンバスを作成
            self.canvas = tk.Canvas(
                self.overlay_window,
                width=screen_width,
                height=screen_height,
                bg='white',
                highlightthickness=0
            )
            self.canvas.pack()
            
            print(f"オーバーレイウィンドウを作成しました: {screen_width}x{screen_height}")
            
        except Exception as e:
            print(f"オーバーレイウィンドウ作成エラー: {e}")
    
    def _draw_simple_game_arrow(self, x: int, y: int, size: int):
        """
        ゲームチュートリアル風のシンプルな矢印を描画（添付画像のデザイン）
        
        Args:
            x: X座標（tkinter座標系）
            y: Y座標（tkinter座標系）
            size: 矢印のサイズ
        """
        try:
            if not self.canvas:
                return
            
            # 添付画像と同じシンプルな矢印の形状を定義（左向き→右向きに変更）
            # 矢印の基本サイズ比率
            arrow_length = size
            arrow_height = size * 0.6
            arrow_head_width = size * 0.4
            
            # 矢印の座標を計算（右向き）
            arrow_points = [
                # 矢印の先端（右）
                x + arrow_length//2, y,
                # 上の羽根
                x + arrow_length//4, y - arrow_head_width//2,
                # 上の胴体
                x + arrow_length//4, y - arrow_height//4,
                # 左端上
                x - arrow_length//2, y - arrow_height//4,
                # 左端下
                x - arrow_length//2, y + arrow_height//4,
                # 下の胴体
                x + arrow_length//4, y + arrow_height//4,
                # 下の羽根
                x + arrow_length//4, y + arrow_head_width//2
            ]
            
            # 影を描画（立体感のため）
            shadow_points = []
            for i in range(0, len(arrow_points), 2):
                shadow_points.extend([arrow_points[i] + 3, arrow_points[i+1] + 3])
            
            shadow_arrow = self.canvas.create_polygon(
                shadow_points,
                fill='#8B0000',  # 暗い赤（影）
                outline='',
                width=0
            )
            self.arrow_items.append(shadow_arrow)
            
            # メインの矢印を描画（添付画像と同じ鮮やかな赤）
            main_arrow = self.canvas.create_polygon(
                arrow_points,
                fill='#FF0000',  # 鮮やかな赤
                outline='#FFFFFF',  # 白い縁取り
                width=2
            )
            self.arrow_items.append(main_arrow)
            
            # 軽いパルス効果（ゲームらしく）
            self._animate_simple_arrow()
            
            print(f"シンプルゲーム矢印を描画しました: tkinter座標({x}, {y})")
            
        except Exception as e:
            print(f"シンプル矢印描画エラー: {e}")
    
    def _draw_pointing_arrow(self, x: int, y: int, size: int):
        """
        方向指定矢印を描画（中信頼度用）
        
        Args:
            x: X座標（tkinter座標系）
            y: Y座標（tkinter座標系）
            size: 矢印のサイズ
        """
        try:
            if not self.canvas:
                return
            
            # 画面の中心からの方向を計算
            screen_center_x = self.screen_info['tk_width'] // 2
            screen_center_y = self.screen_info['tk_height'] // 2
            
            # 方向ベクトルを計算
            dx = x - screen_center_x
            dy = y - screen_center_y
            
            # 角度を計算
            angle = math.atan2(dy, dx)
            
            # 方向矢印の位置を調整（画面端から指す）
            if abs(dx) > abs(dy):
                # 水平方向
                arrow_x = screen_center_x + (screen_center_x * 0.7 * (1 if dx > 0 else -1))
                arrow_y = screen_center_y + dy * 0.5
            else:
                # 垂直方向
                arrow_x = screen_center_x + dx * 0.5
                arrow_y = screen_center_y + (screen_center_y * 0.7 * (1 if dy > 0 else -1))
            
            # 方向矢印を描画
            arrow_points = self._calculate_directional_arrow_points(arrow_x, arrow_y, angle, size)
            
            # 影を描画
            shadow_points = [p + 2 for p in arrow_points]
            shadow_arrow = self.canvas.create_polygon(
                shadow_points,
                fill='#8B4513',  # 茶色の影
                outline='',
                width=0
            )
            self.arrow_items.append(shadow_arrow)
            
            # メインの矢印を描画
            main_arrow = self.canvas.create_polygon(
                arrow_points,
                fill='#FF8C00',  # オレンジ色
                outline='#FFFFFF',
                width=2
            )
            self.arrow_items.append(main_arrow)
            
            print(f"方向指定矢印を描画しました: tkinter座標({x}, {y})")
            
        except Exception as e:
            print(f"方向指定矢印描画エラー: {e}")
    
    def _draw_highlight_area(self, x1: int, y1: int, x2: int, y2: int):
        """
        ハイライト領域を描画（低信頼度用）
        
        Args:
            x1: 左上X座標（tkinter座標系）
            y1: 左上Y座標（tkinter座標系）
            x2: 右下X座標（tkinter座標系）
            y2: 右下Y座標（tkinter座標系）
        """
        try:
            if not self.canvas:
                return
            
            # 座標を正規化
            left = min(x1, x2)
            top = min(y1, y2)
            right = max(x1, x2)
            bottom = max(y1, y2)
            
            # ハイライト領域を描画
            highlight_rect = self.canvas.create_rectangle(
                left, top, right, bottom,
                fill='',
                outline='#FFD700',  # 金色
                width=4,
                dash=(10, 5)  # 破線
            )
            self.arrow_items.append(highlight_rect)
            
            # 半透明のオーバーレイ
            overlay_rect = self.canvas.create_rectangle(
                left, top, right, bottom,
                fill='#FFFF00',  # 黄色
                stipple='gray25',  # パターンで半透明効果
                outline=''
            )
            self.arrow_items.append(overlay_rect)
            
            print(f"ハイライト領域を描画しました: tkinter座標({left}, {top})-({right}, {bottom})")
            
        except Exception as e:
            print(f"ハイライト描画エラー: {e}")
    
    def _calculate_directional_arrow_points(self, x: float, y: float, angle: float, size: int) -> list:
        """
        方向矢印の座標を計算
        
        Args:
            x: 中心X座標
            y: 中心Y座標
            angle: 角度（ラジアン）
            size: サイズ
            
        Returns:
            矢印の座標リスト
        """
        # 矢印の基本形状
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        # 矢印の各点を計算
        points = []
        
        # 先端
        tip_x = x + size * cos_a
        tip_y = y + size * sin_a
        points.extend([tip_x, tip_y])
        
        # 左の羽
        left_x = x + (size * 0.6) * math.cos(angle + 2.5)
        left_y = y + (size * 0.6) * math.sin(angle + 2.5)
        points.extend([left_x, left_y])
        
        # 中央
        center_x = x + (size * 0.3) * cos_a
        center_y = y + (size * 0.3) * sin_a
        points.extend([center_x, center_y])
        
        # 右の羽
        right_x = x + (size * 0.6) * math.cos(angle - 2.5)
        right_y = y + (size * 0.6) * math.sin(angle - 2.5)
        points.extend([right_x, right_y])
        
        return points
    
    def _animate_simple_arrow(self):
        """
        シンプル矢印の軽いアニメーション効果（永続表示対応）
        """
        try:
            if not self.canvas or not self.arrow_items:
                return
            
            def gentle_pulse():
                if self.canvas and self.arrow_items and self.overlay_window:
                    try:
                        # 軽いパルス効果（控えめに）
                        for item in self.arrow_items[-1:]:  # メインの矢印のみ
                            try:
                                current_width = self.canvas.itemcget(item, 'width')
                                new_width = 3 if current_width == '2' else 2
                                self.canvas.itemconfig(item, width=new_width)
                            except:
                                pass
                        
                        # 次のパルスをスケジュール（永続表示なので継続）
                        if self.overlay_window and self.overlay_window.winfo_exists():
                            self.overlay_window.after(1500, gentle_pulse)  # ゆっくりとしたパルス
                    except:
                        pass
            
            # アニメーション開始
            gentle_pulse()
            
        except Exception as e:
            print(f"アニメーションエラー: {e}")
    
    def hide(self):
        """
        オーバーレイを非表示にする
        """
        try:
            if self.overlay_window:
                self.overlay_window.destroy()
                self.overlay_window = None
            
            self.canvas = None
            self.arrow_items = []
            
            print("🔄 オーバーレイを非表示にしました")
            
        except Exception as e:
            print(f"オーバーレイ非表示エラー: {e}")


# テスト用のメイン関数
if __name__ == "__main__":
    import time
    
    # テスト実行
    overlay = OverlayModuleImproved()
    
    print("シンプル矢印・永続表示版オーバーレイモジュールのテストを開始します")
    print(f"画面情報: {overlay.screen_info}")
    
    # 座標変換のテスト
    test_screen_x, test_screen_y = 960, 540
    tk_x, tk_y = overlay._convert_screen_to_tk_coordinates(test_screen_x, test_screen_y)
    print(f"座標変換テスト: 画面({test_screen_x}, {test_screen_y}) -> tkinter({tk_x}, {tk_y})")
    
    try:
        # シンプル矢印表示のテスト
        print("\\nシンプル矢印永続表示テストを実行します...")
        overlay.show_arrow(960, 540, 60)
        
        print("💡 矢印が永続表示されています。手動で終了してください。")
        print("   （実際のアプリでは次の操作で自動的に消えます）")
        
        # 10秒間表示してテスト終了
        time.sleep(10)
        
        # 非表示
        overlay.hide()
        
        print("✅ テスト成功")
        
    except Exception as e:
        print(f"❌ テスト失敗: {e}")
    
    print("テスト完了")
