import streamlit as st
from data_loader import search_song
from recommender import hybrid_recommend
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Moodwave", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #080810;
    color: #e8e8f0;
    font-family: 'DM Sans', sans-serif;
}

/* Animated background orbs */
.stApp::before {
    content: '';
    position: fixed;
    width: 600px; height: 600px;
    background: radial-gradient(circle, #5b21b622 0%, transparent 70%);
    top: -200px; left: -200px;
    border-radius: 50%;
    animation: orb1 8s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed;
    width: 500px; height: 500px;
    background: radial-gradient(circle, #be185d22 0%, transparent 70%);
    bottom: -150px; right: -150px;
    border-radius: 50%;
    animation: orb2 10s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}
@keyframes orb1 { from { transform: translate(0,0) scale(1); } to { transform: translate(80px, 60px) scale(1.2); } }
@keyframes orb2 { from { transform: translate(0,0) scale(1); } to { transform: translate(-60px, -80px) scale(1.15); } }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 4rem; max-width: 1100px; margin: auto; position: relative; z-index: 1; }

/* Hero title */
.hero { text-align: center; padding: 3rem 0 2rem; animation: fadeDown 0.8s ease both; }
@keyframes fadeDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }

.hero-logo {
    font-family: 'Syne', sans-serif;
    font-size: 4.5rem;
    font-weight: 800;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #c4b5fd 0%, #f9a8d4 50%, #fb923c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.5rem;
}
.hero-tagline {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 300;
    color: #6b7280;
    letter-spacing: 3px;
    text-transform: uppercase;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #5b21b644, #be185d44, transparent);
    margin: 1.5rem 0;
    animation: fadeIn 1s ease 0.3s both;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

/* Search input override */
.stTextInput > div > div > input {
    background: #12121e !important;
    color: #e8e8f0 !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    font-size: 1rem !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px #7c3aed22 !important;
}
.stTextInput > div > div > input::placeholder { color: #4b5563 !important; }
.stTextInput label { color: #6b7280 !important; font-size: 0.85rem !important; letter-spacing: 1px !important; text-transform: uppercase !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: #12121e !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 14px !important;
    color: #e8e8f0 !important;
}
.stSelectbox label { color: #6b7280 !important; font-size: 0.85rem !important; letter-spacing: 1px !important; text-transform: uppercase !important; }

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #be185d) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 28px !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.2s !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    color: white !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Now playing card */
.now-playing {
    background: linear-gradient(135deg, #12121e, #1a1a2e);
    border: 1px solid #2a2a40;
    border-radius: 20px;
    padding: 24px;
    margin: 1.5rem 0;
    display: flex;
    gap: 20px;
    align-items: center;
    animation: slideUp 0.5s ease both;
    position: relative;
    overflow: hidden;
}
.now-playing::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #7c3aed, #be185d, #fb923c);
}
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.now-playing-label {
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #7c3aed;
    font-weight: 500;
    margin-bottom: 6px;
}
.now-playing-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #f3f4f6;
    line-height: 1.2;
}
.now-playing-artist {
    font-size: 0.95rem;
    color: #9ca3af;
    margin-top: 4px;
    font-weight: 300;
}

/* Rec cards */
.rec-card {
    background: #0e0e1a;
    border: 1px solid #1e1e30;
    border-radius: 16px;
    padding: 14px 18px;
    margin-bottom: 10px;
    transition: border-color 0.25s, background 0.25s, transform 0.2s;
    animation: cardIn 0.4s ease both;
    position: relative;
    overflow: hidden;
}
.rec-card:hover {
    border-color: #5b21b6;
    background: #12121e;
    transform: translateX(4px);
}
@keyframes cardIn {
    from { opacity: 0; transform: translateX(-16px); }
    to { opacity: 1; transform: translateX(0); }
}
.rec-card:nth-child(1)  { animation-delay: 0.05s; }
.rec-card:nth-child(2)  { animation-delay: 0.10s; }
.rec-card:nth-child(3)  { animation-delay: 0.15s; }
.rec-card:nth-child(4)  { animation-delay: 0.20s; }
.rec-card:nth-child(5)  { animation-delay: 0.25s; }
.rec-card:nth-child(6)  { animation-delay: 0.30s; }
.rec-card:nth-child(7)  { animation-delay: 0.35s; }
.rec-card:nth-child(8)  { animation-delay: 0.40s; }
.rec-card:nth-child(9)  { animation-delay: 0.45s; }
.rec-card:nth-child(10) { animation-delay: 0.50s; }

.rec-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: #2d2d45;
    min-width: 28px;
}
.rec-title {
    font-size: 0.98rem;
    font-weight: 500;
    color: #e2e8f0;
    line-height: 1.3;
}
.rec-artist {
    font-size: 0.82rem;
    color: #6b7280;
    font-weight: 300;
    margin-top: 2px;
}
.match-chip {
    background: linear-gradient(135deg, #5b21b6, #9d174d);
    color: #f3e8ff;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    white-space: nowrap;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.3px;
}

/* Section label */
.section-label {
    font-size: 0.72rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4b5563;
    font-weight: 500;
    margin: 2rem 0 1rem;
}

/* Metric */
[data-testid="stMetricValue"] { color: #a78bfa !important; }
[data-testid="stMetricLabel"] { color: #6b7280 !important; }

/* Spinner */
.stSpinner > div { border-top-color: #7c3aed !important; }

/* Plotly chart bg */
.js-plotly-plot { border-radius: 16px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-logo">Moodwave</div>
    <div class="hero-tagline">Music recommendation engine</div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# Search
query = st.text_input("Search for a song", placeholder="e.g.  Fix You · Coldplay   or   Blinding Lights · The Weeknd")

if query:
    with st.spinner("Searching..."):
        results = search_song(query)

    if results:
        st.markdown('<div class="section-label">Select a track</div>', unsafe_allow_html=True)
        options = {f"{r['name']}  ·  {r['artist']}": r for r in results}
        chosen_label = st.selectbox("", list(options.keys()))
        chosen = options[chosen_label]

        # Now playing card
        img_html = f'<img src="{chosen["image"]}" style="width:90px;height:90px;border-radius:12px;object-fit:cover;flex-shrink:0;" />' if chosen.get("image") else '<div style="width:90px;height:90px;border-radius:12px;background:#1e1e3a;display:flex;align-items:center;justify-content:center;font-size:2rem;flex-shrink:0;">🎵</div>'

        st.markdown(f"""
        <div class="now-playing">
            {img_html}
            <div>
                <div class="now-playing-label">&#9654; Selected Track</div>
                <div class="now-playing-title">{chosen['name']}</div>
                <div class="now-playing-artist">{chosen['artist']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("✦  Discover Similar Songs"):
            with st.spinner("Tuning into your vibe..."):
                recs = hybrid_recommend(chosen['id'], top_n=10)

            if recs:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="section-label">Recommended for you</div>', unsafe_allow_html=True)

                # Rec cards
                for i, rec in enumerate(recs):
                    img_tag = f'<img src="{rec["image"]}" style="width:52px;height:52px;border-radius:8px;object-fit:cover;flex-shrink:0;" />' if rec.get("image") else '<div style="width:52px;height:52px;border-radius:8px;background:#1e1e3a;display:flex;align-items:center;justify-content:center;flex-shrink:0;">🎵</div>'
                    st.markdown(f"""
                    <div class="rec-card">
                        <div style="display:flex;align-items:center;gap:14px;">
                            <span class="rec-num">0{i+1}</span>
                            {img_tag}
                            <div style="flex:1;min-width:0;">
                                <div class="rec-title">{rec['name']}</div>
                                <div class="rec-artist">{rec['artist']}</div>
                            </div>
                            <span class="match-chip">{rec['similarity']}% match</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Chart
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="section-label">Similarity breakdown</div>', unsafe_allow_html=True)
                df_viz = pd.DataFrame(recs)[['name', 'artist', 'similarity']]
                df_viz['label'] = df_viz['name'] + "  ·  " + df_viz['artist']
                fig = px.bar(df_viz, x='similarity', y='label', orientation='h',
                             color='similarity', color_continuous_scale='Purples',
                             template='plotly_dark')
                fig.update_layout(
                    paper_bgcolor='#0e0e1a',
                    plot_bgcolor='#0e0e1a',
                    font=dict(family='DM Sans', color='#9ca3af', size=12),
                    yaxis_title="", xaxis_title="Match %",
                    coloraxis_showscale=False,
                    height=380,
                    margin=dict(l=10, r=20, t=20, b=20),
                )
                fig.update_traces(marker_line_width=0)
                fig.update_xaxes(gridcolor='#1e1e30', zerolinecolor='#1e1e30')
                fig.update_yaxes(gridcolor='#1e1e30')
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.warning("No recommendations found. Try a different song!")
    else:
        st.error("No songs found. Try a different search term!")


st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding: 1.5rem 0 0.5rem; font-family:'DM Sans',sans-serif;">
    <span style="font-size:0.75rem; letter-spacing:2px; text-transform:uppercase; color:#4b5563;">Made with ♥ by</span><br><br>
    <span style="font-size:1rem; color:#9ca3af; font-weight:300;">Charmi Jani &nbsp;·&nbsp; Tejashree Karekar &nbsp;·&nbsp; Dnyanesh Panchal</span>
</div>
""", unsafe_allow_html=True)