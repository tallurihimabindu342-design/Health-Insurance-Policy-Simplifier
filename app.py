import streamlit as st
import requests

# ---------------- BACKEND CONFIG ----------------
BACKEND_URL = "http://10.250.6.174:8000"   # change if backend IP changes

st.set_page_config(page_title="PolicyAI", layout="wide")

# ---------------- API FUNCTIONS ----------------
def upload_pdf(file):
    try:
        files = {"file": (file.name, file, "application/pdf")}
        res = requests.post(f"{BACKEND_URL}/upload", files=files)

        if res.status_code != 200:
            st.error(res.text)
            return False

        return True

    except Exception as e:
        st.error(f"Upload failed: {e}")
        return False


def ask_question(question):
    try:
        res = requests.post(
            f"{BACKEND_URL}/ask",
            json={"question": question},
            timeout=120
        )

        if res.status_code != 200:
            return {"answer": "Backend error", "citations": []}

        try:
            return res.json()
        except:
            return {"answer": "Server returned invalid response", "citations": []}

    except Exception as e:
        return {"answer": f"Connection error: {e}", "citations": []}


# ---------------- UI STYLE ----------------
st.markdown("""
<style>
header {visibility:hidden;}
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.title {
    text-align:center;
    font-size:40px;
    font-weight:800;
    color:#10b981;
}

.subtitle {
    text-align:center;
    color:#6b7280;
    margin-bottom:30px;
}

.answer-box {
    background:white;
    padding:22px;
    border-radius:14px;
    border:1px solid #e5e7eb;
    margin-top:20px;
    color:#111827 !important;
}

.citation {
    background:#f9fafb;
    padding:12px;
    border-radius:10px;
    margin-top:10px;
    border-left:4px solid #10b981;
    color:#111827 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">🛡️ PolicyAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Understand your insurance instantly</div>', unsafe_allow_html=True)

# ---------------- UPLOAD SECTION ----------------
st.subheader("📄 Upload Policy")

uploaded_file = st.file_uploader("Upload your insurance PDF", type=["pdf"])

if uploaded_file:
    if st.button("Upload Policy"):
        with st.spinner("Processing document..."):
            success = upload_pdf(uploaded_file)

        if success:
            st.success("✅ Document processed successfully!")

# ---------------- QUESTION SECTION ----------------
st.subheader("💬 Ask Questions")

question = st.text_input(
    "Ask about your policy",
    placeholder="Is surgery covered?"
)

if st.button("Get Answer"):

    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("🤖 AI is thinking..."):
            result = ask_question(question)

        answer = result.get("answer", "No answer received")
        citations = result.get("citations", [])

        # -------- ANSWER --------
        st.markdown(
            f"""
            <div class="answer-box">
                <h4 style="color:#111827;">✅ Answer</h4>
                <p style="color:#111827;">{answer}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # -------- CITATIONS --------
        if citations:
            st.markdown("### 📚 Citations")

            for c in citations:
                st.markdown(
                    f"""
                    <div class="citation">
                        <b>Page:</b> {c['page']}<br>
                        {c['content']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )