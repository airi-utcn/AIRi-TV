import cv2
import numpy as np
from rembg import remove, new_session
import torch
import subprocess
import argparse
import os
##local testing device for my macbook 
#device = 'mps' if torch.backends.mps.is_available() else 'cpu'

##server cuda
device = 'cuda' if torch.cuda.is_available() else 'cpu'

parser = argparse.ArgumentParser(description="add background and logo to final video")
parser.add_argument("input_video", help="path to source video")
parser.add_argument("output_dir",  help="folder and file to save the output")
parser.add_argument("background",  help="path to background image")
parser.add_argument("logo",  help="path to logo PNG with transparency")

args = parser.parse_args()

final_video = args.output_dir
video_path = args.input_video
bg_path = args.background
logo_path = args.logo

model_name = "u2net_human_seg"
session = new_session(model_name=model_name, device=device)

cap = cv2.VideoCapture(video_path)
bg_img_orig = cv2.imread(bg_path)
logo_img = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

temp_output = "temp.mp4"
bg_resized = cv2.resize(bg_img_orig, (width, height))
bg_float = bg_resized.astype(float) / 255.0

logo_width = int(width * 0.08)
aspect_ratio = logo_img.shape[0] / logo_img.shape[1]
logo_height = int(logo_width * aspect_ratio) 
logo_resized = cv2.resize(logo_img, (logo_width, logo_height)) 

padding = 4
y1, y2 = height - logo_height - padding, height - padding
x1, x2 = width - logo_width - padding, width - padding

logo_bgr = logo_resized[:, :, :3].astype(float) / 255.0
if logo_resized.shape[2] == 4:
    logo_mask = (logo_resized[:, :, 3].astype(float) / 255.0)[:, :, np.newaxis]
else:
    logo_mask = np.ones((logo_height, logo_width, 1))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(temp_output, fourcc, fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    result_bgra = remove(frame, session=session)

    alpha = result_bgra[:, :, 3].astype(float) / 255.0
    alpha = cv2.merge([alpha, alpha, alpha])
    fg = result_bgra[:, :, :3].astype(float) / 255.0

    final = (fg * alpha) + (bg_float * (1.0 - alpha))

    roi = final[y1:y2, x1:x2]
    blended_roi = (logo_bgr * logo_mask) + (roi * (1.0 - logo_mask))
    final[y1:y2, x1:x2] = blended_roi

    final_uint8 = (final * 255).astype(np.uint8)
    out.write(final_uint8)

cap.release()
out.release()

cmd = [
    'ffmpeg', '-y',
    '-i', temp_output,
    '-i', video_path,
    '-c', 'copy',
    '-map', '0:v:0',
    '-map', '1:a:0',
    '-shortest',
    final_video
]

subprocess.run(cmd)
del_cmd = ['rm', temp_output]
subprocess.run(del_cmd)