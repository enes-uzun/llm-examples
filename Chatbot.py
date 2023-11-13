import openai
import streamlit as st
import os

st.set_page_config(page_title="🦜🔗 Midheaven Beta Chatbot")
st.title('🦜🔗 Midheaven Beta Chatbot')

# API anahtarını ortam değişkenlerinden al
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

# Session state ayarları
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mevcut mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan yeni bir mesaj al
if prompt := st.chat_input("Yazmak için tıklayınız."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Sistem ve kullanıcı mesajlarını birleştir
        combined_messages = [{"role": "system", "content": "Senin ismin  Midheaven Astroloji Kişisel Chatbot. Biri sana ismini sorarsa benim ismin Midheaven demelisin."}] + \
                            [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

        # API çağrısını yap
        try:
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=combined_messages,
                max_tokens=800
            )
            full_response = response.choices[0].text.strip()
        except Exception as e:
            full_response = f"Bir hata oluştu: {str(e)}"

        # Nihai yanıtı göster
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
