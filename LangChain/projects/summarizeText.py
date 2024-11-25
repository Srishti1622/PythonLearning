# Application in which we will provide any youtube or website url and will be get the summary of content present in that URL

# need to download to libraries
# - validators==0.28.1   -> for validating urls
# - youtube_transcript_api  -> it will help to read the entire transcript of the youtube video
# - pip install pytube
# - pip install unstructured
import streamlit as st
import validators
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from pytube import YouTube
from langchain_core.documents import Document

# streamlit app
st.set_page_config(page_title="Summarize text from Youtube or Website")
st.title("Summarize text from Youtube or Website")

# getting api key from user
api_key=st.sidebar.text_input("Enter Groq API Key",type='password')

# getting url from the user 
url=st.text_input("Provide the URL whose content you want to summarize")


# creating prompt template
prompt_template=""" Provide a summary of the following content in 300 words:
Content:{text}"""

# final prompt 
prompt=PromptTemplate(
    input_variables=['text'],
    template=prompt_template
)

# Function to fetch transcript
def fetch_youtube_transcript(video_url):
    video_id = video_url.split("v=")[-1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        return f"Error fetching transcript: {e}"

# click button to get the summarize content
if st.button("Summarize"):
    if not api_key.strip() or not url.strip():
        st.error("Please provide the information")
    elif not validators.url(url):
        st.error("Please provide valid url")
    else:
        try:
            with st.spinner("Loading..."):
                # llm model
                groq_llm=ChatGroq(model="Gemma-7b-It",groq_api_key=api_key)

                # for loading data from youtube url
                if "youtube.com" in url:
                    # loader=YoutubeLoader.from_youtube_url(url,add_video_info=True)
                    transcript_text = fetch_youtube_transcript(url)
                    if transcript_text.startswith("Error"):
                        st.error(transcript_text)
                    else:
                        docs = [Document(page_content=transcript_text)]
                else:
                    loader=UnstructuredURLLoader(
                        urls=[url],
                        ssl_verify=False,
                        headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                    )
                    docs=loader.load()
                
                st.write(docs)

                # chain for summarization
                chain=load_summarize_chain(llm=groq_llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)

                st.write("reached")
                st.success(output_summary)
        
        except Exception as e:
            st.exception(f"Exception:{e}")