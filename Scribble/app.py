import streamlit as st
import numpy as np
from PIL import Image
import logging
import os
from dotenv import load_dotenv

from utils.ocr_processor import extract_text_from_image
from utils.ai_processor import clean_and_structure_text
from utils.file_export import export_txt, export_csv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="Scribble to Digital",
    page_icon="📝"
)

st.title("📝 Scribble to Digital")
st.write("Convert messy handwritten notes into clean digital text and to-do lists.")

MAX_FILE_SIZE = 5 * 1024 * 1024

uploaded_file = st.file_uploader(
    "Upload handwritten notes image",
    type=["jpg", "jpeg", "png"]
)


def validate_file(file):

    if file.size > MAX_FILE_SIZE:
        return False, "File exceeds 5MB size limit"

    return True, "Valid file"


if uploaded_file:

    valid, message = validate_file(uploaded_file)

    if not valid:
        st.error(message)
        st.stop()

    try:

        image = Image.open(uploaded_file)

        st.subheader("Uploaded Image")
        st.image(image)

        image_np = np.array(image)

        logging.info("Image uploaded successfully")

        if st.button("Convert to Digital"):

            with st.spinner("Running OCR..."):

                raw_text = extract_text_from_image(image_np)

            st.subheader("Raw OCR Text")
            st.text_area("OCR Output", raw_text, height=200)

            logging.info(raw_text)

            with st.spinner("Cleaning text with AI..."):

                clean_text, tasks = clean_and_structure_text(raw_text)

            st.subheader("Clean Notes")
            st.write(clean_text)

            st.subheader("Extracted Tasks")

            if tasks:
                for task in tasks:
                    st.write(f"- {task}")
            else:
                st.info("No tasks detected")

            st.subheader("Download Results")

            col1, col2 = st.columns(2)

            with col1:

                if st.button("Download TXT"):

                    path = export_txt(clean_text)

                    with open(path, "rb") as f:
                        st.download_button(
                            "Download Notes",
                            f,
                            file_name="digital_notes.txt"
                        )

            with col2:

                if tasks:

                    if st.button("Download Tasks CSV"):

                        path = export_csv(tasks)

                        with open(path, "rb") as f:
                            st.download_button(
                                "Download CSV",
                                f,
                                file_name="tasks.csv"
                            )

    except Exception as e:

        logging.error(str(e))

        st.error("Processing error")
        st.code(str(e))