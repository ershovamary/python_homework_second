import urllib.request
import time
import re
import html


def download_page(pageUrl):
    page = urllib.request.urlopen(pageUrl)
    text = page.read().decode('windows-1251')
    return text
    # do something with the downloaded text

commonUrl = 'http://search.ruscorpora.ru/search.xml?env=alpha&mode=poetic&expand=full&sid=0&docid='
for i in range(52465, 53099):
    pageUrl = commonUrl + str(i)
    result = download_page(pageUrl)
    if isinstance(result, str):
        html_content = result
    else:
        continue
    regTag = re.compile('<.*?>', re.DOTALL)  # это рег. выражение находит все тэги
    regTitle = re.compile('<span class="doc">(.*?)</span>', re.DOTALL)  # это рег. выражение находит название
    regText = re.compile('<li>(.*?)</li>', re.DOTALL)  # это рег. выражение находит текст
    regScript = re.compile('<script>.*?</script>', re.DOTALL) # все скрипты
    regComment = re.compile('<!--.*?-->', re.DOTALL)  # все комментарии
    regAlso = re.compile('\[омонимия не снята\]', re.DOTALL)
    regAccent = re.compile('&#768;', re.DOTALL)
    regBar = re.compile('&#8213;', re.DOTALL)
    regBr = re.compile('<br>', re.DOTALL)
    title = regTitle.search(html_content).group(0)
    title = regTag.sub("", title)
    text = regText.findall(html_content)[0]
    # а дальше заменяем ненужные куски на пустую строку
    clean_t = regScript.sub("", text)
    clean_t = regComment.sub("", clean_t)
    clean_t = regBr.sub("\n", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t = regAccent.sub("\'", clean_t)
    clean_t = regBar.sub("―", clean_t)
    clean_t = regAlso.sub("", clean_t)
    clean_t = html.unescape(clean_t)
    with open("Mayakovsky.csv", "a", encoding="utf-8") as f:
        f.write(title + "\t" + clean_t + "\n\n")
    time.sleep(2)