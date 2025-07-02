#!/bin/bash

# 初始化Git仓库并推送到GitHub

echo "🚀 准备部署网易云音乐数据可视化平台..."

# 初始化Git仓库
git init

# 创建.gitignore文件
cat > .gitignore << EOF
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.DS_Store
*.log
EOF

# 添加所有文件
git add .

# 提交
git commit -m "🎵 Initial commit: 网易云音乐数据可视化平台

Features:
- 🔑 Token管理系统
- 📊 数据可视化图表
- 📥 多格式数据下载
- 💻 响应式Web界面
- 🚀 支持云端部署"

echo "✅ Git仓库初始化完成！"
echo ""
echo "📋 下一步操作："
echo "1. 在GitHub上创建新仓库 'netease-music-viz'"
echo "2. 运行以下命令推送代码："
echo "   git remote add origin https://github.com/你的用户名/netease-music-viz.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 然后到 https://render.com 部署应用"
echo ""
echo "🎉 部署完成后，你就有一个在线的音乐数据分析平台了！"
