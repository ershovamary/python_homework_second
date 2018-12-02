from flask import Flask
from flask import url_for, render_template, request, redirect
import json, csv
import matplotlib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/results')
def show_results():
    if request.args:
        lang = request.args['lang'].lower()
        values = []
        table_head = "<th>Язык</th>"
        table_body = ""
        for i in range(8):
            x = True if 'word' + str(i+1) in request.args else False
            values.append(x)
        if len(set(values)) == 1:  ## Проверяю, чтобы выводились все ответы, даже когда ни один чекбокс не отмечен
            values = [True for j in range(8)]
        for x in range(8):
            if values[x]:
                table_head += "<th>Простр. показатель " + str(x+1) + "</th>\n"
        print(table_head)
        with open("data.csv", "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for rows in reader:
                if lang == '' or rows[0] == lang:
                    table_body += "<td>" + rows[0] + "</td>\n"
                    print(table_body)
                    for y in range(8):
                        if values[y]:
                            table_body += "<td>" + rows[y+1] + "</td>\n"
                    print(table_body)
        table_head = "<tr>" + table_head + "</tr>"
        table_body = "<tr>" + table_body + "</tr>"
    return render_template("results.html", table_head = table_head, table_body = table_body)

@app.route('/thanks')
def say_thanks():
    if request.args:
        data = []
        lang = request.args['lang'].lower()
        data.append(lang)
        for i in range(8):
            word = request.args['word' + str(i + 1)].lower()
            data.append(word)
        with open("data.csv", "a+", encoding="utf-8") as f:
            f.write(';'.join(data) + "\n")
    return render_template("thanks.html")

@app.route('/json')
def make_json():
    with open("data.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        mylist = []
        for rows in reader:
            l = [rows[i+1] for i in range(8)]
            mylist.append({rows[0]:l})
    data = json.dumps(mylist, ensure_ascii = False, indent = 4)
    return render_template("json.html", data = data)

@app.route('/stats')
def make_stats():
    return render_template("stats.html")

if __name__ == '__main__':
    app.run(debug=False)