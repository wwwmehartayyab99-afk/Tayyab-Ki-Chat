 import streamlit as st
import os
from PIL import Image
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Tayyab & Owais Chat", page_icon="💬")

# 2. Setup Directories and Files
DB_FILE = "chat_history.txt"
MEDIA_DIR = "chat_media"

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

def save_message(user, content, msg_type="text"):
    with open(DB_FILE, "a", encoding="utf-8") as f:
        # Format: User||Type||Content
        f.write(f"{user}||{msg_type}||{content}\n")

def load_messages():
    if not os.path.exists(DB_FILE):
        return []
    messages = []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "||" in line:
                parts = line.strip().split("||", 2)
                if len(parts) == 3:
                    user, msg_type, content = parts
                    messages.append({"user": user, "type": msg_type, "content": content})
    return messages

# 3. UI Shuru
st.title("🚀 PROFESSOR Private Chat")

# Sidebar for Name and Upload
with st.sidebar:
    st.header("User Profile")
    my_name = st.text_input("Apna Naam Likhein:", value="Tayyab")
    
    st.divider()
    st.header("Upload Media")
    uploaded_file = st.file_uploader("Photo select karein", type=["jpg", "jpeg", "png"])
    
    if st.button("Send Photo") and uploaded_file:
        # Save image file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = os.path.join(MEDIA_DIR, f"{timestamp}_{uploaded_file.name}")
        with open(img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Save reference in TXT
        save_message(my_name, img_path, msg_type="image")
        st.rerun()

    if st.button("Delete All Chat"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        # Clear images folder too
        for file in os.listdir(MEDIA_DIR):
            os.remove(os.path.join(MEDIA_DIR, file))
        st.rerun()

# 4. Display Messages
all_messages = load_messages()
for m in all_messages:
    role = "user" if m["user"] == my_name else "assistant"
    with st.chat_message(role):
        st.write(f"**{m['user']}**")
        if m["type"] == "text":
            st.write(m["content"])
        elif m["type"] == "image":
            st.image(m["content"], use_container_width=True)

# 5. Chat Input (Text)
if prompt := st.chat_input("Message likhein..."):
    save_message(my_name, prompt, msg_type="text")
    st.rerun()           

            
