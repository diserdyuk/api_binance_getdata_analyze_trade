Для реализации нужно зарегистрироваться на сайте https://www.binance.com/ и создать апи для тестов 

Нужно реализовать следующий алгоритм торгового робота:
1. Отслеживаем значения Moving average(для 5 минутных свечей, расчитывать на закрытии 9-ти свечей) по валютной паре BTC-USDT.
2. Если значение цены выше МА на заданное число мы продаем заданный обьем ВТС.
3. Если цена ниже МА на заданное число мы покупаем заданный объём ВТС.
4. После того как мы имеем открытую позицию производим закрытие позиции (обратная сделка), когда цена=МА


Реализовать простейший веб интерфейс для отслеживания открытых и закрытых ордеров
Также в интерфейсе должна быть возможность настраивать отклонение от MA(10%, задать отклонение константой) для покупки и продажи и объем(1,задать объем константой) создаваемого ордера


