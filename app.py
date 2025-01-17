import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

## Function To get response from LLAma 2 model

def getLLamaresponse(input_text, no_words, blog_style):

    ### LLama2 model
    llm = CTransformers(model='https://drive.google.com/file/d/1W-25SJzmXHAWfQJ1kH6dFDs8TwZN2AnP/view?usp=sharing',
                      model_type='llama',
                      config={'max_new_tokens':256,
                              'temperature':0.6})
    
    ## Prompt Template

    template = """
        Write a blog for {blog_style} job profile for a topic {input_text}
        within {no_words} words.
            """
    
    prompt = PromptTemplate(input_variables=["blog_style","input_text",'no_words'],
                          template=template)
    
    ## Generate the ressponse from the LLama 2 model
    response = llm(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
    print(response)
    return response

## STREAMLIT APP

st.set_page_config(page_title="GenBlog",
                    page_icon='👾',
                    layout='centered',
                    initial_sidebar_state='collapsed')

st.header("Blog Generator")

input_text = st.text_input("Enter the Blog Topic")

## creating to more columns for additonal 2 fields

col1, col2 = st.columns([5,5])

with col1:
    no_words = st.text_input('No of Words')
with col2:
    blog_style = st.selectbox('Writing the blog for',
                            ('Researchers','Data Scientist','Students','Common People'), index=0)
    
submit = st.button("Generate")
