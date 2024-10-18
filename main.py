import os
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from loaders import parse_document
from workflow import create_workflow

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Constants
UPLOAD_FOLDER = "uploaded"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Initialize OpenAI chat model
llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)

def setup_page():
    st.set_page_config(page_title="Resume Parsing System", layout="wide")
    st.title("Resume Parsing System")

def ensure_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

def validate_file_size(file: UploadedFile) -> bool:
    if file.size <= MAX_FILE_SIZE:
        return True
    st.error("File size exceeds the 5MB limit. Please upload a smaller file.")
    return False

def save_uploaded_file(file: UploadedFile) -> str:
    file_path = os.path.join(UPLOAD_FOLDER, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path


def get_contents(file_path: str) -> str:
    data=""
    documents=parse_document(file_path)
    for i in documents:
        data+=i.page_content
    
    return data


def main():
    setup_page()
    ensure_upload_folder()

    uploaded_file = st.file_uploader("Choose a resume file", type=['pdf', 'docx'])

    if uploaded_file is not None and validate_file_size(uploaded_file):
        if st.button('Start Processing'):
            with st.spinner('Processing...'):
                try:
                    file_path = save_uploaded_file(uploaded_file)
                    file_content = get_contents(file_path)

                    # Display results
                    st.success(f"Successfully processed uploaded resume.")

                    workflow = create_workflow()
                    initial_state = {
                        "messages": [HumanMessage(content=file_content)],
                        "count": 0,
                        "sender": "",
                    }
                    config = {"configurable": {"thread_id": "abc"}}

                    for s in workflow.stream(initial_state, config):
                        output = list(s.values())[0]
                        sender = output['sender']
                        message = output['messages'][0]
                        
                        with st.expander(f"{sender.capitalize()} Agent Output", expanded=True):
                            st.write(message)
                    
                    st.success("Resume processing complete!")


                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    

if __name__ == "__main__":
    main()

