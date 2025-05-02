import cv2
import os
from time import time

def extract_frames(video_path, extracted_frames_dir, frame_interval=50):  # Changed from 10 to 50
    # Ensure the output directory exists
    if not os.path.exists(extracted_frames_dir):
        print(f"🚨 '{extracted_frames_dir}' folder is missing! Creating it now...")
        os.makedirs(extracted_frames_dir)

    # Open the video
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Error: Could not open {video_path}")
        return False

    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"✅ Video loaded successfully")
    print(f"📊 Total frames in video: {total_frames}")
    print(f"📊 Video FPS: {fps}")
    
    frame_count = 0
    saved_count = 0
    start_time = time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Extract frame at specified interval
            if frame_count % frame_interval == 0:
                frame_filename = os.path.join(extracted_frames_dir, f"frame_{frame_count:04d}.jpg")
                success = cv2.imwrite(frame_filename, frame)
                
                if success:
                    saved_count += 1
                    if saved_count % 10 == 0:  # Status update every 10 saves
                        print(f"💾 Saved {saved_count} frames... (Current: {frame_filename})")
                else:
                    print(f"❌ Failed to save: {frame_filename}")
            
            frame_count += 1
            
            # Optional: Display progress
            if frame_count % 100 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"⏳ Progress: {progress:.1f}% ({frame_count}/{total_frames} frames processed)")

    except KeyboardInterrupt:
        print("\n⚠️ Processing interrupted by user")
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        
        # Print final statistics
        duration = time() - start_time
        print("\n📊 Final Statistics:")
        print(f"✅ Total frames processed: {frame_count}")
        print(f"💾 Frames saved: {saved_count}")
        print(f"⏱️ Processing time: {duration:.2f} seconds")
        print(f"📁 Output directory: {os.path.abspath(extracted_frames_dir)}")

def main():
    # Get the video file from downloads directory
    download_dir = "downloads"
    video_files = [f for f in os.listdir(download_dir) if f.endswith(".mp4")]

    if not video_files:
        print("❌ No video found in downloads/. Make sure a video is downloaded first!")
        return

    video_path = os.path.join(download_dir, video_files[0])
    print(f"🎥 Loading video: {video_path}")

    # Extract frames with updated interval of 50
    extract_frames(video_path, "extracted_frames", frame_interval=50)  # Changed from 10 to 50

if __name__ == "__main__":
    main()
