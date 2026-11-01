import streamlit as st
st.set_page_config(page_title="NEXORA AI", layout="wide")
st.title("🚀 NEXORA AI - Trading Signal")
st.success("WEB BERHASIL DEPLOY KAPTEN!")
pair = st.selectbox("Pilih Pair", ["EURUSD", "XAUUSD", "BTCUSD"])
if st.button("ANALISA SEKARANG"):
    st.write(f"### Sinyal untuk {pair}: BUY")
    st.write("Confidence: 85% - Trend Naik Bos!")
    st.balloons()
