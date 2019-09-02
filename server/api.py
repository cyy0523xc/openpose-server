# -*- coding: utf-8 -*-
#
#
# Author: alex
# Created Time: 2019年09月02日 星期一 10时12分24秒
from extract_pose import get_image_pose, get_openpose
from extract_pose_video import get_video_pose


def image_pose(image_path, output_path=None):
    openpose = get_openpose()
    points = get_image_pose(openpose, image_path, output_path=output_path)
    return points.tolist()


def video_pose(video_path, output_path='out_video.avi'):
    openpose = get_openpose()
    get_video_pose(openpose, video_path, output_path)


if __name__ == '__main__':
    from fireRest import API, app
    API(image_pose)
    API(video_pose)
    # 报错
    # The CPU/GPU pointer data cannot be accessed from a different thread.
    app.run(port=20950, host='0.0.0.0')
