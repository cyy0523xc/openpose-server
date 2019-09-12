# -*- coding: utf-8 -*-
#
# 生成demo视频
# Author: alex
# Created Time: 2019年09月02日 星期一 14时21分56秒
import cv2
from openpose import pyopenpose as op
from extract_pose import params

# 开始结束时间
start = 0
end = 10*1000


def get_video_pose(video_path, output_path):
    vc = cv2.VideoCapture(video_path)
    if vc.isOpened() is False:
        raise Exception('video open false!')

    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    fps = vc.get(cv2.CAP_PROP_FPS)
    size = (int(vc.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print('fps: ', fps)
    print('size: ', size)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, size)
    i = 0
    while True:
        rval, frame = vc.read()
        if rval is False:
            break

        msec = int(vc.get(cv2.CAP_PROP_POS_MSEC))
        if msec < start or msec > end:
            continue

        # Process Image
        datum = op.Datum()
        datum.cvInputData = frame
        opWrapper.emplaceAndPop([datum])
        keypoints, output_image = datum.poseKeypoints, datum.cvOutputData

        output_image = parse_out_image(keypoints, output_image, msec)
        out.write(output_image)
        i += 1
        if i % 100 == 0:
            print('    i: ', i)

    print('Total: ', i)
    vc.release()
    if out is not None:
        out.release()

    cv2.destroyAllWindows()


def parse_out_image(keypoints, output_image, msec):
    """处理输出图像"""
    h, w, _ = output_image.shape
    cv2.putText(output_image, 'DeeAo AI Team', (w-250, h-12),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (128, 255, 0), 2)
    return output_image


def get_action(msec, confs):
    for conf in confs:
        if conf[0] < msec < conf[1]:
            return conf[2]

    return None


if __name__ == '__main__':
    import sys
    get_video_pose(sys.argv[1], sys.argv[2])
