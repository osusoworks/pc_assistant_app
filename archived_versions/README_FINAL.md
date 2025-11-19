# PC操作支援アプリケーション（最終版）

PCで操作をしている際、アプリでもゲームでも不明点があったら教えてくれるAI支援アプリケーションです。

## 🌟 主な機能

- **📷 画面キャプチャ**: ワンクリックまたはホットキー（Ctrl+Alt+S）でスクリーンショット撮影
- **🤖 AI画面解析**: OpenAI GPT-4 Vision APIを使用して画面内容を理解
- **🎤 音声質問**: 音声で質問を入力可能
- **⌨️ テキスト質問**: テキストでも質問を入力可能
- **🎯 操作指示**: 画面上に赤い矢印で操作箇所を表示
- **🔄 常駐機能**: バックグラウンドで動作し、必要時に即座に利用可能

## 🖥️ システム要件

- **OS**: Linux (Ubuntu 22.04で動作確認済み)
- **Python**: 3.11+
- **ハードウェア**: マイクロフォン（音声入力を使用する場合）
- **API**: OpenAI APIキー（AI解析機能を使用する場合）

## 🚀 クイックスタート

### 1. 自動インストール

```bash
# リポジトリをクローンまたはダウンロード
cd pc_assistant_app

# 自動インストールスクリプトを実行
./install.sh
```

### 2. OpenAI APIキーの設定

```bash
export OPENAI_API_KEY='your-api-key-here'

# 永続化する場合
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. アプリケーションの実行

```bash
python3 run_final.py
```

## 📋 使用方法

### 基本的な操作手順

1. **📷 スクリーンショット撮影**
   - UIの「📷 スクリーンショット撮影」ボタンをクリック
   - または `Ctrl+Alt+S`（利用可能な場合）

2. **❓ 質問入力**
   - テキストボックスに質問を入力して「質問する」ボタンをクリック
   - または 🎤 音声入力ボタン（利用可能な場合）

3. **🤖 AI回答の確認**
   - AIが画面を解析して回答を表示
   - 必要に応じて画面上に赤い矢印で操作箇所を指示

### 質問例

- "このボタンは何をするものですか？"
- "次に何をすればいいですか？"
- "エラーメッセージの意味を教えてください"
- "この設定をどこで変更できますか？"
- "このアプリの使い方を教えてください"

## 🏗️ アーキテクチャ

### ファイル構成

```
pc_assistant_app/
├── run_final.py                    # 最終版実行スクリプト
├── main_controller_final.py        # 最終版メインコントローラー
├── capture_module_improved.py      # 改良版画面キャプチャモジュール
├── speech_module.py               # 音声認識モジュール
├── ui_module_improved.py          # 改良版UIモジュール
├── ai_module.py                   # AI解析モジュール
├── overlay_module.py              # オーバーレイ表示モジュール
├── install.sh                     # 自動インストールスクリプト
├── requirements.txt               # 依存関係一覧
├── test_report.md                 # テスト結果レポート
└── README_FINAL.md               # このファイル
```

### モジュール説明

| モジュール | 機能 | 環境制限対応 |
|-----------|------|-------------|
| **main_controller_final.py** | 全体制御・各モジュール連携 | ✅ |
| **capture_module_improved.py** | 画面キャプチャ・ホットキー監視 | ✅ |
| **ui_module_improved.py** | ユーザーインターフェース | ✅ |
| **speech_module.py** | 音声認識 | ⚠️ |
| **ai_module.py** | AI解析 | ⚠️ |
| **overlay_module.py** | 画面オーバーレイ | ⚠️ |

## 🔧 機能状態と制限事項

### ✅ 常に利用可能な機能

- **画面キャプチャ**: PIL.ImageGrabを使用
- **基本UI**: tkinterベース
- **テキスト質問入力**: 標準機能

### ⚠️ 環境依存の機能

| 機能 | 要件 | 制限事項 |
|------|------|---------|
| **ホットキー** | X11環境・pynput | サンドボックス環境では制限あり |
| **音声認識** | マイクロフォン・PyAudio | 音声デバイスが必要 |
| **AI解析** | OpenAI APIキー・インターネット | APIキーとネットワーク接続が必要 |
| **オーバーレイ** | X11環境・ウィンドウマネージャー | 環境により表示制限あり |

## 🛠️ トラブルシューティング

### よくある問題と解決方法

#### 1. PyAudioのインストールエラー

```bash
sudo apt-get install -y build-essential portaudio19-dev python3-dev
pip3 install pyaudio
```

#### 2. tkinterが見つからない

```bash
sudo apt-get install -y python3-tk
```

#### 3. ホットキーが動作しない

- **原因**: X11環境の制限、他のアプリケーションとの競合
- **対策**: UIボタンを使用してスクリーンショットを撮影

#### 4. 音声認識が動作しない

- **確認事項**:
  - マイクロフォンが正しく接続されているか
  - システムの音声設定でマイクが有効になっているか
  - ALSAエラーは警告のみで、機能には影響しない場合が多い

#### 5. AI解析でエラーが発生

- **確認事項**:
  - OpenAI APIキーが正しく設定されているか
  - インターネット接続が正常か
  - APIの利用制限に達していないか

#### 6. オーバーレイが表示されない

- **原因**: ウィンドウマネージャーの制限
- **対策**: 実環境での動作確認を推奨

## 🧪 テスト方法

### 個別モジュールのテスト

```bash
# キャプチャモジュール
python3 capture_module_improved.py

