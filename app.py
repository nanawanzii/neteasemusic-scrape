from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import plotly.graph_objs as go
import plotly.utils
import json
import pandas as pd
from data_scraper import NetEaseMusicScraper
import io
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# 全局变量存储scraper实例
scraper = None
current_data = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': '网易云音乐数据可视化平台运行正常'})

@app.route('/update_token', methods=['POST'])
def update_token():
    global scraper
    csrf_token = request.form.get('csrf_token')
    cookie = request.form.get('cookie')
    
    if not csrf_token or not cookie:
        flash('请提供完整的csrf_token和cookie信息', 'error')
        return redirect(url_for('index'))
    
    scraper = NetEaseMusicScraper(csrf_token, cookie)
    flash('Token更新成功！', 'success')
    return redirect(url_for('index'))

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    global scraper, current_data
    
    if not scraper:
        return jsonify({'error': '请先更新Token信息'}), 400
    
    data = scraper.fetch_songs_data()
    if data is None:
        return jsonify({'error': '获取数据失败，请检查Token是否有效'}), 400
    
    current_data = data
    
    # 创建可视化图表
    charts = create_charts(data)
    
    return jsonify({
        'success': True,
        'charts': charts,
        'data_preview': data.head(10).to_dict('records'),
        'total_songs': len(data)
    })

def create_charts(df):
    """创建各种图表"""
    charts = {}
    
    # 确保数据列存在
    if df.empty:
        return charts
    
    # 获取数据列名
    columns = df.columns.tolist()
    
    # 图表1：歌曲播放量排行（假设有播放量相关字段）
    if any(col in columns for col in ['playCount', 'score', 'listenCount']):
        play_col = next((col for col in ['playCount', 'score', 'listenCount'] if col in columns), None)
        if play_col:
            top_songs = df.nlargest(10, play_col)
            
            fig1 = go.Figure(data=[
                go.Bar(x=top_songs.get('songName', top_songs.iloc[:, 0]), 
                       y=top_songs[play_col],
                       marker_color='lightblue')
            ])
            fig1.update_layout(
                title='Top 10 歌曲播放量',
                xaxis_title='歌曲名',
                yaxis_title='播放量',
                xaxis_tickangle=-45
            )
            charts['top_songs'] = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 图表2：数据分布饼图（基于数据类型或分类）
    if len(columns) > 1:
        # 如果有分类字段，创建饼图
        category_col = None
        for col in columns:
            if df[col].dtype == 'object' and df[col].nunique() < 20:
                category_col = col
                break
        
        if category_col:
            category_counts = df[category_col].value_counts().head(8)
            
            fig2 = go.Figure(data=[go.Pie(
                labels=category_counts.index,
                values=category_counts.values,
                hole=0.3
            )])
            fig2.update_layout(title=f'{category_col} 分布')
            charts['category_distribution'] = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 图表3：时间趋势（如果有时间字段）
    time_cols = [col for col in columns if 'time' in col.lower() or 'date' in col.lower()]
    if time_cols and len(df) > 1:
        time_col = time_cols[0]
        try:
            df_time = df.copy()
            df_time[time_col] = pd.to_datetime(df_time[time_col], errors='coerce')
            df_time = df_time.dropna(subset=[time_col])
            
            if len(df_time) > 1:
                time_series = df_time.groupby(df_time[time_col].dt.date).size()
                
                fig3 = go.Figure(data=[
                    go.Scatter(x=time_series.index, y=time_series.values,
                              mode='lines+markers',
                              line=dict(color='green'))
                ])
                fig3.update_layout(
                    title='时间趋势',
                    xaxis_title='日期',
                    yaxis_title='数量'
                )
                charts['time_trend'] = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        except:
            pass
    
    # 图表4：数值字段统计
    numeric_cols = df.select_dtypes
    if len(numeric_cols) > 0:
        fig4 = go.Figure()
        
        for col in numeric_cols[:3]:  # 最多显示3个数值字段
            fig4.add_trace(go.Box(y=df[col], name=col))
        
        fig4.update_layout(title='数值字段分布')
        charts['numeric_distribution'] = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

@app.route('/download/<format>')
def download_data(format):
    global current_data
    
    if current_data is None:
        flash('没有可下载的数据', 'error')
        return redirect(url_for('index'))
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            current_data.to_excel(writer, sheet_name='网易云音乐数据', index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'netease_music_data_{timestamp}.xlsx'
        )
    
    elif format == 'csv':
        output = io.StringIO()
        current_data.to_csv(output, index=False, encoding='utf-8-sig')
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'netease_music_data_{timestamp}.csv'
        )
    
    elif format == 'json':
        output = io.StringIO()
        current_data.to_json(output, orient='records', force_ascii=False, indent=2)
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'netease_music_data_{timestamp}.json'
        )
    
    else:
        flash('不支持的文件格式', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
