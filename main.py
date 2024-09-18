import os

import streamlit as st
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import torch
import time
import random
import os
from datetime import datetime

def intialisation():
    if 'output_folder_path' not in st.session_state:
        output_dir = os.path.join(root_dir, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(output_dir)
        st.session_state.output_folder_path = output_dir

    repo_id = "stabilityai/stable-diffusion-2-base"
    pipe = DiffusionPipeline.from_pretrained(repo_id, torch_dtype=torch.float16, variant="fp16")

    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")
    return pipe
def on_plus_click():
    st.session_state.widget_count += 1
    st.session_state.data_storage.append(['', 1])

def on_submit_click():
    global current_progress
    pipe = intialisation()
    total_number_of_images = sum(map(lambda x: x[1], st.session_state.data_storage))
    progress_steps = 1/total_number_of_images
    if st.session_state.progress_bar is not None:
        st.session_state.progress_bar.empty()
    st.session_state.progress_bar = st.progress(current_progress, "Dataset is being generated ...")
    for i, data in enumerate(st.session_state.data_storage):
        prompt = data[0]
        for id in range(data[1]):
            image = pipe(prompt, num_inference_steps=50).images[0]
            image.save(os.path.join(st.session_state.output_folder_path, f'image_{i}_{id}.png'))
            current_progress+=progress_steps
            if current_progress > 1:
                current_progress = 1
            st.session_state.progress_bar.progress(current_progress, random.choice(progress_messages)+ f" ||  🅿︎🆁︎🅾︎🅶︎🆁︎🅴︎🆂︎🆂︎ : {current_progress*100:.2f}%")
    current_progress = 1
    st.session_state.progress_bar.progress(current_progress, "Done and dusted! Your images are all set!")
    st.success('Process completed successfully!')
    st.session_state.progress_bar.empty()

current_progress = 0

st.set_page_config(
    page_title="Generate Synthetic Datasets",
    page_icon="favicon.ico"
)
root_dir = "output"

progress_messages = [
    "🍳 Cooking up images in the AI kitchen—smells like creativity!",
    "🖼️ Turning words into pixels—no pixie dust required!",
    "🌍 Your text is on a world tour, and the images are coming back soon!",
    "🎨 ☕ Imagery in the making—like a digital artist with a caffeine boost.",
    "🖌️ Converting your prompts into art—AI's got its paintbrush ready!",
    "💤 🌟 Pixels are getting their beauty sleep—almost time for the reveal!",
    "✨ From words to wonders—our AI is working its magic.",
    "🖼️ 🖌️ Turning text into art—our virtual brush is at work!",
    "🍲 🧑‍🎨 Loading up your visual treat—our AI is brewing something special.",
    "📝 🍲 We’re translating your words into images—AI’s version of a secret recipe.",
    "🧙‍♂️ 🖼️ Making images out of text—think of it as digital wizardry.",
    "💫 Creating visuals—your text is getting its glow-up!",
    "💪 🎨 Sculpting your words into images—AI’s equivalent of a workout session.",
    "🧑‍🎨 Your visuals are being handcrafted—AI’s busy in the art studio.",
    "🖼️ 🖍️ Text-to-image transformation—our AI is flexing its creative muscles!"
]

with st.sidebar:
    st.header("Information", divider="green")
    st.write("Your go to tool generating computer vision datasets")
    st.image('product_image.png', use_column_width=True, width=500)
    st.header("Help", divider="green")
    st.markdown("""
    1. Choose the model you want to use for generating images. 🏗️
    2. Provide description of the image and the number of images. 📝
    3. Click on the ➕ icon to add additional prompts . ✨
    4. Finally Click on the "Process All" button ,you will receive a confirmation message upon successful completion. ✅
    """)
st.title("Synthetic Data Generation")

st.empty().markdown("")
st.empty().markdown("")
st.empty().markdown("")


if "widget_count" not in st.session_state:
    st.session_state.widget_count = 1
if "data_storage" not in st.session_state:
    st.session_state.data_storage = [['',1]]
if "progress_bar" not in st.session_state:
    st.session_state.progress_bar = None




options = ['Stable diffusion', 'Option 2 - coming soon', 'Option 3 - coming soon']
selected_option = st.selectbox(label='Select GenAI model:', options=options)

st.button(label = "➕", on_click=on_plus_click)

for i in range(st.session_state.widget_count):
    col1, col2, col3 = st.columns([1, 4, 2])

    with col1:
        st.write(f"Prompt {i + 1}:")

    with col2:
        st.session_state.data_storage[i][0] = st.text_input(label=f"Prompt {i+1}", key=f'textarea_{i}, ', placeholder="Military tank near a creek with top down view", label_visibility="hidden")

    with col3:
        st.session_state.data_storage[i][1] = st.number_input(label="Number of images", min_value=1, step=1, key=f'num_images_{i}')

st.button("Process All", on_click=on_submit_click)