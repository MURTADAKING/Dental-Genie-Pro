# ==========================================
# 1. Import Libraries
# ==========================================
import os
import traceback
from typing import List, Optional

import gradio as gr
from google import genai


# ============================================
# 2. API Key Configuration
# ============================================
MY_API_KEY = "............................."


# ============================================
# 3. Initialize AI Client
# ============================================
my_dental_bot = genai.Client(api_key=MY_API_KEY)


# =============================================
# 4. System Instructions
# =============================================
instructions = """
You are an expert dental AI assistant for students and clinicians.

Rules:
1. Always provide evidence-based answers. Cite textbooks, guidelines, or peer-reviewed sources if possible.
2. Use correct professional dental terminology (e.g., Mesial, Distal, Buccal, Periapical, Endodontic).
3. Structure all answers clearly:
   - Diagnosis or Main Finding
   - Explanation / Reasoning
   - Differential Diagnosis (if applicable)
   - Recommended Next Steps /
   Management
4. When analyzing X-ray images:
   - Describe all visible structures and any pathologies
   - Do not make assumptions beyond what is visible
   - Use standard radiology terminology
5. For clinical case questions:
   - Provide logical step-by-step reasoning
   - Include patient safety considerations
6. For quizzes:
   - Make them challenging but educational
   - Provide correct answers with explanations
7. If asked about non-dental topics:
   - Politely decline and redirect to dental topics
8. Never hallucinate data, dates, or make up studies.
9. Keep answers professional, concise, and educational.
10. Always format answers in clear sections with headings when possible.
"""


# ==============================================
# 5. The helper function
# ==============================================
def call_dental_bot(prompt_or_contents) -> str:
    """
    Call the Gemini AI model with error handling.
    Accepts either a string prompt or a list of contents (for images, etc.).
    """
    try:
        response = my_dental_bot.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt_or_contents
        )
        return response.text
    except Exception as error:
        return f"System Error: {error}\nTraceback:\n{traceback.format_exc()}"


# ===============================================
# 6. The Main Functions
# ===============================================


# ------------------
# Chatbot
# ------------------
def ask_gemini(message, history):
    conversation = ""
    for user, bot in history:
        conversation += f"User: {user}\nAssistant: {bot}\n"
    prompt = (
        instructions
        + "\nConversation:\n"
        + conversation
        + f"\nStudent: {message}\nDental Genie:"
    )

    return call_dental_bot(prompt)


# --------------------
# X-Ray Analysis
# --------------------
def analyze_xray_image(image) -> str:
    if image is None:
        return "Please upload an image for analysis."
    return call_dental_bot([
        "Analyze this dental X-ray. What pathology do you see?",
        image
    ])


# --------------------
# Quiz Generation
# --------------------
def generate_quiz(topic=None):
    topic_text = topic if topic else "General Dentistry"
    prompt = f"""
{instructions}

QUIZ MODE INSTRUCTIONS:

    You are a high-level dental education AI specialized in board-style examinations
(BDS, DDS, MDent, MFDS, NBDE, INBDE).

Quiz Rules:
1. Generate clinically-oriented multiple-choice questions (MCQs), not factual recall only.
2. Each question must test:
   - Diagnosis
   - Clinical reasoning
   - Treatment planning
   - Complications or prognosis
3. Prefer case-based stems when appropriate:
   - Include age, symptoms, clinical findings, and radiographic clues.
4. Each question must have:
   - One BEST answer
   - 3–4 plausible distractors
5. After each question, provide:
   - Correct Answer
   - Detailed Explanation
   - Why the other options are incorrect
6. Use correct professional dental terminology:
   (e.g. Irreversible pulpitis, Periapical radiolucency,Vertical root fracture)
7. Base all questions on:
   - Standard dental textbooks
   - Evidence-based clinical guidelines
8. Difficulty level:
   - Intermediate to Advanced
   - Suitable for final-year students and residents
9. Do NOT ask non-dental questions.
10. Do NOT invent statistics or fake references.

Output Format (STRICT):
Question X:
[Clinical Stem]

A.
B.
C.
D.

Correct Answer:
Explanation:
Why others are wrong:
Topic: {topic_text}
Generate 3 board-style MCQs.
"""
    return call_dental_bot(prompt)


