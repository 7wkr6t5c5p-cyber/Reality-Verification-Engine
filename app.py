cd ~/Desktop
pip install opencv-python openai streamlit
cat << 'EOF' > app.py
import streamlit as st
import cv2
import tempfile
import base64
from openai import OpenAI

st.title("Reality Verification Engine")

api_key = st.sidebar.text_input("API Key", type="password")
user_input = st.text_area("Observation or Context:", placeholder="Describe what you want to verify or look for in this video...")
uploaded_file = st.file_uploader("Upload Video File", type=["mp4", "mov", "avi", "mkv"])

def extract_key_frames(video_path, max_frames=6):
vidcap = cv2.VideoCapture(video_path)
total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
step = max(total_frames // max_frames, 1)
frames = []
count = 0
success, image = vidcap.read()
while success:
if count % step == 0 and len(frames) < max_frames:
_, buffer = cv2.imencode(".jpg", image)
frames.append(buffer.tobytes())
success, image = vidcap.read()
count += 1
vidcap.release()
return frames

if st.button("Run Reality Verification"):
if not api_key:
st.error("Please enter your OpenAI API key in the sidebar.")
elif not uploaded_file:
st.warning("Please upload a video file to analyze.")
elif not user_input.strip():
st.warning("Please enter a description or observation to guide the analysis.")
else:
client = OpenAI(api_key=api_key)

with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
tmp.write(uploaded_file.read())
tmp_path = tmp.name

with st.spinner("Processing video frames and running analysis..."):
try:
frames = extract_key_frames(tmp_path)

content = [{"type": "text", "text": f"Analyze the provided video frame sequence based on this observation: {user_input}"}]

for frame_bytes in frames:
encoded_img = base64.b64encode(frame_bytes).decode('utf-8')
content.append({
"type": "image_url",
"image_url": {"url": f"data:image/jpeg;base64,{encoded_img}"}
})

response = client.chat.completions.create(
model="gpt-4o",
messages=[{"role": "user", "content": content}],
max_tokens=1000
)

st.success("Verification Complete!")
st.write(response.choices[0].message.content)

except Exception as e:
st.error(f"An error occurred during analysis: {e}")
EOF
streamlit run app.py
streamlit run app.py
