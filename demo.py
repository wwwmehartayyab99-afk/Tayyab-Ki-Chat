import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="Tayyab & Owais Chat", page_icon="💬")

# 2. Database File Setup (Messages yahan save honge)
DB_FILE = "chat_history.txt"

def save_message(user, text):
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{user}||{text}\n")

def load_messages():
    if not os.path.exists(DB_FILE):
        return []
    messages = []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "||" in line:
                user, text = line.strip().split("||", 1)
                messages.append({"user": user, "content": text})
    return messages

# 3. UI Shuru
st.title("🚀 PROFESSOR Private Chat")

# Sidebar for Name
with st.sidebar:
    st.header("User Profile")
    my_name = st.text_input("Apna Naam Likhein:", value="Tayyab")
    if st.button("Delete All Chat"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        st.rerun()

# 4. Display Messages
all_messages = load_messages()
for m in all_messages:
    with st.chat_message("user" if m["user"] == my_name else "assistant"):
        st.write(f"**{m['user']}**: {m['content']}")

# 5. Chat Input
if prompt := st.chat_input("Message likhein..."):
    # Save to file
    save_message(my_name, prompt)
    # Refresh screen
    st.rerun()
