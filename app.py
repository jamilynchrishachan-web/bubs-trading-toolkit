import os
import json
import random
import gradio as gr
import anthropic
from datetime import datetime

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

GLOSSARY_PATH = "glossary.json"

def load_glossary():
    try:
        with open(GLOSSARY_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_glossary(glossary):
    with open(GLOSSARY_PATH, "w") as f:
        json.dump(glossary, f, indent=2)

def explain_concept(term):
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[
            {"role": "user", "content": f"Explain what '{term}' means in forex/CFD trading, for someone who is a complete beginner and whose first language is not English. Use short sentences, simple everyday words, and one concrete example. Avoid complex vocabulary. Keep it under 80 words."}
        ]
    )
    return response.content[0].text

def learn_term_gradio(term):
    if not term.strip():
        return "Please type a term first."
    glossary = load_glossary()
    existing = next((e for e in glossary if e["term"].lower() == term.lower()), None)
    if existing:
        return f"(Already learned — saved version)\n\n{existing['explanation']}"
    explanation = explain_concept(term)
    glossary.append({"term": term, "explanation": explanation, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
    save_glossary(glossary)
    return explanation

def get_quiz_question():
    glossary = load_glossary()
    if not glossary:
        return "No saved terms yet. Learn a few first!", None
    entry = random.choice(glossary)
    return f"What does '{entry['term']}' mean?", entry

def grade_quiz_answer(question_state, user_answer):
    if question_state is None:
        return "Click 'New Question' first."
    if not user_answer.strip():
        return "Type an answer first."
    entry = question_state
    feedback_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[
            {"role": "user", "content": f"A beginner trader was asked to explain '{entry['term']}'. Their answer was: \"{user_answer}\". The correct explanation is: \"{entry['explanation']}\". In one short, encouraging sentence, tell them if they got it right, close, or not quite — using simple English. Be kind, not harsh."}
        ]
    )
    feedback = feedback_response.content[0].text
    return f"{feedback}\n\nFull explanation:\n{entry['explanation']}"

def view_glossary_gradio():
    glossary = load_glossary()
    if not glossary:
        return "Glossary is empty. Learn some terms first!"
    lines = [f"You've learned {len(glossary)} terms:\n"]
    for entry in glossary:
        lines.append(f"- {entry['term']} (saved {entry['date']})")
    return "\n".join(lines)

def calculate_risk(account_balance, risk_percent, entry_price, stop_loss_price):
    try:
        account_balance = float(account_balance)
        risk_percent = float(risk_percent)
        entry_price = float(entry_price)
        stop_loss_price = float(stop_loss_price)
    except ValueError:
        return "Please enter valid numbers in all fields."
    if entry_price == stop_loss_price:
        return "Entry price and stop loss can't be the same."
    risk_amount = account_balance * (risk_percent / 100)
    price_distance = abs(entry_price - stop_loss_price)
    position_size = risk_amount / price_distance
    return (
        f"Amount you're risking: ${risk_amount:.2f}\n"
        f"Distance to stop loss: {price_distance:.5f}\n"
        f"Suggested position size: {position_size:.2f} units\n\n"
        f"If price hits your stop loss, you lose about ${risk_amount:.2f} — no more, no less.\n"
        f"Always double-check this against what MT5 shows before trading."
    )

with gr.Blocks(title="Bub's Trading Toolkit") as demo:
    gr.Markdown("# Bub's Trading Study Toolkit")

    with gr.Tab("Learn"):
        term_input = gr.Textbox(label="What trading term do you want explained?")
        learn_btn = gr.Button("Explain")
        learn_output = gr.Textbox(label="Explanation", lines=10)
        learn_btn.click(learn_term_gradio, inputs=term_input, outputs=learn_output)

    with gr.Tab("Quiz"):
        quiz_question_state = gr.State(None)
        quiz_question_display = gr.Textbox(label="Question", interactive=False)
        new_question_btn = gr.Button("New Question")
        quiz_answer_input = gr.Textbox(label="Your answer")
        submit_answer_btn = gr.Button("Submit Answer")
        quiz_feedback = gr.Textbox(label="Feedback", lines=6)

        def new_question_wrapper():
            question_text, entry = get_quiz_question()
            return question_text, entry, ""

        new_question_btn.click(new_question_wrapper, outputs=[quiz_question_display, quiz_question_state, quiz_feedback])
        submit_answer_btn.click(grade_quiz_answer, inputs=[quiz_question_state, quiz_answer_input], outputs=quiz_feedback)

    with gr.Tab("Glossary"):
        glossary_output = gr.Textbox(label="Your saved terms", lines=15)
        refresh_btn = gr.Button("Refresh")
        refresh_btn.click(view_glossary_gradio, outputs=glossary_output)

    with gr.Tab("Risk Calculator"):
        gr.Markdown("Figure out how much to trade based on how much you're okay losing.")
        balance_input = gr.Textbox(label="Account balance ($)")
        risk_percent_input = gr.Textbox(label="Risk % per trade (e.g. 1 or 2)")
        entry_input = gr.Textbox(label="Entry price")
        stop_input = gr.Textbox(label="Stop loss price")
        calc_btn = gr.Button("Calculate")
        calc_output = gr.Textbox(label="Result", lines=6)
        calc_btn.click(calculate_risk, inputs=[balance_input, risk_percent_input, entry_input, stop_input], outputs=calc_output)

demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))