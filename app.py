from flask import Flask, render_template, request, redirect
import os
import json

app = Flask(__name__)

DATA_DIR = 'data'
DIARY_DIR = 'diary'
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DIARY_DIR, exist_ok=True)

# HOME
@app.route('/')
def home():
    return render_template('home.html')

# Wiki Main Page (문서 목록)
@app.route('/wiki')
def index():
    pages = [f[:-5] for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    return render_template('index.html', pages=pages)

# View Page (문서 보기)
@app.route('/<title>')
def view_page(title):
    path = os.path.join(DATA_DIR, title + '.json')
    if not os.path.exists(path):
        return render_template('edit.html', title=title, content='')
    with open(path, 'r', encoding='utf-8') as f:
        content = json.load(f)['content']
    return render_template('view.html', title=title, content=content)

# Edit Page (문서 편집)
@app.route('/edit/<title>', methods=['GET', 'POST'])
def edit_page(title):
    path = os.path.join(DATA_DIR, title + '.json')
    if request.method == 'POST':
        content = request.form['content']
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'content': content}, f)
        return redirect(f'/{title}')
    else:
        content = ''
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = json.load(f)['content']
        return render_template('edit.html', title=title, content=content)

# Travel Diary Page (여행일지)
@app.route('/diary', methods=['GET', 'POST'])
def diary():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        diary_entry = {'title': title, 'content': content}
        entry_id = len(os.listdir(DIARY_DIR)) + 1
        with open(os.path.join(DIARY_DIR, f'{entry_id}.json'), 'w', encoding='utf-8') as f:
            json.dump(diary_entry, f, ensure_ascii=False)
        return redirect('/diary')

    posts = []
    for filename in sorted(os.listdir(DIARY_DIR)):
        with open(os.path.join(DIARY_DIR, filename), 'r', encoding='utf-8') as f:
            posts.append(json.load(f))

    return render_template('diary.html', posts=posts)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
