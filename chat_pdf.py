import os
import tempfile
import streamlit as st
from embedchain import App
import base64
from streamlit_chat import message
from PIL import Image

# Load the chatbot's avatar image
chatbot_avatar = Image.open("download.png")

# Function to create the embedchain bot with the specified configuration
def embedchain_bot(db_path):
    return App.from_config(
        config={
            "llm": {"provider": "ollama", "config": {"model": "llama3.2:latest", "max_tokens": 250, 
                     "temperature": 0.5, "stream": True, "base_url": "http://localhost:11434"}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "ollama", "config": {"model": "llama3.2:latest", "base_url": "http://localhost:11434"}},
        }
    )

# Function to display a PDF file in the Streamlit app
def display_pdf(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')  # Encode the PDF to base64
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="400" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)  # Display the PDF in an iframe

# Set up the main title and description of the app
st.title("PersoBot")
st.caption("This is a personal chatbot that works without internet. It's based on llama3.2:latest")

# Create a temporary path for the knowledge base
db_path = tempfile.mktemp()

# Initialize the app and messages if they don't exist in session state
if 'app' not in st.session_state:
    st.session_state.app = embedchain_bot(db_path)
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar for uploading PDFs
with st.sidebar:
    st.header("PDF Upload")
    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

    # If a PDF file is uploaded, show a preview
    if pdf_file:
        st.subheader("PDF Preview")
        display_pdf(pdf_file)
        
        # Button to add the uploaded PDF to the knowledge base
        if st.sidebar.button("Add to Knowledge Base"):
            with st.spinner("Adding PDF to knowledge base..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
                    f.write(pdf_file.getvalue())
                    st.session_state.app.add(f.name, data_type="pdf_file")  # Add PDF to the bot's knowledge
                os.remove(f.name)  # Clean up the temporary file
            st.success(f"Added {pdf_file.name} to knowledge base!")

# Display the chat messages with avatar for the assistant (bot)
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=str(i))
    else:
        col1, col2 = st.columns([1, 9])  # Use columns to display avatar and message side by side
        with col1:
            st.image(chatbot_avatar, width=50)  # Display the avatar for the bot
        with col2:
            message(msg["content"], is_user=False, key=str(i))

# Input field for the user to ask questions
if prompt := st.chat_input("Ask any question about the PDF"):
    st.session_state.messages.append({"role": "user", "content": prompt})  # Save the user's message
    message(prompt, is_user=True)  # Display the user's message

    with st.spinner("Thinking..."):
        response = st.session_state.app.chat(prompt)  # Get the bot's response
        st.session_state.messages.append({"role": "assistant", "content": response})  # Save the bot's response
        # Display bot response with avatar
        col1, col2 = st.columns([1, 9])
        with col1:
            st.image(chatbot_avatar, width=50)
        with col2:
            message(response, is_user=False)

# Button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.messages = []  # Reset messages
    st.success("Chat history cleared!")
