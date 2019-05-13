import os.path
from flask import Flask
from flask import url_for, render_template, request, redirect
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()

app = Flask(__name__)


@app.route('/')
def index():
    if request.args:
        sent = request.args["replica"]
        data = modify(sent)
        return render_template('answer.html', data=data)
    return render_template('index.html')


def create_csv():
    with open("1grams.txt", "r", encoding="utf-8") as f1:
        for line in f1.readlines():
            w = line.split()[1]
            par = morph.parse(w)[0]
            for p in par.lexeme:
                with open("my_words.csv", "a", encoding="utf-8") as f2:
                    text = str(p.word) + '\t' + str(p.tag) + '\n'
                    f2.write(text)


def modify(replica):
    answer = ''
    my_words = {}
    with open("my_words.csv", "r", encoding="utf-8") as f3:
        for line in f3.readlines():
            my_words[line.split("\t")[0]] = line.split("\t")[1]
    for word in replica.split():
        p = morph.parse(word)[0]
        for k, v in my_words.items():
            if v == p.tag and k != word:
                if word.islower():
                    answer += k + ' '
                else:
                    answer += k.capitalize() + ' '
                break
    return answer

if __name__ == '__main__':
    if os.path.isfile("my_words.csv"):
        pass
    else:
        create_csv()
    app.run(debug=False)
