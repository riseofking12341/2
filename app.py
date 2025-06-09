import streamlit as st
from googlenews import GoogleNews
import openai

st.set_page_config(page_title="Smart Nyhetsanalys", layout="centered")
st.title("🔍 Smart Nyhetsanalys för Företag")

openai.api_key = st.secrets["OPENAI_API_KEY"]

def fetch_news(company):
    googlenews = GoogleNews(lang='sv')
    googlenews.search(company)
    results = googlenews.results()
    return results[:3]

def analyze_news(news, company):
    text = f"{news['title']}. {news['desc']}"
    prompt = f"""
    Här är en nyhet relaterad till {company}:

    {text}

    Vad kan detta innebära för {company}?

    Svara med:
    - En kort sammanfattning
    - Hur stor påverkan det kan ha på aktien (liten/medel/stor)
    - Risk för nedgång (1–10)
    - Sannolikhet för uppgång (1–10)
    - Kort förklaring till båda
    - Eventuell påverkan på marknadsvärde eller vinstmarginaler
    """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

company = st.text_input("🔎 Sök företag (ex: Astor Scandinavian Group)", value="Astor Scandinavian Group")

if st.button("Analysera nyheter"):
    with st.spinner("Hämtar nyheter och analyserar..."):
        news_list = fetch_news(company)
        for news in news_list:
            st.subheader(news["title"])
            st.write(news["date"])
            st.write(f"[Länk till nyhet]({news['link']})")
            analysis = analyze_news(news, company)
            st.success(analysis)