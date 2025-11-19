#!/usr/bin/env python3
"""
SENPAI - PC操作ガイド（シンプルライブラリ機能付き）実行ファイル
安定版ベースにシンプルなお気に入り機能を追加
"""

import sys
import os

# パスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_controller_with_simple_library import main

if __name__ == "__main__":
    main()
