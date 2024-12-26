import streamlit as st
from langchain.prompts import PromptTemplate
from transformers import pipeline

## Function to get response from LLaMA 2 model using Hugging Face

def getLLamaresponse(input_text, no_words, blog_style):

    ## Load the Llama-2 model via Hugging Face
    model_name = "TheBloke/Llama-2-7B-Chat-GGML"  # Make sure the model is available on Hugging Face
    generator = pipeline("text-generation", model=model_name, tokenizer=model_name, device=0)  # device=0 for GPU, -1 for CPU
    
    ## Prompt Template
    template = """
        Write a blog for {blog_style} job profile for a topic {input_text}
        within {no_words} words.
    """
    
    prompt = PromptTemplate(input_variables=["blog_style", "input_text", "no_words"], template=template)
    
    ## Generate the response from the LLaMA 2 model
    response = generator(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words), max_length=256, temperature=0.01)
    
    return response[0]['generated_text']


st.set_page_config(page_title="Generate Blogs",
                   page_icon='👾',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Blog Generator")

input_text = st.text_input("Enter the Blog Topic")

## creating two more columns for additional 2 fields

col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No. of Words')
with col2:
    blog_style = st.selectbox('Writing the blog for',
                            ('Researchers', 'Data Scientist', 'Common People'), index=0)
    
submit = st.button("Generate")

## Final response
if submit:
    response = getLLamaresponse(input_text, no_words, blog_style)
    st.write(response)
