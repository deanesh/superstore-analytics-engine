
#### Superstore Analytics Engine

Analyze Indian superstore data with python, visualize insights with Streamlit and perform customer segmentation and return prediction.

##### 📁 Folder Structure
```
superstore-analytics-engine/
    README.md
    main.py
    pyproject.toml
    requirements.txt
    uv.lock
    app/
        app.py
        model/
            fetch_data.py
    data/
        indian_superstore_data.xlsx
    notebooks/
        analysis.ipynb
    pipeline/
        pipeline.py
    src/
        analysis.py
        data_loader.py
        plots.py
        preprocess.py
    utils/
        logger.py
```

##### 📝 Features

- Interactive Streamlit dashboard:
  - Shift-wise and overall analysis
  - Regional/State/District/City views
  - Product category and profit dashboards
  - Customer segmentation (RFM)
- Automated pipeline:
  - Data preprocessing
  - RFM segmentation
  - Return prediction (XGBoost)
  - Sales & return visualizations
- Logs stored in `logs/superstore_analytics.log`.

##### 📂 Data

    data/indian_superstore_data.xlsx contains Orders, People, and Returns sheets

##### ⚙️ Setup

```bash
git clone <repo-url>
cd superstore-analytics-engine
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python main.py
streamlit run app/app.py
