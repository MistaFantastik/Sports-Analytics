import cv2
import os
import torch
from ultralytics import YOLO

# Load YOLOv8 model (pre-trained on COCO dataset)
model = YOLO("yolov8m.pt")  # 'n' = nano, change to 's', 'm', 'l' for larger models

# Class labels in COCO dataset
BASKETBALL_CLASS_ID = 32  # Basketball class in COCO
PERSON_CLASS_ID = 0  # Person class in COCO

# Folder where extracted frames are stored
frames_dir = "extracted_frames"
output_dir = "detected_frames"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process each frame in extracted_frames folder
for frame_file in sorted(os.listdir(frames_dir)):
    if frame_file.endswith(".jpg"):
        frame_path = os.path.join(frames_dir, frame_file)
        image = cv2.imread(frame_path)

        # Run YOLOv8 on the image
        results = model(image)

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls.item())  # Get class ID
                conf = box.conf.item()  # Confidence score

                if class_id in [PERSON_CLASS_ID, BASKETBALL_CLASS_ID] and conf > 0.4:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Assign different colors for player and basketball
                    color = (0, 255, 0) if class_id == PERSON_CLASS_ID else (0, 0, 255)
                    
                    # Draw bounding box
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

                    # Label the detection
                    label = "Player" if class_id == PERSON_CLASS_ID else "Basketball"
                    cv2.putText(image, f"{label} ({conf:.2f})", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Save the processed frame
        output_path = os.path.join(output_dir, frame_file)
        cv2.imwrite(output_path, image)

        print(f"✅ Processed: {frame_file}")

print("\n🏀 Detection complete! Check the 'detected_frames' folder.")
