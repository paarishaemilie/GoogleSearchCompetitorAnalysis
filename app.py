# app.py
from flask import Flask, render_template, request
import spacy
from googlesearch import search
from newspaper import Article
from bs4 import BeautifulSoup
from collections import Counter
import statistics

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def fetch_google_results(query, buffer=90):
    results = []
    try:
        for url in search(query, num_results=buffer):
            results.append(url)
            if len(results) >= buffer:
                break
    except Exception as e:
        print(f"Error during search: {e}")
    return results

def extract_keywords_spacy(text, top_n=10):
    doc = nlp(text.lower())
    words = [token.text for token in doc if token.is_alpha and not token.is_stop]
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]
    word_freq = Counter(words)
    bigram_freq = Counter(bigrams)
    top_keywords = word_freq.most_common(top_n)
    top_bigrams = bigram_freq.most_common(top_n)
    return top_keywords, [bigram for bigram, _ in top_bigrams]

def analyze_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        soup = BeautifulSoup(article.html, 'html.parser')

        title = soup.title.string if soup.title else "No Title"
        description = soup.find('meta', attrs={'name': 'description'})
        meta_description = description['content'] if description else "No Description"

        num_images = len(soup.find_all('img'))
        num_videos = len(soup.find_all('video'))
        num_words = len(article.text.split())
        if num_words < 500:
            return None

        headings = {
            "h1": len(soup.find_all("h1")),
            "h2": len(soup.find_all("h2")),
            "h3": len(soup.find_all("h3")),
            "h4": len(soup.find_all("h4")),
            "h5": len(soup.find_all("h5")),
            "h6": len(soup.find_all("h6"))
        }

        return {
            'url': url,
            'title': title,
            'meta_description': meta_description,
            'characters': len(article.text),
            'words': num_words,
            'media': num_images + num_videos,
            'headings': headings,
            'text': article.text
        }
    except Exception as e:
        print(f"Skipping URL due to error: {url} ({e})")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        count = int(request.form['count'])
        all_results = fetch_google_results(keyword, buffer=count * 3)

        table_data = []
        all_words, all_bigrams = [], []
        char_list, word_list, media_list = [], [], []
        idx = 1

        for url in all_results:
            stats = analyze_article(url)
            if stats:
                keywords, bigrams = extract_keywords_spacy(stats['text'])
                all_words.extend([word for word, _ in keywords])
                all_bigrams.extend(bigrams)
                char_list.append(stats['characters'])
                word_list.append(stats['words'])
                media_list.append(stats['media'])

                table_data.append({
                    'idx': idx,
                    'url': stats['url'],
                    'title': stats['title'],
                    'meta': stats['meta_description'],
                    'chars': stats['characters'],
                    'words': stats['words'],
                    'media': stats['media'],
                    'keywords': ", ".join([kw for kw, _ in keywords]),
                    'bigrams': ", ".join(bigrams),
                    'headings': ", ".join([f"H{i}: {head_count}" for i, head_count in stats['headings'].items()])
                })
                idx += 1
            if len(table_data) == count:
                break

        if table_data:
            table_data.append({
                'idx': 'AVG',
                'url': '—',
                'title': '—',
                'meta': '—',
                'chars': round(statistics.mean(char_list), 2),
                'words': round(statistics.mean(word_list), 2),
                'media': round(statistics.mean(media_list), 2),
                'keywords': '—',
                'bigrams': '—',
                'headings': '—'
            })

        keyword_summary = Counter(all_words).most_common(10)
        bigram_summary = Counter(all_bigrams).most_common(10)

        return render_template("index.html", results=table_data,
                               keyword_summary=keyword_summary,
                               bigram_summary=bigram_summary,
                               keyword=keyword)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