# -------------------------
# Clinical Case Stimulation
# -------------------------
def clinical_case(age, gender, complaint, medical_history, exam):
    prompt = f"""
{instructions}

Build a realistic dental clinical case using the following data:

Patient Age: {age}
Gender: {gender}
Chief Complaint: {complaint}
Medical/Dental History: {medical_history}
Clinical Examination Findings: {exam}

Required Output Structure:
1. Case Summary
2. Diagnosis
3. Differential Diagnosis
4. Radiographic Recommendations
5. Step-by-Step Management Plan
6. Patient Safety & Red Flags
"""
    return call_dental_bot(prompt)


# ============================================================
# 6. UI Design
# ============================================================


# --------------------------
# Theme & Custom CSS
# --------------------------
dental_theme = gr.themes.Soft()


custom_css = """

.gradio-container,
.gradio-container * {
    font-size: 1rem !important;
    line-height: 1.6 !important;
    font-family: 'Inter', sans-serif !important;
    color: #e5e7eb !important;
}

.gradio-container{
    width: 95% !important;
    max-width: 700px !important;
    margin: 0 auto !important;
    padding: 5px !important;
}

.main-tab {
    height: 60vh !important;
    overflow-y: auto !important;
}

html, .light, .dark, body gradio-app{
    background-color: #0e1629 !important;
}

.gradio-container label span,
.block label span,
fieldset span {
    background-color: transparent !important;
    border: none !important;
    color: #e6e6e6 !important;
}

input[type="radio"] {
    display: none !important;
}

.block, .panel {
    background-color: #0e1629 !important;
    border: none !important;
    border-color: #0e1629 !important;
    border-radius: 0px !important;
}

button.primary,
gr-button.secondary {
    background: linear-gradient(180deg, #1e40af, #1e3a8a);
    color: #e5e7eb !important;
    border: none !important;
    border-radius: 8px !important;
}

button.primary:active,
button.secondary:active {
    box-shadow: 0 0 15px rgba(14, 165, 233, 0.5);
    transform: translateY(-1px);
}

.gradio-container .examples button,
.gradio-container .gradio-examples button,
div[data-testid="examples"] button,
.gr-samples-gallery button {
    background: rgba(14, 165, 233, 0.15) !important;
    border: 1px solid rgba(14, 165, 233, 0.5) !important;
    color: #e0f2fe !important;
    border-radius: 8px !important;
    padding: 10px !important;
    font-size: 14px !important;
    transition: all 0.3s !important;
    box-shadow: none !important;
}

.gradio-container .examples button:hover,
.gradio-container .gradio-examples button:hover,
div[data-testid="examples"] button:hover {
    background: rgba(14, 165, 233, 0.35) !important;
    border-color: #38bdf8 !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(14, 165, 233, 0.2) !important;
}

.gr-samples-table tr,
.gr-samples-table td,
button {
    z-index: 100 !important;
    position: relative !important;
    pointer-events: auto !important;
}

textarea, .gradio-textbox input, select {
    background-color: #1e293b !important;
    border: 1px solid #334155 !important;
    color: #e5e7eb !important;
    border-radius: 10px !important;
    font-size: 16px !important;
}

textarea:focus, .gradio-textbox input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2) !important;
}

.message.user, .user-row .message {
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
    color: #ffffff !important;
    border-radius: 12px 12px 2px 12px !important;
    border: none !important;
    font-weight: 500;
}

.message.bot, .bot-row .message {
    background-color: #1e293b !important;
    color: #e5e7eb !important;
    border: none !important;
    border-radius: 12px 12px 12px 2px !important;
    line-height: 1.6 !important;
}

.message.bot ul, .message.bot ol {
    margin-left: 20px !important;
    color: #cbd5e1 !important;
    border: none !important;
}

.message.bot code {
    background-color: #1e293b !important;
    border: 1px solid #475569;
    color: #38bdf8 !important;
}

:root, .light, .dark {
    --background-fill-secondary: #1e293b !important;
    --block-label-background-fill: transparent !important;
    --block-label-border-color: transparent !important;
    --body-text-color: #e6e6e6 !important;
    --input-background-fill: #1e293b !important;
}

footer {
    display: none !important;
}"""


