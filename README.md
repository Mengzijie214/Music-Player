网易云风格音乐播放器 🎵
一款参考网易云音乐 UI 设计的本地音乐播放器，支持拖拽导入主流音乐格式，自动解码播放，提供完整的音乐管理和播放控制功能。
🌟 核心功能
拖拽导入：直接将音乐文件拖入界面即可自动导入并存储
多格式支持：兼容 MP3、FLAC、WAV、OGG、M4A、AAC、WMA 等主流格式
音乐管理：自动读取音频元数据（标题、艺术家、专辑、时长），支持删除操作
播放控制：播放 / 暂停、上一曲 / 下一曲、进度条拖拽跳转
网易云风格 UI：深色主题设计，简洁美观，操作流畅
自动存储：导入的音乐文件自动复制到应用专属目录，避免原文件删除影响播放
📋 支持格式
格式	扩展名
MP3	.mp3
FLAC	.flac
WAV	.wav
OGG	.ogg
M4A	.m4a
AAC	.aac
WMA	.wma
🚀 环境要求
Python 3.8+
操作系统：Windows/macOS/Linux
📦 安装步骤
1. 克隆 / 下载项目
bash
运行
# 克隆仓库（如果使用Git）
git clone https://github.com/mengzijie214/Music-Player.git
cd netease-music-player
2. 安装依赖
bash
运行
pip install -r requirements.txt
3. 准备图标资源
在 resources/icons/ 目录下放置以下图标文件（PNG 格式，建议尺寸）：
图标文件	用途	建议尺寸
play.png	播放按钮	48x48
pause.png	暂停按钮	48x48
prev.png	上一曲按钮	48x48
next.png	下一曲按钮	48x48
delete.png	删除按钮（可选）	24x24
推荐图标下载网站：Flaticon、IconFinder、Material Icons
4. 运行程序
bash
运行
python main.py
🎮 使用说明
1. 导入音乐
直接将本地音乐文件（支持格式见上表）拖入窗口中间的拖拽区域
导入成功后，音乐列表会自动刷新，显示歌曲标题、艺术家、专辑、时长等信息
2. 播放音乐
点击音乐列表中的任意歌曲，即可选中该歌曲
点击底部控制栏的 红色播放按钮 开始播放
播放过程中可通过进度条拖拽调整播放位置
3. 播放控制
按钮	功能
上一曲	切换到上一首歌曲
播放 / 暂停	开始播放或暂停当前歌曲
下一曲	切换到下一首歌曲
进度条	拖拽调整播放进度
4. 管理音乐
删除歌曲：点击音乐列表右侧的「删除」按钮，确认后即可删除（同时删除文件和数据库记录）
歌曲会自动按导入时间倒序排列
📂 项目结构
plaintext
netease_music_player/
├── main.py                  # 程序入口
├── requirements.txt         # 依赖包列表
├── ui/                      # UI界面相关
│   ├── main_window.py       # 主窗口布局
│   └── components/          # 组件封装（拖拽区、列表、控制栏）
├── core/                    # 核心逻辑
│   ├── music_manager.py     # 音乐管理（数据库+文件存储）
│   ├── player_engine.py     # 播放引擎
│   └── audio_decoder.py     # 音频解码
├── utils/                   # 工具函数
│   ├── file_utils.py        # 文件处理（格式筛选、复制）
│   └── audio_utils.py       # 音频工具（元数据、时长）
├── data/                    # 数据存储
│   ├── music_db.sqlite3     # 音乐数据库
│   └── music_files/         # 导入的音乐文件存储目录
└── resources/               # 资源文件
    ├── icons/               # 按钮图标
    └── styles/              # 主题样式（QSS）
❗ 常见问题
1. 拖拽文件后无反应？
检查文件格式是否在支持列表中
检查文件路径是否包含中文或特殊字符
确保应用有文件读写权限
2. 按钮没有显示图标？
确认图标文件已放在 resources/icons/ 目录下
确认图标文件名与代码中一致（区分大小写）
检查图标文件格式是否为 PNG
3. 播放无声音？
检查系统音量是否正常
确认音乐文件未损坏（可先用其他播放器测试）
重新安装依赖：pip install --upgrade pygame
4. 程序启动报错？
检查 Python 版本是否≥3.8
确认所有依赖已安装：pip install -r requirements.txt
检查项目目录结构是否完整
📌 注意事项
导入的音乐文件会自动复制到 data/music_files/ 目录，原文件可随意移动 / 删除
数据库文件 data/music_db.sqlite3 存储音乐元数据，请勿手动修改
程序关闭时会自动保存播放状态，下次启动可继续播放
建议定期清理 data/music_files/ 目录下不需要的音乐文件，释放存储空间
🚀 扩展建议
如果需要扩展功能，可参考以下方向：
添加音乐分类（按艺术家、专辑、导入时间）
实现播放列表功能（创建、编辑、保存）
添加音量控制滑块
支持音乐搜索功能
实现歌词显示（支持.lrc 文件）
添加音乐收藏功能
支持皮肤切换（浅色 / 深色主题）
实现音乐格式转换
添加均衡器调节功能
支持托盘图标控制（最小化时后台运行）
📄 许可证
本项目仅供学习使用，请勿用于商业用途。
如果遇到问题或有功能建议，欢迎提交 Issues 或 Pull Request！