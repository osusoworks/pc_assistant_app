#!/bin/bash

# PC操作支援アプリケーション - インストールスクリプト

echo "=========================================="
echo "PC操作支援アプリケーション - インストール"
echo "=========================================="
echo

# システム情報を表示
echo "🔍 システム情報:"
echo "OS: $(lsb_release -d | cut -f2)"
echo "Python: $(python3 --version)"
echo

# システムパッケージの更新
echo "📦 システムパッケージを更新中..."
sudo apt-get update

# 必要なシステムパッケージをインストール
echo "🔧 必要なシステムパッケージをインストール中..."
sudo apt-get install -y \
    python3-tk \
    build-essential \
    portaudio19-dev \
    python3-dev \
    python3.11-dev \
    python3-pip

# Pythonライブラリをインストール
echo "🐍 Pythonライブラリをインストール中..."
pip3 install --upgrade pip

# requirements.txtからインストール
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
else
    # 個別にインストール
    pip3 install \
        openai \
        Pillow \
        pynput \
        SpeechRecognition \
        pyaudio
fi

# インストール結果を確認
echo
echo "✅ インストール完了チェック:"

# Python モジュールの確認
python3 -c "
import sys
modules = ['tkinter', 'PIL', 'openai', 'speech_recognition', 'pynput']
missing = []

for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}: OK')
    except ImportError:
        print(f'❌ {module}: 不足')
        missing.append(module)

if missing:
    print(f'\\n⚠️  不足しているモジュール: {missing}')
    sys.exit(1)
else:
    print('\\n🎉 すべてのモジュールが正常にインストールされました！')
"

if [ $? -eq 0 ]; then
    echo
    echo "🚀 インストールが完了しました！"
    echo
    echo "📋 次のステップ:"
    echo "1. OpenAI APIキーを設定:"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
    echo
    echo "2. アプリケーションを実行:"
    echo "   python3 run_final.py"
    echo
    echo "📖 詳細な使用方法は README.md をご覧ください。"
else
    echo
    echo "❌ インストール中にエラーが発生しました。"
    echo "上記のエラーメッセージを確認して、必要な修正を行ってください。"
    exit 1
fi
