#!/bin/bash
# 
# 将项目打包压缩（用于正式打包）
# Author: alex
# Created Time: 2019年03月11日 星期一 10时38分16秒
cd ../
name="openpose-server"
if [ ! -d "$name" ]; then
    echo "$PWD: 当前目录错误."
fi
version=
if [ $# = 1 ]; then 
    version="-$1"
fi

# 删除旧的打包文件
date_str=`date -I`
filename="$name-${date_str//-/}$version".zip
if [ -f "$filename" ]; then
    rm -f "$filename"
fi

# 第一次打包时，记得把模型文件也打包在一起
# 正式发布时，记得过滤src目录中的内容
zip -r "$filename" "$name" \
    -x "*/.git/*" \
    -x "*/.*" \
    -x "*/src/*" \
    -x "*/*/*.swp" \
    -x "*/__pycache__/*" \
    -x "*/zip.sh" 

scp "$filename" ibbd@192.168.80.242:~/ocr/

date
echo "说明："
echo "第一次启动前，需要先安装基础库"
echo ""
echo ""
