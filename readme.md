# Chat with Multiple PDFs App

The MultiPDF Chat App is a Python application that allows you to chat with multiple PDF documents. You can ask questions about the PDFs using natural language, and the application will provide relevant responses based on the content of the documents. This app utilizes a language model to generate accurate answers to your queries. Please note that the app will only respond to questions related to the loaded PDFs.

## Installation

1. Clone the repository.
2. Install the required Python packages by running `pip install -r requirements.txt`.

## Usage

1. Run the app by executing `streamlit  run app.py` in the terminal.
2. Upload your PDF documents using the file uploader.
3. Ask questions about the documents in the text input field.
4. Click on the "Process" button to process the documents and get answers to your questions.

## Configuration

- Make sure you have the necessary environment variables(e.g= open_ai_api_key) set. Refer to the `.env` file for the required variables.

## How it works

-The application follows these steps to provide responses to your questions:

-PDF Loading: The app reads multiple PDF documents and extracts their text content.

-Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively.

-Language Model: The application utilizes a language model to generate vector representations (embeddings) of the text chunks.

-Similarity Matching: When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones.

-Response Generation: The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs.


## Known Issues

- The app may have performance issues when processing large PDF documents.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.