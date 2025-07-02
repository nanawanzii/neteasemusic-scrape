# 🚀 部署指南 - 免费云服务器

## 方案一：Render (推荐) ⭐

Render提供免费的Web服务，支持自动部署。

### 步骤：

1. **创建GitHub仓库**
   ```bash
   cd /Users/wangzi/Desktop/templates
   git init
   git add .
   git commit -m "Initial commit"
   # 在GitHub上创建新仓库，然后推送代码
   git remote add origin https://github.com/你的用户名/netease-music-viz.git
   git push -u origin main
   ```

2. **在Render部署**
   - 访问 [render.com](https://render.com)
   - 注册账号并连接GitHub
   - 点击 "New Web Service"
   - 选择你的GitHub仓库
   - 配置如下：
     - Name: `netease-music-viz`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`

3. **部署完成**
   - Render会自动分配一个URL，如：`https://netease-music-viz.onrender.com`
   - 每次推送代码到GitHub，会自动重新部署

**优点**: 
- 完全免费
- 自动SSL证书
- 自动部署
- 支持自定义域名

**限制**: 
- 免费版会在无活动时休眠
- 每月750小时运行时间

---

## 方案二：Railway

1. 访问 [railway.app](https://railway.app)
2. 连接GitHub仓库
3. 选择你的项目
4. Railway会自动检测并部署

---

## 方案三：Heroku

虽然Heroku不再提供免费计划，但你可以使用学生优惠。

---

## 方案四：PythonAnywhere (推荐新手)

1. 注册 [pythonanywhere.com](https://www.pythonanywhere.com)
2. 上传文件到Web应用目录
3. 配置WSGI文件

### PythonAnywhere配置：

创建 `/var/www/你的用户名_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

# 添加项目路径
project_home = '/home/你的用户名/netease-music-viz'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application

if __name__ == '__main__':
    application.run()
```

---

## 环境变量配置

对于生产环境，建议设置以下环境变量：

```
FLASK_ENV=production
SECRET_KEY=你的密钥
```

---

## 本地测试生产配置

在部署前，你可以本地测试生产配置：

```bash
# 安装gunicorn
pip install gunicorn

# 测试运行
gunicorn app:app

# 指定端口
gunicorn app:app --bind 0.0.0.0:8000
```

---

## 部署后优化

1. **设置自定义域名** (如果有)
2. **启用HTTPS** (大多数平台自动提供)
3. **监控和日志** (查看应用运行状态)
4. **设置环境变量** (保护敏感信息)

---

## 注意事项

1. **免费服务限制**: 大多数免费服务有资源限制
2. **休眠机制**: 无活动时应用可能休眠，首次访问会稍慢
3. **数据持久化**: 免费服务通常不提供持久化存储
4. **流量限制**: 注意每月流量限制

---

## 推荐部署流程

1. **Render** - 最简单，自动化程度高
2. **Railway** - 界面友好，配置简单  
3. **PythonAnywhere** - 适合Python应用，有免费计划

选择Render的话，只需要推送代码到GitHub，然后在Render上点几下就能部署成功！
