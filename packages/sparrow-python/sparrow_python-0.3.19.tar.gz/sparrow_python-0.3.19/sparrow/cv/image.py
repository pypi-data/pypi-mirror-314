import cv2
import numpy as np
from PIL import Image


def extract_frames(filename, start_time, end_time=-1, fps=None, n_frames=None, return_pil=True):
    """ extract frames """
    # 打开视频文件
    video = cv2.VideoCapture(filename)

    # 获取视频的帧率、总帧数、宽度和高度
    video_fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 计算开始和结束的帧
    start_frame = int(start_time * video_fps)
    if end_time == -1:
        end_frame = total_frames
    else:
        end_frame = int(end_time * video_fps)

    # 如果指定了fps，计算需要提取的帧数
    if fps:
        n_frames = int((end_frame / video_fps - start_time) * fps)

    # 如果既没有指定fps也没有指定n_frames，使用视频的原始帧率
    if n_frames is None:
        n_frames = end_frame - start_frame

    # 计算每隔多少帧提取一帧
    step = (end_frame - start_frame) / n_frames

    # 提取帧
    extracted_frames = []
    for i in np.arange(start_frame, end_frame, step):
        video.set(cv2.CAP_PROP_POS_FRAMES, int(i))
        ret, frame = video.read()
        if ret:
            # 将BGR转换为RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if return_pil:
                # 创建PIL图像对象
                pil_image = Image.fromarray(rgb_frame)
                extracted_frames.append(pil_image)
            else:
                extracted_frames.append(rgb_frame)
        else:
            break

    # 释放视频对象
    video.release()

    return {
        "shape": [width, height],
        "total_frames": total_frames,
        "original_fps": video_fps,
        "extracted_frames": extracted_frames
    }