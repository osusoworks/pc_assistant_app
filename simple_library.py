#!/usr/bin/env python3
"""
シンプルライブラリ管理モジュール
お気に入り機能のみを提供する軽量なライブラリシステム
"""

import os
import json
import datetime
from pathlib import Path
from typing import List, Dict, Optional


class SimpleLibrary:
    """シンプルなお気に入り管理クラス"""
    
    def __init__(self):
        """初期化"""
        self.library_dir = Path.home() / "SENPAI" / "favorites"
        self.index_file = Path.home() / "SENPAI" / "favorites_index.json"
        
        # ディレクトリを作成
        self._ensure_directories()
        
        print("シンプルライブラリが初期化されました")
    
    def _ensure_directories(self):
        """必要なディレクトリを作成"""
        try:
            self.library_dir.mkdir(parents=True, exist_ok=True)
            print(f"ライブラリディレクトリ: {self.library_dir}")
        except Exception as e:
            print(f"ディレクトリ作成エラー: {e}")
    
    def _generate_favorite_id(self) -> str:
        """お気に入りIDを生成"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"favorite_{timestamp}"
    
    def _load_index(self) -> Dict:
        """インデックスファイルを読み込み"""
        try:
            if self.index_file.exists():
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"favorites": [], "last_updated": ""}
        except Exception as e:
            print(f"インデックス読み込みエラー: {e}")
            return {"favorites": [], "last_updated": ""}
    
    def _save_index(self, index_data: Dict):
        """インデックスファイルを保存"""
        try:
            index_data["last_updated"] = datetime.datetime.now().isoformat()
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"インデックス保存エラー: {e}")
    
    def save_favorite(self, question: str, answer: str, tag: str = "", screenshot_path: str = "") -> bool:
        """
        お気に入りを保存
        
        Args:
            question: 質問テキスト
            answer: 回答テキスト
            tag: タグ（オプション）
            screenshot_path: スクリーンショットパス（オプション）
            
        Returns:
            bool: 保存成功時True
        """
        try:
            # お気に入りIDを生成
            favorite_id = self._generate_favorite_id()
            
            # お気に入りデータを作成
            favorite_data = {
                "id": favorite_id,
                "question": question,
                "answer": answer,
                "tag": tag,
                "created_at": datetime.datetime.now().isoformat(),
                "screenshot_path": screenshot_path
            }
            
            # お気に入りファイルを保存
            favorite_file = self.library_dir / f"{favorite_id}.json"
            with open(favorite_file, 'w', encoding='utf-8') as f:
                json.dump(favorite_data, f, ensure_ascii=False, indent=2)
            
            # インデックスを更新
            index_data = self._load_index()
            index_data["favorites"].append({
                "id": favorite_id,
                "question": question[:50] + "..." if len(question) > 50 else question,
                "tag": tag,
                "created_at": favorite_data["created_at"]
            })
            self._save_index(index_data)
            
            print(f"お気に入りを保存しました: {favorite_id}")
            return True
            
        except Exception as e:
            print(f"お気に入り保存エラー: {e}")
            return False
    
    def get_favorites_list(self) -> List[Dict]:
        """
        お気に入り一覧を取得
        
        Returns:
            List[Dict]: お気に入り一覧
        """
        try:
            index_data = self._load_index()
            # 新しい順にソート
            favorites = sorted(
                index_data["favorites"], 
                key=lambda x: x["created_at"], 
                reverse=True
            )
            return favorites
        except Exception as e:
            print(f"お気に入り一覧取得エラー: {e}")
            return []
    
    def get_favorite(self, favorite_id: str) -> Optional[Dict]:
        """
        特定のお気に入りを取得
        
        Args:
            favorite_id: お気に入りID
            
        Returns:
            Dict: お気に入りデータ（見つからない場合はNone）
        """
        try:
            favorite_file = self.library_dir / f"{favorite_id}.json"
            if favorite_file.exists():
                with open(favorite_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"お気に入りが見つかりません: {favorite_id}")
                return None
        except Exception as e:
            print(f"お気に入り取得エラー: {e}")
            return None
    
    def delete_favorite(self, favorite_id: str) -> bool:
        """
        お気に入りを削除
        
        Args:
            favorite_id: お気に入りID
            
        Returns:
            bool: 削除成功時True
        """
        try:
            # お気に入りファイルを削除
            favorite_file = self.library_dir / f"{favorite_id}.json"
            if favorite_file.exists():
                favorite_file.unlink()
                print(f"お気に入りファイルを削除しました: {favorite_file}")
            
            # インデックスから削除
            index_data = self._load_index()
            index_data["favorites"] = [
                fav for fav in index_data["favorites"] 
                if fav["id"] != favorite_id
            ]
            self._save_index(index_data)
            
            print(f"お気に入りを削除しました: {favorite_id}")
            return True
            
        except Exception as e:
            print(f"お気に入り削除エラー: {e}")
            return False
    
    def get_favorites_count(self) -> int:
        """
        お気に入りの総数を取得
        
        Returns:
            int: お気に入りの総数
        """
        try:
            index_data = self._load_index()
            return len(index_data["favorites"])
        except Exception as e:
            print(f"お気に入り数取得エラー: {e}")
            return 0
    
    def search_favorites(self, query: str) -> List[Dict]:
        """
        お気に入りを検索
        
        Args:
            query: 検索クエリ（質問内容やタグで検索）
            
        Returns:
            List[Dict]: 検索結果のお気に入り一覧
        """
        try:
            if not query.strip():
                return []
            
            query_lower = query.lower().strip()
            results = []
            
            # インデックスから検索
            index_data = self._load_index()
            for fav_info in index_data["favorites"]:
                # 質問内容で検索
                if query_lower in fav_info["question"].lower():
                    # 詳細データを取得
                    detail = self.get_favorite(fav_info["id"])
                    if detail:
                        results.append(detail)
                # タグで検索
                elif query_lower in fav_info.get("tag", "").lower():
                    detail = self.get_favorite(fav_info["id"])
                    if detail:
                        results.append(detail)
            
            print(f"検索結果: {len(results)}件 (クエリ: '{query}')")
            return results
            
        except Exception as e:
            print(f"お気に入り検索エラー: {e}")
            return []


def test_simple_library():
    """シンプルライブラリのテスト"""
    print("=== シンプルライブラリ テスト ===")
    
    # ライブラリを初期化
    library = SimpleLibrary()
    
    # テスト用お気に入りを保存
    success = library.save_favorite(
        question="この青いボタンをクリックしたいです",
        answer="画面上の青いボタンをクリックするには、座標(100, 200)をクリックしてください。",
        tag="ボタンクリック"
    )
    print(f"保存テスト: {'成功' if success else '失敗'}")
    
    # お気に入り一覧を取得
    favorites = library.get_favorites_list()
    print(f"お気に入り数: {len(favorites)}")
    
    for fav in favorites:
        print(f"- {fav['id']}: {fav['question']} ({fav['tag']})")
    
    # 詳細を取得
    if favorites:
        detail = library.get_favorite(favorites[0]['id'])
        if detail:
            print(f"詳細取得テスト: 成功")
            print(f"  質問: {detail['question']}")
            print(f"  回答: {detail['answer'][:50]}...")
    
    print("=== テスト完了 ===")


if __name__ == "__main__":
    test_simple_library()
