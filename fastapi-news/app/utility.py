
import os
from groq import Groq

def generate_summary(news_body):
    # Setting the environment variable for the API key
    os.environ['GROQ_API_KEY'] = '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'
    
    # Instantiate the Groq client without passing the API key directly
    client = Groq()
    
    chat_completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in news summarization in English. Please summarize the following news article in the top 4-6 bullet points in the English language."
            },
            {
                "role": "user",
                "content": news_body
            }
        ],
        temperature=0,
        max_tokens=32768,
        top_p=1,
        stream=False,
        stop=None,
    )
    return chat_completion.choices[0].message.content

# Run Steamlit: python -m streamlit run Home.py
if __name__ == '__main__':
    data = generate_summary('''
                           The prime index of the Dhaka Stock Exchange ended its five-day losing streak as opportunistic investors continued to take positions in sector-specific stocks.
The prime index of the Dhaka Stock Exchange (DSE) increased 11.15 points to settle at 5,145.
The prime index of the DSE broke its five-day losing streak as investors continued taking positions in the sector-specific scrips in anticipation of quick gains, according to the EBL securities.
The blue-chip index DS30, comprising 30 leading companies, increased by 8.61 points to 1,902.88, while the DSES Index, representing Shariah-compliant companies, increased by 4.98 points to 1,155.53 by the close.
Turnover, a crucial indicator of the market, stood at Tk 3.68 billion, up 1.19 per cent from the previous trading day.
The majority of the stocks saw a price increase, as out of the 396 issues traded, 172 closed higher, 160 ended lower, and 64 remained unchanged on the DSE trading floor.
ADN Telecom was the most-traded stock, with shares worth Tk 146.20 million changing hands, followed by Asiatic Laboratories, Taufika Foods and Lovello Ice-cream, Khan Brothers PP Woven Bag Industries and Orion Infusion.
The Chittagong Stock Exchange (CSE) ended up with its All Share Price Index (CASPI) increasing 12.50 points to settle at 14364 and the Selective Categories Index (CSCX) increasing 7 points to settle at 8735.
The port city bourse traded 1.83 million shares and mutual fund units with a turnover volume of Tk 32.68 million.

                  ''')

    print(data)