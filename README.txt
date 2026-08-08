 
MarketVista is a Streamlit dashboard for exploring public company
financials and comparing market leaders side by side.
 
Search any company or ticker to view its price, key financial
metrics, business summary, custom charts of annual financials,
auto-generated insights (valuation, growth, risk, profitability),
and executive leadership. Or add up to 5 companies to a comparison
view with radar, scatter, and bar charts benchmarking them against
each other.
 
Data is pulled live from Yahoo Finance via the yfinance library.
Charts are built with Plotly, and data is wrangled with pandas.
 
Run it with:
    pip install -r requirements.txt
    streamlit run StockDisplay.py
 
Note: data comes from an unofficial source and may be delayed or
occasionally unavailable. Not financial advice.
 
