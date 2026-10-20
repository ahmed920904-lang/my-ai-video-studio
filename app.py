import streamlit as st
from gtts import gTTS
import os
import requests
import urllib.parse
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="استوديو الفيديو الخاص بي", page_icon="🎬")
st.title("🎬 استوديو الفيديو الخاص بي")
st.write("أهلاً بك! اكتب موضوع الفيديو وسأقوم بكتابة القصة، توليد الصوت، وجلب الصور لصناعة فيديو كامل.")

topic = st.text_area("اكتب موضوع الفيديو هنا:", "مغامرة طفل صغير يكتشف باباً سحرياً في غرفته")

if st.button("توليد الفيديو الكامل"):
    if topic:
        with st.spinner('جاري العمل... (كتابة السيناريو، الصوت، الصور، والمونتاج). يرجى الانتظار قليلاً...'):
            
            # 1. كتابة السيناريو (نص تجريبي)
            script = f"هذه قصة عن {topic}. كان هناك طفل صغير، يبلغ من العمر ثماني سنوات، يحب استكشاف الأشياء الغريبة. في يوم من الأيام، بينما كان يلعب في غرفته، وجد شيئاً غامضاً..."
            
            # 2. توليد الصوت
            audio_file = "voice.mp3"
            tts = gTTS(text=script, lang='ar')
            tts.save(audio_file)
            
            # 3. جلب 3 صور من الإنترنت (كصور عشوائية للتجربة)
            image_urls = [
                "https://images.unsplash.com/photo-1519689680058-324335c77eba?w=800", 
                "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800", 
                "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800"  
            ]
            
            image_clips = []
            duration_per_image = 5 
            
            for url in image_urls:
                try:
                    response = requests.get(url)
                    img = Image.open(BytesIO(response.content))
                    img.save("temp.jpg")
                    clip = ImageClip("temp.jpg").set_duration(duration_per_image).resize(height=720)
                    clip = clip.resize(lambda t: 1 + 0.02*t)
                    image_clips.append(clip)
                except Exception as e:
                    st.error(f"حدث خطأ في جلب الصور: {e}")

            if image_clips:
                # 4. المونتاج (دمج الصور مع الصوت)
                video = concatenate_videoclips(image_clips, method="compose")
                audio = AudioFileClip(audio_file)
                
                video = video.set_duration(audio.duration) 
                if video.duration > (len(image_clips) * duration_per_image):
                    video = concatenate_videoclips([video] * 3, method="compose").set_duration(audio.duration)

                video = video.set_audio(audio)
                
                # حفظ الفيديو
                output_file = "final_video.mp4"
                video.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")
                
                st.success("تم إنشاء الفيديو بنجاح! 🎉")
                st.write("### 🎬 الفيديو النهائي:")
                st.video(output_file)
                
    else:
        st.warning("الرجاء كتابة موضوع أولاً.")
