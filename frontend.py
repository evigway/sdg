import streamlit as st

st.set_page_config(
    page_title="SDG",       # Title of the page
    page_icon="path/to/favicon.ico"        # Path to the favicon file
)
i_col1, i_col2 = st.columns([1, 4])
with i_col1:
    st.image('product_image.png', use_column_width=True)
with i_col2:
    st.title("Synthetic Data Generation")

st.empty().markdown("")
st.empty().markdown("")
st.empty().markdown("")


if "widget_count" not in st.session_state:
    st.session_state.widget_count = 1
if "data_storage" not in st.session_state:
    st.session_state.data_storage = ['']

def on_plus_click():
    st.session_state.widget_count += 1
    st.session_state.data_storage.append('')

def on_submit_click():
    st.write("You entered:")
    for i, data in enumerate(st.session_state.data_storage):
        st.write(f"Prompt {i + 1}: {data}")


options = ['Stable diffusion', 'Option 2 - coming soon', 'Option 3 - coming soon']
selected_option = st.selectbox('Select GenAI model:', options)

st.button("➕", on_click=on_plus_click)

for i in range(st.session_state.widget_count):
    print(i)
    col1, col2, col3 = st.columns([1, 4, 2])

    with col1:
        st.write(f"Prompt {i + 1}:")

    with col2:
        st.session_state.data_storage[i] = st.text_input("", key=f'textarea_{i}, ', placeholder="Military tank near a creek with top down view")

    with col3:
        st.number_input("Number of images", min_value=1, step=1, key=f'num_images_{i}', on_change=lambda: st.session_state.update())

st.button("Process All", on_click=on_submit_click)