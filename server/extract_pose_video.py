# -*- coding: utf-8 -*-
#
#
# Author: alex
# Created Time: 2019年09月02日 星期一 10时18分10秒
import cv2


def get_video_pose(openpose, video_path, output_path):
    vc = cv2.VideoCapture(video_path)
    if vc.isOpened() is False:
        raise Exception('video open false!')

    fps = vc.get(cv2.CAP_PROP_FPS)
    size = (int(vc.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print('fps: ', fps)
    print('size: ', size)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, fps, size)
    i = 0
    while True:
        rval, frame = vc.read()
        if rval is False:
            break

        _, output_image = openpose.forward(frame, True)
        out.write(output_image)
        i += 1
        if i % 100 == 0:
            print('    i: ', i)

    print('Total: ', i)
    vc.release()
    if out is not None:
        out.release()

    cv2.destroyAllWindows()
