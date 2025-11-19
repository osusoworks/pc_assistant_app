#!/usr/bin/env python3
"""
SENPAI プロジェクトクリーンアップスクリプト
不要な旧バージョンファイルを整理し、最新の安定版のみを残します
"""

import os
import shutil
import datetime
from pathlib import Path


class ProjectCleanup:
    """プロジェクトクリーンアップクラス"""
    
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.backup_dir = self.project_dir / "archived_versions"
        
        # 保持するファイル（最新の安定版）
        self.keep_files = {
            # 実行ファイル
            "run_simple_library.py",
            "run_ui_hide.py",  # サブ版として保持
            
            # メインコントローラー
            "main_controller_with_simple_library.py",
            "main_controller_final_ui_hide.py",  # サブ版として保持
            
            # UIモジュール
            "ui_module_hide_aware.py",
            
            # キャプチャモジュール
            "capture_module_ui_aware.py",
            
            # AIモジュール
            "ai_module_improved.py",
            
            # オーバーレイモジュール
            "overlay_module_improved.py",
            
            # 音声モジュール
            "speech_module.py",
            
            # ライブラリ機能
            "simple_library.py",
            "library_ui_improved.py",
            
            # 設定・ドキュメント
            "requirements.txt",
            "install.sh",
            "README_SIMPLE_LIBRARY.md",
            "README_UI_HIDE.md",
            "SIMPLE_LIBRARY_DESIGN.md",
            
            # クリーンアップ関連
            "cleanup_project.py"
        }
        
        # アーカイブするファイル（旧バージョン）
        self.archive_files = {
            # 旧実行ファイル
            "run_app.py",
            "run_enhanced.py",
            "run_final.py",
            "run_auto_screenshot.py",
            
            # 旧メインコントローラー
            "main_controller.py",
            "main_controller_enhanced.py",
            "main_controller_final.py",
            "main_controller_auto_screenshot.py",
            
            # 旧UIモジュール
            "ui_module.py",
            "ui_module_improved.py",
            "ui_module_auto_screenshot.py",
            
            # 旧キャプチャモジュール
            "capture_module.py",
            "capture_module_improved.py",
            
            # 旧AIモジュール
            "ai_module.py",
            
            # 旧オーバーレイモジュール
            "overlay_module.py",
            
            # 旧ライブラリUI
            "library_ui.py",
            "library_ui_broken.py",
            
            # 旧ドキュメント
            "README.md",
            "README_ENHANCED.md",
            "README_FINAL.md",
            "README_AUTO_SCREENSHOT.md",
            "test_report.md"
        }
    
    def create_backup_directory(self):
        """バックアップディレクトリを作成"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ バックアップディレクトリを作成: {self.backup_dir}")
        else:
            print(f"📁 バックアップディレクトリが存在: {self.backup_dir}")
    
    def archive_old_files(self):
        """旧ファイルをアーカイブ"""
        archived_count = 0
        
        for filename in self.archive_files:
            file_path = self.project_dir / filename
            if file_path.exists():
                # アーカイブ先パス
                archive_path = self.backup_dir / filename
                
                try:
                    shutil.move(str(file_path), str(archive_path))
                    print(f"📦 アーカイブ: {filename}")
                    archived_count += 1
                except Exception as e:
                    print(f"❌ アーカイブ失敗: {filename} - {e}")
        
        print(f"✅ {archived_count}個のファイルをアーカイブしました")
        return archived_count
    
    def create_archive_readme(self):
        """アーカイブディレクトリにREADMEを作成"""
        readme_content = f"""# SENPAI - アーカイブされた旧バージョン

