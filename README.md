**Market Analysis and Intraday Stock Price Prediction Framework**

This study presents a data-driven market analysis framework for equities listed on the National Stock Exchange (NSE) of India, designed to support intraday close price prediction using machine learning and deep learning methodologies. The system integrates financial data acquisition, feature engineering, and predictive modeling within a unified analytical pipeline.

Market data is retrieved programmatically using the `yFinance` API, enabling extraction of historical and intraday OHLCV (Open, High, Low, Close, Volume) information for selected NSE-listed securities. The dataset is further enriched to capture temporal price dynamics and market behavior.

For predictive modeling, multiple learning approaches are employed, including five conventional machine learning algorithms alongside a deep learning architecture for sequence modeling of time-series data. These models are trained on engineered feature sets to learn nonlinear relationships between historical market variables and subsequent intraday closing prices.

Model performance is evaluated using standard regression metrics, allowing comparative analysis of predictive accuracy and generalization capability across different algorithms. The framework emphasizes robustness in short-term financial forecasting and provides a systematic approach for assessing model effectiveness in volatile intraday market conditions.

The proposed system demonstrates the applicability of hybrid machine learning pipelines in financial time-series prediction, combining statistical feature engineering with both classical and deep learning-based predictive techniques.

Tech Stack:
1. Frontend / UI: Streamlit (interactive dashboard for visualization and user interaction)
2. Data Source: yFinance API (for NSE stock market data retrieval)
3. Backend / Processing: Python (data preprocessing, feature engineering, model training, and prediction pipeline)
4. Machine Learning & Deep Learning: Scikit-learn, TensorFlow / Keras (for regression models and sequence-based prediction models)
5. Data Handling & Analysis: Pandas, NumPy
6. Visualization: Plotly / Matplotlib (for charts and market trend visualization)

Project Setup Guide:

1. Clone the Repository : git clone https://github.com/sayanwita7/StockPricePredictionIntraday
2. Navigate to the folder: cd StockPricePredictionIntraday
3. Create a virtual environment: python -m venv venv 
4. Activate the virtual environment: venv\Scripts\activate # On Windows source venv/bin/activate # On Mac/Linux
5. Install dependencies: pip install -r requirements.txt
6. Run the streamlit app: streamlit run index.py