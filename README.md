# my_shooter_client
射手网字幕下载. 不同于射手页面上根据电影名来查找字幕, 这个脚本用的是SPlayer的公开API, 根据视频文件的指纹和文件名来查找的. 因此可靠性应相对更高.
根据https://github.com/xiaket/shooter_client 进行修改，修正了hash算法。禁用了ext字段。

##用法
python my_shooter_client.py Z:/剧集/black.mirror/black.mirror.s03e04.720p.webrip.x264-skgtv.mkv
