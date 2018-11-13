## git仓库的发布版版本信息获取程序
### 程序功能
从指定git仓库文件夹中获取发布的tag信息，包括发布的版本号，版本号时间，以及该版本包含的代码量
### 文件内容介绍
此目录下包含两个文件
- git_tag_msg.py: python脚本程序，信息获取程序源码。
- git_tag_ms: git_tag_msg.py程序编译得到的可执行程序
### 使用说明
linux系统下直接运行git_tag_msg可执行程序，具体说明如下：
- 目录结构： git仓库文件夹 和 git_tag_msg可执行程序 在同一目录下
- 运行命令： ./git_tag_msg <parameter>  参数为git仓库名字 
    例如：同一目录下包含lz4git仓库文件夹，使用命令./git_tag_msg lz4
- 注意事项：
    1. git仓库名字后不要加 ‘/’ 
    2. linux系统安装了cloc ( 代码量统计工具 )

