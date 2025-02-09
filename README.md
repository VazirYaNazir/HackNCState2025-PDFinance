# PDFinance
## Inspiration
- Financial analysts, investors, and professionals deal with massive amounts of documents (SEC filings, earnings reports, contracts).
- Searching for specific insights manually is time-consuming and inefficient.
- We wanted to build a smart, AI-powered tool that makes finding answers to document-based queries fast, accurate, and effortless.

## What it does
✅ **Uploads & stores PDFs** in an SQLite database (financial reports, contracts, whitepapers)
✅ **Extracts and processes text** from pages based on a user's query
✅ **Uses vector-based search** to find the most relevant documents
✅ **Generates intelligent answers** from the retrieved content using an AI model
✅ **Provides an intuitive Tkinter GUI** for seamless user interaction

## How we built it
💾 **Database:** SQLite3 for storing PDFs and extracted text
📄 **Text Extraction:** PyPDF2 for parsing and extracting PDFs
🧠 **Vector Search:** LangChain for document processing and AI interactions
🤖 **AI Model:** OpenAI’s API (ChatGPT) for generating responses based on retrieved information
🖥️ **Frontend:** Tkinter for an interactive user interface
📂 **File Management:** Shutil for file operations
🔑 **Environment Variables:** Dotenv for managing environment variables

## Challenges we ran into
🚧 Integrating multiple components
📉 Working with objects to analyze vectors
🔄 Refactoring & redoing multiple sections to increase efficiency

## Accomplishments that we're proud of
🏆 Successfully built a working AI-powered document search tool!
📊 Achieved accurate retrieval of insights from PDFs
💡 Developed a scalable solution that could be extended to other industries
🚀 Learned how to integrate vector search & AI models effectively

## What we learned
📌 Implementing a local SQLite3 database and PyQt6 GUI
📌 Integrating vector search with AI models
📌 Optimizing systems for real-time performance


WARNING - CHATGPT API WAS USED IN THIS PROJECT. A PERSONAL API KEY IS REQUIRED FOR INDIVIDUAL USE
