# 42/Sogrape Hackathon

Table of Contents
- [About](#about)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Acknowledgements](#acknowledgements)

# About

`Hack'a'Wine` is a simple, reliable and easy to use `Data Visualization app` that allows users to filter through wine prices over a range of brands available on several online stores. This implementation was the result of 3 days of work during 42/Sogrape Hackathon 2023.

# Usage

1. Clone repo
```
git clone <repo-url>
```

2. `cd` into the project folder and create a virtual environment
```
python -m venv .venv
```

3. Activate the virtual environment
```
source <env-name>/bin/activate
```

4. Install frontend dependencies
```
pip install -r hack_dashboard/requirements.txt
```

5. Run Streamlit app
```
cd hack_dashboard
streamlit run main.py
```

# Dependencies

- (Streamlit)[https://streamlit.io/]
- (pandas)[https://pandas.pydata.org/docs/]
- (SQLAlchemy)[https://www.sqlalchemy.org/]
- (BeautifulSoup)[https://www.crummy.com/software/BeautifulSoup/]
- (Requests)[https://docs.python-requests.org/en/latest/]

# Acknowledgements 

This code base was developed by Team 1 for Sogrape's Hackathon 2023 at 42 school, by the following members (by 42 student ID):
- passunca
- amenses-
