# 网易云音乐数据可视化平台

一个基于Flask的Web应用，用于爬取、可视化和下载网易云音乐数据。

## 功能特性

🎵 **数据获取**: 从网易云音乐API获取歌曲数据
📊 **数据可视化**: 提供多种图表展示数据分析结果
📥 **数据下载**: 支持Excel、CSV、JSON格式下载
🔑 **Token管理**: 方便更新csrf_token和cookie

## 使用说明

### 1. 启动应用

```bash
cd /Users/wangzi/Desktop/templates
python3.12 app.py
```

应用将在 `http://127.0.0.1:5001` 启动

### 2. 更新访问凭证

由于网易云音乐的csrf_token会定期更新，你需要：

1. 打开网易云音乐网页版
2. 登录你的账号
3. 打开浏览器开发者工具 (F12)
4. 进入Network标签页
5. 刷新页面或进行一些操作
6. 找到包含`csrf_token`参数的请求
7. 复制最新的`csrf_token`和完整的`cookie`
8. 在网站首页填入这些信息并点击"更新Token"

### 3. 获取和查看数据

1. 点击"获取音乐数据"按钮
2. 等待数据加载完成
3. 查看生成的可视化图表
4. 浏览数据预览表格

### 4. 下载数据

数据获取成功后，你可以选择以下格式下载：
- **Excel (.xlsx)**: 适合在Excel中进一步分析
- **CSV**: 通用的表格数据格式
- **JSON**: 适合程序处理

## 可视化图表

应用会根据数据自动生成以下图表：

1. **热门歌曲排行**: 显示播放量最高的歌曲
2. **分类分布**: 饼图展示数据的分类分布
3. **时间趋势**: 如果有时间数据，显示趋势变化
4. **数值分布**: 箱线图展示数值字段的分布

## 文件结构

```
templates/
├── app.py              # Flask主应用
├── data_scraper.py     # 数据爬取模块
├── requirements.txt    # 依赖包列表
├── templates/
│   └── index.html     # 前端模板
└── README.md          # 说明文档
```

## 依赖包

- Flask: Web框架
- plotly: 数据可视化
- pandas: 数据处理
- requests: HTTP请求
- openpyxl: Excel文件处理

## 注意事项

1. **Token更新**: csrf_token和cookie需要定期更新，建议每次使用前都检查
2. **请求频率**: 不要频繁请求，避免被网易云音乐封IP
3. **数据准确性**: 数据来源于网易云音乐API，请以官方数据为准
4. **合规使用**: 请遵守网易云音乐的使用条款，仅用于个人学习和研究

## 开发模式

当前运行在开发模式下，如需生产部署，建议使用：
- Gunicorn作为WSGI服务器
- Nginx作为反向代理
- 设置适当的安全配置

## 🚀 免费部署

你可以免费部署到以下平台：

### 推荐：Render
1. 将代码推送到GitHub
2. 在 [render.com](https://render.com) 创建Web服务
3. 连接GitHub仓库，自动部署

### 其他选项：
- **Railway**: [railway.app](https://railway.app)
- **PythonAnywhere**: [pythonanywhere.com](https://www.pythonanywhere.com)

详细部署步骤请查看 `DEPLOYMENT.md` 文件。

## 故障排除

1. **Token失效**: 重新获取并更新csrf_token和cookie
2. **数据获取失败**: 检查网络连接和API可用性
3. **端口占用**: 修改app.py中的端口号
4. **依赖问题**: 运行 `pip install -r requirements.txt`

## 联系支持

如果遇到问题，请检查：
1. Python版本是否为3.7+
2. 所有依赖包是否正确安装
3. csrf_token和cookie是否有效
4. 网络连接是否正常
