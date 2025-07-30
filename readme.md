# 📝 Gender Bias Annotation Tool

This is a simple Streamlit app for annotating gender bias predictions.

## 📄 Requirements

Make sure you have a CSV file named `predictions_new.csv` in the root directory.  
Or edit the filename in `app.py` to match your CSV.

The CSV must contain the following columns:
masked_sentence, Expected Gender, Predictions, TOP 1, Top 5, T1 Predicted Gender, T5 Male, T5 Female, T5 Neutral, Wrong, comment, comments



## ⚙️ Setup & Run

Use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install streamlit pandas
```
Then run the app:

On Ubuntu/macOS:
```bash

streamlit run app.py
```
On Windows:
```bash
python -m streamlit run app.py
```

