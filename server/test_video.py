# -*- coding: utf-8 -*-
#
# 生成demo视频
# Author: alex
# Created Time: 2019年09月02日 星期一 14时21分56秒
import re
import cv2
import numpy as np
from openpose import pyopenpose as op
from extract_pose import params

# 配置动作
src_config = [
    ["00:01 — 00:16 sleep",
     "00:20 — 00:38 nap",
     "00:47 — 00:53 play_phone"],
    ["00:01 — 00:12 sleep",
     "00:13 — 00:24 call",
     "00:26 — 00:40 nap",
     "00:41 — 00:53 play_phone"],
    ["00:01 — 00:11 sleep",
     "00:26 — 00:40 nap",
     "00:44 — 00:53 nap"],
    ["00:01 — 00:11 sleep",
     "00:14 — 00:23 call",
     "00:23 — 00:24 play_phone",
     "00:29 — 00:53 nap"],
    ["00:01 — 00:26 sleep",
     "00:26 — 00:39 nap",
     "00:42 — 00:53 play_phone"],
]
src_config = [
    [
        # "00:02 — 00:03 hurdle",
        "00:01 — 00:02 nap",
        "00:03 — 00:10 sleep",
    ],
]
config = None


def parse_config():
    global config
    pattern = re.compile('00:(\\d+) — 00:(\\d+) (.+)')
    config = []
    for index, person_config in enumerate(src_config):
        print(pattern.findall(person_config[0]))
        row = [pattern.findall(rule)[0] for rule in person_config]
        row = [(int(i[0])*1000, int(i[1])*1000, i[2]) for i in row]
        config.append(row)


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

        # Process Image
        datum = op.Datum()
        datum.cvInputData = frame
        opWrapper.emplaceAndPop([datum])
        keypoints, output_image = datum.poseKeypoints, datum.cvOutputData

        msec = int(vc.get(cv2.CAP_PROP_POS_MSEC))
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
    if len(np.atleast_1d(keypoints)) < 2 and keypoints.size < 2:
        return output_image

    # TODO 下面部分是临时的处理
    if len(src_config) > 1:
        if len(keypoints) != len(src_config):
            # TODO 通过keypoints来判断人数并不对
            return output_image

    px, py = [], []
    for p in keypoints:
        px.append([r[0] for r in p if r[2] > 0.1])
        py.append([r[1] for r in p if r[2] > 0.1])

    rects = [(int(min(x)), int(min(y)), int(max(x)), int(max(y)),
              sum(x)/len(x))
             for x, y in zip(px, py)]
    if len(src_config) > 1:
        rects = sorted(rects, key=lambda x: x[-1])
    else:
        x = [i[0] for i in rects]
        y = [i[1] for i in rects]
        xb = [i[2] for i in rects]
        yb = [i[3] for i in rects]
        rects = [(int(min(x)), int(min(y)), int(max(xb)), int(max(yb)), 0)]

    print(rects)
    for conf, rect in zip(config, rects):
        # 判断第i个人当前的状态
        action = get_action(msec, conf)
        if action is None:
            continue
        x, y, xb, yb, _ = rect
        x = max(x-9, 0)
        y = max(y-28, 0)
        xb = min(xb+9, w)
        yb = min(yb+9, h)
        cv2.rectangle(output_image, (x, y), (xb, yb), (0, 0, 255),
                      thickness=2)
        cv2.putText(output_image, action, (x+5, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (128, 255, 0), 2)

    return output_image


def get_action(msec, confs):
    for conf in confs:
        if conf[0] < msec < conf[1]:
            return conf[2]

    return None


if __name__ == '__main__':
    import sys
    parse_config()
    get_video_pose(sys.argv[1], sys.argv[2])
