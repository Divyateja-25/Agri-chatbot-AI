# 🌱 AgriBot: AI-Powered Agriculture Assistant

AgriBot is an intelligent chatbot web application designed to assist farmers and agricultural enthusiasts. It provides real-time advice on crop management, pest control, and soil health using a hybrid approach: a curated local knowledge base for instant answers and **Google's Gemini 2.0 AI** for complex queries.

## 🚀 Features

* **🤖 AI-Powered Conversationalist:** Integrated with **Google Gemini 2.0 Flash** (Free Tier) to answer complex agricultural questions.
* **🍃 Image Disease Analysis:** Users can upload photos of crops/leaves to detect diseases and get treatment recommendations.
* **🌐 Multilingual Support:** Capable of understanding and replying in **English, Hindi, and Tamil**.
* **📚 Hybrid Knowledge Engine:** Prioritizes a verified local dataset (`kb.json`) for speed and accuracy, falling back to AI for broader topics.
* **🔐 User System:** Secure login/registration with profile management (Crop & Region preferences).
* **🛡️ Admin Dashboard:** Interface for administrators to view user stats and chat history.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **AI Engine:** Google Gemini API (`google-generativeai`)
* **Database:** SQLite (via SQLAlchemy)
* **Frontend:** HTML5, CSS3, JavaScript
* **Tools:** Git, VS Code

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/Divyateja-25/Agri-chatbot-AI.git](https://github.com/Divyateja-25/Agri-chatbot-AI.git)
cd "Agri-chatbot-AI/Agrobot ai-pro"

2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
Bash
pip install -r requirements.txt

4. Set Up API Keys 🔑
This project requires a Google Gemini API Key (Free).
Get your free key from Google AI Studio.
Create a new file named .env in the project root folder.
Add the following line to the file:
Plaintext

GOOGLE_API_KEY=your_actual_api_key_here
(Note: Do not use quotes around the key. The .env file is ignored by Git for security.)

5. Run the Application
Bash

python app.py
Open your browser and go to: http://127.0.0.1:5000

📂 Project Structure
Plaintext

Agrobot ai-pro/
├── app.py                 # Main Flask application entry point
├── chatbot_model.py       # AI logic (Gemini + Local KB handling)
├── database.py            # Database models (User, ChatHistory)
├── requirements.txt       # Python dependencies
├── .env                   # API Keys (Hidden from GitHub)
├── kb.json                # Local Knowledge Base (JSON)
├── static/                # CSS, JS, and Images
└── templates/             # HTML Templates
📸 Usage Guide
Register/Login: Create an account to save your chat history.

Ask a Question: Type queries like "Best fertilizer for paddy" or "How to treat tomato blight?".

Upload Image: Click the "Image" button to upload a photo of a sick plant for diagnosis.

Profile: Update your preferred crop and region in the profile settings for personalized advice.