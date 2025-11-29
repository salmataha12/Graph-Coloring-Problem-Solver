# edugen_app.py
import os
import re
import textwrap
import requests
import streamlit as st
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration


os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

# -----------------------------------------------------------
# Configuration: Put your HF API key here (hard-coded)
# -----------------------------------------------------------
HF_API_KEY = st.secrets.get("HF_API_KEY")  # <-- REPLACE if you rotate/delete the token
HF_DEFAULT_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
HF_CHAT_URL = "https://router.huggingface.co/v1/chat/completions"

# -----------------------------------------------------------
# Streamlit page & enhanced styling
# -----------------------------------------------------------
st.set_page_config(page_title="EduGen AI", page_icon="📘", layout="centered")

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

* { 
    font-family: 'Inter', sans-serif; 
}

.stApp { 
    background: linear-gradient(to bottom, #f8f9fe 0%, #ffffff 100%);
}

.main .block-container { 
    max-width: 900px; 
    padding-top: 2rem; 
    padding-bottom: 3rem; 
}

/* Header Card */
.header-card { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    padding: 2.5rem 2rem; 
    border-radius: 16px; 
    color: white; 
    margin-bottom: 2rem; 
    text-align: center;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.header-card h2 {
    margin: 0;
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.header-card .subtitle {
    opacity: 0.95;
    font-size: 1.1rem;
    margin-top: 0.5rem;
    font-weight: 400;
}

/* Content Card */
.content-card { 
    background: white; 
    padding: 1.5rem; 
    border-radius: 12px; 
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); 
    margin-bottom: 1.5rem;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

/* Buttons */
.stButton>button { 
    border-radius: 10px; 
    padding: 0.6rem 1.5rem; 
    font-weight: 600; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white;
    border: none;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

/* Tab Navigation */
.tab-button {
    background: white;
    border: 2px solid #667eea;
    color: #667eea;
    padding: 0.7rem 1.5rem;
    border-radius: 10px;
    font-weight: 600;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.tab-button:hover {
    background: #667eea;
    color: white;
}

/* Question Card */
.question-card { 
    background: linear-gradient(to right, #f8f9fe 0%, #ffffff 100%);
    padding: 1.25rem; 
    border-radius: 12px; 
    border: 2px solid #e8ecff; 
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}

.question-card:hover {
    border-color: #667eea;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.15);
}

.question-card strong {
    color: #667eea;
    font-size: 1.1rem;
}

/* Flashcard styling */
.stExpander {
    background: white;
    border-radius: 12px;
    border: 2px solid #e8ecff;
    margin-bottom: 1rem;
}

/* Input fields */
.stTextInput>div>div>input,
.stTextArea>div>div>textarea {
    border-radius: 10px;
    border: 2px solid #e8ecff;
    padding: 0.75rem;
    transition: all 0.3s ease;
}

.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Sidebar styling */
.css-1d391kg, [data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #f8f9fe 0%, #ffffff 100%);
}

/* Radio buttons */
.stRadio > div {
    gap: 0.75rem;
}

.stRadio > div > label {
    background: white;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 2px solid #e8ecff;
    transition: all 0.3s ease;
}

.stRadio > div > label:hover {
    border-color: #667eea;
    background: #f8f9fe;
}

/* Section headers */
h1, h2, h3 {
    color: #2d3748;
    font-weight: 700;
}

/* Success/Error messages */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 10px;
    padding: 1rem;
}

/* Divider */
hr {
    margin: 2rem 0;
    border: none;
    height: 2px;
    background: linear-gradient(to right, transparent, #e8ecff, transparent);
}

/* Tab container */
.stTabs [data-baseweb="tab-list"] {
    gap: 1rem;
}

.stTabs [data-baseweb="tab"] {
    padding: 1rem 2rem;
    border-radius: 10px;
    background: white;
    border: 2px solid #e8ecff;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white !important;
    border-color: #667eea;
}

/* Slider */
.stSlider > div > div > div {
    background: #667eea;
}

/* Score display */
.score-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    font-size: 1.3rem;
    font-weight: 700;
    margin: 1.5rem 0;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
}
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------
# Local model fallback (FLAN-T5) - only loaded if needed
# -----------------------------------------------------------
@st.cache_resource
def load_local_model(model_name: str = "google/flan-t5-large"):
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return tokenizer, model, device

def generate_local(tokenizer, model, device, prompt: str, max_len=400):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding="longest")
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)
    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=max_len,
        temperature=0.3,
        top_p=0.9,
        repetition_penalty=1.2,
        no_repeat_ngram_size=3,
        do_sample=False,
        num_return_sequences=1
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

# -----------------------------------------------------------
# Hugging Face Router Chat call
# -----------------------------------------------------------
def call_hf_chat(api_key: str, prompt: str, model_name: str = HF_DEFAULT_MODEL, max_tokens: int = 512):
    url = HF_CHAT_URL
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are an expert educational assistant that produces clear explanations, concise summaries, multiple-choice questions (MCQs) with 4 options, and a one-sentence explanation for each correct answer. Follow the output format instructions exactly."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.25,
        "top_p": 0.9
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=90)
    if resp.status_code == 200:
        data = resp.json()
        # Adapter for HF response shape
        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            return str(data)
    else:
        raise Exception(f"HF API error {resp.status_code}: {resp.text}")

# -----------------------------------------------------------
# Prompt builders (include difficulty)
# -----------------------------------------------------------
def build_explain_prompt(topic: str):
    return textwrap.dedent(f"Explain the following topic in clear, student-friendly language (2–4 short paragraphs):\n\nTopic: {topic}")

def build_summary_prompt(text: str):
    snippet = text if len(text) < 4000 else text[:4000] + " ... (truncated)"
    return textwrap.dedent(f"Summarize the following text into concise bullet points suitable for students:\n\nText:\n{snippet}")

def build_mcq_prompt_from_topic(topic: str, n_questions: int, difficulty: str):
    return textwrap.dedent(f"""
        Generate exactly {n_questions} multiple-choice questions about {topic}.
        Difficulty level: {difficulty}.
        Each question MUST follow EXACTLY this format and include a one-sentence Explanation after the correct answer:

        Q1. <question text>
        A. <option A>
        B. <option B>
        C. <option C>
        D. <option D>
        Correct Answer: <A/B/C/D>
        Explanation: <one short sentence>

        Topic: {topic}
    """)

def build_mcq_prompt_from_text(text: str, n_questions: int, difficulty: str):
    snippet = text if len(text) < 4000 else text[:4000] + " ... (truncated)"
    return textwrap.dedent(f"""
        Generate exactly {n_questions} multiple-choice questions based ONLY on the text below.
        Difficulty level: {difficulty}.
        Each question MUST follow EXACTLY this format and include a one-sentence Explanation after the correct answer:

        Q1. <question text>
        A. <option A>
        B. <option B>
        C. <option C>
        D. <option D>
        Correct Answer: <A/B/C/D>
        Explanation: <one short sentence>

        Text:
        {snippet}
    """)

def build_flashcard_prompt(topic: str):
    return textwrap.dedent(f"""
        Generate 8 flashcards for studying the topic: {topic}
        Format:
        Flashcard 1:
        Front: <short question or concept>
        Back: <clear explanation>

        Flashcard 2:
        Front: ...
        Back: ...

        Keep them concise and student-friendly.
    """)

def build_flashcard_prompt_from_text(text: str):
    snippet = text if len(text) < 4000 else text[:4000] + " ... (truncated)"
    return textwrap.dedent(f"""
        Generate 8 flashcards based on the following text for study purposes.
        Format:
        Flashcard 1:
        Front: <short question or concept>
        Back: <clear explanation>

        Flashcard 2:
        Front: ...
        Back: ...

        Keep them concise and student-friendly.
        
        Text:
        {snippet}
    """)

# -----------------------------------------------------------
# Parsers (robust for Format A + Explanation)
# -----------------------------------------------------------
def parse_mcqs_format_a(raw: str):
    mcqs = []
    text = raw.replace("\r\n", "\n").replace("\r", "\n").strip()
    pattern = re.compile(
        r"Q\d+\.\s*(?P<q>.*?)\n\s*A\.\s*(?P<A>.*?)\n\s*B\.\s*(?P<B>.*?)\n\s*C\.\s*(?P<C>.*?)\n\s*D\.\s*(?P<D>.*?)\n\s*Correct Answer:\s*(?P<ans>[A-Da-d])\s*(?:\n\s*Explanation:\s*(?P<expl>.*?))?(?=\nQ\d+\.|\Z)",
        re.DOTALL | re.IGNORECASE
    )
    for m in pattern.finditer(text):
        mcqs.append({
            "q": m.group("q").strip(),
            "options": {"A": m.group("A").strip(), "B": m.group("B").strip(), "C": m.group("C").strip(), "D": m.group("D").strip()},
            "answer": m.group("ans").upper().strip(),
            "explanation": m.group("expl").strip() if m.group("expl") else ""
        })
    # fallback: split by Q
    if not mcqs:
        parts = re.split(r"\n(?=Q\d+\.)", text)
        for part in parts:
            if part.strip().startswith("Q"):
                lines = [ln.strip() for ln in part.strip().splitlines() if ln.strip()]
                qline = lines[0]
                q_text = qline.split(".", 1)[1].strip() if "." in qline else qline
                opts = {}
                ans = None
                expl = ""
                for ln in lines[1:]:
                    if re.match(r"^[A-Da-d]\.", ln):
                        key = ln[0].upper()
                        val = ln[2:].strip()
                        opts[key] = val
                    elif ln.lower().startswith("correct answer:"):
                        m2 = re.search(r"[A-Da-d]", ln)
                        if m2:
                            ans = m2.group(0).upper()
                    elif ln.lower().startswith("explanation:"):
                        expl = ln.split(":", 1)[1].strip()
                if len(opts) == 4 and ans:
                    mcqs.append({"q": q_text, "options": opts, "answer": ans, "explanation": expl})
    return mcqs

def parse_flashcards(raw: str):
    cards = []
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    pattern = re.compile(r"Flashcard\s*\d+:\s*Front:\s*(?P<front>.*?)\s*Back:\s*(?P<back>.*?)(?=Flashcard\s*\d+:|\Z)", re.DOTALL | re.IGNORECASE)
    for m in pattern.finditer(text):
        cards.append({"front": m.group("front").strip(), "back": m.group("back").strip()})
    return cards

# -----------------------------------------------------------
# Session state initializations
# -----------------------------------------------------------
if "mcqs" not in st.session_state: st.session_state["mcqs"] = []
if "flashcards" not in st.session_state: st.session_state["flashcards"] = []
if "explanation_text" not in st.session_state: st.session_state["explanation_text"] = ""
if "show_tab" not in st.session_state: st.session_state["show_tab"] = "summary"
if "user_answers" not in st.session_state: st.session_state["user_answers"] = {}
if "submitted" not in st.session_state: st.session_state["submitted"] = False
if "score" not in st.session_state: st.session_state["score"] = None

# -----------------------------------------------------------
# UI layout
# -----------------------------------------------------------
st.markdown('''
<div class="header-card">
    <h2>📚 EduGen AI</h2>
    <div class="subtitle">Transform any topic into engaging educational content</div>
</div>
''', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    st.info(f"**Model:** {HF_DEFAULT_MODEL}")
    local_model_choice = st.selectbox("🔄 Local fallback model", ["google/flan-t5-large", "google/flan-ul2"])
    st.markdown("---")
    n_mcqs = st.slider("📝 Number of MCQs", 3, 10, value=5, key="n_mcqs_slider")
    difficulty = st.selectbox("🎯 Difficulty Level", ["Easy", "Medium", "Hard"])
    max_tokens = st.slider("⚡ Max generation tokens", 200, 1200, 600, step=50)
    st.markdown("---")
    show_raw = st.checkbox("🔍 Show raw output (debug)", value=False)

tab1, tab2 = st.tabs(["📌 From Topic", "📄 From Text"])

# -------------------------
# Tab 1: From Topic
# -------------------------
with tab1:
    topic = st.text_input("🎓 Enter a topic to explore", key="topic_input", placeholder="e.g., Photosynthesis, World War II, Quantum Physics...")
    if st.button("✨ Generate Content", key="gen_topic", use_container_width=True):
        if not topic.strip():
            st.warning("⚠️ Please enter a topic.")
        else:
            with st.spinner("🔮 Generating educational content..."):
                # Explanation
                prompt = build_explain_prompt(topic)
                try:
                    text_out = call_hf_chat(HF_API_KEY, prompt, max_tokens=max_tokens)
                except Exception:
                    tokenizer, model, device = load_local_model(local_model_choice)
                    text_out = generate_local(tokenizer, model, device, prompt, max_len=max_tokens)
                st.session_state["explanation_text"] = text_out

                # MCQs
                prompt_mcq = build_mcq_prompt_from_topic(topic, n_questions=n_mcqs, difficulty=difficulty)
                try:
                    raw_mcq = call_hf_chat(HF_API_KEY, prompt_mcq, max_tokens=max_tokens+300)
                except Exception:
                    tokenizer, model, device = load_local_model(local_model_choice)
                    raw_mcq = generate_local(tokenizer, model, device, prompt_mcq, max_len=max_tokens+300)
                if show_raw: st.code(raw_mcq)
                mcqs = parse_mcqs_format_a(raw_mcq)
                if mcqs:
                    st.session_state["mcqs"] = mcqs
                else:
                    st.error("❌ Failed to parse MCQs. Enable 'Show raw model output' to debug.")

                # Flashcards
                prompt_flash = build_flashcard_prompt(topic)
                try:
                    raw_flash = call_hf_chat(HF_API_KEY, prompt_flash, max_tokens=400)
                except Exception:
                    tokenizer, model, device = load_local_model(local_model_choice)
                    raw_flash = generate_local(tokenizer, model, device, prompt_flash, max_len=400)
                if show_raw: st.code(raw_flash)
                cards = parse_flashcards(raw_flash)
                st.session_state["flashcards"] = cards

                st.session_state["show_tab"] = "summary"
                st.rerun()


# -------------------------
# Tab 2: From Text
# -------------------------
with tab2:
    user_text = st.text_area("📋 Paste your text here", height=260, key="text_input", placeholder="Paste any educational text, article, or notes...")
    if st.button("✨ Generate Content", key="gen_text", use_container_width=True):
        if not user_text.strip():
            st.warning("⚠️ Please paste some text.")
        else:
            with st.spinner("🔮 Generating educational content..."):
                # Summary
                prompt = build_summary_prompt(user_text)
                try:
                    text_out = call_hf_chat(HF_API_KEY, prompt, max_tokens=400)
                except Exception:
                    tokenizer, model, device = load_local_model(local_model_choice)
                    text_out = generate_local(tokenizer, model, device, prompt, max_len=400)
                st.session_state["explanation_text"] = text_out

                # MCQs
                prompt_mcq = build_mcq_prompt_from_text(user_text, n_questions=n_mcqs, difficulty=difficulty)
                try:
                    raw_mcq = call_hf_chat(HF_API_KEY, prompt_mcq, max_tokens=max_tokens+300)
                except Exception:
                    tokenizer, model, device = load_local_model(local_model_choice)
                    raw_mcq = generate_local(tokenizer, model, device, prompt_mcq, max_len=max_tokens+300)
                if show_raw: st.code(raw_mcq)
                mcqs = parse_mcqs_format_a(raw_mcq)
                if mcqs:
                    st.session_state["mcqs"] = mcqs
                else:
                    st.error("❌ Failed to parse MCQs. Enable 'Show raw model output' to debug.")

                # Flashcards
                prompt_flash = build_flashcard_prompt_from_text(user_text)
                try:
                    raw_flash = call_hf_chat(HF_API_KEY, prompt_flash, max_tokens=400)
                except Exception:
                    tokenizer, model, device = load_local_model(local_model_choice)
                    raw_flash = generate_local(tokenizer, model, device, prompt_flash, max_len=400)
                if show_raw: st.code(raw_flash)
                cards = parse_flashcards(raw_flash)
                st.session_state["flashcards"] = cards

                st.session_state["show_tab"] = "summary"
                st.rerun()


# -------------------------
# Content tabs: Summary / Questions / Flashcards
# -------------------------
st.markdown("---")
tab_col1, tab_col2, tab_col3 = st.columns(3)
with tab_col1:
    if st.button("📖 Summary", key="show_summary_tab", use_container_width=True):
        st.session_state["show_tab"] = "summary"
        st.rerun()

with tab_col2:
    if st.button("❓ Questions", key="show_questions_tab", use_container_width=True):
        st.session_state["show_tab"] = "questions"
        st.rerun()

with tab_col3:
    if st.button("🎴 Flashcards", key="show_flashcards_tab", use_container_width=True):
        st.session_state["show_tab"] = "flashcards"
        st.rerun()


# Render the chosen view
st.markdown("---")
if st.session_state["show_tab"] == "summary":
    st.markdown("## 📖 Summary")
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if st.session_state["explanation_text"]:
        st.write(st.session_state["explanation_text"])
    else:
        st.info("💡 Generate content to see the summary here.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state["show_tab"] == "questions":
    st.markdown("## ❓ Practice Questions")
    if not st.session_state["mcqs"]:
        st.info("💡 Generate content to see practice questions here.")
    else:
        for i, q in enumerate(st.session_state["mcqs"]):
            st.markdown(f'<div class="question-card"><strong>Q{i+1}.</strong> {q["q"]}</div>', unsafe_allow_html=True)
            options = [
                f"A. {q['options']['A']}",
                f"B. {q['options']['B']}",
                f"C. {q['options']['C']}",
                f"D. {q['options']['D']}",
            ]
            prev = st.session_state["user_answers"].get(str(i))
            default_index = 0
            if prev:
                for idx_o, opt_letter in enumerate(["A","B","C","D"]):
                    if opt_letter == prev:
                        default_index = idx_o
                        break
            choice = st.radio("", options, index=default_index, key=f"q_{i}", label_visibility="collapsed")
            st.session_state["user_answers"][str(i)] = choice.split(".", 1)[0].strip()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Submit Answers", key="submit_answers", use_container_width=True):
            score = 0
            results = []
            for idx, q in enumerate(st.session_state["mcqs"]):
                user = st.session_state["user_answers"].get(str(idx))
                correct = q.get("answer")
                if not correct:
                    correct = q.get("correct")
                is_correct = (user == correct)
                if is_correct:
                    score += 1
                results.append({"idx": idx, "user": user, "correct": correct, "is_correct": is_correct, "explanation": q.get("explanation", "")})
            
            st.markdown(f'<div class="score-card">🎯 Your Score: {score} / {len(st.session_state["mcqs"])}</div>', unsafe_allow_html=True)
            
            st.markdown("### 📊 Results Breakdown")
            for r in results:
                if r["is_correct"]:
                    st.success(f"✅ **Q{r['idx']+1}** — Correct! Your answer: **{r['user']}**")
                else:
                    st.error(f"❌ **Q{r['idx']+1}** — Your answer: **{r['user']}** | Correct: **{r['correct']}**")
                if r["explanation"]:
                    st.info(f"💡 **Explanation:** {r['explanation']}")

elif st.session_state["show_tab"] == "flashcards":
    st.markdown("## 🎴 Flashcards")
    if not st.session_state["flashcards"]:
        st.info("💡 Generate content to see flashcards here.")
    else:
        for i, fc in enumerate(st.session_state["flashcards"]):
            with st.expander(f"**Flashcard {i+1}:** {fc['front']}", expanded=False):
                st.markdown(f"**Answer:** {fc['back']}")