## 📅 アーカイブ日時
{datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

## 📁 アーカイブ内容

このディレクトリには、SENPAI PC操作ガイドの旧バージョンファイルが保存されています。

### 🗂️ ファイル分類

#### 実行ファイル（旧版）
- `run_app.py` - 基本版（初期バージョン）
- `run_enhanced.py` - 拡張版
- `run_final.py` - 最終版
- `run_auto_screenshot.py` - 自動スクリーンショット版

#### メインコントローラー（旧版）
- `main_controller.py` - 基本版
- `main_controller_enhanced.py` - 拡張版
- `main_controller_final.py` - 最終版
- `main_controller_auto_screenshot.py` - 自動版

#### UIモジュール（旧版）
- `ui_module.py` - 基本版
- `ui_module_improved.py` - 改良版
- `ui_module_auto_screenshot.py` - 自動版

#### その他モジュール（旧版）
- `capture_module.py` - 基本キャプチャ
- `capture_module_improved.py` - 改良キャプチャ
- `ai_module.py` - 基本AI
- `overlay_module.py` - 基本オーバーレイ

#### ライブラリUI（旧版）
- `library_ui.py` - 基本ライブラリUI
- `library_ui_broken.py` - 破損版（開発中の失敗版）

#### ドキュメント（旧版）
- `README.md` - 基本版説明書
- `README_ENHANCED.md` - 拡張版説明書
- `README_FINAL.md` - 最終版説明書
- `README_AUTO_SCREENSHOT.md` - 自動版説明書
- `test_report.md` - テストレポート

## ⚠️ 注意事項

- これらのファイルは開発履歴として保存されています
- 現在のプロジェクトでは使用されません
- 必要に応じて参照・復元可能です
- 削除する場合は慎重に判断してください

## 🔄 復元方法

必要なファイルを復元する場合:
```bash
# 個別ファイル復元
cp archived_versions/filename.py ./

# 全体復元（非推奨）
cp archived_versions/* ./
```

## 📊 開発履歴

1. **基本版** - 基本的なスクリーンショット・AI解析機能
2. **拡張版** - UI・機能改善
3. **自動版** - 自動スクリーンショット機能追加
4. **最終版** - 統合・安定化
5. **UI非表示版** - UI非表示撮影機能追加
6. **ライブラリ版** - お気に入り機能追加（現在の最新版）

---

*アーカイブ作成者: SENPAI クリーンアップスクリプト*
"""
        
        readme_path = self.backup_dir / "README_ARCHIVE.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"📝 アーカイブREADMEを作成: {readme_path}")
    
    def create_clean_project_structure(self):
        """クリーンなプロジェクト構造ドキュメントを作成"""
        structure_content = f"""# SENPAI - クリーンプロジェクト構造

## 📁 現在のファイル構成

### 🚀 実行ファイル
```
run_simple_library.py          # メイン実行ファイル（推奨）
run_ui_hide.py                 # UI非表示版実行ファイル
```

### 🎮 コントローラー
```
main_controller_with_simple_library.py    # メインコントローラー（推奨）
main_controller_final_ui_hide.py          # UI非表示版コントローラー
```

### 🖥️ UIモジュール
```
ui_module_hide_aware.py        # UI非表示対応版UIモジュール
```

### 📷 キャプチャモジュール
```
capture_module_ui_aware.py     # UI非表示対応版キャプチャ
```

### 🤖 AIモジュール
```
ai_module_improved.py          # 改良版AI解析モジュール
```

### 🏹 オーバーレイモジュール
```
overlay_module_improved.py     # 改良版オーバーレイモジュール
```

### 🎤 音声モジュール
```
speech_module.py               # 音声認識モジュール
```

### 📚 ライブラリ機能
```
simple_library.py              # シンプルライブラリ管理
library_ui_improved.py         # 改善版ライブラリUI
```

### 📖 ドキュメント・設定
```
README_SIMPLE_LIBRARY.md       # メイン説明書
README_UI_HIDE.md             # UI非表示版説明書
SIMPLE_LIBRARY_DESIGN.md      # 設計仕様書
requirements.txt              # Python依存関係
install.sh                    # インストールスクリプト
```

### 🛠️ 管理ツール
```
cleanup_project.py            # プロジェクトクリーンアップスクリプト
```

## 🎯 使用方法

### メイン版（推奨）
```bash
python run_simple_library.py
```

### UI非表示版
```bash
python run_ui_hide.py
```

## 📊 統計

- **総ファイル数**: {len(self.keep_files)}個
- **実行可能ファイル**: 2個
- **コアモジュール**: 7個
- **ライブラリ機能**: 2個
- **ドキュメント**: 5個

## 🔄 クリーンアップ履歴

- **実行日**: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
- **アーカイブファイル数**: {len(self.archive_files)}個
- **保持ファイル数**: {len(self.keep_files)}個

---

*クリーンアップ完了 - SENPAI プロジェクト*
"""
        
        structure_path = self.project_dir / "PROJECT_STRUCTURE.md"
        with open(structure_path, 'w', encoding='utf-8') as f:
            f.write(structure_content)
        
        print(f"📋 プロジェクト構造ドキュメントを作成: {structure_path}")
    
    def verify_cleanup(self):
        """クリーンアップ結果を検証"""
        print("\\n🔍 クリーンアップ結果を検証中...")
        
        # 現在のファイル一覧
        current_files = set()
        for file_path in self.project_dir.glob("*.py"):
            current_files.add(file_path.name)
        for file_path in self.project_dir.glob("*.md"):
            current_files.add(file_path.name)
        for file_path in self.project_dir.glob("*.txt"):
            current_files.add(file_path.name)
        for file_path in self.project_dir.glob("*.sh"):
            current_files.add(file_path.name)
        
        # 保持されるべきファイルの確認
        missing_files = self.keep_files - current_files
        if missing_files:
            print(f"⚠️  不足しているファイル: {missing_files}")
        else:
            print("✅ 必要なファイルはすべて保持されています")
        
        # 不要ファイルの確認
        unwanted_files = current_files & self.archive_files
        if unwanted_files:
            print(f"⚠️  まだ残っている旧ファイル: {unwanted_files}")
        else:
            print("✅ 旧ファイルは正常にアーカイブされました")
        
        # アーカイブディレクトリの確認
        if self.backup_dir.exists():
            archived_files = list(self.backup_dir.glob("*"))
            print(f"📦 アーカイブされたファイル数: {len(archived_files)}個")
        
        print(f"📁 現在のプロジェクトファイル数: {len(current_files)}個")
    
    def run_cleanup(self):
        """クリーンアップを実行"""
        print("🧹 SENPAI プロジェクトクリーンアップを開始...")
        print(f"📁 対象ディレクトリ: {self.project_dir}")
        
        # バックアップディレクトリ作成
        self.create_backup_directory()
        
        # 旧ファイルをアーカイブ
        archived_count = self.archive_old_files()
        
        # アーカイブREADME作成
        self.create_archive_readme()
        
        # プロジェクト構造ドキュメント作成
        self.create_clean_project_structure()
        
        # 結果検証
        self.verify_cleanup()
        
        print(f"\\n✅ クリーンアップ完了!")
        print(f"   - アーカイブファイル: {archived_count}個")
        print(f"   - 保持ファイル: {len(self.keep_files)}個")
        print(f"   - バックアップ場所: {self.backup_dir}")
        
        return True


def main():
    """メイン関数"""
    try:
        # 現在のディレクトリでクリーンアップを実行
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cleanup = ProjectCleanup(current_dir)
        
        # 確認メッセージ
        print("🧹 SENPAI プロジェクトクリーンアップ")
        print("=" * 50)
        print(f"対象ディレクトリ: {current_dir}")
        print(f"アーカイブ予定ファイル数: {len(cleanup.archive_files)}個")
        print(f"保持予定ファイル数: {len(cleanup.keep_files)}個")
        print()
        
        response = input("クリーンアップを実行しますか？ (y/N): ")
        if response.lower() in ['y', 'yes']:
            cleanup.run_cleanup()
        else:
            print("❌ クリーンアップをキャンセルしました")
            
    except Exception as e:
        print(f"❌ クリーンアップエラー: {e}")
        return False
    
    return True


if __name__ == "__main__":
    main()
