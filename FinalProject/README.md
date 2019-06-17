# Финальный проект: Маяковский каждый день
### Что
Телеграм-бот **[@Mayakovsky_rhymes](https://web.telegram.org/p=@Mayakovsky_bot)** отвечает на сообщения пользователя "рифмующимися" цитатами из творчества В. В. Маяковского.
Корпус стихотворений был создан на основе поэтического корпуса НКРЯ ([ссылка](http://search.ruscorpora.ru/search.xml?env=alpha&mode=poetic&sort=gr_created_&text=meta&doc_author=%c2.%20%c2.%20%cc%e0%ff%ea%ee%e2%f1%ea%e8%e9))
### Как
Реплики "рифмуются" по ударным гласным с помощью библиотеки [russtress](https://pypi.org/project/russtress/).
### Почему
Почему в кавычках? Маяковский считал, что рифма не должна быть простой ([Источник вдохновения](https://ru.wikisource.org/wiki/%D0%9A%D0%B0%D0%BA_%D0%B4%D0%B5%D0%BB%D0%B0%D1%82%D1%8C_%D1%81%D1%82%D0%B8%D1%85%D0%B8%3F_(%D0%9C%D0%B0%D1%8F%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9))), поэтому ответы бота - это не более чем заготовки для новых, уникальных форм.
### Где
Бот работает на сервере [Heroku](https://app-mayakovsky.herokuapp.com/).
