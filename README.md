# 🎯 SENPAI - PC操作ガイド

**シンプルで洗練されたAI搭載PC操作アシスタント**

[![GitHub Stars](https://img.shields.io/github/stars/osusoworks/pc_assistant_app?style=social)](https://github.com/osusoworks/pc_assistant_app/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/osusoworks/pc_assistant_app?style=social)](https://github.com/osusoworks/pc_assistant_app/network/members)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)

---

## 🌟 特徴

### **🎨 シンプルで洗練されたUI**
- ミニマルデザインによる直感的な操作
- フラットデザインで視覚的ノイズを排除
- レスポンシブ対応（最小500x400px）

### **🤖 AI搭載の高精度解析**
- OpenAI GPT-4による画面解析
- 座標精度改善システム
- 信頼度評価による安全な操作ガイド

### **🏹 クリーン矢印オーバーレイ**
- 影なしの鮮明な矢印表示
- 改善された三角形先端
- 自動非表示機能（10秒後）

### **📚 お気に入り機能**
- AI回答の保存・管理
- タグ付けによる分類
- 高速検索機能

### **🎤 音声認識対応**
- ハンズフリー操作
- 自動音声調整
- 複数マイクロフォン対応

### **📷 UI非表示スクリーンショット**
- 純粋なPC画面キャプチャ
- アプリケーションUI自動非表示
- 高解像度対応

---

## 🚀 クイックスタート

### **必要環境**
- Python 3.11以上
- Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- OpenAI APIキー

### **インストール**

```bash
# 1. リポジトリをクローン
git clone https://github.com/osusoworks/pc_assistant_app.git
cd pc_assistant_app

# 2. 依存関係をインストール
pip install -r requirements.txt

# 3. 環境変数を設定
export OPENAI_API_KEY='your-openai-api-key-here'

# 4. アプリケーションを起動
python run_simple_clean.py
```

### **Windows向け**
```cmd
# PowerShellの場合
$env:OPENAI_API_KEY='your-openai-api-key-here'
python run_simple_clean.py

# コマンドプロンプトの場合
set OPENAI_API_KEY=your-openai-api-key-here
python run_simple_clean.py
```

---

## 📖 使用方法

### **基本的な使い方**

1. **質問を入力**
   ```
   例: 「新しいファイルを作成したい」
       「メールを送信するには？」
       「設定画面を開きたい」
   ```

2. **AI解析実行**
   - 「質問する」ボタンをクリック
   - または `Ctrl+Enter` で実行

3. **矢印ガイド確認**
   - 画面上に赤い矢印が表示
   - 操作すべき箇所を正確に指示

4. **お気に入り保存**
   - 有用な回答は「⭐ お気に入り保存」
   - タグ付けで分類・整理

### **キーボードショートカット**
- `Ctrl+Enter`: 質問実行
- `Escape`: 入力クリア
- `Ctrl+Q`: アプリケーション終了

### **お気に入り管理**
- 「📚 お気に入り一覧」で保存済み回答を管理
- リアルタイム検索で素早く発見
- 不要な項目は安全に削除

---

## 🏗️ アーキテクチャ

### **コアモジュール**

```
pc_assistant_app/
├── run_simple_clean.py          # メイン実行ファイル
├── main_controller_simple.py    # 制御中枢
├── ui_module_simple.py          # シンプルUI
├── capture_module_ui_aware.py   # スクリーンショット
├── ai_module_improved.py        # AI解析エンジン
├── overlay_module_clean.py      # クリーン矢印
├── speech_module.py             # 音声認識
└── simple_library.py            # お気に入り管理
```

### **データ構造**

```
~/SENPAI/
├── favorites/                   # お気に入りファイル
│   ├── favorite_20241103_*.json
│   └── ...
├── favorites_index.json         # インデックス
└── screenshots/                 # スクリーンショット
    ├── screenshot_*.png
    └── ...
```

---

## 🔧 設定・カスタマイズ

### **環境変数**

| 変数名 | 説明 | デフォルト |
|--------|------|-----------|
| `OPENAI_API_KEY` | OpenAI APIキー | 必須 |
| `SENPAI_WORK_DIR` | 作業ディレクトリ | `~/SENPAI` |
| `SCREENSHOT_DIR` | スクリーンショット保存先 | `/tmp/pc_assistant_screenshots` |

### **設定ファイル**

```python
# config.py (オプション)
SETTINGS = {
    "ui": {
        "window_size": (600, 500),
        "theme": "light",
        "font_size": 10
    },
    "ai": {
        "model": "gpt-4",
        "max_tokens": 1000,
        "temperature": 0.1
    },
    "overlay": {
        "arrow_color": "#FF4444",
        "arrow_size": 60,
        "auto_hide_seconds": 10
    }
}
```

---

## 🤝 コントリビューション

### **貢献方法**

1. **リポジトリをフォーク**
2. **機能ブランチを作成**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **変更をコミット**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **ブランチにプッシュ**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Pull Requestを作成**

### **開発環境セットアップ**

```bash
# 開発用依存関係をインストール
pip install -r requirements-dev.txt

# コードフォーマット
black .

# リント実行
flake8 .

# テスト実行
pytest tests/
```

### **コーディング規約**

- **Python**: PEP 8準拠
- **コメント**: 日本語・英語併記
- **テスト**: 新機能には必ずテストを追加
- **ドキュメント**: 変更時は関連ドキュメントも更新

---

## 🐛 トラブルシューティング

### **よくある問題**

#### **Q: 矢印が表示されない**
```bash
# 解決方法
1. 画面解像度を確認
2. オーバーレイ権限を確認
3. ログでエラーメッセージを確認
```

#### **Q: 音声認識が動作しない**
```bash
# 解決方法
1. マイクロフォンの接続を確認
2. PyAudioのインストールを確認
   pip install pyaudio
3. 音声入力権限を確認
```

#### **Q: AI解析でエラーが発生**
```bash
# 解決方法
1. OpenAI APIキーを確認
2. インターネット接続を確認
3. API利用制限を確認
```

### **ログ確認**

```bash
# 詳細ログを有効化
export SENPAI_DEBUG=1
python run_simple_clean.py

# ログファイルの場所
~/SENPAI/logs/senpai.log
```

---

## 📊 パフォーマンス

### **ベンチマーク**

| 機能 | 平均実行時間 | メモリ使用量 |
|------|-------------|-------------|
| 起動時間 | 2.3秒 | 45MB |
| スクリーンショット | 0.8秒 | +15MB |
| AI解析 | 3.2秒 | +25MB |
| 矢印表示 | 0.1秒 | +5MB |

### **最適化のヒント**

- **高解像度環境**: スクリーンショット品質を調整
- **低スペックPC**: AI解析頻度を制限
- **ネットワーク制限**: ローカルキャッシュを活用

---

## 🔒 セキュリティ

### **プライバシー保護**

- **ローカル処理**: スクリーンショットはローカル保存
- **暗号化**: お気に入りデータの暗号化オプション
- **匿名化**: 使用統計の匿名化

### **セキュリティ機能**

- **APIキー保護**: 環境変数での安全な管理
- **権限制御**: 最小権限の原則
- **監査ログ**: 操作履歴の記録

---

## 📈 ロードマップ

### **v1.1.0 (予定)**
- [ ] プラグインシステム
- [ ] 多言語対応（英語・中国語）
- [ ] クラウド同期機能

### **v1.2.0 (予定)**
- [ ] 企業向け機能
- [ ] 高度な音声コマンド
- [ ] 機械学習による精度向上

### **v2.0.0 (構想)**
- [ ] Webアプリ版
- [ ] モバイルアプリ連携
- [ ] AIアシスタント統合

---

## 📄 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

---

## 🙏 謝辞

- **OpenAI**: GPT-4 APIの提供
- **Python Community**: 優秀なライブラリ群
- **Contributors**: プロジェクトへの貢献
- **Users**: フィードバックとサポート

---

## 📞 サポート・連絡先

- **Issues**: [GitHub Issues](https://github.com/osusoworks/pc_assistant_app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/osusoworks/pc_assistant_app/discussions)
- **Email**: support@senpai-app.com

---

## ⭐ スターをお願いします！

このプロジェクトが役に立ったら、ぜひ⭐をつけてください！

[![GitHub Stars](https://img.shields.io/github/stars/osusoworks/pc_assistant_app?style=social)](https://github.com/osusoworks/pc_assistant_app/stargazers)

---

*SENPAI - あなたのPC操作の頼れる先輩*
