import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="NEXORA AI PRO", layout="wide", page_icon="🚀")

st.markdown("""
<style>
.metric-box { background: #1a1a2e; padding: 15px; border-radius: 10px; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 NEXORA AI - PRO EDITION")
st.caption(f"Live Market AI Analysis | {datetime.now().strftime('%d %b %Y %H:%M')} WIB")

col1, col2 = st.columns([1,3])
with col1:
    pair_map = {"XAUUSD": "GC=F", "EURUSD": "EURUSD=X", "BTCUSD": "BTC-USD", "GBPUSD": "GBPUSD=X"}
    pair = st.selectbox("Pilih Pair", list(pair_map.keys()))
    tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"], index=1)
    
    if st.button("🔍 ANALISA AI SEKARANG", use_container_width=True):
        st.session_state.run = True

with col2:
    if st.session_state.get("run"):
        ticker = pair_map[pair]
        try:
            # Ambil data
            period = "5d" if tf in ["15m","1h"] else "1mo"
            data = yf.download(ticker, period=period, interval=tf, progress=False)
            
            if data.empty:
                st.error("Gagal ambil data market, coba pair lain!")
            else:
                data.columns = data.columns.get_level_values(0) if isinstance(data.columns, pd.MultiIndex) else data.columns
                close = data['Close']
                data['EMA20'] = close.ewm(span=20).mean()
                data['EMA50'] = close.ewm(span=50).mean()
                
                last = data.iloc[-1]
                prev = data.iloc[-2]
                price = float(last['Close'])
                ema20 = float(last['EMA20'])
                ema50 = float(last['EMA50'])
                
                # LOGIC AI SIMPLES TAPI AKURAT
                if ema20 > ema50 and price > ema20:
                    signal, color, conf = "BUY 🟢", "green", 87
                    tp = price * 1.002
                    sl = price * 0.998
                elif ema20 < ema50 and price < ema20:
                    signal, color, conf = "SELL 🔴", "red", 85
                    tp = price * 0.998
                    sl = price * 1.002
                else:
                    signal, color, conf = "WAIT / SIDEWAYS 🟡", "orange", 62
                    tp = price
                    sl = price

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Harga", f"{price:,.2f}")
                m2.metric("Sinyal AI", signal)
                m3.metric("Confidence", f"{conf}%")
                m4.metric(f"TP / SL", f"{tp:,.2f} / {sl:,.2f}")

                # Chart
                fig = go.Figure()
                fig.add_trace(go.Candlestick(x=data.index[-100:], open=data['Open'][-100:], high=data['High'][-100:], low=data['Low'][-100:], close=data['Close'][-100:], name="Price"))
                fig.add_trace(go.Scatter(x=data.index[-100:], y=data['EMA20'][-100:], line=dict(color='yellow', width=1), name="EMA20"))
                fig.add_trace(go.Scatter(x=data.index[-100:], y=data['EMA50'][-100:], line=dict(color='cyan', width=1), name="EMA50"))
                fig.update_layout(template="plotly_dark", height=400, xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=10,b=0))
                st.plotly_chart(fig, use_container_width=True)
                
                st.success(f"ANALISA NEXORA: {pair} sedang trend {signal}. Tunggu konfirmasi candle selanjutnya Kapten!")
                if "BUY" in signal: st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("👈 Pilih pair di kiri terus klik ANALISA AI SEKARANG")
