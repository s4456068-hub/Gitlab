"""Банк вопросов: чтение файла и подсчёты.

Этот модуль ничего не печатает. Он возвращает результат, а печатает main.py.
Названия функций и то, что они принимают, менять нельзя: их вызывают
main.py и тесты. Меняй только тела функций — то, что под описанием.

Пока тела не написаны, функции возвращают пустые значения: программа
запускается, но отвечает нулями.
"""

# Э.: начни с одной строки. Разбери её на поля — остальные сорок устроены так же.

TOPICS = ["строки", "числа", "списки", "ошибки"]


def load_bank(path):
    """Прочитать банк из файла по пути path.

    Возвращает два значения: список вопросов и число пропущенных строк.

    Первая строка файла — заголовок, это не вопрос.
    Каждый вопрос в списке — словарь с семью ключами:

        {"id": 23, "topic": "списки", "level": 2, "type": "короткий",
         "text": "Что напечатает код?\\nitems = [3, 1, 2]\\nprint(items[0])",
         "options": [], "answer": "3"}

    - "id" и "level" — числа, остальное — строки;
    - в "text" каждые два символа \\n из файла заменены настоящим переносом строки;
    - "options" — список вариантов; у вопросов типа «короткий» он пустой.

    Задание 1: верни все вопросы файла и 0.
    Задание 4: испорченные строки не попадают в список, их число — второе значение.

    Если файла нет, ошибку здесь не перехватывай: её перехватывает main.py.
    """
    questions = []
    skipped = 0
    with open(path, encoding="utf-8") as file:
        file.readline()
        for line in file:
            if not line.strip():
                skipped += 1
                continue
            fields = line.rstrip("\n").split(";")
            if len(fields) != 7:
                skipped += 1
                continue
            try:
                level = int(fields[2])
            except ValueError:
                skipped += 1
                continue
            if level not in [1, 2, 3, 4, 5]:
                skipped += 1
                continue
            options = []
            if fields[5]:
                options = fields[5].split("|")
            question = {
                "id": int(fields[0]),
                "topic": fields[1],
                "level": level,
                "type": fields[3],
                "text": fields[4].replace("\\n", "\n"),
                "options": options,
                "answer": fields[6]
            }
            questions.append(question)
    return questions, skipped


def find_question(questions, qid):
    """Найти в списке questions вопрос с номером qid (число).

    Возвращает словарь этого вопроса или None, если такого номера нет.
    """
    for question in questions:
        if question["id"] == qid:
            return question
    return None


def question_lines(question):
    """Строки, которые увидит человек на экзамене, — списком.

    Сначала строки текста вопроса, потом варианты: "1) ...", "2) ..." и так далее.
    Тема, уровень и ответ в эти строки не попадают.
    """
    lines = question["text"].split("\n")
    number = 1
    for option in question["options"]:
        lines.append(str(number) + ") " + option)
        number += 1
    return lines


def count_levels(questions):
    """Сколько вопросов на каждом уровне.

    Возвращает словарь {уровень: число}, например {1: 10, 2: 9, ...}.
    """
    counts = {}
    for question in questions:
        level = question["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts


def count_topics(questions):
    """Сколько вопросов в каждой теме.

    Возвращает словарь {тема: число}, например {"строки": 12, ...}.
    """
    counts = {}
    for question in questions:
        topic = question["topic"]
        counts[topic] = counts.get(topic, 0) + 1
    return counts


def count_matrix(questions):
    """Задание 8 (дополнительное). Сколько вопросов каждой темы на каждом уровне.

    Возвращает словарь словарей {тема: {уровень: число}},
    например {"строки": {1: 4, 2: 2, ...}, ...}.
    """
    matrix = {}
    for topic in TOPICS:
        matrix[topic] = {}
        for level in [1, 2, 3, 4, 5]:
            matrix[topic][level] = 0
    for question in questions:
        topic = question["topic"]
        level = question["level"]
        matrix[topic][level] += 1
    return matrix
