# -*- coding: utf-8 -*-
#
# 参考：https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/v1.5.0/examples/tutorial_api_python/01_body_from_image.py
# Author: alex
# Created Time: 2019年09月02日 星期一 09时48分42秒
import cv2
# from openpose.openpose import OpenPose
from openpose import pyopenpose as op
from utils import parse_input_image, parse_output_image

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


def image_pose(image='', image_path='', image_type='jpg',
               return_data=True, return_image=False):
    """获取一个图片的人体关键点
    :param image 图片对象使用base64编码
    :param image_path 图片路径
    :param image_type 输入图像类型, 取值jpg或者png
    :param return_data 是否返回数据，默认为True。
    :param return_image 是否返回图片对象，base64编码，默认值为false
        当return_image=true时，返回值为{'image': 图片对象}，image值也是base64编码
    :return {'keypoints': [], 'image': str}
    """
    # Read new image
    img = parse_input_image(image=image, image_path=image_path,
                            image_type=image_type)
    keypoints, output_image = do_image_pose(img)

    data = {}
    if return_data:
        data['keypoints'] = keypoints.tolist()

    out_img = None
    if return_image:
        # output logo
        h, w, _ = output_image.shape
        cv2.putText(output_image, 'DeeAo AI Team', (w-250, h-12),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (128, 255, 0), 2)
        out_img = parse_output_image(output_image)

    return {
        'data': data,
        'image': out_img,
    }


def do_image_pose(img):
    """获取一个图片的人体关键点"""
    # Read new image
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
    return keypoints, output_image


if __name__ == '__main__':
    import sys
    image_path, output_path = None, None
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        raise Exception('need params: image_path')

    keypoints = image_pose(image_path)
    print(keypoints)
