import streamlit as st
from decision import analyze_text

st.set_page_config(page_title="Anti-India Campaign Detector", layout="centered")
st.title("Anti-India Campaign Detector (Demo)")

st.markdown("Paste a tweet/post/news text and click **Analyze**.")

text = st.text_area("Text to analyze", height=150)

if st.button("Analyze"):
    if not text.strip():
        st.warning("Please paste some text first.")
    else:
        res = analyze_text(text)
        st.subheader("Result")
        st.write("**Suspicious?**", "🔴 Yes" if res['suspicious'] else "🟢 No")
        st.write("**Confidence:**", res['confidence'])
        st.write("**Fake/Anti-India probability (model):**", round(res['fake_prob'], 3))
        st.write("**Sentiment:**", res['sentiment'], round(res['sentiment_score'], 3))
        st.write("**Keywords found:**", res['keywords'])
        st.write("---")
        st.write("Cleaned text (used by classifier):")
        st.code(res['cleaned'])
