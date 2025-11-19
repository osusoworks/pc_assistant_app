# PC操作支援アプリケーション

PCで操作をしている際、アプリでもゲームでも不明点があったら教えてくれるAI支援アプリケーションです。

## 機能

- **画面キャプチャ**: `Ctrl+Alt+S` でスクリーンショットを撮影
- **AI画面解析**: OpenAI GPT-4 Vision APIを使用して画面内容を理解
- **音声質問**: 音声で質問を入力可能
- **テキスト質問**: テキストでも質問を入力可能
- **操作指示**: 画面上に赤い矢印で操作箇所を表示
- **常駐機能**: バックグラウンドで動作し、必要時に即座に利用可能

## システム要件

- Python 3.11+
- Linux (Ubuntu 22.04で動作確認済み)
- マイクロフォン（音声入力を使用する場合）
- OpenAI APIキー

## インストール

### 1. 依存関係のインストール

```bash
# システムパッケージをインストール
sudo apt-get update
sudo apt-get install -y build-essential portaudio19-dev python3-dev python3.11-dev

# Pythonライブラリをインストール
pip3 install -r requirements.txt
```

### 2. OpenAI APIキーの設定

```bash
export OPENAI_API_KEY='your-api-key-here'
```

または、`.bashrc`に追加して永続化：

```bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## 使用方法

### 1. アプリケーションの起動

```bash
python3 run_app.py
```

### 2. 基本的な使用手順

1. **スクリーンショット撮影**: `Ctrl+Alt+S` を押してスクリーンショットを撮影
2. **質問入力**: 
   - 音声で質問（Right Shiftキーを押しながら話す）
   - またはテキストボックスに質問を入力
3. **回答確認**: AIが画面を解析して回答を表示
4. **操作指示**: 必要に応じて画面上に赤い矢印で操作箇所を表示

### 3. 質問例

- "このボタンは何をするものですか？"
- "次に何をすればいいですか？"
- "エラーメッセージの意味を教えてください"
- "この設定をどこで変更できますか？"

## ファイル構成

```
pc_assistant_app/
├── run_app.py              # メイン実行スクリプト
├── main_controller.py      # メインコントローラー
├── capture_module.py       # 画面キャプチャモジュール
├── speech_module.py        # 音声認識モジュール
├── ui_module.py           # ユーザーインターフェースモジュール
├── ai_module.py           # AI解析モジュール
├── overlay_module.py      # オーバーレイ表示モジュール
├── requirements.txt       # 必要なライブラリ一覧
└── README.md             # このファイル
```

## 各モジュールの説明

### main_controller.py
アプリケーション全体の制御を行うメインコントローラー。各モジュール間の連携を管理します。

### capture_module.py
画面キャプチャとホットキー監視を担当。`Ctrl+Alt+S`でスクリーンショットを撮影します。

### speech_module.py
音声認識機能を提供。SpeechRecognitionライブラリを使用してリアルタイム音声認識を行います。

### ui_module.py
ユーザーインターフェースを提供。tkinterを使用したGUIで質問入力と回答表示を行います。

### ai_module.py
AI解析機能を提供。OpenAI GPT-4 Vision APIを使用して画面解析と質問応答を行います。

### overlay_module.py
画面オーバーレイ機能を提供。透明ウィンドウを使用して画面上に矢印を表示します。

## トラブルシューティング

### PyAudioのインストールエラー

```bash
sudo apt-get install -y build-essential portaudio19-dev python3-dev
pip3 install pyaudio
```

### 音声認識が動作しない

1. マイクロフォンが正しく接続されているか確認
2. システムの音声設定でマイクが有効になっているか確認
3. 権限の問題がないか確認

### ホットキーが動作しない

1. 他のアプリケーションが同じホットキーを使用していないか確認
2. アプリケーションに適切な権限があるか確認

### オーバーレイが表示されない

1. ウィンドウマネージャーの設定を確認
2. 他のアプリケーションが最前面表示を妨げていないか確認

## 開発者向け情報

### テスト実行

各モジュールは個別にテスト可能です：

```bash
# キャプチャモジュールのテスト
python3 capture_module.py

# 音声認識モジュールのテスト
python3 speech_module.py

# UIモジュールのテスト
python3 ui_module.py

# オーバーレイモジュールのテスト
python3 overlay_module.py
```

### カスタマイズ

- ホットキーの変更: `capture_module.py`の`start()`メソッド内
- UI デザインの変更: `ui_module.py`の`_create_widgets()`メソッド内
- AI プロンプトの調整: `ai_module.py`の`_build_system_prompt()`メソッド内

## ライセンス

MIT License

## 作成者

**Manus AI** - PC操作支援アプリケーション開発チーム
