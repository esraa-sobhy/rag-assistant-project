import requests
import streamlit as st

from api_client import ask_question, API_BASE_URL


st.set_page_config(
    page_title="Ancient Egypt RAG",
    page_icon="🏺",
    layout="centered",
)

# ---------- Simple Styling ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f5f1;
    }

    .title {
        text-align: center;
        font-size: 34px;
        font-weight: 700;
        color: #332f2a;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #77706a;
        margin-bottom: 30px;
    }

    .answer-box {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd7cf;
        margin-top: 10px;
        line-height: 1.6;
    }

    .source-box {
        background-color: #eeeae4;
        padding: 12px;
        border-radius: 8px;
        margin-top: 10px;
    }

    .sidebar-text {
        color: #666;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Session State ----------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------- Sidebar ----------
with st.sidebar:
    st.header("🏺 Ancient Egypt")

    st.markdown(
        """
        <div class="sidebar-text">
        A RAG-powered assistant that answers questions
        using the Ancient Egypt document.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.write("**Document:** Ancient Egypt")
    st.write("**Vector Store:** Chroma")
    st.write("**Embeddings:** all-MiniLM-L6-v2")
    st.write("**LLM:** GPT-OSS-20B via Groq")

    st.divider()

    # Backend status
    try:
        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=3
        )

        if response.status_code == 200:
            st.success("Backend connected")
        else:
            st.warning("Backend unavailable")

    except requests.exceptions.RequestException:
        st.error("Backend offline")

    st.divider()

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------- Main Title ----------
st.markdown(
    '<div class="title">🏺 Ancient Egypt RAG Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Ask questions about Ancient Egypt using the provided document."
    "</div>",
    unsafe_allow_html=True,
)


# ---------- Chat History ----------
for message in st.session_state.messages:

    if message["role"] == "user":
        st.markdown("**You:**")
        st.write(message["content"])

    else:
        st.markdown("**Assistant:**")

        st.markdown(
            f"""
            <div class="answer-box">
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if message.get("sources"):
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.write(f"• {source}")


# ---------- Question Input ----------
question = st.text_input(
    "Your question",
    placeholder="e.g. What was the importance of the Nile River?",
)


# ---------- Ask Button ----------
if st.button("Ask", use_container_width=True):

    if not question.strip():
        st.warning("Please enter a question.")

    else:

        # Add user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        # Call backend
        with st.spinner("Searching the document..."):

            try:
                result = ask_question(question)

                answer = result.get(
                    "answer",
                    "No answer was returned.",
                )

                sources = result.get(
                    "sources",
                    [],
                )

                # Add assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

                st.rerun()

            except requests.exceptions.RequestException:
                st.error(
                    "Could not connect to the backend. "
                    "Make sure FastAPI is running on port 8000."
                )

            except Exception as e:
                st.error(
                    f"Something went wrong: {e}"
                )