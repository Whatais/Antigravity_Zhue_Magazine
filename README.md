
🚀 Magazine Cover Generator
Automated design powered by Antigravity Skills.

Stop designing covers pixel-by-pixel. This repository houses a robust pipeline that accepts raw assets (headlines, hero images, barcodes) and utilizes Antigravity Skills to assemble high-resolution, print-ready magazine covers automatically.

✨ Key Features
Antigravity Integration: deeply integrated with Antigravity Skills for intelligent layout handling and asset positioning.
Dynamic Typography: Automatic font scaling and color adjustment based on background contrast.
Template Engine: Switch between "Tech", "Fashion", or "News" styles with a single config flag.
Batch Processing: Generate 100+ variations in seconds for A/B testing or serialization.

⚡ Usage
No code execution or manual configuration is required. 
Usage: To generate a cover, follow these two simple steps:
1. Configure the Visuals: Update the Image.json file with the JSON code for your desired background image.
2. Run the Orchestrator: Open the Antigravity chat and enter the following prompt:
"I want to use the Zhué Magazine Master Orchestrator skill to produce the today's Zhué Magazine Cover"

🧩 Agent Skills Ecosystem
This repository utilizes a multi-agent architecture where specialized "Skills" collaborate to produce the final output. The Master Orchestrator manages the flow of data between the following agents:

1. 🌍 Global News Editorial Synthesizer
Role: Content Ingestion & Analysis

Function: Connects to global RSS feeds to extract trending news and current events. It filters and synthesizes this data to determine the editorial theme for the day's issue.

2. 🎨 Zhué Master Cover Architect
Role: Visual Synthesis

Function: Takes the thematic direction from the Editorial Synthesizer and generates the high-resolution background artwork or photography that serves as the visual anchor for the cover.

3. 📝 ZHUÉ Magazine Cover Generator
Role: Contextualization & Prompting

Function: Analyzes the generated background image to provide deep contextual descriptions. It bridges the gap between the raw visual and the editorial narrative, ensuring the headline matches the visual mood.

4. 📐 Zhué Magazine Cover Designer
Role: Composition & Assembly

Function: The layout engine. It takes the background image, the headlines, and the branding elements (logo, barcode, date) and composites them into the final, print-ready cover image.

5. 🎬 Animate ZHUÉ Magazine Cover
Role: Motion Graphics

Function: Takes the static cover produced by the Designer and applies motion effects to create a video version suitable for social media and digital distribution.

🤖 The Controller
⚡ Zhué Magazine Master Orchestrator
Role: Pipeline Manager

Function: This is the single entry point for the user. It autonomously chains the other five skills in the correct order—passing the RSS data to the Architect, the image to the Generator, and the assets to the Designer—executing the entire production workflow with a single prompt.

