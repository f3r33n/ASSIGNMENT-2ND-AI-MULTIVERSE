import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
# i would be using two ai model api's one gemini and another cohere
from google import genai
import cohere
st.title("AI MULTIVERSE")
st.header("This chatbot is based on cohere and gemini api")
st.write("Ask anything and get AI powered responses")
st.divider()
#creating a sidebar now
# This sidebar is for selecting modes like  - PERSONALITY and MODELS and RESPONSE LENGTH and CREATIVITY 
# i HAVE MADE THE INDEX NONE SO THAT NOTHING IS WRIITEN IN THERE AND KEPT ONE AS PLACEHOLDER FOR  A MESSAGE TO BE SHOWN IN THE BOX 
personality=st.sidebar.selectbox("who do u want to talk to",["friendly","sarcastic","professional"], index=None , placeholder="select your personality")
models=st.sidebar.selectbox("which model do u want to use",["cohere","gemini"], index=None , placeholder="select your model")
response_length = st.sidebar.selectbox("How long should the response be" ,["long","short","medium"], index=None , placeholder = "select the length")
creativity=st.sidebar.selectbox("how creative do u want the response to be",["low","medium","high"], index=None , placeholder="select your creativity level")
user_message =st.text_input("Enter your message", value=None, placeholder = "here goes your message")
if st.button("SEND"):
    if not personality:
        st.error("please select ur personality")
    if not models:
        st.error("please select ur model")
    if not creativity:
        st.error("please select ur creativity level")
    if not response_length:
        st.warning("please enter response length")
    if not user_message:
        st.warning("please enter your message")
    else:
        # setting up cohere model
        if models=="cohere":
            cohere_client = cohere.ClientV2(api_key =os.getenv("cohere_api_key"))
            prompt = f"you are a {models} chatbot with {personality} personality and Respone length {response_length} and {creativity} creativity level. respond to the following message : {user_message}"
            # here we will use a spinner to show that the response is being generated
            with st.spinner("generating response hang on there for a moment..."):
             # here for response of cohere client COHERE uses the generate word as "chat" e.g cohere_client.chat and not generate_content(as its in gemini)
             response = cohere_client.chat(model="command-a-plus-05-2026", messages=[{"role": "user", "content": prompt}])
            # I created a loop here - it was throwing error otherwise
            for content in response.message.content:
                if content.type == "text":
                    st.success(f"ANSWER: {content.text}")
         # setting up gemini now ( i added bit more features in gemini here)           
        elif models=="gemini":
            client= genai.Client(api_key = os.getenv("google_api_key"))
            prompt = f"you are a {models} chatbot with {personality} personality Respone length {response_length} and {creativity} creativity level. respond to the following message : {user_message}"
            # here i havent used sippner but laoding screen - ist loading screen empty and then once response is generated then loading_screen.empty() again
            # it removed the loading screen then once response gets generated
            loading_screen = st.empty()
            loading_screen.info("generating response hang on there for a moment...")
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            # this loading_screen.empty() is necessary here - once response is generated the laoding screen disappears
            loading_screen.empty()
            st.subheader("Here is your response")
            # keep response in a nice container for better UI
            with st.container():
                st.subheader("AI RESPONSE")
                st.write(f"🧠 Model : {models}")
                st.write(f"🎭 personality : {personality}")
                st.write(f"creativity : {creativity}")
                st.write(f"length : {response_length}")
                st.divider() 
                st.markdown(response.text)
                character_count = len(user_message) # To measure character count
                st.info (f"Character count: {character_count}")
st.caption("Powered by Gemini & Cohere Made with ❤️ by faizan using Streamlit")
            