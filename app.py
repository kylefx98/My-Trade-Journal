# pip install streamlit web3

import streamlit as st
from web3 import Web3
import config
import os
import base64

# ---------------------- BACKGROUND FUNCTIONS ----------------------
def set_bg(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{data}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

def clear_bg():
    st.markdown(
        """
        <style>
        .stApp {
            background: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------------- PAGE ----------------------
st.set_page_config(page_title=config.APP_NAME, layout="wide")

LOGO_PATH = "assets/logo.png"
DASHBOARD_BG_PATH = "assets/dashboard.png"

# ---------------------- HEADER ----------------------
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)
else:
    st.sidebar.title(config.APP_NAME)

st.caption(config.APP_TAGLINE)

# ---------------------- WEB3 ----------------------
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(
    address=w3.to_checksum_address(config.CONTRACT_ADDRESS),
    abi=config.CONTRACT_ABI
)

# ---------------------- SESSION ----------------------
if "last_trade_id" not in st.session_state:
    st.session_state["last_trade_id"] = 1

for key in ["weekly_watch", "daily_watch", "wildcards"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ---------------------- NAV ----------------------
page = st.sidebar.radio("Navigate", [
    "Dashboard",
    "Watchlist",
    "Log New Trade",
    "Close Trade",
    "View Trade"
])

# ---------------------- DASHBOARD ----------------------
if page == "Dashboard":
    set_bg(DASHBOARD_BG_PATH)

    # CSS for Glass UI and Bubbles
    st.markdown("""
        <style>
        .glass {
            background: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(12px);
            border-radius: 18px;
            padding: 22px;
            border: 1px solid rgba(255, 255, 255, 0.35);
            margin-bottom: 18px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        }
        .bubble {
            background: rgba(255, 255, 255, 0.55);
            border-radius: 12px;
            padding: 10px 14px;
            margin: 8px 0;
            border: 1px solid rgba(255, 255, 255, 0.3);
            font-weight: 500;
            color: #111;
        }
        .metric-label { font-size: 13px; color: #555; }
        .metric-value { font-size: 26px; font-weight: 800; color: #111; }
        </style>
    """, unsafe_allow_html=True)

    # Welcome Banner
    st.markdown(f"""
    <div class="glass">
        <div style="font-size: 28px; font-weight: 700;">🦅 Welcome To {config.APP_NAME}</div>
        <div style="font-size: 14px; color: #444; margin-top: 6px;">
            {config.APP_TAGLINE}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Data Handling
    try:
        total = contract.functions.tradeCount().call()
        status_color = "#1b5e20"
        status_text = "Connected"
    except:
        total = 0
        status_color = "#b71c1c"
        status_text = "Offline"

    # Metrics Row
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="glass"><div class="metric-label">Total Trades (Blockchain)</div><div class="metric-value">{total}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="glass"><div class="metric-label">Last Trade ID</div><div class="metric-value">{st.session_state["last_trade_id"]}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="glass"><div class="metric-label">System Status</div><div class="metric-value" style="color:{status_color};">{status_text}</div></div>', unsafe_allow_html=True)

    # Watchlist Bubbles
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<div class="glass"><h3>📅 Weekly Focus</h3>', unsafe_allow_html=True)
        if st.session_state["weekly_watch"]:
            for item in st.session_state["weekly_watch"]:
                st.markdown(f'<div class="bubble">🎯 {item}</div>', unsafe_allow_html=True)
        else:
            st.write("No weekly pairs yet.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="glass"><h3>⚡ Daily Watchlist</h3>', unsafe_allow_html=True)
        if st.session_state["daily_watch"]:
            for item in st.session_state["daily_watch"]:
                st.markdown(f'<div class="bubble">🔥 {item}</div>', unsafe_allow_html=True)
        else:
            st.write("No daily setups yet.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- WATCHLIST ----------------------
elif page == "Watchlist":
    clear_bg()
    st.header("Watchlist 📊")

    pair = st.text_input("Pair (e.g. EUR/USD)")
    category = st.selectbox("Category", ["Weekly", "Daily", "Wildcard"])
    note = st.text_area("Reason")

    if st.button("Add"):
        item = f"{pair} — {note}"

        if category == "Weekly":
            st.session_state["weekly_watch"].append(item)
        elif category == "Daily":
            st.session_state["daily_watch"].append(item)
        else:
            st.session_state["wildcards"].append(item)

        st.success(f"{pair} added")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Weekly")
        for i in st.session_state["weekly_watch"]:
            st.write("•", i)

    with col2:
        st.subheader("Daily")
        for i in st.session_state["daily_watch"]:
            st.write("•", i)

    with col3:
        st.subheader("Wildcards")
        for i in st.session_state["wildcards"]:
            st.write("•", i)

    if st.button("Reset Weekly"):
        st.session_state["weekly_watch"] = []
        st.success("Weekly cleared")

# ---------------------- LOG TRADE ----------------------
elif page == "Log New Trade":
    clear_bg()
    st.header("Log New Trade")

    with st.form("log_trade"):

        date = st.date_input("Date")

        st.subheader("Screenshots")

        st.file_uploader("D")
        st.text_area("D Note")

        st.file_uploader("4H")
        st.text_area("4H Note")

        st.file_uploader("1H")
        st.text_area("1H Note")

        st.file_uploader("15m")
        st.text_area("15m Note")

        st.file_uploader("5m")
        st.text_area("5m Note")

        risk = st.text_input("Risk")
        entry_time = st.time_input("Entry Time")
        session = st.selectbox("Session", ["London", "New York", "Asia"])
        rr = st.text_input("RR")
        thought = st.text_area("Thought Process")

        submit = st.form_submit_button("Submit")

        if submit:
            st.session_state["last_trade_id"] += 1
            trade_id = st.session_state["last_trade_id"]

            st.success(f"Trade Logged 🎯 ID: {trade_id}")

# ---------------------- CLOSE TRADE ----------------------
elif page == "Close Trade":
    clear_bg()
    st.header("Close Trade")

    trade_id = st.number_input(
        "Trade ID",
        min_value=1,
        value=int(st.session_state["last_trade_id"])
    )

    date = st.date_input("Date")
    result = st.selectbox("Result", ["Win", "Loss", "Break Even"])
    pct = st.number_input("Percentage", value=0.0)

    st.subheader("Screenshots")

    st.file_uploader("D")
    st.text_area("D Note")

    st.file_uploader("4H")
    st.text_area("4H Note")

    st.file_uploader("1H")
    st.text_area("1H Note")

    st.file_uploader("15m")
    st.text_area("15m Note")

    st.file_uploader("5m")
    st.text_area("5m Note")

    duration = st.text_input("Duration")
    thought = st.text_area("Post Analysis")

    if st.button("Close Trade"):
        st.success(f"Trade {trade_id} Closed ✔")

# ---------------------- VIEW TRADE ----------------------
elif page == "View Trade":
    clear_bg()
    st.header("View Trade")

    trade_id = st.number_input(
        "Trade ID",
        min_value=1,
        value=int(st.session_state["last_trade_id"])
    )

    if st.button("Fetch"):
        st.info(f"Showing trade #{trade_id}")