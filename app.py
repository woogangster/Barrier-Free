from flask import Flask, render_template, request, redirect
import os, json

app = Flask(__name__)
DATA_DIR = "pages"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/')
def index():
    pages = [f[:-5] for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    return render_template('index.html', pages=pages)

@app.route('/<title>')
def view_page(title):
    path = os.path.join(DATA_DIR, title + '.json')
    if not os.path.exists(path):
        return render_template('edit.html', title=title, content='')
    with open(path, 'r', encoding='utf-8') as f:
        content = json.load(f)['content']
    return render_template('view.html', title=title, content=content)

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

if __name__ == '__main__':
    app.run(debug=True)
