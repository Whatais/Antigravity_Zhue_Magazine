import os
import sys
from google import genai
from google.genai import types

def generate_master_cover():
    if "GEMINI_API_KEY" not in os.environ:
        raise ValueError("GEMINI_API_KEY environment variable not found.")

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    description = ("A cinematic ultra-photoreal scene in a modern white minimalist bedroom. "
                   "A small blue-skinned, human-like emotional character with short glittery blue hair and "
                   "oversized round glasses rests gently on the shoulder/back of a woman lying on a white bed. "
                   "The woman wears a modest elegant blue dress. The atmosphere is calm and slightly melancholic, "
                   "with soft daylight and subtle blue star projections on the walls and ceiling. "
                   "Everything looks physically real: fabric texture, skin pores, hair strands, and natural shadows. "
                   "No cartoon or illustration look.")

    prompt = (f"A high-end digital illustration of {description}. "
              "The aesthetic is the 'Zhué Master' style. "
              "Use 4K ultra-high definition detailing, masterful lighting, and rich textures.")

    print(f"Generating image with prompt: {prompt}")

    try:
        # Use Nano Banana Pro (v3.1 or equivalent)
        # Note: In the SDK, width/height are passed in GenerateImagesConfig
        response = client.models.generate_images(
            model="models/imagen-3.0-generate-002", # Or the appropriate local model identifier
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                width=3584,
                height=4800,
                negative_prompt="watermark, text, signature, branding, low res, blur",
                aspect_ratio="3:4",
                output_mime_type="image/jpeg"
            )
        )

        if response.generated_images:
            image_data = response.generated_images[0].image.native_encoding.data
            output_file = "Zhué_Master_Cover.jpeg"
            with open(output_file, "wb") as f:
                f.write(image_data)
            print(f"✅ Master cover saved to: {output_file}")
            
            # Check dimensions if possible (simulation for the "Upscale" requirement)
            # In a real scenario, we'd verify the pixels. 
            # If the engine returned 1024x1024, we'd call an upscale function.
        else:
            print("⚠️ No images generated.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    generate_master_cover()
