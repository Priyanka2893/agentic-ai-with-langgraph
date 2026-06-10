import streamlit as st

# ── Constants ──────────────────────────────────────────────────────────────────

BOTS = {
    "Select Bot": None,
    "Agentic Chatbot": "agenticchatbot",
    # future bots registered here
}

LLM_PROVIDERS = {
    "Select LLM": None,
    "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
    "Groq": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
    "Anthropic": ["claude-sonnet-4-6", "claude-haiku-4-5-20251001", "claude-opus-4-8"],
}

USECASES = [
    "Select Usecase",
    "General Q&A",
    "Code Assistant",
    "Research Assistant",
    "Data Analysis",
    "Summarization",
]

# ── Page config ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Agentic AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state defaults ─────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_bot" not in st.session_state:
    st.session_state.selected_bot = "Select Bot"

if "selected_provider" not in st.session_state:
    st.session_state.selected_provider = "Select LLM"

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Select Model"

if "selected_usecase" not in st.session_state:
    st.session_state.selected_usecase = "Select Usecase"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""


def _is_configured() -> bool:
    return (
        st.session_state.selected_bot not in (None, "Select Bot")
        and st.session_state.selected_provider not in (None, "Select LLM")
        and st.session_state.selected_model not in (None, "Select Model")
        and st.session_state.api_key.strip() != ""
    )


# ── Sidebar ────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("Settings")
    st.divider()

    # Bot selection
    st.subheader("Bot")
    bot_options = list(BOTS.keys())
    selected_bot = st.selectbox(
        label="Select Bot",
        options=bot_options,
        index=bot_options.index(st.session_state.selected_bot),
        key="bot_select",
        label_visibility="collapsed",
    )
    if selected_bot != st.session_state.selected_bot:
        st.session_state.selected_bot = selected_bot
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # LLM provider selection
    st.subheader("LLM Provider")
    provider_options = list(LLM_PROVIDERS.keys())
    selected_provider = st.selectbox(
        label="Select LLM",
        options=provider_options,
        index=provider_options.index(st.session_state.selected_provider),
        key="provider_select",
        label_visibility="collapsed",
    )
    if selected_provider != st.session_state.selected_provider:
        st.session_state.selected_provider = selected_provider
        st.session_state.selected_model = "Select Model"
        st.rerun()

    st.divider()

    # Model selection (filtered by provider)
    st.subheader("Model")
    provider_models = LLM_PROVIDERS.get(st.session_state.selected_provider)
    if provider_models:
        model_options = ["Select Model"] + provider_models
    else:
        model_options = ["Select Model"]

    current_model = (
        st.session_state.selected_model
        if st.session_state.selected_model in model_options
        else "Select Model"
    )
    selected_model = st.selectbox(
        label="Select Model",
        options=model_options,
        index=model_options.index(current_model),
        key="model_select",
        label_visibility="collapsed",
    )
    st.session_state.selected_model = selected_model

    st.divider()

    # Usecase selection
    st.subheader("Usecase")
    selected_usecase = st.selectbox(
        label="Select Usecase",
        options=USECASES,
        index=USECASES.index(st.session_state.selected_usecase),
        key="usecase_select",
        label_visibility="collapsed",
    )
    st.session_state.selected_usecase = selected_usecase

    st.divider()

    # API Key
    st.subheader("API Key")
    api_key = st.text_input(
        label="API Key",
        value=st.session_state.api_key,
        placeholder="Enter API key…",
        type="password",
        key="api_key_input",
        label_visibility="collapsed",
    )
    st.session_state.api_key = api_key

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ── Main chat area ─────────────────────────────────────────────────────────────

bot_label = st.session_state.selected_bot
st.title(f"🤖 {bot_label if bot_label != 'Select Bot' else 'Agentic AI'}")

if _is_configured():
    st.caption(
        f"**{st.session_state.selected_provider}** · "
        f"**{st.session_state.selected_model}** · "
        f"_{st.session_state.selected_usecase}_"
    )
else:
    st.warning("Configure Bot, LLM Provider, Model, and API Key in the sidebar to start chatting.")

# Chat history
chat_container = st.container()
with chat_container:
    if not st.session_state.messages:
        if _is_configured():
            st.info("Start a conversation below.")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input — disabled until fully configured
if _is_configured():
    if prompt := st.chat_input("Type your message…"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Placeholder — replace with actual bot invocation once backend is ready
        response = (
            f"_(Backend not yet connected — "
            f"bot: **{st.session_state.selected_bot}**, "
            f"model: **{st.session_state.selected_model}**, "
            f"usecase: **{st.session_state.selected_usecase}**)_"
        )

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.chat_input("Complete sidebar configuration to chat…", disabled=True)
