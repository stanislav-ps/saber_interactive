Task_one:  
  
Saber Interactive

Тестовое задание

1. Слияние логов  
Имеется два файла с логами в формате JSONL, пример лога:  
…  
  {"timestamp": "2021-02-26 08:59:20",  "log_level": "INFO", "message": "Hello"}  
  {"timestamp": "2021-02-26 09:01:14", "log_level": "INFO", "message": "Crazy"}  
  {"timestamp": "2021-02-26 09:03:36", "log_level": "INFO", "message": "World!"}  
    …  

Сообщения в заданных файлах упорядочены по полю timestamp в порядке возрастания.  
Требуется написать скрипт, который объединит эти два файла в один.  
При этом сообщения в получившемся файле тоже должны быть упорядочены в порядке возрастания по полю timestamp.

К заданию прилагается вспомогательный скрипт на python3, который создает два файла "log_a.jsonl" и "log_b.jsonl".  
Командлайн для запуска:  
log_generator.py <path/to/dir>    
Ваше приложение должно поддерживать следующий командлайн:  
<your_script>.py <path/to/log1> <path/to/log2> -o <path/to/merged/log>
  
  ***
Task_one_answer:  
Log merge
The goal of this project is to create a script that merges two log files into one.

The following technologies are used to implement the service:

Python 3.10.6
Usage:  

$ git clone https://github.com/stanislav-ps/saber_interactive

Run the console from the root project folder  
Execute the following command: python logs-merge.py <path/to/log1> <path/to/log2> -o <path/to/merged/log>  
Example:  
python merge_logs.py ./input/log_a.jsonl ./input/log_b.jsonl -o ./output -f  

***
Task_two:  
2. Миграция базы данных  
Есть база данных и два типа сервисов А и Б:  
• Сервисы типа А добавляют в базу записи в формате: id, name, status, timestamp.  
• Сервисы типа Б читают эти данные для агрегации и прочих нужд.  

В какой-то момент выясняется, что строковые имена в этих записях занимают слишком много памяти, и при этом
часто повторяются. Поэтому целесообразно вынести их в отдельную табличку.  

В результате данные должны будут добавляться в следующем формате: id, name_id, status, timestamp. Где
name_id внешний ключ к новой таблице с полями: id, name.  

Задача заключается в том, чтобы составить пошаговый план миграции базы и сервисов на новый формат данных, 
при этом не разломав работоспособность системы.  

ВАЖНО:  

1. Нельзя остановить и обновить все сервисы разом (т.е. нельзя остановить сразу все сервисы типа А, либо все 
сервисы типа Б, обновление сервисов происходит по одному за раз).  

2. В базе данных атомарно можно делать только следующие запросы:
 - добавить колонку
 - удалить колонку
 - переименовать колонк
  
  ***
Task_two_answer:  

Рабочую таблицу назовем events, а новая таблица пусть называется names

1. Создать резервную копию БД

2. Создать новую таблицу names

3. Добавить в таблицу names колонку id (Primary Key)

4. Добавить в таблицу names колонку name с ограничением UNIQUE

5. Заполнить колонку name в таблице names уникальными значениями колонки name из таблицы events

6. Добавить в таблицу events колонку name_id без значений по умолчанию

7. Установить на колонку name_id ограничение Foreign Key используя NOT VALID

8. По одному обновить сервисы типа А таким образом, чтобы они начинали писать данные в формате id, name_id, name status, timestamp

9. Применить Foreign Key используя VALIDATE CONSTRAINT к столбцу id из таблицы events

10. Заполнить колонку name_id таблицы events значениями id из таблицы names

11. По одному обновить сервисы типа Б таким образом, чтобы они начинали читать данные из колонки name_id вместо name в таблице events

12. По одному обновить сервисы типа А таким образом, чтобы они перестали писать данные в колнку name из таблицы events

13. Проверить что в коде сервисов А и Б не осталось ссылок на колонку name из таблицы events

14. Проверить что в БД не осталось зависимостей связанных с колонкой name из таблицы events

15. Удалить колонку name из таблицы events
