import streamlit as st
import os, json, uuid, base64
import pandas as pd

# ---------------- STORAGE ----------------
DATA_FILE = "trades.json"
UPLOAD_DIR = "trade_uploads"
LOGO_PATH = "assets/logo.png"
BG_PATH = "assets/background.png"  # ✅ ADDED: Path to your background image

os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_trades():
    if os.path.exists(DATA_FILE):
        return json.load(open(DATA_FILE))
    return {}

def save_trades(data):
    json.dump(data, open(DATA_FILE, "w"), indent=4)

def save_image(file, trade_id, label):
    if file is None:
        return None
    path = os.path.join(UPLOAD_DIR, f"{trade_id}_{label}_{uuid.uuid4().hex}.png")
    with open(path, "wb") as f:
        f.write(file.getbuffer())
    return path

# ---------------- CONFIG ----------------
st.set_page_config("Falcon FX Journal", layout="wide")

# ---------------- SIDEBAR ----------------
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)
else:
    st.sidebar.title("Falcon FX Journal")

st.sidebar.caption("Execute with precision.")

# ---------------- SESSION ----------------
if "last_trade_id" not in st.session_state:
    trades = load_trades()
    st.session_state["last_trade_id"] = int(max(trades.keys(), default=0)) if trades else 0

# ---------------- NAV ----------------
page = st.sidebar.radio("Navigate", [
    "Dashboard",
    "Log Trade",
    "Trade History"
])

# ---------------- STYLE ----------------
# ✅ ADDED: Function to load local image as base64 and set as background
def set_background(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        
        # Apply the background to the main Streamlit app container
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Call the background function
set_background(BG_PATH)

# Original glassmorphism style
st.markdown("""
<style>
.glass {
    background: rgba(255,255,255,0.65);
    padding:20px;
    border-radius:18px;
    margin-bottom:15px;
    backdrop-filter: blur(10px); /* ✅ ADDED: Blur effect to make the glass stand out against your new background */
}
</style>
""", unsafe_allow_html=True)

# ---------------- PAIRS ----------------
PAIRS = [
    "GBP/USD","EUR/USD","GBP/AUD","AUD/USD","NZD/USD",
    "AUD/NZD","GBP/JPY","EUR/JPY","CAD/JPY",
    "AUD/CAD","NZD/CAD","EUR/AUD","EUR/NZD",
    "XAU/USD"
]

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    trades = load_trades()

    total = len(trades)
    wins = len([t for t in trades.values() if t["rr"] > 0])
    losses = len([t for t in trades.values() if t["rr"] < 0])
    breakeven = len([t for t in trades.values() if t["rr"] == 0])

    win_rate = (wins / total * 100) if total > 0 else 0
    avg_rr = (sum([t["rr"] for t in trades.values()]) / total) if total > 0 else 0

    st.markdown('<div class="glass"><h2>🦅 Falcon Forex Journal</h2></div>', unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Trades", total)
    c2.metric("Wins", wins)
    c3.metric("Losses", losses)
    c4.metric("Win Rate", f"{win_rate:.1f}%")
    c5.metric("Avg R:R", f"{avg_rr:.2f}")

# ---------------- LOG TRADE ----------------
elif page == "Log Trade":
    st.header("Log Trade (Complete Entry + Result)")

    pair = st.selectbox("Pair", PAIRS)
    session = st.selectbox("Session", ["London","New York","Asia"])
    risk = st.text_input("Risk %")
    rr = st.text_input("Final R:R")
    result = st.selectbox("Result", ["Win","Loss","Break Even"])

    thought = st.text_area("Thought Process")

    st.markdown("## Before vs After Analysis")

    def timeframe_row(tf):
        st.markdown(f"### {tf}")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Before**")
            b_img = st.file_uploader(f"{tf} Before Image", key=f"b_{tf}")
            if b_img:
                st.image(b_img)
            b_note = st.text_area(f"{tf} Before Note", key=f"bn_{tf}")

        with col2:
            st.markdown("**After**")
            a_img = st.file_uploader(f"{tf} After Image", key=f"a_{tf}")
            if a_img:
                st.image(a_img)
            a_note = st.text_area(f"{tf} After Note", key=f"an_{tf}")

        return {
            "before": {"img": b_img, "note": b_note},
            "after": {"img": a_img, "note": a_note}
        }

    tf_data = {}
    for tf in ["Daily","4H","1H","15m","5m"]:
        tf_data[tf] = timeframe_row(tf)

    def validate(data):
        for tf, d in data.items():
            if d["after"]["img"] is None or not d["after"]["note"]:
                return False
        return True

    if st.button("Save Trade"):
        if not validate(tf_data):
            st.error("⚠️ Complete ALL AFTER images and notes before saving.")
            st.stop()

        trades = load_trades()
        tid = str(st.session_state["last_trade_id"] + 1)
        st.session_state["last_trade_id"] += 1

        structured = {}
        for tf, d in tf_data.items():
            structured[tf] = {
                "before": {
                    "image": save_image(d["before"]["img"], tid, f"{tf}_before"),
                    "note": d["before"]["note"]
                },
                "after": {
                    "image": save_image(d["after"]["img"], tid, f"{tf}_after"),
                    "note": d["after"]["note"]
                }
            }

        try:
            rr_val = float(rr)
        except:
            rr_val = 0

        trades[tid] = {
            "pair": pair,
            "session": session,
            "risk": risk,
            "rr": rr_val,
            "result": result,
            "thought": thought,
            "timeframes": structured
        }

        save_trades(trades)
        st.success(f"Trade #{tid} saved ✅")

# ---------------- TRADE HISTORY ----------------
elif page == "Trade History":
    st.header("Trade History")

    trades = load_trades()
    tid = st.text_input("Enter Trade ID")

    if tid in trades:
        t = trades[tid]

        st.subheader(f"Trade #{tid}")
        st.write(f"Pair: {t.get('pair','N/A')} | Result: {t.get('result')} | RR: {t.get('rr')}")
        st.write(f"Thought: {t.get('thought','')}")

        for tf, d in t["timeframes"].items():
            st.markdown(f"### {tf}")
            c1, c2 = st.columns(2)

            with c1:
                st.write("Before")
                if d["before"]["image"]:
                    st.image(d["before"]["image"])
                st.write(d["before"]["note"])

            with c2:
                st.write("After")
                if d["after"]["image"]:
                    st.image(d["after"]["image"])
                st.write(d["after"]["note"])
