# gemini_pdf_chat_frontend.py

import streamlit as st
from gemini_pdf_chat_backend import process_pdfs

# Custom CSS
css = '''
<style>
.chat-message { padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex }
.chat-message.user { background-color: #2b313e }
.chat-message.bot { background-color: #475063 }
.chat-message .avatar { width: 20%; }
.chat-message .avatar img { max-width: 78px; max-height: 78px; border-radius: 50%; object-fit: cover; }
.chat-message .message { width: 80%; padding: 0 1.5rem; color: #fff; }
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/TRc5gW7/pexels-danxavier-1239288.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/KwQgfPc/pexels-utpaladhikary-15844719.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                st.session_state.conversation = process_pdfs(pdf_docs)

if __name__ == '__main__':
    main()