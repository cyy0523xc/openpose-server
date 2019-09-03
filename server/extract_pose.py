# -*- coding: utf-8 -*-
#
# 参考：https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/v1.4.0/examples/tutorial_python/1_extract_pose.py
# Author: alex
# Created Time: 2019年09月02日 星期一 09时48分42秒
import cv2
# from openpose.openpose import OpenPose
from openpose import pyopenpose as op

# 路径配置
MODEL_ROOT = "/opt/openpose/models/"

params = dict()
params["model_folder"] = MODEL_ROOT
# params["logging_level"] = 3
# params["output_resolution"] = "-1x-1"
# params["net_resolution"] = "-1x368"
# params["model_pose"] = "BODY_25"
# params["alpha_pose"] = 0.6
# params["scale_gap"] = 0.3
# params["scale_number"] = 1
# params["render_threshold"] = 0.05
# If GPU version is built, and multiple GPUs are available, set the ID here
# params["num_gpu_start"] = 0
# params["disable_blending"] = False
# Ensure you point to the correct path where models are located
# params["default_model_folder"] = MODEL_ROOT
# Construct OpenPose object allocates GPU memory


def get_image_pose(image_path, display_image=False, output_path=None):
    """获取一个图片的人体关键点"""
    # Read new image
    img = cv2.imread(image_path)

    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    datum.cvInputData = img
    opWrapper.emplaceAndPop([datum])
    # Output keypoints and the image with the human skeleton blended on it
    # 人体 Body part 位置和检测的置信度(confidence)
    # 格式：[x, y, confidence]
    keypoints, output_image = datum.poseKeypoints, datum.cvOutputData

    if display_image:
        # Display the image
        cv2.imshow("output", output_image)
        cv2.waitKey(15)

    if output_path is not None:
        cv2.imwrite(output_path, output_image)

    return keypoints


if __name__ == '__main__':
    import sys
    image_path, output_path = None, None
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        raise Exception('need params: image_path')

    keypoints = get_image_pose(image_path, output_path=output_path)
    print(keypoints)
