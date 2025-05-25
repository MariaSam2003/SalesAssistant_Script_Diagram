# SalesAssistant_Script_Diagram
# 📞 AI Sales Assistant: Negotiation & Closing Strategy Script and Diagram Generator

## Overview
This **AI Sales Assistant** application is designed to help sales professionals streamline their negotiation and deal-closing processes. Powered by a Large Language Model (LLM) like **chatgpt-4o-mini*, it generates tailored, multi-turn call scripts focused on overcoming objections and securing commitments. The assistant enhances conversations through the application of persuasive principles, providing a structured approach to finalize deals.

## ✨ Features
* **Customizable Context:** Generate scripts based on specific industry, buyer persona, product offer, call type, sales objective, and sales framework.
* **Intelligent Framework Selection:** Choose from various sales frameworks (e.g., Challenger, SPIN, MEDDIC) or let the AI automatically select the most suitable one.
* **AI-Generated Negotiation Script:** Produces a dynamic, multi-turn dialogue between an Agent and a Client, complete with simulated objections and persuasive responses.
* **Structured Deal Flowchart:** Provides a clear, visual representation of the typical negotiation and closing process, including common branching paths for handling different client responses.
* **Persuasion Principles:** The AI agent is prompted to incorporate techniques like social proof, scarcity, and urgency triggers within the dialogue to guide the conversation effectively.
* **Branded PDF Export:** Compiles the generated script, key engagement overview (objective, framework), and the deal flowchart into a professionally formatted, downloadable PDF document with customizable logos.

##  Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```
    *(Remember to replace `your-username/your-repo-name` with the actual path to your repository.)*

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    # On Windows: .\venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    pip install -r requirements.txt
    ```
    *(You will need to create a `requirements.txt` file as detailed in the "Libraries Used" section below.)*

3.  **Install Graphviz:**
    This application uses `Graphviz` to generate flowcharts. Ensure it's installed and accessible in your system's PATH.
    * **On Windows:** Download and install from [Graphviz website](https://graphviz.org/download/gpl/). Make sure to add Graphviz to your system's PATH during installation.
   

4.  **Set your LLM API Key:**
    The application requires an API key for the Large Language Model. Create a `.env` file in the root of your project and add your API key:
    ```
    GOOGLE_API_KEY="your-chatgpt-api-key-here"

##  Usage

Run the app using:
```bash
streamlit run app.py
