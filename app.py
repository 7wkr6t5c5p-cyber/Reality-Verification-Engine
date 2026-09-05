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
video_path = tfile.name

if st.button("Run Video Verification"):
with st.spinner("Extracting frames and analyzing video..."):
try:
cap = cv2.VideoCapture(video_path)
frames = []
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
step = max(int(frame_count / 6), 1)
current_frame = 0

while cap.isOpened() and len(frames) < 6:
ret, frame = cap.read()
if not ret:
break
if current_frame % step == 0:
frame = cv2.resize(frame, (640, 360))
success, buffer = cv2.imencode(".jpg", frame)
if success:
base64_image = base64.b64encode(buffer).decode("utf-8")
frames.append(base64_image)
current_frame += 1
cap.release()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
content_list = [
{
"type": "text",
"text": f"Analyze these video frames in connection with this context/observation: '{user_input}'"
}
]

for f in frames:
content_list.append({
"type": "image_url",
"image_url": {"url": f"data:image/jpeg;base64,{f}"}
})

response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[{"role": "user", "content": content_list}],
max_tokens=500
)

st.subheader("Verification Analysis Result")
st.write(response.choices[0].message.content)

except Exception as e:
st.error(f"Error processing video: {e}")
else:
st.info("Unlock advanced video uploads by entering your access pass above.")
