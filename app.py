# 1. install necessary libraries for AI and UI
import os
from google import genai
import gradio as gr
import os

# -----------------------------------------------------------
# API Key Configuration
# This key connects my app to Google's servers
MY_API_KEY = "................................"
# -----------------------------------------------------------

# Initialize the AI Client
my_dental_bot = genai.Client(api_key=MY_API_KEY)

# System Instructions (The Brain Logic)
# Defining the AI's persona as an expert dental consultant
instructions = """
You are an expert AI consultant specifically for dental students.
Your Role:
1. Explain dental anatomy, pathology, and treatments with high scientific precision.
2. Use correct professional terminology (e.g., Mesial, Distal, Buccal).
3. If asked about non-dental topics, politely decline to maintain focus.
"""

# 2. The main function to handle student queries for chat interface
def ask_gemini(student_question, chat_history): # chat_history is passed by gr.ChatInterface
    try:
        # Sending request to the latest Gemini 3 model
        response = my_dental_bot.models.generate_content(
            model="gemini-3-flash-preview",
            contents=instructions + "\n\nQuestion: " + student_question
        )
        return response.text
    except Exception as error:
        return f"System Error: {error}"

# 3. Function for X-ray analysis , generate quiz and clinical case
def analyze_xray_image(image):
    if image is None:
        return "Please upload an image for analysis."
    try:
        # Assuming the image is a PIL Image object as type="pil" suggests
        # Using a vision model for image analysis
        response = my_dental_bot.models.generate_content(
            model="gemini-3-flash-preview", # Use a vision-capable model for images
            contents=["Analyze this dental X-ray. What pathology do you see?", image]
        )
        return response.text
    except Exception as error:
      return f"System Error: {error}"

# Placeholder functions for quiz and clinical case, as they were incomplete
def generate_quiz(topic):
    # This function needs implementation based on the prompt's intent.
    # For now, it returns a placeholder.
    return f"Quiz for topic: {topic}\n(Implementation pending)"

def clinical_case():
    # This function needs implementation based on the prompt's intent.
    # For now, it returns a placeholder.
    return "New patient scenario generated!\n(Implementation pending)"

# 4. User Interface Design (UI) using gr.Blocks for multiple tabs
with gr.Blocks(title="🦷 Dental Genie | AI Student Assistant") as app:
    gr.Markdown("""
    # 🦷 Dental Genie | AI Student Assistant
    An intelligent assistant powered by **Gemini 3** technology, designed to help dental students with:
    * 🦴 Tooth Anatomy & Morphology.
    * 💊 Treatment Planning & Pharmacology.
    * 🔬 Clinical Diagnosis & Pathology.
    """)

    with gr.Tab("📝 Chat with Dental Genie"):
        gr.ChatInterface(
            fn=ask_gemini,
            examples=[
                ["Explain the anatomy of the Maxillary First Molar"],
                ["What are the steps of Root Canal Treatment?"],
                ["Difference between Gingivitis and Periodontitis"],
            ],
            submit_btn="Ask Gemini 🚀"
        )

    with gr.Tab("🩻 X-Ray Analysis"):
        gr.Markdown("Upload a dental X-ray to detect caries or pathologies.")
        with gr.Row():
            img_input = gr.Image(type="pil", label="Upload X-Ray", height=300)
            output_text = gr.Textbox(label="Diagnosis", lines=5)
        gr.Button("Analyze X-Ray").click(
            fn=analyze_xray_image,
            inputs=img_input,
            outputs=output_text
        )

    with gr.Tab("🎓 Quiz Mode"):
        gr.Markdown("### Test your knowledge!")
        topic_in = gr.Textbox(label="Enter Topic (e.g., Pulpitis, Local Anesthesia)")
        quiz_out = gr.Textbox(label="MCQs")
        btn_quiz = gr.Button("Generate Quiz", variant="secondary")
        btn_quiz.click(generate_quiz, inputs=topic_in, outputs=quiz_out)

    with gr.Tab("💡 Clinical Case Sim"):
        gr.Markdown("### Virtual Patient Scenario")
        case_btn = gr.Button("Start New Case 😷", variant="primary")
        case_out = gr.Textbox(label="Patient Scenario", lines=8)
        case_btn.click(clinical_case, inputs=None, outputs=case_out)

# Launch the application
app.launch()
