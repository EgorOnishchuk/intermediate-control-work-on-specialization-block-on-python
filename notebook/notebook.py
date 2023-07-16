"""
Предоставляет функциональность для использования текстового файла
в качестве блокнота заметок с возможностью создания, поиска,
изменения и удаления заметки и вывода всех заметок. Передача данных
происходит в формате JSON, а взаимодействие с пользователем - через
терминал.
"""

import datetime
import json

def actions_menu(file):
    """
    Меню действий с заметкой или заметками или выходом из программы.
    Принимает в качестве аргумента путь к файлу, который будет
    использоваться в качестве блокнота заметок. В случае отсутствия в 
    начале файла объекта JSON формата "{'notes': []}" он будет создан, а
    в случае отсутствия файла появится сообщение об ошибке.
    """
    try:
        with open(file, encoding='utf-8') as notebook_file:
            if not notebook_file.read().startswith('{'):
                with open(file, 'w', encoding='utf-8') as notebook_file:
                    json.dump({'notes': []}, notebook_file, indent=4)
    except FileNotFoundError:
        print('Файл отсутствует.')
        return

    actions = {'создание': create_note, 'поиск': search_note,
               'изменение': edit_note, 'удаление': delete_note,
               'вывод': print_notes}

    while True:
        action = get_value("действие: 'создание', 'поиск', 'изменение' " \
                           "и 'удаление' заметки, 'вывод' всех заметок " \
                           "или 'выход' из программы")
        if action in actions:
            actions[action](file)
        elif action == 'выход':
            break
        else:
            print('Действие введено некорректно.')

def create_note(file):
    """
    Создаёт заметку, состоящую из заголовка, содержания и времени
    создания или последнего изменения, если заметка изменялась, которое
    является уникальным идентификатором.
    """
    with open(file, encoding='utf-8') as notebook_file:
        notebook = json.load(notebook_file)

    notebook['notes'].append({'title': get_value('заголовок ' \
                                                 'заметки'),
                              'content': get_value('содержание ' \
                                                   'заметки'),
                              'time': str(datetime.datetime.now())[:19]})

    with open(file, 'w', encoding='utf-8') as notebook_file:
        json.dump(notebook, notebook_file, ensure_ascii=False, indent=4)
        
def search_note(file):
    """
    Выводит все заметки, созданные или изменённые в выбранную дату,
    состоящую из года, года и месяца или года, месяца и дня, или
    информационное сообщение, если по выбранной дате заметки
    отсутствуют.
    """
    with open(file, encoding='utf-8') as notebook_file:
        notebook = json.load(notebook_file)
    date = get_value("дату заметки в форматах 'ГГГГ', 'ГГГГ-ММ' "
                     "или 'ГГГГ-ММ-ДД'")
    is_found = False

    for i in notebook['notes']:
        if i['time'].startswith(date):
            print(f"\n{i['title']}\n{i['content']}")
            is_found = True

    if not is_found:
        print('Заметки отсутствуют.')
    else:
        print()

def edit_note(file):
    """
    Изменяет заметку, созданную или изменённую в выбранное время,
    состоящее из года, месяца, дня, часа, минуты и секунды или выводит
    информационное сообщение, если заметка отсутствует.
    """
    with open(file, encoding='utf-8') as notebook_file:
        notebook = json.load(notebook_file)
    time = get_value("время заметки в формате 'ГГГГ-ММ-ДД ЧЧ:ММ:СС'")
    is_found = False

    for i in notebook['notes']:
        if time == i['time']: 
            i['title'] = get_value('заголовок заметки')
            i['content'] = get_value('содержание заметки')
            i['time'] = str(datetime.datetime.now())[:19]
            is_found = True

    if not is_found:
        print('Заметка отсутствует.')
    else:
        with open(file, 'w', encoding='utf-8') as notebook_file:
            json.dump(notebook, notebook_file, ensure_ascii=False, indent=4)
            
def delete_note(file):
    """
    Удаляет заметку, созданную или изменённую в выбранное время,
    состоящее из года, месяца, дня, часа, минуты и секунды или выводит
    информационное сообщение, если заметка отсутствует.
    """
    with open(file, encoding='utf-8') as notebook_file:
        notebook = json.load(notebook_file)
    time = get_value("время заметки в формате 'ГГГГ-ММ-ДД ЧЧ:ММ:СС'")
    is_found = False

    for i in notebook['notes']:
        if time == i['time']:
            notebook['notes'].remove(i)
            is_found = True

    if not is_found:
        print('Заметка отсутствует.')
    else:
        with open(file, 'w', encoding='utf-8') as notebook_file:
            json.dump(notebook, notebook_file, ensure_ascii=False, indent=4)
            
def print_notes(file):
    """
    Выводит все заметки или информационное сообщение, если заметки
    отсутствуют.
    """
    with open(file, encoding='utf-8') as notebook_file:
        notebook = json.load(notebook_file)

    if not notebook['notes']:
        print('Заметки отсутствуют.')
    else:
        for i in notebook['notes']:
            print(f"\n{i['title']}\n{i['content']}\nВремя - {i['time']}.")
        print()

def get_value(element):
    """Возвращает значение элемента, введённое пользователем."""
    return input(f'Введите {element}. ')