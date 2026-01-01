# Windshield Inspector

An AI-powered application that uses computer vision and AWS Bedrock to assess windshield damage, providing real-time classification and analysis of windshield conditions.

You can view a short demo video in the "Demo" folder.

## Features

- Real-time windshield damage detection
- Image classification (Good/Damaged)
- Confidence score reporting
- Detailed analysis explanation
- Support for multiple image formats
- Interactive web interface
- Streaming response display

## Architecture

### Components
- Frontend: Streamlit web application
- AI Model: AWS Bedrock (Claude-3)
- Image Processing: PIL (Python Imaging Library)
- Cloud Infrastructure: AWS Services

## Prerequisites

- AWS Account with access to:
  - AWS Bedrock
  - Claude-3 Sonnet model
- Python 3.8+
- AWS CLI configured
- Required permissions for AWS Bedrock

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd windshield-inspector
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials:
```bash
aws configure
```

## Environment Variables

```bash
AWS_REGION=us-west-2
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Upload a windshield image
3. View the analysis results:
   - Classification (Good/Damaged)
   - Confidence percentage
   - Detailed explanation

## Supported Image Formats

- PNG
- JPG/JPEG
- WebP

## Features in Detail

### Image Analysis
- Crack detection
- Chip identification
- Distortion analysis
- Visibility assessment

### AI Model
- Few-shot learning approach
- High accuracy classification
- Detailed reasoning
- Confidence scoring

### Response Format
- Binary classification
- Confidence percentage
- Explanatory text
- Real-time streaming

## Dependencies

```
streamlit
boto3
Pillow
python-dotenv
```