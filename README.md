# 🎵 Moodwave — Song Recommendation Engine

> Discover songs that match your vibe, energy, and style.

Built with Python, Streamlit, and the Last.fm API.

---

## 👥 Team

Made with ♥ by **Charmi Jani**, **Tejashree Karekar** and **Dnyanesh Panchal**

---

## 📌 What is Moodwave?

Moodwave is a music recommendation web app that takes any song as input and returns a list of similar songs based on vibe, artist style, and musical similarity — powered by the Last.fm API.

---

## 🚀 Features

- Search any song by name or artist
- Select from top matching results
- Get 10 similar song recommendations instantly
- View similarity scores as a bar chart
- Clean, animated dark-themed UI

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| Recommendation | Last.fm API |
| Data Processing | Pandas, Scikit-learn |
| Charts | Plotly |

---

## 📁 Project Structure

```
moodwave/
├── app.py              # Streamlit frontend
├── recommender.py      # Recommendation engine
├── data_loader.py      # Last.fm API calls
├── features.py         # Feature engineering helpers
├── requirements.txt    # Python dependencies
├── .env                # API keys (not uploaded to GitHub)
└── .gitignore
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/moodwave.git
cd moodwave
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get a free Last.fm API key
1. Go to [last.fm/api/account/create](https://www.last.fm/api/account/create)
2. Sign up and create an app
3. Copy your API key

### 5. Create a `.env` file
```
LASTFM_API_KEY=your_api_key_here
```

### 6. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🌐 Deployment

This app is deployed on **Streamlit Cloud**.

To deploy your own:
1. Push the project to a public GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `app.py` as the main file
5. Add your `LASTFM_API_KEY` under **Settings → Secrets**

---

## 📦 Requirements

```
streamlit
pandas
numpy
scikit-learn
requests
python-dotenv
plotly
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `LASTFM_API_KEY` | Your Last.fm API key |

---

## 📸 How It Works

1. User searches for a song
2. App queries Last.fm for matching tracks
3. User selects the exact song
4. App calls Last.fm's `track.getSimilar` endpoint
5. Results are ranked by similarity score and displayed

---

## 📄 License

This project is for educational purposes only.
