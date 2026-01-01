import streamlit as st
import boto3
from botocore.config import Config
from PIL import Image

st.markdown('<h1 class="title">Windshield Inspector</h1>', unsafe_allow_html=True)
st.write("")
st.write("")

# Constants
BEDROCK_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
#BEDROCK_MODEL_ID = "us.meta.llama3-2-90b-instruct-v1:0"
AWS_REGION = "us-west-2"

# Initialize the AWS Bedrock client
config = Config(read_timeout=1000, retries=dict(max_attempts=5))
bedrock_client = boto3.client('bedrock-runtime', region_name=AWS_REGION, config=config)

# Define the refined few-shot prompt
prompt = """
I will show you several examples of windshields, and I need you to classify the next image as either "Good" or "Damaged."

Example 1:
- Label: Good
- Description: A windshield with no visible damage. It is completely clear and intact, with no cracks, chips, or impairments.

Example 2:
- Label: Good
- Description: A perfectly clear windshield with no visible chips, cracks, or distortions. The glass is in pristine condition.

Example 3:
- Label: Damaged
- Description: A windshield with a large crack running across the center, compromising the structural integrity of the glass. It is unsafe for driving.

Example 4:
- Label: Damaged
- Description: A windshield with a small chip near the corner. While the chip isn't yet a crack, it has the potential to expand, posing a future hazard.

Now, classify the following windshield:
- Label: ?
- Description: A windshield with visible damage (e.g., crack, chip, or distortion). You should analyze it based on these visible impairments, even if the image is taken from inside or outside the vehicle, or at an angle that doesn’t show a close-up.

**Key Instructions:**
- **Classify the windshield as "Good" if you can clearly see through it, and there are no visible cracks, chips, distortions, or any other impairments.**  
- **Classify the windshield as "Damaged" if there are visible cracks, chips, distortions, or other impairments that could affect safety or visibility.**  
- **Even if the image is not focused solely on the windshield, as long as the windshield is visible, clear of damage (no cracks, chips, or distortions), and you can see through it clearly, classify it as "Good."**

Even if the close-up of the windshield is not uploaded, use the following guidelines to help you determine the quality of the windshield:

1. **Viewpoint Consideration:** The image might be captured from inside the vehicle, outside, or at an angle. Pay attention to any visible impairments, regardless of the perspective. Even if the windshield is not the main focus of the image, as long as it is clearly visible and undamaged, classify it as "Good."

2. **Type of Damage:** Look for visible signs of cracks, chips, distortions, or other damage. This could include:
   - **Cracks:** Any visible cracks that run across the glass, even if not large, may compromise the integrity of the windshield.
   - **Chips:** A small chip, especially near edges or the driver's line of sight, could lead to more severe damage over time.
   - **Distortions:** These may not be cracks or chips but could affect the safety or clarity of vision, such as a haze or warping.

3. **Classifications:**
   - **Good:** No visible defects. The windshield should be free from any damage or imperfections, and you can see through it clearly.
   - **Damaged:** Any visible damage that could compromise safety, such as cracks, chips, or distortions that may worsen over time or obstruct visibility.

**Please include the following in your response:**
1. The classification: "Good" or "Damaged."
2. Your confidence percentage (e.g., 90% confident) indicating how certain you are about the classification.
3. A brief explanation of why you made this classification decision, including any visible damage or absence of damage that led to your conclusion.

**Do not say "I cannot classify the windshield as 'Good' or 'Damaged'."**  
**If the uploaded image is a windshield, always classify it as either "Good" or "Damaged."**  
**If the uploaded image does not appear to be a windshield, kindly ask the user to upload a valid windshield image for evaluation.**
"""

# Function to display the image in the Streamlit app
def display_image(image):
    # st.image(image, caption="Uploaded Windshield Image", use_container_width=True)
    st.image(image, caption="Uploaded Windshield Image", use_column_width=True)
    
# Function to query AWS Bedrock model for image analysis
def get_image_insights(image_data, prompt):
    try:
        # Prepare the message payload for Bedrock model
        messages = [
            {
                "role": "user",
                "content": [
                    {"image": {"format": "png", "source": {"bytes": image_data}}},
                    {"text": prompt},
                ]
            }
        ]

        # Send request to Bedrock API
        response = bedrock_client.converse_stream(
            modelId=BEDROCK_MODEL_ID,
            messages=messages,
            inferenceConfig={"maxTokens": 2000, "temperature": 1, "topP": 0.999}
        )

        # Handle and display the streamed response
        output_placeholder = st.empty()
        full_response = ""
        for chunk in response["stream"]:
            if "contentBlockDelta" in chunk:
                text = chunk["contentBlockDelta"]["delta"]["text"]
                full_response += text
                output_placeholder.markdown(f"<div class='wrapped-text'>{full_response}</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"ERROR: Can't invoke '{BEDROCK_MODEL_ID}'. Reason: {e}")

# Streamlit file uploader
uploaded_file = st.file_uploader("Choose a Windshield image...", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file:
    # Display the image in the Streamlit app
    image = Image.open(uploaded_file)
    display_image(image)
    
    # Convert image to bytes for processing
    image_bytes = uploaded_file.getvalue()
    
    # Get insights for the uploaded image
    get_image_insights(image_data=image_bytes, prompt=prompt)
