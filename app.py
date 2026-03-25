"""Interface de chat Streamlit para o PensionistaAgent."""

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

import streamlit as st
from agent.core import PensionistaAgent

# --- Page Config ---
st.set_page_config(
    page_title="PensionistaAgent",
    page_icon="🧓",
    layout="centered",
)


@st.cache_resource
def get_agent():
    return PensionistaAgent(data_dir=str(PROJECT_DIR / "data"))


agent = get_agent()

# --- Sidebar ---
with st.sidebar:
    st.title("🧓 PensionistaAgent")
    st.caption("Assistente para Aposentados e Pensionistas")

    st.divider()

    mode_label = "🔧 DRY-RUN" if agent.dry_run else "🟢 LIVE"
    st.metric("Modo", mode_label)

    dry_toggle = st.toggle("Forçar Dry-Run", value=agent.dry_run)
    agent.dry_run = dry_toggle

    st.divider()
    st.subheader("Skills Disponíveis")
    for name, skill in agent.skills.items():
        with st.expander(f"📘 {name}"):
            st.write(f"**Domínio:** {skill.domain}")
            st.write(f"**Keywords:** {', '.join(skill.keywords[:8])}...")

    st.divider()
    forced = st.selectbox(
        "Forçar skill específica:",
        ["Auto (router decide)"] + agent.list_skills(),
    )
    forced_skill = None if forced.startswith("Auto") else forced

# --- Chat ---
st.title("💬 Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "skills" in msg:
            st.caption(f"Skills: {msg['skills']}")

# User input
if user_input := st.chat_input("Digite sua pergunta..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            result = agent.generate_response(user_input, skill_name=forced_skill)

        skills_str = ", ".join(result["skills_used"])
        st.caption(f"{'🔧 DRY-RUN | ' if result['dry_run'] else ''}Skills: {skills_str}")
        st.markdown(result["answer"])

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "skills": ", ".join(result["skills_used"]),
    })
