import streamlit as st

# ── Constants ──────────────────────────────────────────────────────────────────

BOTS = {
    "Agentic Chatbot": "agenticchatbot",
    # future bots registered here
}

LLM_PROVIDERS = {
    "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
    "Groq": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
    "Anthropic": ["claude-sonnet-4-6", "claude-haiku-4-5-20251001", "claude-opus-4-8"],
}

USECASES = [
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
    st.session_state.selected_bot = None

if "selected_provider" not in st.session_state:
    st.session_state.selected_provider = None

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "selected_usecase" not in st.session_state:
    st.session_state.selected_usecase = None

if "api_key" not in st.session_state:
    st.session_state.api_key = ""


def _is_configured() -> bool:
    return (
        st.session_state.selected_bot is not None
        and st.session_state.selected_provider is not None
        and st.session_state.selected_model is not None
        and st.session_state.api_key.strip() != ""
    )


# ── Sidebar ────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### Settings")

    def _label(text: str) -> None:
        st.markdown(f"<p style='margin:0 0 2px 0; font-size:0.8rem; font-weight:600; color:grey'>{text}</p>", unsafe_allow_html=True)

    # Bot selection
    _label("Select Bot")
    bot_options = list(BOTS.keys())
    bot_index = bot_options.index(st.session_state.selected_bot) if st.session_state.selected_bot in bot_options else None
    selected_bot = st.selectbox(
        label="Select Bot",
        options=bot_options,
        index=bot_index,
        placeholder="Choose a bot…",
        key="bot_select",
        label_visibility="collapsed",
    )
    if selected_bot != st.session_state.selected_bot:
        st.session_state.selected_bot = selected_bot
        st.session_state.messages = []
        st.rerun()

    # LLM provider selection
    _label("Select LLM")
    provider_options = list(LLM_PROVIDERS.keys())
    provider_index = provider_options.index(st.session_state.selected_provider) if st.session_state.selected_provider in provider_options else None
    selected_provider = st.selectbox(
        label="Select LLM",
        options=provider_options,
        index=provider_index,
        placeholder="Choose a provider…",
        key="provider_select",
        label_visibility="collapsed",
    )
    if selected_provider != st.session_state.selected_provider:
        st.session_state.selected_provider = selected_provider
        st.session_state.selected_model = None
        st.rerun()

    # Model selection (filtered by provider)
    _label("Select Model")
    model_options = LLM_PROVIDERS.get(st.session_state.selected_provider, [])
    model_index = model_options.index(st.session_state.selected_model) if st.session_state.selected_model in model_options else None
    selected_model = st.selectbox(
        label="Select Model",
        options=model_options,
        index=model_index,
        placeholder="Choose a model…",
        disabled=not model_options,
        key="model_select",
        label_visibility="collapsed",
    )
    st.session_state.selected_model = selected_model

    # Usecase selection
    _label("Select Usecase")
    usecase_index = USECASES.index(st.session_state.selected_usecase) if st.session_state.selected_usecase in USECASES else None
    selected_usecase = st.selectbox(
        label="Select Usecase",
        options=USECASES,
        index=usecase_index,
        placeholder="Choose a usecase…",
        key="usecase_select",
        label_visibility="collapsed",
    )
    st.session_state.selected_usecase = selected_usecase

    # API Key
    _label("API Key")
    api_key = st.text_input(
        label="API Key",
        value=st.session_state.api_key,
        placeholder="Enter your API key…",
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

bot_label = st.session_state.selected_bot or "Agentic AI"
st.title(f"🤖 {bot_label}")

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
