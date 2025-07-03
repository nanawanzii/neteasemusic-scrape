# 🚀 一键部署到云端 (修复版)

## 问题修复

之前的部署错误是由于 pandas 2.1.3 与 Python 3.13 不兼容导致的。现在已修复：

1. ✅ 指定 Python 3.11.7 版本
2. ✅ 使用兼容的 pandas 2.0.3 版本
3. ✅ 添加 numpy 版本锁定

## 快速部署

### 方法一：使用脚本 (推荐)

```bash
cd /Users/wangzi/Desktop/templates
./deploy_setup.sh
```

然后按照脚本提示操作即可。

### 方法二：手动部署

1. **创建GitHub仓库**
   - 访问 [github.com](https://github.com)
   - 点击 "New repository"
   - 仓库名：`netease-music-viz`
   - 设为Public

2. **推送代码**
   ```bash
   cd /Users/wangzi/Desktop/templates
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/你的用户名/netease-music-viz.git
   git branch -M main
   git push -u origin main
   ```

3. **部署到Render**
   - 访问 [render.com](https://render.com)
   - 注册并连接GitHub
   - 点击 "New Web Service"
   - 选择你的仓库
   - 配置：
     - Name: `netease-music-viz`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - 点击 "Create Web Service"

4. **完成！**
   - 等待部署完成（约2-3分钟）
   - 获得你的在线地址：`https://你的应用名.onrender.com`

## 其他免费选项

### Railway
- 访问 [railway.app](https://railway.app)
- 连接GitHub，选择仓库
- 自动部署

### PythonAnywhere
- 注册 [pythonanywhere.com](https://www.pythonanywhere.com)
- 上传代码到Web apps
- 配置WSGI文件

## 部署后测试

1. 访问你的应用URL
2. 更新csrf_token和cookie
3. 测试数据获取和下载功能

## 注意事项

- 免费服务可能有休眠机制
- 首次访问可能需要等待几秒钟
- 建议定期访问保持活跃状态

🎉 **恭喜！现在你有一个专属的在线音乐数据分析平台了！**
