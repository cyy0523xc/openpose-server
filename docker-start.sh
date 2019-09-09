#!/bin/bash
# 
# 
# Author: alex
# Created Time: 2019年09月02日 星期一 10时09分39秒
docker rm -f ibbd-openpose
docker run -d -u $(id -u):$(id -g) --rm --runtime=nvidia \
    -p 20950:20950 \
    --name ibbd-openpose \
    -v `pwd`:/opt/openpose/server \
    -e PYTHONPATH=/opt/openpose/python \
    -w /opt/openpose/server \
    registry.cn-hangzhou.aliyuncs.com/ibbd/pose:openpose \
    $*
