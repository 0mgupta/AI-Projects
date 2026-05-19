# import streamlit as st
# import pandas as pd
# import tempfile
# import os
# import time
# from src.pipeline.prediction_pipeline import PredictionPipeline

# # Page configuration
# st.set_page_config(
#     page_title="Spam Email Classifier",
#     page_icon="📧",
#     layout="centered"
# )

# # Initialize pipeline
# @st.cache_resource
# def get_pipeline():
#     return PredictionPipeline(load_models=True)
   
# try:
#     pipeline = get_pipeline()
# except Exception as e:
#     st.error(f"Error loading models: {str(e)}").  
#     st.stop()

# st.title("📧 Spam Email Classifier")
# st.markdown("Classify emails as **Spam** or **Ham** (Clean) using Machine Learning.")

# # Tabs for different modes
# tab1, tab2 = st.tabs(["Single Email", "Batch MBOX Processing"])

# with tab1:
#     st.header("Check a Single Email")
#     email_text = st.text_area("Paste the email content here:", height=200, placeholder="Dear friend, I have a business proposal...")
    
#     if st.button("Classify Email", type="primary"):
#         if email_text.strip():
#             with st.spinner("Analyzing..."):
#                 try:
#                     # Get prediction
#                     result = pipeline.predict_single_email(email_text)
#                     prediction = result['prediction']
#                     confidence = result.get('confidence', 0)
                    
#                     # Display result
#                     if prediction == "Spam":
#                         st.error(f"🚨 This email is **SPAM**")
#                     else:
#                         st.success(f"✅ This email is **HAM** (Safe)")
                    
#                     if confidence:
#                         st.info(f"Confidence Score: {confidence:.1f}%")
                        
#                 except Exception as e:
#                     st.error(f"Error analyzing email: {str(e)}")
#         else:
#             st.warning("Please enter some text to classify.")

# with tab2:
#     st.header("Process MBOX File")
#     uploaded_file = st.file_uploader("Upload an MBOX file", type=['mbox', 'txt'])
    
#     if uploaded_file is not None:
#         if st.button("Process File"):
#             with st.spinner("Processing file... this may take a moment"):
#                 try:
#                     # Save uploaded file to temp
#                     with tempfile.NamedTemporaryFile(delete=False, suffix='.mbox') as tmp_file:
#                         tmp_file.write(uploaded_file.getvalue())
#                         tmp_path = tmp_file.name
                    
#                     try:
#                         # Process file
#                         df = pipeline.predict_mbox_file(tmp_path)
                        
#                         # Show summary metrics
#                         col1, col2 = st.columns(2)
#                         spam_count = len(df[df['Prediction'] == 'Spam'])
#                         ham_count = len(df[df['Prediction'] == 'Ham'])
                        
#                         col1.metric("Total Emails", len(df))
#                         col2.metric("Spam Found", spam_count, delta_color="inverse")
                        
#                         # Show previews
#                         st.subheader("Results Preview")
#                         st.dataframe(df[['Time', 'Subject', 'Prediction']].head(10))
                        
#                         # Download button
#                         csv = df.to_csv(index=False).encode('utf-8')
#                         st.download_button(
#                             label="Download Full Results (CSV)",
#                             data=csv,
#                             file_name=f"predictions_{int(time.time())}.csv",
#                             mime="text/csv",
#                         )
                        
#                     finally:
#                         # Cleanup temp file
#                         if os.path.exists(tmp_path):
#                             try:
#                                 os.unlink(tmp_path)
#                             except:
#                                 pass # Sometimes file lock prevents deletion on Windows
                                
#                 except Exception as e:
#                     st.error(f"Error processing file: {str(e)}")
import streamlit as st
import pandas as pd
import tempfile
import os
import time
from src.pipeline.prediction_pipeline import PredictionPipeline

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SpamShield AI",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* ── Root palette ── */
:root {
    --bg-deep:    #050d1a;
    --bg-card:    #0b1628;
    --bg-input:   #0f1e35;
    --border:     #1a3050;
    --teal:       #00e5c3;
    --teal-dim:   #00b89e;
    --red:        #ff3b5c;
    --red-dim:    #c02640;
    --yellow:     #ffd166;
    --text:       #cfe4f7;
    --text-muted: #5a7a9a;
    --glow-teal:  0 0 18px rgba(0,229,195,.35);
    --glow-red:   0 0 18px rgba(255,59,92,.35);
}

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: var(--bg-deep) !important;
    color: var(--text) !important;
}
.main > .block-container {
    max-width: 780px;
    padding: 2.5rem 2rem 4rem;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.8rem 0 1.8rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: .65rem;
    letter-spacing: .18em;
    color: var(--teal);
    border: 1px solid var(--teal);
    border-radius: 2px;
    padding: .25rem .75rem;
    margin-bottom: 1rem;
    text-transform: uppercase;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.05;
    margin: 0 0 .6rem;
    background: linear-gradient(135deg, #0a2a3a 30%, var(--teal));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: var(--text-muted);
    font-size: 1rem;
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.6;
}
.hero-line {
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, var(--teal), transparent);
    margin: 1.4rem auto 0;
    border-radius: 2px;
}

