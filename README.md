Saber Interactive
 
Тестовое задание
1. Слияние логов
Имеется два файла с логами в формате JSONL, пример лога:
…
{"timestamp": "2021-02-26 08:59:20", "log_level": "INFO", "message": "Hello"}
{"timestamp": "2021-02-26 09:01:14", "log_level": "INFO", "message": "Crazy"}
{"timestamp": "2021-02-26 09:03:36", "log_level": "INFO", "message": "World!"}
…
Сообщения в заданных файлах упорядочены по полю timestamp в порядке возрастания.
Требуется написать скрипт, который объединит эти два файла в один.
При этом сообщения в получившемся файле тоже должны быть упорядочены в порядке возрастания по полю 
timestamp.
К заданию прилагается вспомогательный скрипт на python3, который создает два файла "log_a.jsonl" и 
"log_b.jsonl".
Командлайн для запуска: 
log_generator.py <path/to/dir>
Ваше приложение должно поддерживать следующий командлайн:
<your_script>.py <path/to/log1> <path/to/log2> -o <path/to/merged/log>


Log merge
The goal of this project is to create a script that merges two log files into one.

The following technologies are used to implement the service:

Python 3.11
Usage:

$ git clone https://github.com/stanislav-ps/saber
Run the console from the root project folder
Execute the following command: python logs-merge.py <path/to/log1> <path/to/log2> -o <path/to/merged/log>
Example:
python merge_logs.py ./input/log_a.jsonl ./input/log_b.jsonl -o ./output -f
