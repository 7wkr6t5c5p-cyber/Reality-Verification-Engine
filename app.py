import streamlit as st
import cv2
import tempfile
import base64
from openai import OpenAI

st.title("Reality Verification Engine")

user_input = st.text_area("Describe your scenario or observation:")

if st.button("Analyze Scenario (Free)"):
if not user_input.strip():
st.warning("Please enter a description.")
else:
try:
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[{"role": "user", "content": user_input}]
)
st.write(response.choices[0].message.content)
except Exception as e:
st.error(f"Error connecting to AI: {e}")

st.markdown("---")

st.subheader("Advanced Video Verification (Gated Feature)")
access_code = st.text_input("Enter your access pass or code to unlock video analysis:", type="password")

if access_code == "YOUR_SECRET_PAID_PASSCODE":
st.success("Video analysis unlocked!")
uploaded_file = st.file_uploader("Upload Video File", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
tfile = tempfile.NamedTemporaryFile(delete=False)
tfile.write(uploaded_file.read())