/* ── Grid stats ── */
.stat-row {
    display: flex;
    gap: 1rem;
    margin: 1.8rem 0;
}
.stat-card {
    flex: 1;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.1rem 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--teal);
}
.stat-card.red::before { background: var(--red); }
.stat-card .stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--teal);
}
.stat-card.red .stat-num { color: var(--red); }
.stat-card .stat-label {
    font-size: .72rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-top: .2rem;
}

/* ── Tab strip ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: .78rem !important;
    letter-spacing: .06em !important;
    color: var(--text-muted) !important;
    border-radius: 6px !important;
    padding: .55rem 1.4rem !important;
    border: none !important;
    background: transparent !important;
    transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
    background: var(--teal) !important;
    color: #000 !important;
    font-weight: 700 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.6rem !important;
}

/* ── Section labels ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: .68rem;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: var(--teal);
    margin-bottom: .6rem;
}

/* ── Textarea ── */
.stTextArea textarea {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: .82rem !important;
    line-height: 1.7 !important;
    padding: 1rem !important;
    transition: border-color .2s, box-shadow .2s !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: var(--teal) !important;
    box-shadow: var(--glow-teal) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: var(--text-muted) !important; }

/* ── Primary button ── */
.stButton > button[kind="primary"],
div[data-testid="stButton"] > button {
    background: var(--teal) !important;
    color: #000 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: .8rem !important;
    font-weight: 700 !important;
    letter-spacing: .08em !important;
    border: none !important;
    border-radius: 6px !important;
    padding: .65rem 1.8rem !important;
    cursor: pointer !important;
    transition: box-shadow .2s, transform .15s !important;
    width: 100% !important;
}
.stButton > button[kind="primary"]:hover,
div[data-testid="stButton"] > button:hover {
    box-shadow: var(--glow-teal) !important;
    transform: translateY(-1px) !important;
}

/* ── Result banners ── */
.result-spam {
    background: linear-gradient(135deg, #1a0510, #200a15);
    border: 1px solid var(--red);
    border-left: 4px solid var(--red);
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    display: flex;
    align-items: center;
    gap: .9rem;
    box-shadow: var(--glow-red);
    animation: slideIn .3s ease;
}
.result-ham {
    background: linear-gradient(135deg, #011510, #041a13);
    border: 1px solid var(--teal);
    border-left: 4px solid var(--teal);
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    display: flex;
    align-items: center;
    gap: .9rem;
    box-shadow: var(--glow-teal);
    animation: slideIn .3s ease;
}
.result-icon { font-size: 2rem; }
.result-title {
    font-size: .65rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: .2rem;
}
.result-label-spam {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--red);
}
.result-label-ham {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--teal);
}

/* ── Confidence bar ── */
.conf-wrap {
    margin-top: 1.1rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.2rem;
}
.conf-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: .55rem;
}
.conf-label {
    font-family: 'Space Mono', monospace;
    font-size: .65rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--text-muted);
}
.conf-value {
    font-family: 'Space Mono', monospace;
    font-size: .9rem;
    font-weight: 700;
    color: var(--teal);
}
.conf-bar-bg {
    height: 6px;
    background: var(--border);
    border-radius: 3px;
    overflow: hidden;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--teal-dim), var(--teal));
    box-shadow: 0 0 8px rgba(0,229,195,.5);
    transition: width 1s ease;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 10px !important;
    padding: 1.5rem !important;
    text-align: center !important;
    transition: border-color .2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--teal) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    border: 1px solid var(--teal) !important;
    color: var(--teal) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: .78rem !important;
    letter-spacing: .06em !important;
    border-radius: 6px !important;
    transition: background .2s, box-shadow .2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(0,229,195,.1) !important;
    box-shadow: var(--glow-teal) !important;
}

/* ── Spinner text ── */
[data-testid="stSpinner"] p {
    font-family: 'Space Mono', monospace !important;
    font-size: .78rem !important;
    color: var(--teal) !important;
    letter-spacing: .06em !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border) !important;
    margin: 1.6rem 0 !important;
}

/* ── Animations ── */
@keyframes slideIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: .45; }
}
.scanning-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: var(--teal);
    border-radius: 50%;
    margin-right: .5rem;
    animation: pulse 1.2s infinite;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI-Powered Detection</div>
    <h1>SpamShield AI</h1>
    <p>Instant, accurate spam detection powered by machine learning. Protect your inbox in real time.</p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ── Initialize pipeline ────────────────────────────────────────────────────────
@st.cache_resource
def get_pipeline():
    return PredictionPipeline(load_models=True)

try:
    pipeline = get_pipeline()
