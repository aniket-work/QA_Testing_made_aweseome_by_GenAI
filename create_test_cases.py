import streamlit as st
from PIL import Image, ImageFilter
from OllamaModelLoader import OllamaModelLoader
from image_utils import convert_image_to_base64, display_base64_image
import pandas as pd
import json

# App title and description
st.set_page_config(page_title="Make Test cases using GenAI", page_icon=":Target:")

# Add a blurred background image
background_image = Image.open("background.png")
blurred_background = background_image.filter(ImageFilter.GaussianBlur(radius=3))
st.image(blurred_background, use_column_width=True)

# Add text on top of the blurred image
st.markdown(
    """
    <div style="position: relative;">
        <h1 style="color: white; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); text-align: center; margin-top: -150px;">Make Test cases using GenAI</h1>
        <p style="color: white; font-size: 20px; font-weight: bold; text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5); text-align: center; margin-top: -20px;">Revolutionize QA Testing : Capture, Click, Test - AI Writes the Rest!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# upload images
def upload_image():

    # Use Markdown syntax to set font size
    st.markdown("<span style='font-size: 20px;'>Submit your Webpage snap, AI write test cases. !</span>",
                unsafe_allow_html=True)

    # Use file_uploader as usual
    images = st.file_uploader("", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    assert len(images) <= 4, (st.error("Please upload at most 4 images"), st.stop())

    if images:
        # convert images to base64
        images_b64 = []
        for image in images:
            image_b64 = convert_image_to_base64(image)
            images_b64.append(image_b64)

        # display images in multiple columns
        cols = st.columns(len(images_b64))
        for i, col in enumerate(cols):
            col.markdown(f"**Image {abs((i+1)-len(cols))+1}**")
            col.markdown(display_base64_image(images_b64[i]), unsafe_allow_html=True)
        st.markdown("---")
        return images_b64
    st.stop()


import json

def generate_table(response):
    try:
        # Find the start and end index of the JSON part
        start_index = response.find("```json") + len("```json")
        end_index = response.find("```", start_index)

        # Extract the JSON part
        json_part = response[start_index:end_index]

        # Load JSON data
        data = json.loads(json_part)

        # Convert JSON data to DataFrame
        df = pd.DataFrame(data)

        # Number the steps in the "Steps to Perform the Test Case" column
        for index, row in df.iterrows():
            steps = row["Steps to Perform the Test Case"]
            numbered_steps = "<br>".join([f"{i}. {step}" for i, step in enumerate(steps, start=1)])
            df.at[index, "Steps to Perform the Test Case"] = numbered_steps

        # Generate HTML table from DataFrame
        html_table = df.to_html(index=False, escape=False)

        return html_table
    except Exception as e:
        return f"Failed to parse the response: {str(e)}"

# init session state of the uploaded image
image_b64 = upload_image()

# Define a flag to track whether the question has been asked before
if 'question_asked' not in st.session_state:
    st.session_state.question_asked = False

# Ask question
if not st.session_state.question_asked:
    st.session_state.question_asked = True
else:
    q = st.chat_input("Do you want more custom test cases? Let me know !")
    if q:
        question = q
    else:
        # if isinstance(image_b64, list):
        if len(image_b64) > 1:
            question = f"Describe the {len(image_b64)} images:"
        else:
            question = "Write 5 QA 'Test cases' in JSON format for this image,  make these as json keys for each test case : 'Test Case ID' 'Description of the Test Case' 'Steps to Perform the Test Case' 'Expected Result' 'Actual Results', in 'Actual Results' put TODO: To be Tested"

    # load Ollama model using OllamaModelLoader
    config_file_path = 'ollama_config.json'  # Path to the JSON configuration file
    ollama_loader = OllamaModelLoader(config_file_path)
    mllm = ollama_loader.load_ollama_model()

    # Run the language model
    @st.cache_data(show_spinner=False)
    def run_language_model(query, image_base64):
        """
        Runs the language model with the given query and image context.

        Args:
            query (str): The user's question or prompt.
            image_base64 (str): The base64-encoded image data.

        Returns:
            str: The language model's response.
        """
        llm_with_image_context = mllm.bind(images=image_base64)
        response = llm_with_image_context.invoke(query)
        return response

    # Display the user's question
    with st.container():
        st.markdown(
            f"""
            <div style="background-color: #f0f0f0; padding: 16px; border-radius: 8px;">
                <h3 style="margin-top: 0;">QA Test case customization:</h3>
                <p style="font-size: 16px; font-weight: bold;">{question}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Define the custom spinner
    spinner_html = """
        <style>
            @keyframes spinner-rotation {
                from {
                    transform: rotate(0deg);
                }
                to {
                    transform: rotate(360deg);
                }
            }
            .spinner {
                width: 48px;
                height: 48px;
                border-radius: 50%;
                border: 8px solid #f3f3f3;
                border-top: 8px solid #3498db;
                animation: spinner-rotation 1s linear infinite;
            }
        </style>
        <div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
            <div class="spinner"></div>
        </div>
    """

    # Run the language model and display the response
    with st.container():
        spinner_placeholder = st.empty()
        spinner_placeholder.markdown(spinner_html, unsafe_allow_html=True)
        response = run_language_model(question, image_b64)
        print(response)
        html_table = generate_table(response)
        print(html_table)
        spinner_placeholder.empty()

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="background-color: #e6f7ff; padding: 16px; border-radius: 8px;max-width: 5000px;">
                <h3 style="margin-top: 0;">Response:</h3>
                <p style="font-size: 16px;">{html_table}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