# UIモジュール
python3 ui_module_improved.py

# 音声認識モジュール
python3 speech_module.py

# オーバーレイモジュール
python3 overlay_module.py
```

### 統合テスト

```bash
# 最終版アプリケーション
python3 run_final.py
```

## 🔒 セキュリティ考慮事項

- **APIキー管理**: 環境変数を使用してAPIキーを安全に管理
- **画面キャプチャ**: 一時ファイルは定期的に削除
- **ネットワーク通信**: OpenAI APIとの通信のみ
- **権限**: 最小限の権限で動作

## 🚀 実環境での展開

### 推奨環境

- **OS**: Ubuntu 20.04 LTS以降
- **デスクトップ環境**: GNOME、KDE、XFCE
- **Python**: 3.8以降
- **メモリ**: 2GB以上
- **ストレージ**: 100MB以上の空き容量

### 本番環境での設定

1. **依存関係のインストール**
   ```bash
   ./install.sh
   ```

2. **APIキーの設定**
   ```bash
   # システム全体で設定
   sudo echo 'export OPENAI_API_KEY="your-key"' >> /etc/environment
   
   # ユーザー固有で設定
   echo 'export OPENAI_API_KEY="your-key"' >> ~/.bashrc
   ```

3. **自動起動の設定**
   ```bash
   # デスクトップエントリを作成
   cat > ~/.local/share/applications/pc-assistant.desktop << EOF
   [Desktop Entry]
   Name=PC Assistant
   Comment=PC操作支援アプリケーション
   Exec=/path/to/pc_assistant_app/run_final.py
   Icon=applications-utilities
   Terminal=false
   Type=Application
   Categories=Utility;
   EOF
   ```

## 📈 今後の拡張予定

- **多言語対応**: 英語・中国語などの対応
- **プラグインシステム**: カスタム機能の追加
- **クラウド連携**: 設定の同期機能
- **高度なAI機能**: より詳細な画面解析
- **モバイル対応**: スマートフォン版の開発

## 🤝 コントリビューション

プルリクエストやイシューの報告を歓迎します。

### 開発環境のセットアップ

```bash
git clone <repository-url>
cd pc_assistant_app
./install.sh
```

### コーディング規約

- **Python**: PEP 8に準拠
- **コメント**: 日本語で記述
- **テスト**: 新機能には必ずテストを追加

## 📄 ライセンス

MIT License

## 👥 作成者

**Manus AI** - PC操作支援アプリケーション開発チーム

---

## 📞 サポート

問題が発生した場合は、以下の情報を含めてお問い合わせください：

- OS とバージョン
- Python バージョン
- エラーメッセージ
- 実行したコマンド
- test_report.md の内容

**🎉 PC操作支援アプリケーションをお楽しみください！**
