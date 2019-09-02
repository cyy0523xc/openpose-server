# -*- coding: utf-8 -*-
#
# 参考：https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/v1.4.0/examples/tutorial_python/1_extract_pose.py
# Author: alex
# Created Time: 2019年09月02日 星期一 09时48分42秒
import sys
import cv2

# 路径配置
PYTHON_API_ROOT = '/opt/openpose/python/'
MODEL_ROOT = "/opt/openpose/models/"

# Remember to add your installation path here
# Option a
sys.path.append(PYTHON_API_ROOT);
# Option b
# If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
# sys.path.append('/usr/local/python')

# Parameters for OpenPose. Take a look at C++ OpenPose example for meaning of components. Ensure all below are filled
try:
    from openpose import OpenPose
except:
    raise Exception('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')

params = dict()
params["logging_level"] = 3
params["output_resolution"] = "-1x-1"
params["net_resolution"] = "-1x368"
params["model_pose"] = "BODY_25"
params["alpha_pose"] = 0.6
params["scale_gap"] = 0.3
params["scale_number"] = 1
params["render_threshold"] = 0.05
# If GPU version is built, and multiple GPUs are available, set the ID here
params["num_gpu_start"] = 0
params["disable_blending"] = False
# Ensure you point to the correct path where models are located
params["default_model_folder"] = MODEL_ROOT
# Construct OpenPose object allocates GPU memory

openpose = OpenPose(params)


def get_image_pose(image_path, display_image=False, output_path=None):
    """获取一个图片的人体关键点"""
    # Read new image
    img = cv2.imread(image_path)
    # Output keypoints and the image with the human skeleton blended on it
    keypoints, output_image = openpose.forward(img, True)
    # Print the human pose keypoints, i.e., a [#people x #keypoints x 3]-dimensional numpy object with the keypoints of all the people on that image
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
