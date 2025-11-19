#!/usr/bin/env python3
"""
音声認識モジュール
"""

import threading
import time
from typing import Callable, Optional
import speech_recognition as sr
import pyaudio


class SpeechModule:
    """音声認識を担当するモジュール"""
    
    def __init__(self, callback: Callable[[str], None]):
        """
        初期化
        
        Args:
            callback: 音声認識結果を受け取るコールバック関数
        """
        self.callback = callback
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.listening = False
        self.listen_thread: Optional[threading.Thread] = None
        
        # マイクロフォンの初期化
        self._initialize_microphone()
    
    def _initialize_microphone(self):
        """マイクロフォンを初期化"""
        try:
            # 利用可能なマイクロフォンを取得
            mic_list = sr.Microphone.list_microphone_names()
            print(f"利用可能なマイクロフォン: {len(mic_list)}個")
            
            # デフォルトマイクロフォンを使用
            self.microphone = sr.Microphone()
            
            # 環境ノイズに合わせて調整
            print("環境ノイズを調整中...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("マイクロフォンの初期化が完了しました")
            
        except Exception as e:
            print(f"マイクロフォンの初期化に失敗しました: {e}")
            self.microphone = None
    
    def start(self):
        """音声認識を開始"""
        if not self.microphone:
            print("マイクロフォンが利用できません")
            return
        
        self.listening = True
        self.listen_thread = threading.Thread(target=self._listen_continuously, daemon=True)
        self.listen_thread.start()
        
        print("音声認識を開始しました")
    
    def stop(self):
        """音声認識を停止"""
        self.listening = False
        
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
            self.listen_thread = None
        
        print("音声認識を停止しました")
    
    def _listen_continuously(self):
        """継続的に音声を監視"""
        while self.listening:
            try:
                # 音声を録音
                with self.microphone as source:
                    print("音声を待機中... (話しかけてください)")
                    
                    # タイムアウトを設定して音声を待機
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # 音声認識を実行
                print("音声を認識中...")
                text = self.recognizer.recognize_google(audio, language='ja-JP')
                
                print(f"認識結果: {text}")
                
                # コールバックを呼び出し
                if self.callback and text.strip():
                    self.callback(text)
                
            except sr.WaitTimeoutError:
                # タイムアウトは正常な動作
                continue
            except sr.UnknownValueError:
                print("音声を認識できませんでした")
            except sr.RequestError as e:
                print(f"音声認識サービスエラー: {e}")
                time.sleep(1)  # エラー時は少し待機
            except Exception as e:
                print(f"音声認識エラー: {e}")
                time.sleep(1)
    
    def recognize_once(self, timeout: int = 5) -> Optional[str]:
        """
        一度だけ音声認識を実行
        
        Args:
            timeout: タイムアウト時間（秒）
            
        Returns:
            認識されたテキスト、失敗時はNone
        """
        if not self.microphone:
            print("マイクロフォンが利用できません")
            return None
        
        try:
            print("音声を録音中...")
            
            with self.microphone as source:
                # 環境ノイズを調整
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # 音声を録音
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            print("音声を認識中...")
            
            # 音声認識を実行
            text = self.recognizer.recognize_google(audio, language='ja-JP')
            
            print(f"認識結果: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("音声入力がタイムアウトしました")
            return None
        except sr.UnknownValueError:
            print("音声を認識できませんでした")
            return None
        except sr.RequestError as e:
            print(f"音声認識サービスエラー: {e}")
            return None
        except Exception as e:
            print(f"音声認識エラー: {e}")
            return None
    
    def set_recognition_settings(self, energy_threshold: int = None, 
                               dynamic_energy_threshold: bool = True):
        """
        音声認識の設定を変更
        
        Args:
            energy_threshold: エネルギー闾値
            dynamic_energy_threshold: 動的エネルギー闾値の使用
        """
        if energy_threshold is not None:
            self.recognizer.energy_threshold = energy_threshold
        
        self.recognizer.dynamic_energy_threshold = dynamic_energy_threshold
        
        print(f"音声認識設定を更新しました: "
              f"energy_threshold={self.recognizer.energy_threshold}, "
              f"dynamic_energy_threshold={dynamic_energy_threshold}")
    
    def is_available(self) -> bool:
        """
        音声認識機能が利用可能かどうかを確認
        
        Returns:
            bool: 利用可能な場合True
        """
        try:
            # マイクロフォンが初期化されているか確認
            if self.microphone is None:
                return False
            
            # speech_recognitionライブラリが利用可能か確認
            if not hasattr(sr, 'Recognizer'):
                return False
            
            # pyaudioが利用可能か確認
            try:
                import pyaudio
                # PyAudioのインスタンスを作成してテスト
                p = pyaudio.PyAudio()
                p.terminate()
                return True
            except Exception:
                return False
                
        except Exception as e:
            print(f"音声認識利用可能性チェックエラー: {e}")
            return False


# テスト用のメイン関数
if __name__ == "__main__":
    def test_callback(text):
        print(f"テスト: 音声認識結果 - {text}")
    
    # テスト実行
    speech = SpeechModule(test_callback)
    speech.start()
    
    print("音声認識テストを開始しました")
    print("話しかけてください（Ctrl+C で終了）")
    
    try:
        # メインスレッドを維持
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nテストを終了します")
        speech.stop()
