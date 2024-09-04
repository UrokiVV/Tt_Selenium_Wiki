# Tt_Selenium.py  03-04.09.2024
from selenium import webdriver
from selenium.webdriver import Keys    # ввод данные на сайт с клавиатуры
from selenium.webdriver.common.by import By  # поиск элементов на сайте
import time

MAX_N_RUN = 35

browser = webdriver.Firefox()
browser.set_window_size(700, 700)

#  стр солнечной системы:
#  url_ini = ("https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D0%BB%D0%BD%D0%B5%D1%87%D0%BD%D0%B0%D1%8FЭ
#             "_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0")
#  title_ini = "Солнечная система"

url_ini = ("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F"
           "_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
title_ini = "Википедия"

url_last = url_ini
m_all_hats = []     # <div class= "hatnote navigation-not-searchable" />
m_all_names = []    # <a - text of link
m_last_url = []     # stack of url
m_last_title = []   # stack of url-title

def get_all_next_pages(url):     # inf для Перехода на след. страницы (all_names, all_hats)
    all_hats = []
    all_names = []
    title = browser.title
    try:
        browser.get(url)
        title = browser.title
    except:
        len_last = len(m_last_url)
        if len_last >= 2:
            m_last_url.pop()
            m_last_title.pop()
            ind_last = len_last-2
            url = m_last_url[ind_last]
            browser.get(url)
            title = browser.title

    for element in browser.find_elements(By.TAG_NAME, "div"):
        try:
            cl = element.get_attribute("class")
            if cl == "hatnote navigation-not-searchable":
                all_hats.append(element)
                a_text = element.find_element(By.TAG_NAME, "a").get_attribute("text")
                all_names.append(a_text)
        except:
            n_len = len(all_hats)

    n_len = len(all_hats)

    dict_result = {
        "names": all_names,
        "hats": all_hats,
        "title": browser.title
    }
    return dict_result

def find_new_page():    # поиск новой страницы  ==> url новой страницы
    text_find = input("\nДля поиска введите наименование статьи:")
    try:
        search_box = browser.find_element(By.ID, "searchInput")
        search_box.send_keys(text_find)
        search_box.send_keys(Keys.RETURN) # введение текста и его отправку
        time.sleep(2)   # надо подумать...
        a = browser.find_element(By.LINK_TEXT, text_find)
        a.click()
        time.sleep(2)  # надо подумать...
        url = browser.current_url
    except:
        print(f"\n Ошибка: страница с названием '{text_find}' не найдена")
        url = None
    dict = {
        "text_find": text_find,
        "url": url
    }
    return dict

def get_last_page(text_dump,  dict):   # Возвращает url_last, title_last
    len_m_last = len(m_last_url)
    if len_m_last >= 2:
        m_last_url.pop()
        m_last_title.pop()
        len_m_last = len(m_last_url) -1
        url_last = m_last_url[len_m_last]
        title_last = m_last_title[len_m_last]
    else:
        url_last = m_last_url[0]  # url_last
        title_last = m_last_title[0]

    dict_result = {
        "url_last": url_last,
        "title_last": title_last
    }
    return dict_result

def get_next_page(n_answer, title_this_page):
    j = n_answer-1   # индекс j в m_all_names
    next_name = m_all_names[j]
    hatnote = m_all_hats[j]
    a_text = hatnote.find_element(By.TAG_NAME, "a").get_attribute("text")
    link = hatnote.find_element(By.TAG_NAME, "a").get_attribute("href")
    # browser.get(link)
    url_next = link
    return url_next

def print_paragraphs():
    print("\n листать параграфы статьи:  Enter")
    print(" Выход из режима листания:  -1 \n")

    all_paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for paragraph in all_paragraphs:
        print(paragraph.text)
        str = input()
        if len(str) >0:
            break

def print_all_names(hat, m_all_names):
    i_name = 0
    for name in m_all_names:
        k_user = i_name+1
        print(f"{k_user}: {m_all_names[i_name]}")
        i_name += 1

def read_user_answer(n_len_in, title):
    n_len = n_len_in
    print(f"\n Текущая стр: {title}")
    print("Вы можете:")
    print("возврат на предыд. статью: -1")
    print("листать параграфы статьи:   0")
    if n_len >0:             # есть вложенные стр:  ---NO ! n_len = len(m_all_names) -1
        max_len = n_len+1    # max номер для пользователя вложенной стр.
        print(f"ввести номер следующей статьи ( 1 - {max_len})")
    print("найти новую статью: 99")
    print(f"закончить работу: 100")
    user_answer = input("Ваш выбор:")
    if user_answer == "":
        n_answer = 100
    else:
        try:
            n_answer = int(user_answer)
        except:
            print(f"*** Ошибка в числе ='{user_answer}' ")
            user_answer = input("Повтерите Ваш выбор: ")
            try:
                n_answer = int(user_answer)
            except:
                n_answer = -1
                print("Снова ошибка! Заканчиваем работу")
        if n_len == 0:
            if not (n_answer -1 or n_answer == 00 or n_answer == 99  or n_answer == 100 ):
                n_answer = 200

        elif n_len >0 and (n_answer > (n_len+1) and n_answer != 99) or n_answer <= -2:
            n_answer = 200
    return n_answer

def get_user_answer(n_len_in, title_last):
    # дает пользователю исправить ошибочный ответ
    n_answr = read_user_answer(n_len_in, title_last)
    if n_answr == 200:
        print("Ошибка. Попробуйте еще раз")
        n_answr = read_user_answer(n_len_in, title_last)
        if n_answr == 200:
            n_answr = 100   # конец работы
    return n_answr


url = url_ini
title = title_ini
m_last_url.append(url)
m_last_title.append(title)
fl_new_found_page = False # Вставить инф о новой найденной стр.
FL_CONSTRUCT_V_10 = True

for i_run in range(MAX_N_RUN):
    # if FL_DUMP:
    #   print(f"\n run step={i_run}")
    #   print_all_names(f"step {i_run}:", m_last_title)
    dict = get_all_next_pages(url)
    m_all_names = dict.get("names")
    m_all_hats = dict.get("hats")
    title = dict.get("title")
    n_len = len(m_all_hats)
    print("\n Просмотренные страницы:")
    print_all_names("last_title :",  m_last_title)
    print("\n Связанные страницы:")
    print_all_names("Next pages:",  m_all_names)

    n_answer = get_user_answer(n_len, title)
    if n_answer == 100:
        break

    if n_answer == -1:  # back: возврат на предыд. стр.
        dict_last = get_last_page("возврат на -1 ", dict)
        url = dict_last.get("url_last")
        browser.get(url)
        title = browser.title
    elif n_answer == 0:
        print_paragraphs()
        url = browser.current_url
    elif n_answer == 99:
        dict_find = find_new_page()
        text_find = dict_find.get("text_find")
        url = dict_find.get("url")
        fl_ok = False
        fl_url_ok = False
        if url != None:
            browser.get(url)
            title = browser.title
            fl_url_ok = True
            fl_ok = title.startswith(text_find)
            if fl_ok:
                m_last_url.append(url)
                m_last_title.append(title)
        if not (fl_ok and fl_url_ok):
            print(f"\n Ошибка: Не найдена страница '{text_find}' ")
            i1 = input(f" Для продолжения нажмите на Enter ")
            n_last = len(m_last_url) -1
            url = m_last_url[n_last]
    else:   # чтение "подчиненной" страницы
        url = get_next_page(n_answer, title)  # переход на новую стр
        if url != None:
            browser.get(url)
            title = browser.title
            m_last_url.append(url)
            m_last_title.append(title)

print("\n Конец работы \n")
browser.close()
