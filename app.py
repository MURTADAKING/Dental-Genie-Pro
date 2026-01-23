# --------------------------------------------
# 1. install necessary libraries for AI and UI
#---------------------------------------------
import os
from google import genai
import gradio as gr
import os

# ---------------------------------------------------
# API Key Configuration
# This key connects my app to Google's servers
MY_API_KEY = os.environ.get("MY_API_KEY")
# ----------------------------------------------------

# Initialize the AI Client
my_dental_bot = genai.Client(api_key=MY_API_KEY)

# System Instructions (The Brain Logic)
instructions="""
You are an expert AI consultant specifically for dental students.
Your Role:
1. Explain dental anatomy, pathology, and treatments with high scientific precision.
2. Use correct professional terminology (e.g., Mesial, Distal, Buccal).
3. If asked about non-dental topics, politely decline to maintain focus."""


#------------------------------------------------------------------
# 2. The main function to handle student queries for chat interface
#------------------------------------------------------------------
def ask_gemini(student_question, chat_history): 
    try:
        # Sending request to the latest Gemini 3 model
        prompt= instructions +"\nconversation:\n"+ str (chat_history) +"\nStudent: " + student_question +"\nDental Genie"
        response = my_dental_bot.models.generate_content(
            model="gemini-3-flash-preview",
            contents= prompt)
        
        return response.text
    except Exception as error:
        return f"System Error: {error}"

#-----------------------------------------------------------------
# 3. Function for X-ray analysis , generate quiz and clinical case
#-----------------------------------------------------------------
def analyze_xray_image(image):
    if image is None:
        return "Please upload an image for analysis."
    try:
        # Assuming the image is a PIL Image object as type="pil" suggests
        # Using a vision model for image analysis
        response = my_dental_bot.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=["Analyze this dental X-ray. What pathology do you see?", image]
        )
        return response.text
    except Exception as error:
      return f"System Error: {error}"

def generate_quiz(topic):
    current_topic = topic if topic else "General Dentistry"
    try:
        return my_dental_bot.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=f"Create 3 challenging dental MCQs about {current_topic} with answers.",
            config={
                "max_output_tokens":2028 ,
                "temperature": 0.5 })
        return response.text
    except Exception as e: return str(e)

def clinical_case():
    try:
        return my_dental_bot.models.generate_content(
            model="gemini-3-flash-preview", 
            contents="Write a realistic dental clinical case scenario for diagnosis.").text
        return response.text
    except Exception as e: return str(e)

#----------------------------------------------------------------
# 4. User Interface Design (UI) using gr.Blocks for multiple tabs
#----------------------------------------------------------------
dental_theme = gr.themes.Soft(
primary_hue="cyan"
,secondary_hue="teal"
,neutral_hue="slate",
). set (button_primary_background_fill="*primary_500", button_primary_background_fill_hover="*primary_600")
custom_css ="""
#header {text-align: center; color: #0891b2;margin-bottom: 20px; }
#subtitle {text-align: center; font-size: 1.2em;color: #64748b}"""

with gr. Blocks (theme=dental_theme,css=custom_css,
title="Dental Genie Pro") as app :
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
        submit_btn="Ask Gemini 🚀")
        

    with gr.Tab("🩻 X-Ray Analysis"):
        gr.Markdown("Upload a dental X-ray to detect caries or pathologies.")
        with gr.Row():
            img_input = gr.Image(type="pil", label="Upload X-Ray", height=300)
            output_text = gr.Textbox(label="Diagnosis", lines=5)
        gr.Button("Analyze X-Ray").click(
            fn=analyze_xray_image,
            inputs=img_input,
            outputs=output_text)
        

    with gr.Tab("🎓 Quiz Mode"):
        gr.Markdown("### Test your knowledge!")
        topic_in = gr.Textbox(label="Enter Topic (e.g., Pulpitis, Local Anesthesia)")
        quiz_out = gr.Textbox(label="MCQs" , lines=20)
        btn_quiz = gr.Button("Generate Quiz", variant="secondary")
        btn_quiz.click(generate_quiz, inputs=topic_in, outputs=quiz_out)

    with gr.Tab("💡 Clinical Case Sim"):
        gr.Markdown("### Virtual Patient Scenario")
        case_btn = gr.Button("Start New Case 😷", variant="primary")
        case_out = gr.Textbox(label="Patient Scenario", lines=15)
        case_btn.click(clinical_case, inputs=None, outputs=case_out)
#--------------------------
# 5. Launch the application
#--------------------------
app.launch()
