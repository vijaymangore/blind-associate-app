# To navigate into a specific folder or path using the cd (change directory) command in Visual Studio Code, follow these steps:

# 1. Open the Integrated Terminal
# In VS Code, open the terminal by:
# Clicking on Terminal in the top menu and selecting New Terminal.
# Using the shortcut:
# Windows/Linux: `Ctrl + ``
# Mac: `Cmd + ``
# 2. Use the cd Command
# Use the cd command followed by the folder or path you want to navigate to. Examples:
# Navigate to a folder in the current directory:
# bash
# Copy code
# cd folder_name
# Navigate to a specific path:
# bash
# Copy code
# cd C:\Users\YourUsername\Documents\MyProject
# (Replace the path with the actual one you want to access.)
# 3. Tips for Using cd
# To go up one level:
# bash
# Copy code
# cd ..
# To navigate to the root directory:
# bash
# Copy code
# cd /
# To navigate to your home directory:
# bash
# Copy code
# cd ~
# 4. Auto-Complete Paths
# Type the initial letters of a folder or path and press the Tab key to auto-complete it.
# 5. Open Current Folder in VS Code
# If you want to open the folder you’ve navigated to in the terminal:
# bash
# Copy code
# code .
# This command opens the folder in the current VS Code instance.
# Example Scenario
# Say your project is in C:\Projects\MyApp:
# Open the terminal in VS Code.
# Navigate using:
# bash
# Copy code
# cd C:\Projects\MyApp
# Verify the directory by typing:
# bash
# Copy code
# pwd  # prints the working directory (on Linux/Mac)
# echo %cd%  # prints the current directory (on Windows)


import streamlit as st
from PIL import Image
import pyttsx3
import pytesseract
import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI

# Specify the Tesseract executable path (if not in PATH)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust based on your system

# Set API Key for Google Generative AI
f =  open('key.txt')
GOOGLE_API_KEY = f.read().strip()

# Initialize Google Generative AI
llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=GOOGLE_API_KEY)

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Add Custom CSS for Styling
st.markdown(
    """
    <style>
        body { background-color: #f7f9fc; }
        .main-title { font-size: 42px; font-weight: 600; text-align: center; color: #4A90E2; margin-bottom: 10px; }
        .subtitle { font-size: 18px; text-align: center; color: #666; margin-bottom: 30px; }
        .section-title { font-size: 22px; font-weight: 600; margin-top: 30px; margin-bottom: 15px; color: #333; }
        button { background-color: #4A90E2 !important; color: white !important; border-radius: 5px !important; }
        footer { text-align: center; margin-top: 50px; color: #777; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Application Title and Subtitle
# st.markdown('<div class="main-title">AI Vijay Assist</div>', unsafe_allow_html=True)
import streamlit as st

st.title(":blue[AI VIJAY ASSIST]")

# Function Definitions
def extract_text(image):
    """Extract text from an image using Tesseract OCR."""
    try:
        return pytesseract.image_to_string(image)
    except Exception as e:
        raise RuntimeError(f"Error during OCR: {e}")
    

from gtts import gTTS
from io import BytesIO

def text_to_speech(text):
    """Convert text to speech using gTTS and play in Streamlit."""
    try:
        tts = gTTS(text=text, lang='en')
        audio = BytesIO()
        tts.write_to_fp(audio)
        audio.seek(0)
        st.audio(audio, format="audio/mp3")
    except Exception as e:
        st.error(f"Error during Text-to-Speech: {e}")


# def text_to_speech(text):
#     """Convert text to speech using pyttsx3."""
#     try:
#         # Initialize the engine locally
#         engine = pyttsx3.init()
#         engine.say(text)
#         engine.runAndWait()
#         engine.stop()  # Stop the engine to reset the loop
#     except Exception as e:
#         raise RuntimeError(f"Error during Text-to-Speech: {e}")


def generate_scene_description(prompt, image_data):
    """Generate a scene description using Google Generative AI."""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content([prompt, image_data[0]])
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error generating scene description: {e}")

# Input Prompt for Scene Understanding
input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. A list of detected items and their purposes.
2. An overall description of the image.
3. Current status and past status of that images.
4. Make future predictions based on image analysis
5. Suggestions or precautions for visually impaired users.

"""

# Image Upload Section
st.markdown('<div class="section-title">📤 Upload an Image</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

# if uploaded_file:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image", use_container_width=True)
if uploaded_file:
    from PIL import ImageOps

    # Open the image
    image = Image.open(uploaded_file)

    # Resize image to reduce height while maintaining aspect ratio
    desired_height = 200  # Set your desired height in pixels
    aspect_ratio = image.width / image.height
    new_width = int(aspect_ratio * desired_height)
    resized_image = image.resize((new_width, desired_height))

    # Display the resized image
    st.image(resized_image, caption="Uploaded Image", use_container_width=False)



# Features Section
st.markdown('<div class="section-title">⚙️ Features</div>', unsafe_allow_html=True)
col1, col2, col3,col4 = st.columns(4)

scene_button = col1.button("🔍 Describe Scene")
ocr_button = col2.button("📝 Extract Text")
tts_button = col3.button("🔊 Text-to-Speech")
audio_scene_button = col4.button("🎤 Describe Scene in Audio")

# Process User Actions
if uploaded_file:
    # Prepare image data for Google Generative AI
    image_data = [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]

    # Describe Scene
    if scene_button:
        with st.spinner("Generating scene description..."):
            try:
                description = generate_scene_description(input_prompt, image_data)
                st.markdown('<div class="section-title">🔍 Scene Description</div>', unsafe_allow_html=True)
                st.write(description)
            except Exception as e:
                st.error(e)

    # Extract Text
    if ocr_button:
        with st.spinner("Extracting text..."):
            try:
                extracted_text = extract_text(image)
                st.markdown('<div class="section-title">📝 Extracted Text</div>', unsafe_allow_html=True)
                st.text_area("Extracted Text", extracted_text, height=200)
            except Exception as e:
                st.error(e)

    # Text-to-Speech
    if tts_button:
        with st.spinner("Converting text to speech..."):
            try:
                extracted_text = extract_text(image)
                if extracted_text.strip():
                    text_to_speech(extracted_text)
                    st.success("✅ Text-to-Speech completed!")
                else:
                    st.warning("No text found in the image.")
            except Exception as e:
                st.error(e)

# Add Button for Audio Scene Description
# audio_scene_button = st.button("🎤 Describe Scene in Audio")

if uploaded_file:
    # Prepare image data for Google Generative AI
    image_data = [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]

    # Describe Scene in Audio
    if audio_scene_button:
        with st.spinner("Generating scene description and audio..."):
            try:
                # Generate scene description using Google Generative AI
                description = generate_scene_description(input_prompt, image_data)

                # Display the description in text
                st.markdown('<div class="section-title">🔍 Scene Description</div>', unsafe_allow_html=True)
                st.write(description)

                # Convert the description to speech
                text_to_speech(description)
                st.success("✅ Scene description has been spoken!")
            except Exception as e:
                st.error(f"Error generating or narrating scene description: {e}")

























































