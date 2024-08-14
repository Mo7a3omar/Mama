import streamlit as st
from mistralai import Mistral

# Initialize Mistral client with your API key
client = Mistral(api_key="f3pMUmrbB5SPB6Jy8YEvigbyj5jgWWTZ")  # Replace with your actual API key

# Define the MamaBot class
class MamaBot:
    def __init__(self, id, query):
        self.id = id
        self.user_query = query

    def send_query(self):
        try:
            chat_response = client.agents.complete(
                agent_id=self.id,
                messages=[{"role": "user", "content": self.user_query}],
            )
            output = chat_response.choices[0].message.content
            return output
        except Exception as e:
            return f"An error occurred while processing your request: {str(e)}"

# Initialize chat history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "user_query" not in st.session_state:
    st.session_state["user_query"] = ""

# Define the function to handle user input and generate responses
def mama_bot_response(query):
    id = "ag:befd46a2:20240813:mama:e547f219"  # Replace with the appropriate agent ID for MamaBot

    # Create an instance of MamaBot
    mamabot = MamaBot(id, query)
    response = mamabot.send_query()

    # Update the chat history
    st.session_state["chat_history"].append((query, response))
    st.session_state["user_query"] = ""  # Clear the input field after sending the message

# Mommy-themed Streamlit UI
st.markdown("""
    <style>
    .main {
        background-color: #f7e7dc;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    .stButton button {
        background-color: #ffb6c1;
        color: #d2691e;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        margin-top: 10px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stTextInput > div > div > input {
        border: 2px solid #ffb6c1;
        padding: 10px;
        border-radius: 10px;
    }
    .stMarkdown {
        font-size: 20px;
        color: #d2691e;
    }
    .stTextArea textarea {
        border: 2px solid #ffb6c1;
        border-radius: 10px;
    }
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: #d2691e;'> اتكلم مع ماما يا حبيبي 💖</h4>", unsafe_allow_html=True)

# Display the chat history with mommy-themed style
if st.session_state["chat_history"]:
    st.markdown("<h3 style='color: #d2691e;'>كلامك مع ماما:</h3>", unsafe_allow_html=True)
    for query, response in st.session_state["chat_history"]:
        st.markdown(f"<p style='color: #d2691e;'><strong>أنت:</strong> {query}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #d2691e;'><strong>ماما:</strong> {response} 🍪</p>", unsafe_allow_html=True)

# Text input for user query placed below the conversation
user_query = st.text_input("ابعت..", st.session_state["user_query"])

# Center the "Send to Mama" button
if st.button("ابعت  لماما", key="send"):
    if user_query:
        st.session_state["user_query"] = user_query  # Store the query in session state
        mama_bot_response(user_query)
        st.experimental_rerun()  # Force a rerun to immediately update the state

# Center the "Clear Chat" button
if st.button("امسح الكلام", key="clear"):
    st.session_state["chat_history"] = []