except Exception as e:
    st.markdown(f"""
    <div class="result-spam">
        <div class="result-icon">⚠️</div>
        <div>
            <div class="result-title">Pipeline Error</div>
            <div class="result-label-spam" style="font-size:1rem">{str(e)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["⬡  Single Email", "⬡  Batch MBOX"])

# ─── TAB 1: Single Email ───────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-label">// Paste email content</div>', unsafe_allow_html=True)
    email_text = st.text_area(
        "",
        height=220,
        placeholder="Dear friend, I have an exciting business proposal that will make you rich overnight...",
        label_visibility="collapsed",
    )

    if st.button("🔍  Analyse Email", type="primary"):
        if email_text.strip():
            with st.spinner("Scanning message patterns..."):
                try:
                    result = pipeline.predict_single_email(email_text)
                    prediction = result['prediction']
                    confidence = result.get('confidence', 0)

                    if prediction == "Spam":
                        st.markdown(f"""
                        <div class="result-spam">
                            <div class="result-icon">🚨</div>
                            <div>
                                <div class="result-title">Classification Result</div>
                                <div class="result-label-spam">SPAM DETECTED</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-ham">
                            <div class="result-icon">✅</div>
                            <div>
                                <div class="result-title">Classification Result</div>
                                <div class="result-label-ham">CLEAN — HAM</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    if confidence:
                        bar_color = "var(--red)" if prediction == "Spam" else "var(--teal)"
                        st.markdown(f"""
                        <div class="conf-wrap">
                            <div class="conf-header">
                                <span class="conf-label">Confidence Score</span>
                                <span class="conf-value" style="color:{bar_color}">{confidence:.1f}%</span>
                            </div>
                            <div class="conf-bar-bg">
                                <div class="conf-bar-fill" style="width:{confidence}%;
                                    background:linear-gradient(90deg,{bar_color}99,{bar_color});
                                    box-shadow:0 0 8px {bar_color}80;">
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                except Exception as e:
                    st.markdown(f"""
                    <div class="result-spam">
                        <div class="result-icon">⚠️</div>
                        <div>
                            <div class="result-title">Error</div>
                            <div class="result-label-spam" style="font-size:.95rem">{str(e)}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:var(--bg-card);border:1px solid var(--yellow);border-left:4px solid var(--yellow);
                        border-radius:8px;padding:1rem 1.2rem;color:var(--yellow);
                        font-family:'Space Mono',monospace;font-size:.82rem;">
                ⚠ &nbsp; Please paste some email text before analysing.
            </div>
            """, unsafe_allow_html=True)

# ─── TAB 2: Batch MBOX ────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-label">// Upload .mbox or .txt file</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['mbox', 'txt'], label_visibility="collapsed")

    if uploaded_file is not None:
        st.markdown(f"""
        <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:8px;
                    padding:.9rem 1.2rem;display:flex;align-items:center;gap:.8rem;margin-bottom:1rem;">
            <span style="color:var(--teal);font-size:1.3rem">📂</span>
            <div>
                <div style="font-family:'Space Mono',monospace;font-size:.78rem;
                            color:var(--text-muted);letter-spacing:.08em;text-transform:uppercase;">
                    File Ready</div>
                <div style="font-weight:600;font-size:.95rem">{uploaded_file.name}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚡  Process MBOX File", type="primary"):
            with st.spinner("Processing emails — this may take a moment..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mbox') as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name

                    try:
                        df = pipeline.predict_mbox_file(tmp_path)
                        spam_count = len(df[df['Prediction'] == 'Spam'])
                        ham_count  = len(df[df['Prediction'] == 'Ham'])
                        spam_pct   = round(spam_count / len(df) * 100, 1) if len(df) else 0

                        # Stats row
                        st.markdown(f"""
                        <div class="stat-row">
                            <div class="stat-card">
                                <div class="stat-num">{len(df)}</div>
                                <div class="stat-label">Total Emails</div>
                            </div>
                            <div class="stat-card red">
                                <div class="stat-num">{spam_count}</div>
                                <div class="stat-label">Spam Detected</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-num">{ham_count}</div>
                                <div class="stat-label">Clean Emails</div>
                            </div>
                            <div class="stat-card red">
                                <div class="stat-num">{spam_pct}%</div>
                                <div class="stat-label">Spam Rate</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown('<div class="section-label">// Results Preview — top 10</div>',
                                    unsafe_allow_html=True)
                        st.dataframe(
                            df[['Time', 'Subject', 'Prediction']].head(10),
                            use_container_width=True,
                            hide_index=True,
                        )

                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="⬇  Download Full Results (CSV)",
                            data=csv,
                            file_name=f"spamshield_results_{int(time.time())}.csv",
                            mime="text/csv",
                        )

                    finally:
                        if os.path.exists(tmp_path):
                            try:
                                os.unlink(tmp_path)
                            except:
                                pass

                except Exception as e:
                    st.markdown(f"""
                    <div class="result-spam">
                        <div class="result-icon">⚠️</div>
                        <div>
                            <div class="result-title">Processing Error</div>
                            <div class="result-label-spam" style="font-size:.95rem">{str(e)}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<hr>
<div style="text-align:center;font-family:'Space Mono',monospace;font-size:.65rem;
            letter-spacing:.12em;color:var(--text-muted);padding-bottom:1rem;">
    SPAMSHIELD AI &nbsp;·&nbsp; ML-POWERED EMAIL CLASSIFICATION &nbsp;·&nbsp; 
    <span style="color:var(--teal)">● ONLINE</span>
</div>
""", unsafe_allow_html=True)
