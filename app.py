"""
╔══════════════════════════════════════════════════════════╗
║         CryptoDesk Pro — Streamlit + CCXT Edition        ║
║   إدارة صفقات الكريبتو مع ربط Binance اللحظي            ║
╚══════════════════════════════════════════════════════════╝
"""

import streamlit as st
import ccxt
import pandas as pd
import time
import json
from datetime import datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG  (أول سطر دائماً)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CryptoDesk Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — Dark Military Terminal Aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Tajawal:wght@300;400;700;900&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    background-color: #070b10 !important;
    color: #c9d8e8 !important;
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
}

/* ── Streamlit Chrome ── */
.stApp { background: #070b10; }
header[data-testid="stHeader"] { background: #070b10; border-bottom: 1px solid #1a2d45; }
section[data-testid="stSidebar"] {
    background: #0a1018 !important;
    border-left: 1px solid #1a2d45;
}
section[data-testid="stSidebar"] > div { padding-top: 1rem; }

/* ── Cards ── */
.trade-card {
    background: #0d1520;
    border: 1px solid #1a2d45;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
}
.trade-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff44, transparent);
}
.trade-card.alert-sl::before  { background: linear-gradient(90deg, transparent, #ff3d5a99, transparent); }
.trade-card.alert-t1::before  { background: linear-gradient(90deg, transparent, #ffd70099, transparent); }
.trade-card.alert-t2::before  { background: linear-gradient(90deg, transparent, #00ff8899, transparent); }

/* ── Metric Boxes ── */
.metric-box {
    background: #0d1520;
    border: 1px solid #1a2d45;
    border-radius: 8px;
    padding: 14px 16px;
    text-align: center;
}
.metric-label {
    font-size: 10px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #5a7a96;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'Share Tech Mono', monospace;
    font-size: 22px;
    font-weight: 700;
    color: #00d4ff;
}
.metric-value.green { color: #00ff88; }
.metric-value.red   { color: #ff3d5a; }
.metric-value.yellow{ color: #ffd700; }

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 4px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    font-weight: 700;
}
.badge-green  { background: rgba(0,255,136,0.12); color: #00ff88; border: 1px solid rgba(0,255,136,0.3); }
.badge-red    { background: rgba(255,61,90,0.12);  color: #ff3d5a; border: 1px solid rgba(255,61,90,0.3); }
.badge-yellow { background: rgba(255,215,0,0.12);  color: #ffd700; border: 1px solid rgba(255,215,0,0.3); }
.badge-blue   { background: rgba(0,212,255,0.12);  color: #00d4ff; border: 1px solid rgba(0,212,255,0.3); }

/* ── Alert Banners ── */
.alert-banner {
    border-radius: 8px;
    padding: 14px 18px;
    margin: 8px 0;
    display: flex;
    align-items: center;
    gap: 12px;
    animation: fadeIn 0.4s ease;
}
@keyframes fadeIn { from { opacity:0; transform: translateY(-6px); } to { opacity:1; transform: translateY(0); } }
.alert-t1 { background: rgba(255,215,0,0.08); border: 1px solid rgba(255,215,0,0.35); }
.alert-t2 { background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.30); }
.alert-sl { background: rgba(255,61,90,0.10); border: 1px solid rgba(255,61,90,0.35); }
.alert-banner .icon { font-size: 22px; flex-shrink: 0; }
.alert-banner .body { flex: 1; }
.alert-banner .title { font-size: 14px; font-weight: 900; margin-bottom: 2px; }
.alert-sl   .title { color: #ff3d5a; }
.alert-t1   .title { color: #ffd700; }
.alert-t2   .title { color: #00ff88; }
.alert-banner .desc { font-size: 12px; color: #7a9bb5; }

/* ── Progress bar ── */
.prog-track {
    background: #0a1018;
    border: 1px solid #1a2d45;
    border-radius: 4px;
    height: 8px;
    overflow: hidden;
    margin: 6px 0 2px;
}
.prog-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
}

/* ── Streamlit widgets overrides ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: #0a1018 !important;
    border: 1px solid #1a2d45 !important;
    border-radius: 7px !important;
    color: #c9d8e8 !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #00d4ff, #007aaa) !important;
    color: #000 !important;
    font-weight: 900 !important;
    border: none !important;
    border-radius: 7px !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
div[data-testid="stMetric"] {
    background: #0d1520;
    border: 1px solid #1a2d45;
    border-radius: 8px;
    padding: 12px 16px;
}
div[data-testid="stMetricLabel"] { color: #5a7a96 !important; font-size: 11px !important; }
div[data-testid="stMetricValue"] { color: #00d4ff !important; font-family: 'Share Tech Mono', monospace !important; }
.stDataFrame { background: #0d1520 !important; }
.stDataFrame table { color: #c9d8e8 !important; font-family: 'Share Tech Mono', monospace !important; }
.stSlider > div > div > div { background: #00d4ff !important; }
hr { border-color: #1a2d45 !important; }
label { color: #7a9bb5 !important; font-size: 13px !important; }
h1,h2,h3 { color: #c9d8e8 !important; }
.stTabs [data-baseweb="tab"] { color: #5a7a96 !important; }
.stTabs [aria-selected="true"] { color: #00d4ff !important; border-bottom-color: #00d4ff !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
if "trades" not in st.session_state:
    st.session_state.trades = []       # list of dicts
if "equity_history" not in st.session_state:
    st.session_state.equity_history = []
if "total_balance" not in st.session_state:
    st.session_state.total_balance = 1000.0
if "risk_pct" not in st.session_state:
    st.session_state.risk_pct = 10.0

# ─────────────────────────────────────────────
#  BINANCE CLIENT (Public — no keys needed)
# ─────────────────────────────────────────────
@st.cache_resource
def get_exchange():
    return ccxt.binance({"enableRateLimit": True})

exchange = get_exchange()

def fetch_price(symbol: str) -> float | None:
    """جلب السعر الحالي من Binance عبر CCXT."""
    try:
        sym = symbol.upper().replace("USDT", "/USDT")
        if "/" not in sym:
            sym = sym + "/USDT"
        ticker = exchange.fetch_ticker(sym)
        return float(ticker["last"])
    except Exception:
        try:
            # Fallback: raw Binance REST
            import urllib.request, json as _json
            raw = symbol.upper().replace("/", "")
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={raw}"
            with urllib.request.urlopen(url, timeout=4) as r:
                return float(_json.loads(r.read())["price"])
        except Exception:
            return None

# ─────────────────────────────────────────────
#  CALCULATIONS
# ─────────────────────────────────────────────
def calc_trade(entry: float, sl: float, rrr: float, balance: float, risk_pct: float) -> dict:
    """
    حساب كل أهداف الصفقة بناءً على RRR وحجم المركز.
    """
    risk_per_unit   = abs(entry - sl)
    risk_pct_entry  = risk_per_unit / entry * 100          # % مخاطرة من سعر الدخول

    # الهدف الأول = RRR 1:1 (نقطة التعادل الحقيقية)
    target1 = entry + risk_per_unit if entry > sl else entry - risk_per_unit

    # الهدف النهائي بناءً على RRR
    target2 = entry + risk_per_unit * rrr if entry > sl else entry - risk_per_unit * rrr

    # حجم المركز بالدولار
    risk_amount    = balance * (risk_pct / 100)            # $ مخاطرة
    position_usd   = risk_amount / (risk_pct_entry / 100) # $ حجم المركز الكامل
    qty            = position_usd / entry                  # عدد الوحدات

    return {
        "risk_per_unit":  round(risk_per_unit, 6),
        "risk_pct_entry": round(risk_pct_entry, 3),
        "target1":        round(target1, 6),
        "target2":        round(target2, 6),
        "risk_amount":    round(risk_amount, 2),
        "position_usd":   round(position_usd, 2),
        "qty":            round(qty, 6),
    }

def get_pnl(trade: dict, current_price: float) -> dict:
    """حساب P&L وحالة التنبيه لصفقة واحدة."""
    entry     = trade["entry"]
    sl        = trade["sl"]
    t1        = trade["target1"]
    t2        = trade["target2"]
    qty       = trade["qty"]
    side      = trade["side"]   # "long" | "short"

    if side == "long":
        pnl_pct   = (current_price - entry) / entry * 100
        pnl_usd   = (current_price - entry) * qty
        # progress toward t2 (0→1)
        rng       = t2 - entry
        prog      = (current_price - entry) / rng if rng != 0 else 0
        prog      = max(-0.5, min(1.2, prog))  # clip for display
        near_sl   = current_price <= sl * 1.005              # ≤ 0.5% فوق SL
        hit_t1    = current_price >= t1
        hit_t2    = current_price >= t2
    else:  # short
        pnl_pct   = (entry - current_price) / entry * 100
        pnl_usd   = (entry - current_price) * qty
        rng       = entry - t2
        prog      = (entry - current_price) / rng if rng != 0 else 0
        prog      = max(-0.5, min(1.2, prog))
        near_sl   = current_price >= sl * 0.995
        hit_t1    = current_price <= t1
        hit_t2    = current_price <= t2

    status = "open"
    if near_sl:   status = "danger"
    elif hit_t2:  status = "target2"
    elif hit_t1:  status = "target1"

    return {
        "pnl_pct":  round(pnl_pct,  3),
        "pnl_usd":  round(pnl_usd,  2),
        "progress": round(prog,      3),
        "status":   status,
        "near_sl":  near_sl,
        "hit_t1":   hit_t1,
        "hit_t2":   hit_t2,
    }

# ─────────────────────────────────────────────
#  HTML HELPERS
# ─────────────────────────────────────────────
def mono(val, color="#00d4ff", size=16):
    return f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:{size}px;color:{color}">{val}</span>'

def badge(text, kind="blue"):
    return f'<span class="badge badge-{kind}">{text}</span>'

def fmt_price(p):
    if p is None: return "---"
    if p >= 100:  return f"{p:,.2f}"
    if p >= 1:    return f"{p:.4f}"
    return f"{p:.6f}"

def fmt_usd(v):
    sign = "+" if v >= 0 else ""
    return f"{sign}${abs(v):,.2f}"

def progress_bar(pct, color="#00d4ff"):
    w = max(0, min(100, pct * 100))
    return f"""
    <div class="prog-track">
      <div class="prog-fill" style="width:{w:.1f}%;background:{color}"></div>
    </div>
    """

# ─────────────────────────────────────────────
#  SIDEBAR — Portfolio Settings
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:12px 0 20px">
      <div style="font-size:28px">📊</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:18px;
                  background:linear-gradient(90deg,#00d4ff,#00ff88);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  font-weight:700">CryptoDesk Pro</div>
      <div style="font-size:11px;color:#3d5a73;margin-top:4px;letter-spacing:1px">TRADE MANAGER v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 💼 إعدادات المحفظة")
    total_balance = st.number_input(
        "الرصيد الكلي ($)",
        min_value=10.0, max_value=10_000_000.0,
        value=st.session_state.total_balance,
        step=100.0, format="%.2f"
    )
    risk_pct = st.slider(
        "نسبة المخاطرة في الصفقة (%)",
        min_value=0.5, max_value=25.0,
        value=st.session_state.risk_pct,
        step=0.5
    )
    st.session_state.total_balance = total_balance
    st.session_state.risk_pct      = risk_pct

    risk_usd = total_balance * risk_pct / 100
    st.markdown(f"""
    <div class="metric-box" style="margin-top:8px">
      <div class="metric-label">المخاطرة لكل صفقة</div>
      <div class="metric-value yellow">${risk_usd:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ➕ صفقة جديدة")

    with st.form("new_trade_form", clear_on_submit=True):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            symbol = st.text_input("العملة", value="BTC/USDT", placeholder="BTC/USDT").upper().strip()
        with col_s2:
            side   = st.selectbox("الاتجاه", ["Long 📈", "Short 📉"])
        side_key = "long" if "Long" in side else "short"

        entry = st.number_input("سعر الدخول ($)", min_value=0.000001, value=100.0, format="%.6f", step=0.01)
        sl    = st.number_input("وقف الخسارة ($)", min_value=0.000001, value=95.0,  format="%.6f", step=0.01)
        rrr   = st.selectbox("نسبة العائد للمخاطرة (RRR)", [1.5, 2.0, 2.5, 3.0, 4.0, 5.0],
                             index=1, format_func=lambda x: f"1 : {x}")

        submitted = st.form_submit_button("📥 إضافة الصفقة")

    if submitted:
        # Validation
        valid = True
        if side_key == "long"  and sl >= entry:
            st.error("❌ وقف الخسارة يجب أن يكون أقل من سعر الدخول للشراء"); valid = False
        if side_key == "short" and sl <= entry:
            st.error("❌ وقف الخسارة يجب أن يكون أكبر من سعر الدخول للبيع"); valid = False

        if valid:
            with st.spinner("جاري جلب السعر الحالي..."):
                cur = fetch_price(symbol)

            c = calc_trade(entry, sl, rrr, total_balance, risk_pct)
            trade = {
                "id":          int(time.time() * 1000),
                "symbol":      symbol,
                "side":        side_key,
                "entry":       entry,
                "sl":          sl,
                "rrr":         rrr,
                "target1":     c["target1"],
                "target2":     c["target2"],
                "risk_amount": c["risk_amount"],
                "position_usd":c["position_usd"],
                "qty":         c["qty"],
                "risk_pct_entry": c["risk_pct_entry"],
                "current_price": cur,
                "added_at":    datetime.now().strftime("%H:%M:%S"),
                "t1_hit":      False,
                "t2_hit":      False,
            }
            st.session_state.trades.append(trade)
            st.success(f"✅ تمت إضافة صفقة {symbol}")
            st.rerun()

    st.markdown("---")
    # Auto refresh toggle
    auto_refresh = st.checkbox("🔄 تحديث تلقائي (كل 5 ثوانٍ)", value=False)
    if st.button("🔄 تحديث الأسعار الآن"):
        for t in st.session_state.trades:
            p = fetch_price(t["symbol"])
            if p: t["current_price"] = p
        st.rerun()

# ─────────────────────────────────────────────
#  MAIN AREA
# ─────────────────────────────────────────────

# ── Header ──
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;
            border-bottom:1px solid #1a2d45;padding-bottom:16px;margin-bottom:20px">
  <div>
    <h1 style="font-family:'Share Tech Mono',monospace;font-size:24px;margin:0;
               background:linear-gradient(90deg,#00d4ff,#00ff88);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent">
      📡 لوحة إدارة الصفقات
    </h1>
    <div style="font-size:12px;color:#3d5a73;margin-top:4px;letter-spacing:1px">
      LIVE CRYPTO TRADE MANAGER — BINANCE
    </div>
  </div>
  <div style="text-align:left">
    <div id="clock" style="font-family:'Share Tech Mono',monospace;font-size:13px;color:#5a7a96">
""" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Portfolio Summary Metrics ──
trades = st.session_state.trades
total_pnl_usd  = 0.0
total_invested = 0.0
for t in trades:
    cp = t.get("current_price") or t["entry"]
    pnl = get_pnl(t, cp)
    total_pnl_usd  += pnl["pnl_usd"]
    total_invested += t["position_usd"]

equity = total_balance + total_pnl_usd
pnl_color   = "green" if total_pnl_usd >= 0 else "red"
equity_color= "green" if equity >= total_balance else "red"

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("💰 الرصيد الكلي", f"${total_balance:,.2f}")
with m2:
    st.metric("📊 قيمة المحفظة", f"${equity:,.2f}",
              delta=f"{total_pnl_usd:+.2f}$")
with m3:
    st.metric("📈 P&L المفتوح", f"${total_pnl_usd:+,.2f}")
with m4:
    st.metric("🎯 عدد الصفقات", len(trades))

st.markdown("<div style='margin:16px 0'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab_monitor, tab_calc, tab_summary = st.tabs(
    ["📡 المراقبة اللحظية", "🧮 حاسبة الصفقة", "📋 ملخص الصفقات"]
)

# ════════════════════════════════════════════
#  TAB 1 — LIVE MONITORING
# ════════════════════════════════════════════
with tab_monitor:
    if not trades:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#3d5a73">
          <div style="font-size:48px;margin-bottom:16px">📭</div>
          <div style="font-size:16px">لا توجد صفقات مفتوحة</div>
          <div style="font-size:13px;margin-top:8px">أضف صفقتك الأولى من الشريط الجانبي</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for idx, trade in enumerate(trades):
            cp = trade.get("current_price") or trade["entry"]
            pnl = get_pnl(trade, cp)

            # card class
            card_class = "trade-card"
            if pnl["status"] == "danger":  card_class += " alert-sl"
            elif pnl["status"] == "target2": card_class += " alert-t2"
            elif pnl["status"] == "target1": card_class += " alert-t1"

            # colors
            pnl_clr = "#00ff88" if pnl["pnl_usd"] >= 0 else "#ff3d5a"
            side_badge = badge("LONG 📈","green") if trade["side"]=="long" else badge("SHORT 📉","red")

            # progress color
            p = pnl["progress"]
            prog_color = "#ff3d5a" if p < 0 else ("#ffd700" if p < 1 else "#00ff88")

            st.markdown(f"""
            <div class="{card_class}">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px">
                <div style="display:flex;align-items:center;gap:10px">
                  <span style="font-family:'Share Tech Mono',monospace;font-size:18px;
                               color:#00d4ff;font-weight:700">{trade['symbol']}</span>
                  {side_badge}
                  {badge(f"RRR 1:{trade['rrr']}","blue")}
                  <span style="font-size:11px;color:#3d5a73">دخل: {trade['added_at']}</span>
                </div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:22px;
                            font-weight:700;color:{pnl_clr}">
                  {pnl['pnl_pct']:+.2f}%
                  <span style="font-size:14px;color:{pnl_clr}">{fmt_usd(pnl['pnl_usd'])}</span>
                </div>
              </div>

              <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:14px">
                <div style="text-align:center">
                  <div style="font-size:9px;color:#3d5a73;letter-spacing:1px;margin-bottom:4px">السعر الحالي</div>
                  <div style="font-family:'Share Tech Mono',monospace;font-size:15px;color:#00d4ff">
                    ${fmt_price(cp)}
                  </div>
                </div>
                <div style="text-align:center">
                  <div style="font-size:9px;color:#3d5a73;letter-spacing:1px;margin-bottom:4px">سعر الدخول</div>
                  <div style="font-family:'Share Tech Mono',monospace;font-size:15px;color:#c9d8e8">
                    ${fmt_price(trade['entry'])}
                  </div>
                </div>
                <div style="text-align:center">
                  <div style="font-size:9px;color:#ff3d5a;letter-spacing:1px;margin-bottom:4px">وقف الخسارة</div>
                  <div style="font-family:'Share Tech Mono',monospace;font-size:15px;color:#ff3d5a">
                    ${fmt_price(trade['sl'])}
                  </div>
                </div>
                <div style="text-align:center">
                  <div style="font-size:9px;color:#ffd700;letter-spacing:1px;margin-bottom:4px">🎯 هدف 1 (1:1)</div>
                  <div style="font-family:'Share Tech Mono',monospace;font-size:15px;color:#ffd700">
                    ${fmt_price(trade['target1'])}
                  </div>
                </div>
                <div style="text-align:center">
                  <div style="font-size:9px;color:#00ff88;letter-spacing:1px;margin-bottom:4px">🚀 هدف 2 (1:{trade['rrr']})</div>
                  <div style="font-family:'Share Tech Mono',monospace;font-size:15px;color:#00ff88">
                    ${fmt_price(trade['target2'])}
                  </div>
                </div>
              </div>

              <div>
                <div style="display:flex;justify-content:space-between;font-size:10px;color:#3d5a73;margin-bottom:2px">
                  <span>SL ❌</span>
                  <span>الدخول</span>
                  <span>T1 🎯</span>
                  <span>T2 🚀</span>
                </div>
                {progress_bar(p, prog_color)}
                <div style="display:flex;justify-content:space-between;font-size:10px;color:#3d5a73">
                  <span>${fmt_price(trade['sl'])}</span>
                  <span>${fmt_price(trade['entry'])}</span>
                  <span>${fmt_price(trade['target1'])}</span>
                  <span>${fmt_price(trade['target2'])}</span>
                </div>
              </div>

              <div style="display:flex;justify-content:space-between;align-items:center;
                          margin-top:12px;padding-top:10px;border-top:1px solid #1a2d45;flex-wrap:wrap;gap:6px">
                <div style="font-size:12px;color:#5a7a96">
                  📦 حجم المركز: <span style="color:#c9d8e8;font-family:'Share Tech Mono',monospace">
                    ${trade['position_usd']:,.0f}</span> |
                  ⚠️ مخاطرة: <span style="color:#ff6b35;font-family:'Share Tech Mono',monospace">
                    ${trade['risk_amount']:,.2f} ({trade['risk_pct_entry']:.2f}%)</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Alerts ──
            if pnl["status"] == "danger":
                st.markdown(f"""
                <div class="alert-banner alert-sl">
                  <div class="icon">🚨</div>
                  <div class="body">
                    <div class="title">⚠️ خطر! السعر قريب جداً من وقف الخسارة!</div>
                    <div class="desc">السعر الحالي ${fmt_price(cp)} — وقف الخسارة عند ${fmt_price(trade['sl'])} | استعد للإغلاق!</div>
                  </div>
                </div>""", unsafe_allow_html=True)

            elif pnl["status"] == "target2":
                st.markdown(f"""
                <div class="alert-banner alert-t2">
                  <div class="icon">🚀</div>
                  <div class="body">
                    <div class="title">تم بلوغ الهدف النهائي! (RRR 1:{trade['rrr']})</div>
                    <div class="desc">أغلق المركز الكامل وسجّل الربح! P&L: {fmt_usd(pnl['pnl_usd'])}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

            elif pnl["status"] == "target1":
                st.markdown(f"""
                <div class="alert-banner alert-t1">
                  <div class="icon">🎯</div>
                  <div class="body">
                    <div class="title">تم الوصول لـ RRR 1:1 — انقل وقف الخسارة للدخول واسحب 50%!</div>
                    <div class="desc">الهدف الأول ${fmt_price(trade['target1'])} — السعر الحالي ${fmt_price(cp)} | بع نصف العقود الآن!</div>
                  </div>
                </div>""", unsafe_allow_html=True)

            # ── Close button ──
            btn_cols = st.columns([4, 1])
            with btn_cols[1]:
                if st.button(f"❌ إغلاق", key=f"close_{trade['id']}"):
                    st.session_state.trades = [
                        t for t in st.session_state.trades if t["id"] != trade["id"]
                    ]
                    st.rerun()

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════
#  TAB 2 — CALCULATOR (standalone, no position added)
# ════════════════════════════════════════════
with tab_calc:
    st.markdown("### 🧮 حاسبة الصفقة — محاكاة بدون إضافة")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        calc_sym    = st.text_input("رمز العملة", value="ETH/USDT", key="calc_sym").upper()
        calc_entry  = st.number_input("سعر الدخول ($)", value=2500.0, min_value=0.00001,
                                       format="%.6f", key="calc_entry")
        calc_sl     = st.number_input("وقف الخسارة ($)", value=2400.0, min_value=0.00001,
                                       format="%.6f", key="calc_sl")
    with c2:
        calc_rrr    = st.selectbox("RRR", [1.5, 2.0, 2.5, 3.0, 4.0, 5.0],
                                    index=1, format_func=lambda x: f"1 : {x}", key="calc_rrr")
        calc_bal    = st.number_input("رصيد المحاكاة ($)", value=total_balance,
                                       min_value=10.0, format="%.2f", key="calc_bal")
        calc_rsk    = st.slider("نسبة المخاطرة (%)", 0.5, 25.0, risk_pct, 0.5, key="calc_rsk")

    if st.button("⚡ احسب الآن", key="calc_btn"):
        if (calc_entry <= 0 or calc_sl <= 0):
            st.error("القيم يجب أن تكون موجبة")
        else:
            res = calc_trade(calc_entry, calc_sl, calc_rrr, calc_bal, calc_rsk)
            t1  = res["target1"]
            t2  = res["target2"]
            side_calc = "long" if calc_entry > calc_sl else "short"

            st.markdown("---")
            st.markdown("#### 📊 نتائج الحاسبة")

            r1, r2, r3 = st.columns(3)
            with r1:
                st.metric("🎯 الهدف الأول (RRR 1:1)", f"${fmt_price(t1)}",
                          delta=f"{(t1-calc_entry)/calc_entry*100:+.2f}%")
            with r2:
                st.metric(f"🚀 الهدف النهائي (1:{calc_rrr})", f"${fmt_price(t2)}",
                          delta=f"{(t2-calc_entry)/calc_entry*100:+.2f}%")
            with r3:
                st.metric("⚠️ مخاطرة بالدولار", f"${res['risk_amount']:,.2f}")

            r4, r5, r6 = st.columns(3)
            with r4:
                st.metric("📦 حجم المركز ($)", f"${res['position_usd']:,.2f}")
            with r5:
                st.metric("🪙 الكمية", f"{res['qty']:,.6f}")
            with r6:
                st.metric("📉 % مخاطرة من الدخول", f"{res['risk_pct_entry']:.3f}%")

            # Expected P&L table
            st.markdown("#### 💡 سيناريوهات الربح والخسارة")
            scenarios = {
                "❌ وقف الخسارة":        (calc_sl - calc_entry) * res["qty"] if side_calc=="long" else (calc_entry - calc_sl) * res["qty"],
                "⚖️ نقطة التعادل (T1)": (t1 - calc_entry) * res["qty"] if side_calc=="long" else (calc_entry - t1) * res["qty"],
                f"🚀 الهدف النهائي (T2)": (t2 - calc_entry) * res["qty"] if side_calc=="long" else (calc_entry - t2) * res["qty"],
            }
            for label, val in scenarios.items():
                clr = "#00ff88" if val > 0 else "#ff3d5a"
                pct = val / res["position_usd"] * 100
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:10px 16px;background:#0d1520;border:1px solid #1a2d45;
                            border-radius:7px;margin-bottom:6px">
                  <span style="font-size:14px">{label}</span>
                  <span style="font-family:'Share Tech Mono',monospace;font-size:16px;color:{clr};font-weight:700">
                    {fmt_usd(val)} ({pct:+.2f}%)
                  </span>
                </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════
#  TAB 3 — SUMMARY TABLE
# ════════════════════════════════════════════
with tab_summary:
    st.markdown("### 📋 ملخص الصفقات النشطة")

    if not trades:
        st.info("لا توجد صفقات مفتوحة.")
    else:
        rows = []
        for t in trades:
            cp  = t.get("current_price") or t["entry"]
            pnl = get_pnl(t, cp)
            rows.append({
                "العملة":         t["symbol"],
                "الاتجاه":        "Long 📈" if t["side"]=="long" else "Short 📉",
                "سعر الدخول":    f"${fmt_price(t['entry'])}",
                "السعر الحالي":  f"${fmt_price(cp)}",
                "وقف الخسارة":   f"${fmt_price(t['sl'])}",
                "الهدف 1":        f"${fmt_price(t['target1'])}",
                "الهدف 2":        f"${fmt_price(t['target2'])}",
                "RRR":            f"1:{t['rrr']}",
                "P&L ($)":        f"{pnl['pnl_usd']:+.2f}",
                "P&L (%)":        f"{pnl['pnl_pct']:+.2f}%",
                "الحجم ($)":      f"${t['position_usd']:,.0f}",
                "الحالة":         {"open":"🔵 مفتوح","target1":"🎯 T1 بلغ","target2":"🚀 T2 بلغ","danger":"🚨 خطر"}.get(pnl['status'],"—"),
            })

        df = pd.DataFrame(rows)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        # Total row
        total_pnl = sum((get_pnl(t, t.get("current_price") or t["entry"]))["pnl_usd"] for t in trades)
        total_invested_sum = sum(t["position_usd"] for t in trades)
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:16px">
          <div class="metric-box">
            <div class="metric-label">إجمالي المراكز المفتوحة</div>
            <div class="metric-value">${total_invested_sum:,.2f}</div>
          </div>
          <div class="metric-box">
            <div class="metric-label">إجمالي P&L المفتوح</div>
            <div class="metric-value {'green' if total_pnl>=0 else 'red'}">{fmt_usd(total_pnl)}</div>
          </div>
          <div class="metric-box">
            <div class="metric-label">العائد على المحفظة</div>
            <div class="metric-value {'green' if total_pnl>=0 else 'red'}">
              {total_pnl/total_balance*100:+.2f}%
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  AUTO REFRESH
# ─────────────────────────────────────────────
if auto_refresh and trades:
    time.sleep(5)
    for t in st.session_state.trades:
        p = fetch_price(t["symbol"])
        if p:
            t["current_price"] = p
    st.rerun()
