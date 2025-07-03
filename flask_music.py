from flask import Flask, render_template, request, send_file, jsonify
import requests
import pandas as pd
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('music_simple.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    csrf_token = data.get('csrf_token', '').strip()
    cookie = data.get('cookie', '').strip()
    if not csrf_token or not cookie:
        return jsonify({'success': False, 'msg': '请填写Token和Cookie'})
    url = f'https://music.163.com/weapi/nmusician/statistics/songs/week?csrf_token={csrf_token}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Referer': 'https://music.163.com/musician/artist/dataCenter',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie
    }
    data_payload = {
        'params': 'ClFG79vP3DQNic5XLqAXBhR62nFX94i6U4WPQLeip/ZDiaeoqayvGWv0MZoEV9uATwU0AujW4EU8Fi9u2cWCaz7sX2R53bzBtfi24ZjTpF/pXJiGfM7CNHE3/8Mz32WJ9ZRl5/U6Sm9XO1HetudtlLGokPM4GjkCpKK3vRw6B42wDUFPk2gDhPc62Tv31DMf6g84X44IjYRbi/NqlLwyIDKiZxzk3vQ8qhDrWrPNsfY=',
        'encSecKey': 'a4a4ea6b5c69c5cda09dc29b4450d09649f8e9fd2b6015617afb028089f0c07b6914e9190324acfcef87e5dbb152610c12be5fee357dc570477234244950e0348c68276f4ad557b479e5c08a8c53fec51d0821dcd7deb6b3437a2939105508af6d3d45cf1a43ec381847c7bd345761cc6d33f09fb2b343b0bd58e75785fe13db'
    }
    try:
        resp = requests.post(url, headers=headers, data=data_payload, timeout=10)
        resp.raise_for_status()
        data_json = resp.json()
        songs = data_json["data"]["list"]
        df = pd.DataFrame(songs)
        preview = df.head(10).to_dict('records')
        return jsonify({'success': True, 'preview': preview, 'columns': list(df.columns), 'count': len(df)})
    except Exception as e:
        return jsonify({'success': False, 'msg': f'爬取失败: {e}'})

@app.route('/download/<fmt>', methods=['POST'])
def download(fmt):
    csrf_token = request.form.get('csrf_token', '').strip()
    cookie = request.form.get('cookie', '').strip()
    if not csrf_token or not cookie:
        return '缺少Token或Cookie', 400
    url = f'https://music.163.com/weapi/nmusician/statistics/songs/week?csrf_token={csrf_token}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Referer': 'https://music.163.com/musician/artist/dataCenter',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie
    }
    data_payload = {
        'params': 'ClFG79vP3DQNic5XLqAXBhR62nFX94i6U4WPQLeip/ZDiaeoqayvGWv0MZoEV9uATwU0AujW4EU8Fi9u2cWCaz7sX2R53bzBtfi24ZjTpF/pXJiGfM7CNHE3/8Mz32WJ9ZRl5/U6Sm9XO1HetudtlLGokPM4GjkCpKK3vRw6B42wDUFPk2gDhPc62Tv31DMf6g84X44IjYRbi/NqlLwyIDKiZxzk3vQ8qhDrWrPNsfY=',
        'encSecKey': 'a4a4ea6b5c69c5cda09dc29b4450d09649f8e9fd2b6015617afb028089f0c07b6914e9190324acfcef87e5dbb152610c12be5fee357dc570477234244950e0348c68276f4ad557b479e5c08a8c53fec51d0821dcd7deb6b3437a2939105508af6d3d45cf1a43ec381847c7bd345761cc6d33f09fb2b343b0bd58e75785fe13db'
    }
    try:
        resp = requests.post(url, headers=headers, data=data_payload, timeout=10)
        resp.raise_for_status()
        data_json = resp.json()
        songs = data_json["data"]["list"]
        df = pd.DataFrame(songs)
        if fmt == 'csv':
            output = io.BytesIO()
            df.to_csv(output, index=False, encoding='utf-8-sig')
            output.seek(0)
            return send_file(output, mimetype='text/csv', as_attachment=True, download_name='netease_music.csv')
        elif fmt == 'xlsx':
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            output.seek(0)
            return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='netease_music.xlsx')
        else:
            return '不支持的格式', 400
    except Exception as e:
        return f'下载失败: {e}', 500

if __name__ == '__main__':
    app.run(debug=True, port=5005)
