# import streamlit as st
# from langchain.prompts import PromptTemplate
# from langchain.llms import CTransformers

# ## Function To get response from LLAma 2 model

# def getLLamaresponse(input_text, no_words, blog_style):

#     ### LLama2 model
#     llm = CTransformers(model='https://drive.google.com/file/d/1W-25SJzmXHAWfQJ1kH6dFDs8TwZN2AnP/view?usp=sharing',
#                       model_type='llama',
#                       config={'max_new_tokens':256,
#                               'temperature':0.6})
    
#     ## Prompt Template

#     template = """
#         Write a blog for {blog_style} job profile for a topic {input_text}
#         within {no_words} words.
#             """
    
#     prompt = PromptTemplate(input_variables=["blog_style","input_text",'no_words'],
#                           template=template)
    
#     ## Generate the ressponse from the LLama 2 model
#     response = llm(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
#     print(response)
#     return response

# ## STREAMLIT APP

# st.set_page_config(page_title="GenBlog",
#                     page_icon='👾',
#                     layout='centered',
#                     initial_sidebar_state='collapsed')

# st.header("Blog Generator")

# input_text = st.text_input("Enter the Blog Topic")

# ## creating to more columns for additonal 2 fields

# col1, col2 = st.columns([5,5])

# with col1:
#     no_words = st.text_input('No of Words')
# with col2:
#     blog_style = st.selectbox('Writing the blog for',
#                             ('Researchers','Data Scientist','Students','Common People'), index=0)
    
# submit = st.button("Generate")

import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

# Function to authenticate and create a Google Drive service instance
def authenticate_google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    return service

# Function to download the model file from Google Drive
def download_file_from_drive(service, file_id, destination):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
    print(f"File downloaded to {destination}.")

# Function to get Llama model response
def getLLamaresponse(input_text, no_words, blog_style):
    try:
        # Load Llama2 model
        model_path = 'llama-2-7b-chat.ggmlv3.q2_K.bin'  # Replace with the downloaded path
        
        # Load Llama2 model
        llm = CTransformers(model=model_path,
                           model_type='llama',
                           config={'max_new_tokens': 256, 'temperature': 0.6})

        # Prompt Template
        template = """
        Write a blog for {blog_style} job profile for a topic {input_text}
        within {no_words} words.
        """

        prompt = PromptTemplate(input_variables=["blog_style", "input_text", 'no_words'], template=template)

        # Generate the response from the Llama 2 model
        response = llm(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
        return response
    except Exception as e:
        return f"Error: {e}"

# Streamlit app setup
st.set_page_config(page_title="GenBlog",
                   page_icon='👾',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Blog Generator")

# Get input from the user
input_text = st.text_input("Enter the Blog Topic")

# Create two columns for additional fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')  # Input for number of words
    try:
        no_words = int(no_words) if no_words else 0  # Ensure input is an integer
    except ValueError:
        no_words = 0  # Default to 0 if not a valid number

with col2:
    blog_style = st.selectbox('Writing the blog for',
                              ('Researchers', 'Data Scientist', 'Students', 'Common People'), index=0)

# Generate the blog response when the button is clicked
submit = st.button("Generate")

if submit:
    # Validate inputs and generate response
    if not input_text:
        st.error("Please enter a blog topic.")
    elif no_words <= 0:
        st.error("Please enter a valid number of words.")
    else:
        # Authenticate and download the model if not present
        if not os.path.exists('llama-2-7b-chat.ggmlv3.q2_K.bin'):
            service = authenticate_google_drive()
            file_id = '1W-25SJzmXHAWfQJ1kH6dFDs8TwZN2AnP'  # Replace with the actual file ID from Google Drive
            download_file_from_drive(service, file_id, 'llama-2-7b-chat.ggmlv3.q2_K.bin')

        # Generate response from the model
        st.write(getLLamaresponse(input_text, no_words, blog_style))


## Final response
if submit:
    st.write(getLLamaresponse(input_text, no_words, blog_style))