# ============================================================
# 7. Gradio App
# ============================================================
with gr.Blocks(title="Dental Genie Pro", theme=dental_theme, css=custom_css) as app:

    gr.Markdown(
        """
        ## 🦷 Dental Genie Pro
        AI-assistant by **Gemini 3** for dental students — learning , and clinical reasoning.
        """
    )


# ---------------------------
# Chat Tab
# ---------------------------

    with gr.Tab("🧞‍♂️ Chat"):
        gr.Markdown()
        gr.ChatInterface(
            fn=ask_gemini,
            chatbot=gr.Chatbot(label="Dental AI", height='60vh', allow_tags=True),
            submit_btn="Ask Gemini ✨",
            examples=[
                "Explain the anatomy of the Maxillary First Molar",
                "Steps of Root Canal Treatment",
                "Difference between Acute and Chronic Pulpitis"
            ]
        )


# -----------------------
# X-Ray Analysis Tab
# -----------------------
    with gr.Tab("🩻 X-Ray Analysis"):
        gr.Markdown()
        with gr.Row():
            with gr.Column(scale=1):
                img_input = gr.Image(type="pil", label="Dental X-Ray", height=150)
                analyze_btn = gr.Button("Analyze Radiograph", variant="secondary")
            with gr.Column(scale=3):
                output_text = gr.Textbox(
                    label="AI Interpretation",
                    container=False,
                    lines=4,
                    max_lines=25,
                    placeholder="Findings will appear here…",
                    elem_id="xray-output-textbox"
                )
        analyze_btn.click(analyze_xray_image, inputs=img_input, outputs=output_text)


# ---------------------------
# Quiz Tab
# ---------------------------
    with gr.Tab("🎓 Quiz Mode"):
        gr.Markdown()
        topic_in = gr.Textbox(
            label="Dental Topic",
            placeholder="e.g. Local Anesthesia, Pulpitis, Oral Pathology",
        )
        generate_quiz_btn = gr.Button("Generate Quiz", variant="secondary")
        quiz_out = gr.Textbox(
            label="Questions & Answers",
            lines=4,
            max_lines=25,
        )
        generate_quiz_btn.click(generate_quiz, inputs=topic_in, outputs=quiz_out)


# ---------------------------
# Clinical Case Simulation Tab
# ---------------------------
    with gr.Tab("🩺 Clinical Case "):
        gr.Markdown()
        with gr.Row():
            age = gr.Number(label="Patient Age", value=30)
            gender = gr.Radio(
                ["Male", "Female"],
                label="Gender")
        complaint = gr.Textbox(
            label="Chief Complaint",
            placeholder="e.g. Severe pain on biting lower right molar")
        medical_history = gr.Textbox(
            label="Medical & Dental History",
            lines=3,
            placeholder="e.g. Diabetes, previous RCT, medications")
        exam = gr.Textbox(
            label="Clinical Examination Findings",
            lines=4,
            placeholder="e.g. Deep caries on tooth 46, tenderness on percussion")
        generate_clinical_case = gr.Button("Build & Analyze Case")
        case_output = gr.Textbox(
            label="AI Clinical Analysis", lines=4, max_lines=25)
        generate_clinical_case.click(clinical_case, inputs=[age, gender, complaint, medical_history, exam], outputs=case_output)



# ============================================================
# 8. Launch the App
# ============================================================

app.launch(ssr_mode=False)
