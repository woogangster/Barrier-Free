from flask import Flask, render_template, request, redirect
import os
import json

app = Flask(__name__)

DATA_DIR = 'data'
DIARY_DIR = 'diary'
WIKI_DIR = 'wiki'
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DIARY_DIR, exist_ok=True)
os.makedirs(WIKI_DIR, exist_ok=True)

# HOME
@app.route('/')
def home():
    return render_template('home.html')

# Wiki Main Page (문서 목록)
@app.route('/wiki')
def wiki_index():
    pages = [f[:-5] for f in os.listdir(WIKI_DIR) if f.endswith('.json')]
    return render_template('wiki_index.html', pages=pages)

# View Wiki Page
@app.route('/wiki/<title>')
def view_wiki(title):
    path = os.path.join(WIKI_DIR, f'{title}.json')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = json.load(f)['content']
    else:
        content = ''
    return render_template('wiki_view.html', title=title, content=content)

# Edit Wiki Page
@app.route('/wiki/edit/<title>', methods=['GET', 'POST'])
def edit_wiki(title):
    path = os.path.join(WIKI_DIR, f'{title}.json')
    if request.method == 'POST':
        content = request.form['content']
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'content': content}, f, ensure_ascii=False)
        return redirect(f'/wiki/{title}')
    else:
        content = ''
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = json.load(f)['content']
        return render_template('wiki_edit.html', title=title, content=content)

# 여행일지 목록 보기
@app.route('/diary')
def diary_index():
    entries = [f[:-5] for f in os.listdir(DIARY_DIR) if f.endswith('.json')]
    return render_template('diary_index.html', entries=entries)

# 여행일지 작성하기
@app.route('/diary/new', methods=['GET', 'POST'])
def new_diary():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        path = os.path.join(DIARY_DIR, title + '.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'title': title, 'content': content}, f, ensure_ascii=False)
        return redirect('/diary')
    return render_template('diary_new.html')

# 여행일지 상세 보기
@app.route('/diary/<title>')
def view_diary(title):
    path = os.path.join(DIARY_DIR, title + '.json')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            entry = json.load(f)
        return render_template('diary_view.html', entry=entry)
    return redirect('/diary')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
