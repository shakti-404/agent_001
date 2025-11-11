## LLM Tool Agent

An intelligent LLM-powered agent that dynamically selects and executes the right tool (like web search or research paper search) for each query using the **Groq API**.

---

### ⚙️ Features

* Dynamic tool selection (`web_search`, `research_paper_search`)
* Groq API integration for fast inference
* Environment-based configuration

---

### 🧩 Setup Instructions

#### 1. Clone the repository

```bash
git clone https://github.com/shakti-404/agent_001.git
cd agent_001
```

#### 2. Create and activate a virtual environment

```bash
# Create venv
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 🔐 Environment Setup

Create a `.env` file in the root directory and add your credentials:

```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```


---

### 🚀 Run the Agent

Run the main entry file:

```bash
python main.py
```

---

### 🧰 Project Structure

```
.
├── agent.py             # LLM agent class
├── agent_tools.py       # Tool implementations (web, research, etc.)
├── main.py              # Entry point (can be renamed)
├── requirements.txt     # Dependencies
├── .env                 # Environment variables (ignored by git)
└── .gitignore
```
