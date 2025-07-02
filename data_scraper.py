import requests
import pandas as pd
import json
from typing import Optional, Dict, Any

class NetEaseMusicScraper:
    def __init__(self, csrf_token: str, cookie: str):
        self.csrf_token = csrf_token
        self.cookie = cookie
        self.base_url = f'https://music.163.com/weapi/nmusician/statistics/songs/week?csrf_token={csrf_token}'
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Referer': 'https://music.163.com/musician/artist/dataCenter',
            'cookie': cookie,
            'content-type': 'application/x-www-form-urlencoded'
        }
        
        # 这些加密参数可能需要根据实际情况更新
        self.data_payload = {
            'params': 'Yip29TA5eWn3UqsHfWXCmqM8I3iFFYnroboKggaK8ofRvBc1CV/JHzPFk0lU2exgPpE+OtcOwP7sd/XxVyo2ZJdeDsqMfMRC0EDvAO3gPJkeUIs7aIhRYkpnfFNOwc8lhHJMfOUmdzrJvsgtaZvrZmYCJCRhSOu1NzRwUVvnEe0p9cKF+pvy6Ppg8NhPiAPI1K4YuaVx2FT1tq5gdjqLML9GIJ52nxgY8b5Jo7URxlw=',
            'encSecKey': '95d50a72469e5bfa09391cd5a0747602d1a9af693b1fb42ca1117a4b0c2fab8d1d9c7774926321e25ecc775685111ebc8322b252374d5020c9a4293cf5662b40490602f5a92c7102996e84a1e037a8d96715344dcd95e9fe7d4f26f364498f8611cb4b4149f13d214de9f48bcc90130982ecb57fc0b4ece0d062414bf74e63d0'
        }
    
    def fetch_songs_data(self) -> Optional[pd.DataFrame]:
        """获取歌曲数据"""
        try:
            response = requests.post(self.base_url, headers=self.headers, data=self.data_payload)
            response.raise_for_status()
            
            data_json = response.json()
            songs = data_json.get("data", {}).get("list", [])
            
            if not songs:
                return None
                
            df = pd.DataFrame(songs)
            return df
            
        except requests.RequestException as e:
            print(f"请求错误: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"数据解析错误: {e}")
            return None
    
    def update_credentials(self, csrf_token: str, cookie: str):
        """更新认证信息"""
        self.csrf_token = csrf_token
        self.cookie = cookie
        self.base_url = f'https://music.163.com/weapi/nmusician/statistics/songs/week?csrf_token={csrf_token}'
        self.headers['cookie'] = cookie
