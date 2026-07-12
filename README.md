# 🎬 AI Movie Recommendation System

An intelligent Movie Recommendation System built using **LangGraph**, **LangChain**, **Mistral AI**, **OMDb API**, and **Streamlit**.

The application analyzes a movie provided by the user, recommends similar movies, analyzes similarities, checks OTT platform availability, and finally recommends the **Top 5 movies**.

---

## 🚀 Features

- 🎥 Search any Movie or TV Show
- 🤖 AI-powered movie recommendations using Mistral AI
- 🎬 Fetch movie details from OMDb API
- ⭐ Recommend similar movies
- 📺 Check OTT platform availability
- 🏆 Display Top 5 recommended movies
- ⚡ Parallel workflow execution using LangGraph
- 🎨 Interactive Streamlit UI

---

## 🛠 Tech Stack

- Python
- LangGraph
- LangChain
- Mistral AI
- Streamlit
- OMDb API
- Requests
- Python Dotenv

---

## 📁 Project Structure

```
Movie-Recommendation-System/
│
├── .venv/
├── .env
├── parallel.py              # LangGraph workflow
├── main.py               # Streamlit UI
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/CineAgent.git
```

```bash
cd CineAgent
```

---

### Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file.

```env
MISTRAL_API_KEY=YOUR_MISTRAL_API_KEY
```

OMDb API key is configured inside the project.

---

## ▶️ Run the Application

Launch the Streamlit application

```bash
streamlit run run.py
```

---

## 🔄 Workflow

```
                  START
                     │
                     ▼
              Movie Details
                     │
                     ▼
              Movie Finder
               /           \
              /             \
             ▼               ▼
   Review Analyzer     OTT Checker
              \             /
               \           /
                ▼         ▼
             Recommendation
                    │
                    ▼
                   END
```

The workflow uses **parallel execution** after the Movie Finder stage.

---

## 📷 Application Output

### 🎬 Movie Details

- Title
- Genre
- Runtime
- IMDb Rating
- Director
- Cast
- Plot

### 🏆 Top 5 Recommendations

The system recommends the best five movies based on:

- Similarity
- Genre
- Storyline
- Themes
- IMDb Rating
- Audience Appeal

### 📺 OTT Availability

Displays:

- Streaming Platform
- Subscription Type
- Region Availability

---

## 📦 Requirements

Main Libraries

- langgraph
- langchain
- langchain-mistralai
- streamlit
- python-dotenv
- requests

Install all packages using

```bash
pip install -r requirements.txt
```



## ⭐ If you like this project

Give this repository a ⭐ on GitHub.
