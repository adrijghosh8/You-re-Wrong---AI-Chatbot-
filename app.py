import os
import re

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import GoogleGenerativeAI

load_dotenv()

SYSTEM_PROMPT = """
You are "Explain It Like I'm Wrong", a critical reasoning chatbot.

Your job is to challenge the user's claims rather than blindly agreeing.

For every claim:

1. Determine whether it is correct, partially correct, or incorrect.
2. Clearly state the verdict.
3. Explain the reasoning in simple language.
4. Identify the user's misconception, hidden assumption, or logical error.
5. If the claim is correct, try to identify an edge case or limitation.
6. Give one short challenge question that makes the user think.

Never be rude or insulting.
Do not disagree just for the sake of disagreeing.
If the user's claim is correct, explicitly acknowledge it.

Use this format:

VERDICT: [CORRECT / PARTIALLY CORRECT / INCORRECT]

WHY:
[Explanation]

WHAT YOU MISSED:
[Misconception, assumption, or limitation]

CHALLENGE:
[One question for the user]
"""

# ---------- Page setup ----------
st.set_page_config(
    page_title="Explain It Like I'm Wrong",
    page_icon="🧠",
    layout="centered",
)

st.markdown(
    """
    <style>
    .verdict-badge {
        display: inline-block;
        padding: 0.3rem 0.9rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 0.04em;
        margin-bottom: 0.6rem;
    }
    .verdict-correct   { background: #1b5e20; color: #e8f5e9; }
    .verdict-partial   { background: #e65100; color: #fff3e0; }
    .verdict-incorrect { background: #b71c1c; color: #ffebee; }
    .section-title {
        font-weight: 700;
        margin-top: 0.8rem;
        margin-bottom: 0.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Settings")
    model_name = st.text_input("Model", value="gemini-3.1-flash-lite")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.9, 0.05)

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption(
        "Make a claim and the bot will tell you whether it holds up, "
        "where your reasoning slipped, and leave you with a question."
    )


# ---------- Model ----------
@st.cache_resource
def get_model(name: str, temp: float):
    return GoogleGenerativeAI(model=name, temperature=temp)


# ---------- Helpers ----------
VERDICT_RE = re.compile(
    r"VERDICT:\s*\[?\s*(PARTIALLY CORRECT|INCORRECT|CORRECT)\s*\]?", re.IGNORECASE
)
SECTION_RE = re.compile(
    r"WHY:\s*(?P<why>.*?)\s*WHAT YOU MISSED:\s*(?P<missed>.*?)\s*CHALLENGE:\s*(?P<challenge>.*)",
    re.IGNORECASE | re.DOTALL,
)

BADGES = {
    "CORRECT": ("verdict-correct", "✅ CORRECT"),
    "PARTIALLY CORRECT": ("verdict-partial", "⚠️ PARTIALLY CORRECT"),
    "INCORRECT": ("verdict-incorrect", "❌ INCORRECT"),
}


def render_ai_message(text: str):
    """Render a structured reply nicely; fall back to raw text if parsing fails."""
    verdict_match = VERDICT_RE.search(text)
    section_match = SECTION_RE.search(text)

    if not (verdict_match and section_match):
        st.markdown(text)
        return

    css_class, label = BADGES[verdict_match.group(1).upper()]
    st.markdown(
        f'<span class="verdict-badge {css_class}">{label}</span>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">💡 Why</div>', unsafe_allow_html=True)
    st.markdown(section_match.group("why"))

    st.markdown(
        '<div class="section-title">🔍 What you missed</div>', unsafe_allow_html=True
    )
    st.markdown(section_match.group("missed"))

    st.markdown('<div class="section-title">🤔 Challenge</div>', unsafe_allow_html=True)
    st.info(section_match.group("challenge"))


def build_lc_messages(history):
    msgs = [SystemMessage(content=SYSTEM_PROMPT)]
    for m in history:
        if m["role"] == "user":
            msgs.append(HumanMessage(content=m["content"])) # type: ignore
        else:
            msgs.append(AIMessage(content=m["content"])) # type: ignore
    return msgs


# ---------- State ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Header ----------
st.title("🧠 Explain It Like I'm Wrong")
st.caption("Make a claim. I'll challenge it.")

if not os.getenv("GOOGLE_API_KEY"):
    st.error(
        "GOOGLE_API_KEY not found. Add it to your `.env` file "
        "(`GOOGLE_API_KEY=your_key_here`) and restart the app."
    )
    st.stop()

# ---------- Chat history ----------
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "Hi! Tell me something you believe is true, for example "
            "*“Heavier objects fall faster than lighter ones.”*"
        )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            render_ai_message(msg["content"])
        else:
            st.markdown(msg["content"])

# ---------- Input ----------
if prompt := st.chat_input("Type your claim here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking critically..."):
            try:
                model = get_model(model_name, temperature)
                response = model.invoke(build_lc_messages(st.session_state.messages))
            except Exception as e:
                response = None
                st.error(f"Something went wrong: {e}")

        if response is not None:
            render_ai_message(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )