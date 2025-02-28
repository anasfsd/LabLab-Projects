import streamlit as st
import os
from groq import Groq

# Get Groq API Key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("API key is missing! Please set GROQ_API_KEY in your environment variables.")
else:
    client = Groq(api_key=GROQ_API_KEY)

    def get_groq_response(user_input):
        """Generate a response using the Groq API with the LLaMA model and strict filtering."""
        system_prompt = (
            "You are an AI assistant that only responds to questions about challenges and solutions "
            "for schools, colleges, and universities in underserved regions. If the query is not related "
            "to this topic, respond with: 'I'm sorry, but I can only assist with education-related challenges in underserved regions.' "
            "Do not answer any other questions."
        )

        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                model="llama3-70b-8192"
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    # Streamlit UI
    st.title("EduConnect Chatbot (Groq LLaMA-3 70B)")
    st.write("Ask about challenges and solutions for schools, colleges, or universities in underserved regions.")

    user_input = st.text_input("Enter your question:")

    if st.button("Submit"):
        if user_input.strip():
            response = get_groq_response(user_input)
            st.write("### Response:")
            st.write(response)
        else:
            st.warning("Please enter a question.")
