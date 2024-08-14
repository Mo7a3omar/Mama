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
            return "An error occurred, please try again later."

# Initialize chat history and user query in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "user_query" not in st.session_state:
    st.session_state["user_query"] = ""

if "last_message" not in st.session_state:
    st.session_state["last_message"] = ""

if "conversation_started" not in st.session_state:
    st.session_state["conversation_started"] = False

# Define the function to handle user input and generate responses
def mama_bot_response():
    try:
        query = st.session_state["user_query"].strip()

        # Check if the query is the same as the last processed message to avoid duplicates
        if query and query != st.session_state["last_message"]:
            id = "ag:befd46a2:20240813:mama:e547f219"  # Replace with the appropriate agent ID for MamaBot

            # Create an instance of MamaBot
            mamabot = MamaBot(id, query)
            response = mamabot.send_query()

            # Update the chat history
            st.session_state["chat_history"].append((query, response))

            # Store the last processed message
            st.session_state["last_message"] = query

            # Clear the user query after processing
            st.session_state["user_query"] = ""
    except Exception as e:
        # Optionally log the error, but don't show it in the UI
        pass

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
    .chat-message {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        width: 60%;
        text-align: right;
    }
    .user-message {
        background-color: #ffddcc;
        margin-left: auto;
        margin-right: 0;
    }
    .mama-message {
        background-color: #fff2e6;
        margin-left: auto;
        margin-right: 0;
    }
    .center-text {
        text-align: center;
        color: #d2691e;
        font-size: 24px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: #d2691e;'> ماما </h4>", unsafe_allow_html=True)

# Start Button to initialize the conversation
if not st.session_state["conversation_started"]:
    if st.button("اتكلم مع ماما من هنا"):
        st.session_state["conversation_started"] = True
else:
    # Display the chat history with mommy-themed style
    if st.session_state["chat_history"]:
        st.markdown("<h3 class='center-text'>كلامك مع ماما</h3>", unsafe_allow_html=True)
        for query, response in st.session_state["chat_history"]:
            st.markdown(f"<div class='chat-message user-message'><strong>أنت:</strong> {query}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-message mama-message'><strong>ماما:</strong> {response}</div>", unsafe_allow_html=True)

    # Text input for user query placed below the conversation
    st.text_input("اكتب رسالتك هنا...", key="user_query", placeholder="اكتب هنا...")

    # Center the "Send to Mama" button and handle the click event
    if st.button("ابعت لماما"):
        mama_bot_response()

    # Center the "Clear Chat" button
    if st.button("امسح المحادثة"):
        st.session_state["chat_history"] = []
        st.session_state["last_message"] = ""
        st.session_state["conversation_started"] = False  # Reset the conversation started flag
