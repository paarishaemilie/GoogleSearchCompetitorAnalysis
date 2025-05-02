# GoogleSearchCompetitorAnalysis
A Flask web app that fetches top Google search results for a user-defined keyword, extracts content from the articles, and performs NLP-driven keyword analysis using spaCy and Newspaper3k. The app provides rich summaries including top keywords, bigrams, and metadata like word counts, media presence, and heading structure. 

## 🔍 Features

- 🔎 Search top Google results for a user-defined keyword
- 🧠 Extract article text, headings, meta info, images, and videos
- 🧮 Analyze keywords and 2-word phrases using spaCy
- 📊 Display clean summaries with word/character/media stats
- 📋 Visual table output of valid articles (500+ words only)
- 🖼 Responsive UI with loading animation and enhanced UX
- 🧾 Keyword and bigram summaries shown before article results

## 📦 Installation

### Clone the Repository

```bash
git clone https://github.com/paarishaemilie/GoogleSearchCompetitorAnalysis.git
cd GoogleSearchCompetitorAnalysis
```

### Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Run the App
```bash
python app.py
```

### Then open your browser at:
```bash
👉 http://localhost:5000
```

## 🗂 Project Structure
```
GoogleSearchCompetitorAnalysis/
├── app.py               # Flask application logic
├── templates/
│   └── index.html       # Frontend HTML with Bootstrap styling
├── requirements.txt     # Python package list
└── README.md            # Project documentation
```


## 📚 Dependencies
- Flask
- spaCy
- newspaper3k
- beautifulsoup4
- tabulate
- googlesearch-python

## 👤 Author
Built with ❤️ by @paarishaemilie
