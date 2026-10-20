import streamlit as st
from gtts import gTTS
import os

st.set_page_config(page_title="استوديو الفيديو الخاص بي", page_icon="🎬")
st.title("🎬 استوديو الفيديو الخاص بي")
st.write("أهلاً بك في موقعك الخاص! اكتب موضوع الفيديو وسأقوم بكتابة القصة وتوليد الصوت لك.")

topic = st.text_area("اكتب موضوع الفيديو هنا:", "مغامرة طفل صغير يكتشف باباً سحرياً في غرفته")

if st.button("توليد الفيديو"):
    if topic:
        with st.spinner('جاري كتابة السيناريو وتوليد الصوت...'):
            script = f"هذه قصة عن {topic}. كان هناك طفل صغير، يبلغ من العمر ثماني سنوات، يحب استكشاف الأشياء الغريبة. في يوم من الأيام، بينما كان يلعب في غرفته..."
            
            tts = gTTS(text=script, lang='ar')
            audio_file = "voice.mp3"
            tts.save(audio_file)
            
            st.success("تم توليد الصوت بنجاح! (هذه هي النسخة التجريبية الأولى)")
            st.write("### 📝 السيناريو:")
            st.write(script)
            st.write("### 🔊 التعليق الصوتي:")
            st.audio(audio_file)
    else:
        st.warning("الرجاء كتابة موضوع أولاً.")
