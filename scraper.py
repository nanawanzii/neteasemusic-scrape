import requests
import pandas as pd
import json

class NetEaseMusicScraper:
    def __init__(self, csrf_token: str, cookie: str):
        self.csrf_token = csrf_token
        self.cookie = cookie
        self.base_url = f'https://music.163.com/weapi/nmusician/statistics/songs/week?csrf_token={csrf_token}'
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Referer': 'https://music.163.com/musician/artist/dataCenter',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': cookie
        }
        
        # 使用你原始工作的加密参数
        self.data_payload = {
            'params': 'ClFG79vP3DQNic5XLqAXBhR62nFX94i6U4WPQLeip/ZDiaeoqayvGWv0MZoEV9uATwU0AujW4EU8Fi9u2cWCaz7sX2R53bzBtfi24ZjTpF/pXJiGfM7CNHE3/8Mz32WJ9ZRl5/U6Sm9XO1HetudtlLGokPM4GjkCpKK3vRw6B42wDUFPk2gDhPc62Tv31DMf6g84X44IjYRbi/NqlLwyIDKiZxzk3vQ8qhDrWrPNsfY=',
            'encSecKey': 'a4a4ea6b5c69c5cda09dc29b4450d09649f8e9fd2b6015617afb028089f0c07b6914e9190324acfcef87e5dbb152610c12be5fee357dc570477234244950e0348c68276f4ad557b479e5c08a8c53fec51d0821dcd7deb6b3437a2939105508af6d3d45cf1a43ec381847c7bd345761cc6d33f09fb2b343b0bd58e75785fe13db'
        }
    
    def fetch_songs_data(self):
        """获取歌曲数据 - 使用原始工作版本的逻辑"""
        try:
            response = requests.post(self.base_url, headers=self.headers, data=self.data_payload)
            response.raise_for_status()
            
            data_json = response.json()
            songs = data_json["data"]["list"]
            
            if not songs:
                print("没有获取到歌曲数据")
                return None
                
            df = pd.DataFrame(songs)
            print(f"成功获取 {len(df)} 首歌曲数据")
            return df
            
        except Exception as e:
            print(f"获取数据时出错: {e}")
            return None
    
    def update_credentials(self, csrf_token: str, cookie: str):
        """更新认证信息"""
        self.csrf_token = csrf_token
        self.cookie = cookie
        self.base_url = f'https://music.163.com/weapi/nmusician/statistics/songs/week?csrf_token={csrf_token}'
        self.headers['cookie'] = cookie
