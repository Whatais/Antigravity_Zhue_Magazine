import os
import time
import sys
import io
from google import genai
from google.genai import types

# 1. Check for API Key
if "GEMINI_API_KEY" not in os.environ:
    raise ValueError("GEMINI_API_KEY environment variable not found.")

def animate_zhue_cover():
    # Fix for Windows terminal Unicode issues
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # 2. Initialize the new Client
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    image_path = "ZHUÉ_Final_Cover_Jan_2026.png"
    
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} not found.")
        return

    print(f"Animating cover: {image_path}...")

    prompt_text = (
        "Generate a high-quality video preview from this image. "
        "Animate the central elements of the magazine cover to create a cinematic effect. "
        "Keep the 'ZHUÉ' logo and text sharp and readable."
    )

    try:
        # 3. Load Image using SDK types
        image = types.Image.from_file(location=image_path)

        # 4. Generate Video (Asynchronous)
        print("Starting video generation...")
        
        # Build reference images list
        reference_images = [
            types.VideoGenerationReferenceImage(
                image=image,
                reference_type="ASSET"
            )
        ]

        operation = client.models.generate_videos(
            model="veo-001",
            prompt=prompt_text,
            config=types.GenerateVideosConfig(
                reference_images=reference_images
            )
        )
        
        # 5. Poll for completion
        print(f"Operation ID: {operation.name}")
        print("Waiting for video generation to complete...", end="", flush=True)
        
        while not operation.done:
            print(".", end="", flush=True)
            time.sleep(5)
            # Refetch the operation status
            operation = client.operations.get(name=operation.name)

        print("\nGeneration finished.")

        # 6. Handle the Output
        if operation.result and operation.result.generated_videos:
            video = operation.result.generated_videos[0]
            
            # Check for video data
            if video.video and video.video.native_encoding:
                video_bytes = video.video.native_encoding.data
                
                output_file = "ZHUÉ_Cover_Animation_Jan_2026.mp4"
                with open(output_file, "wb") as f:
                    f.write(video_bytes)
                print(f"✅ Animation saved to: {output_file}")
            else:
                print("⚠️ No video data found in response.")
                print(f"Result dump: {operation.result}")
        else:
            print("⚠️ No videos generated.")
            if operation.error:
                print(f"Operation error: {operation.error}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    animate_zhue_cover()
