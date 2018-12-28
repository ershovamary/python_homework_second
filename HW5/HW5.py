import sqlite3
import os
import re
from math import ceil
from flask import Flask
from flask import url_for, render_template, request, redirect

def make_database():
    conn = sqlite3.connect('tamlife.db') # подключаюсь к базе данных
    c = conn.cursor() # инициализирую курсор
    c.execute('CREATE TABLE IF NOT EXISTS '
              'tamlife(head, major text, lemmatised text, '
              'url, author, date, topic)') # создаю БД
    for root, dirs, files in os.walk(".\Tamlife\plain"):
        for name in files:
            filename = os.path.join(root, name)
            with open(filename, 'r', encoding="utf-8") as f:
                lines = f.readlines()
                author = lines.pop(0).lstrip("@au ").rstrip("\n")
                head = lines.pop(0).lstrip("@ti ").rstrip("\n")
                date = lines.pop(0).lstrip("@da ").rstrip("\n")
                topic = lines.pop(0).lstrip("@topic ").rstrip("\n")
                url = lines.pop(0).lstrip("@url ").rstrip("\n")
                text = ''.join(lines).strip()
            new_root = re.sub(r"plain", r"mystem_plain", root)
            with open(os.path.join(new_root, name), 'r', encoding="utf-8") as f:
                lemma_t = f.read().strip()
            c.execute('INSERT INTO tamlife VALUES (?, ?, ?, ?, ?, ?, ?)', 
                      (head, text, lemma_t, url, author, date, topic)) # вставляю строку
    conn.commit() # сохраняю изменения
    conn.close() #закрываю базу

def mystemize(phrase):
    with open("input.txt", "w", encoding="utf-8") as f1:
        f1.write(phrase)
    os.system(''.join([
        'C:\\Users\\ersho\\jupyter_github\\mystem.exe '
        '-c -l -i -d --eng-gr ',
        'input.txt ',
        'output.txt']))
    with open("output.txt", "r", encoding="utf-8") as f2:
        lemmas = f2.read()
    return lemmas

def search(phrase, lemmas):
#    lemmas = re.sub('\{', '\\\{', lemmas)
#    lemmas = re.sub('}', '[^}]*?}', lemmas)
#    lemmas = re.sub('\|', '\\\|', lemmas)
#    print(lemmas)
    answers = {}
    conn = sqlite3.connect('tamlife.db')
    c = conn.cursor()
    for row in c.execute('SELECT head, major text, '
                         'lemmatised text, url FROM tamlife'):
        lemma_str = row[2].splitlines()
        major_str = row[1].splitlines()
        for s in lemma_str:
            match = re.search(lemmas, s)
            if match != None:
                text = major_str[lemma_str.index(s)]
                answers[text] = [row[0], row[3]]
    conn.close()
    return(answers)

class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or                (num > self.page - left_current - 1 and                 num < self.page + right_current) or                num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

app = Flask(__name__)

PER_PAGE = 20

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', defaults={'page': 1})
@app.route('/results/page/<int:page>')
def results(page):
    if request.args:
        print("ok")
        phrase = request.args['phrase']
        content = search(phrase, mystemize(phrase))
        count = len(content)
        if count == 0:
            return render_template('sorry.html')
        if not content and page != 1:
            abort(404)
        pagination = Pagination(page, PER_PAGE, count)
        return render_template('results.html', 
                               pagination = pagination, 
                               content = content)
    return redirect(url_for('index.html'))

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


# In[ ]:


def main():
    if input('Create data base? '
             'Print "create" to do so, '
             'press enter to continue.') == 'create':
        make_database()
    app.run(debug=False)


# In[ ]:


if __name__ == "__main__":
    main()

