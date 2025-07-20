import streamlit as st
import app as main
import tempfile

# Cache the vector store and temp path
@st.cache_resource
def get_vector_store(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file.read())
        tmp_path = tmp_file.name
    db = main.create_vector_store(tmp_path)
    return db

def main_ui():
    st.set_page_config(page_title="💬 Chat with PDF", layout="centered")
    st.title("💬 Chat with PDF")
    st.markdown("Upload a PDF, ask questions, or get a summary.")

    # Upload PDF
    pdf_file = st.file_uploader("Upload your PDF", type="pdf")

    if pdf_file is not None:
        # Reset chat history if a new file is uploaded
        if "last_pdf" not in st.session_state or st.session_state.last_pdf != pdf_file.name:
            st.session_state.chat_history = []
            st.session_state.last_pdf = pdf_file.name

        # Get vector store
        with st.spinner("Processing PDF..."):
            db = get_vector_store(pdf_file)

        # PDF Summarization
        with st.expander("📄 Click to summarize PDF"):
            if st.button("Generate Summary"):
                summary = main.summarize_pdf(db)  # ✅ pass vector store directly
                st.markdown(f"**Summary:**\n\n{summary}")
                st.download_button("📥 Download Summary", summary, file_name="summary.txt")

        # Chat Interface
        st.markdown("### Ask Questions About the PDF")
        user_input = st.text_input("Your Question:", key="input")

        if st.button("Ask"):
            if user_input.strip() != "":
                answer = main.question_pdf(user_input, db)
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Bot", answer))

        # Display Chat History
        for sender, msg in st.session_state.chat_history:
            if sender == "You":
                st.markdown(
                    f"<div style='text-align:right; background-color:#d0f0ff; padding:10px; border-radius:10px; margin:5px'>{msg}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div style='text-align:left; background-color:#f0f0f0; padding:10px; border-radius:10px; margin:5px'>{msg}</div>",
                    unsafe_allow_html=True,
                )

if __name__ == "__main__":
    main_ui()
