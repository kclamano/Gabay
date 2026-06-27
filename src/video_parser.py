import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def parse_video_to_keyframes(video_path, output_folder, ssim_threshold=0.90):
    create_directory(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Hindi mabuksan ang video file sa {video_path}")
        return

    frame_count = 0
    saved_count = 0
    last_saved_frame_gray = None

    print("Processing video frames... Hold on tight!")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if last_saved_frame_gray is None:
            last_saved_frame_gray = gray_frame
            frame_name = os.path.join(output_folder, f"keyframe_{saved_count:03d}_base.jpg")
            cv2.imwrite(frame_name, frame)
            saved_count += 1
            continue

        score, _ = ssim(last_saved_frame_gray, gray_frame, full=True)

        if score < ssim_threshold:
            frame_name = os.path.join(output_folder, f"keyframe_{saved_count:03d}_change.jpg")
            cv2.imwrite(frame_name, frame)
            
            last_saved_frame_gray = gray_frame
            saved_count += 1
            print(f"Frame {frame_count}: Change detected. SSIM: {score:.4f} -> Saved keyframe {saved_count}")

    cap.release()
    print(f"\nTask Complete! Parsed {frame_count} frames down to {saved_count} keyframes.")

if __name__ == "__main__":
    VIDEO_FILE = "input_videos/gcash_sample.mp4" 
    OUTPUT_DIR = "output_keyframes"
    
    parse_video_to_keyframes(VIDEO_FILE, OUTPUT_DIR, ssim_threshold=0.92)