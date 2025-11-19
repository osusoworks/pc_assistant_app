"""
ユーザーフィードバックモジュール
ユーザーからのフィードバックを収集し、学習データとして保存
"""

import os
import json
import time
from typing import Dict, List


class UserFeedbackModule:
    """ユーザーフィードバックを管理するモジュール"""
    
    def __init__(self):
        """初期化"""
        self.feedback_data = []
        self.feedback_dir = os.path.expanduser("~/SENPAI")
        self.feedback_file = os.path.join(self.feedback_dir, "feedback_data.json")
        
        # フィードバックディレクトリを作成
        os.makedirs(self.feedback_dir, exist_ok=True)
    
    def get_user_confirmation(self, result: Dict) -> Dict:
        """
        ユーザーに確認を求める
        
        Args:
            result: 座標結果（複数候補を含む可能性あり）
        
        Returns:
            ユーザーが選択した座標結果
        """
        print("=== ユーザーフィードバック ===")
        
        # 現在のバージョンでは、自動的に信頼度を高に設定
        # 将来的には、UIモジュールを使用してユーザーに確認を求める
        
        # 代替座標がある場合は、複数候補を表示
        candidates = [
            {'x': result['x'], 'y': result['y'], 'description': 'メイン候補'}
        ]
        
        if 'alternative_coordinates' in result:
            for alt in result['alternative_coordinates']:
                candidates.append(alt)
        
        if len(candidates) == 1:
            # 候補が1つの場合は、そのまま使用
            print(f"座標: ({result['x']}, {result['y']})")
            print("（将来的には、ユーザーに正誤確認を求める機能を追加予定）")
            
            result['confidence'] = 'high'
            result['user_confirmed'] = True
        else:
            # 候補が複数の場合は、メイン候補を使用
            print(f"複数の候補があります。メイン候補を使用: ({result['x']}, {result['y']})")
            print("（将来的には、ユーザーに選択させる機能を追加予定）")
            
            result['confidence'] = 'high'
            result['user_selected'] = True
        
        # フィードバックデータを保存
        self._save_feedback(result)
        
        return result
    
    def _save_feedback(self, result: Dict):
        """
        フィードバックデータを保存
        
        Args:
            result: 座標結果
        """
        feedback = {
            'timestamp': time.time(),
            'coordinates': {'x': result['x'], 'y': result['y']},
            'confidence': result['confidence'],
            'method': result.get('method', 'unknown'),
            'user_action': result.get('user_confirmed', False) or result.get('user_corrected', False) or result.get('user_selected', False),
            'verified': result.get('verified', False),
            'correction_applied': result.get('correction_applied', False)
        }
        
        self.feedback_data.append(feedback)
        
        # ファイルに追記
        try:
            with open(self.feedback_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(feedback, ensure_ascii=False) + '\n')
            
            print(f"フィードバックデータを保存: {self.feedback_file}")
        
        except Exception as e:
            print(f"フィードバック保存エラー: {e}")
    
    def get_feedback_statistics(self) -> Dict:
        """
        フィードバック統計を取得
        
        Returns:
            統計情報
        """
        if not os.path.exists(self.feedback_file):
            return {
                'total_count': 0,
                'method_distribution': {},
                'confidence_distribution': {},
                'verification_rate': 0.0,
                'correction_rate': 0.0
            }
        
        try:
            feedback_list = []
            
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                for line in f:
                    feedback_list.append(json.loads(line.strip()))
            
            total_count = len(feedback_list)
            
            # 方式別の分布
            method_distribution = {}
            for feedback in feedback_list:
                method = feedback.get('method', 'unknown')
                method_distribution[method] = method_distribution.get(method, 0) + 1
            
            # 信頼度別の分布
            confidence_distribution = {}
            for feedback in feedback_list:
                confidence = feedback.get('confidence', 'unknown')
                confidence_distribution[confidence] = confidence_distribution.get(confidence, 0) + 1
            
            # 検証率
            verified_count = sum(1 for f in feedback_list if f.get('verified', False))
            verification_rate = verified_count / total_count if total_count > 0 else 0.0
            
            # 修正率
            corrected_count = sum(1 for f in feedback_list if f.get('correction_applied', False))
            correction_rate = corrected_count / total_count if total_count > 0 else 0.0
            
            return {
                'total_count': total_count,
                'method_distribution': method_distribution,
                'confidence_distribution': confidence_distribution,
                'verification_rate': verification_rate,
                'correction_rate': correction_rate
            }
        
        except Exception as e:
            print(f"統計取得エラー: {e}")
            return {
                'total_count': 0,
                'method_distribution': {},
                'confidence_distribution': {},
                'verification_rate': 0.0,
                'correction_rate': 0.0
            }

