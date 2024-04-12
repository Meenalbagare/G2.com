# Problem Statement -2
This project demonstrates how to use SpaCy for  text processing and feature extraction from review data obtained from the G2 API. The code retrieves reviews related to "G2 Marketing Solutions,"
analyzes the reviews using SpaCy, and extracts actionable insights and named entities.

# Requirements
Python 3.x
spacy
nltk
requests

Additionally, you need to download and set up the SpaCy English model (en_core_web_sm) using:
python -m spacy download en_core_web_sm

# Setup
Run the G2.py file

The script will fetch dislike-related reviews for "G2 Marketing Solutions" from an API, process the reviews using SpaCy, and extract relevant features.
Extracted features will be displayed in the console for analysis
