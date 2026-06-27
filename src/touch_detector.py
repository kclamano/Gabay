import cv2
import os
import json
import numpy as np

def find_touch_coordinates(image_path):
    """
    Hahanapin ang bilog na touch indicator at ibabalik ang normalized coordinates (0.0 to 1.0).
    """
    img = cv2.imread(image_path)
    if img is None:
        return None

    height, width, _ = img.shape

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(
        blurred, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=50, 
        param1=50, 
        param2=30, 
        minRadius=10, 
        maxRadius=40
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :1]:
            x_pixel = int(i[0])
            y_pixel = int(i[1])
            radius = int(i[2])

            normalized_x = round(x_pixel / width, 4)
            normalized_y = round(y_pixel / height, 4)

            return {
                "absolute_x": x_pixel,
                "absolute_y": y_pixel,
                "normalized_x": normalized_x,
                "normalized_y": normalized_y,
                "radius": radius
            }
            
    return None

def process_all_keyframes(keyframes_dir):
    print("Scanning keyframes for touch indicators...")
    touch_data_manifest = {}

    files = sorted([f for f in os.listdir(keyframes_dir) if f.endswith('.jpg')])

    for file_name in files:
        full_path = os.path.join(keyframes_dir, file_name)
        coords = find_touch_coordinates(full_path)

        if coords:
            touch_data_manifest[file_name] = coords
            print(f"🎯 Touch detected in {file_name} at: ({coords['normalized_x']}, {coords['normalized_y']})")
        else:
            print(f"⚪ No touch detected in {file_name} (Likely a static transition or loading state)")

    output_json = os.path.join(keyframes_dir, "touch_coordinates.json")
    with open(output_json, "w") as f:
        json.dump(touch_data_manifest, f, indent=4)
        
    print(f"\nMatrix Map successfully compiled and saved to: {output_json}")

if __name__ == "__main__":
    KEYFRAMES_DIR = "output_keyframes"
    process_all_keyframes(KEYFRAMES_DIR)