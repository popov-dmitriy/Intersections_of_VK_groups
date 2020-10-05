import tkinter as tk
import webbrowser
import vk

path = r"C:\Users\dimon\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"

loc_text1_x = 0.1
loc_text1_y = 0.05
loc_text2_x = 0.55
loc_text2_y = 0.05

loc_pls1_x = 0.075
loc_pls2_x = 0.525


def get_members(groupid, min, max, x):  # Функция формирования базы участников сообщества в виде списка
    try:
        first = vk_api.groups.getMembers(group_id=groupid, v=5.101)  # Первое выполнение метода
    except vk.exceptions.VkAPIError:
        try:
            first = vk_api.groups.getMembers(group_id=groupid[4:], v=5.101)
        except vk.exceptions.VkAPIError:
            return []

    data = first["items"]  # Присваиваем переменной первую тысячу id'шников
    count = first["count"] // 1000  # Присваиваем переменной количество тысяч участников
    # С каждым проходом цикла смещение offset увеличивается на тысячу
    # и еще тысяча id'шников добавляется к нашему списку.
    for i in range(1, count + 1):
        lb = tk.Label(root, text=min + ' of ' + max + ': ' + str(round(i / count * 100, 2)) + '%', bg='cornflower blue',
                      fg='yellow', font='Arial 10')
        lb.place(relx=x, rely=0.01)
        data = data + vk_api.groups.getMembers(group_id=groupid, v=5.101, offset=i * 1000)["items"]
        root.update()
        lb.destroy()
    return data


def save_data(data, filename="data.txt"):  # Функция сохранения базы в txt файле
    with open(filename, "w") as file:  # Открываем файл на запись
        for item in data:
            file.write("vk.com/id" + str(item) + "\n")


def union_members(group1, group2):
    group1 = set(group1)
    group2 = set(group2)
    union = group1.intersection(group2)  # intersection(group2)  # *находим пресечение множеств
    return list(union)


def create_screen(links1, links2):
    lbl1 = tk.Label(root, font='Arial 12', text='Введите первый набор групп:', bg='cornflower blue').place(relx=0.1,
                                                                                                           rely=0.01)
    lbl2 = tk.Label(root, font='Arial 12', text='Введите второй набор групп:', bg='cornflower blue').place(relx=0.55,
                                                                                                           rely=0.01)
    txt1 = tk.Entry(root, width=27, font='Arial 14')
    txt1.place(relx=loc_text1_x, rely=loc_text1_y)
    txt2 = tk.Entry(root, width=27, font='Arial 14')
    txt2.place(relx=loc_text2_x, rely=loc_text2_y)
    links1.append(txt1)
    links2.append(txt2)
    plus_btn1 = tk.Button(root, text='+', width=1, height=1, font='Arial 9', command=lambda: p_but1(plus_btn1, links1))
    plus_btn1.place(relx=loc_pls1_x, rely=loc_text1_y)
    plus_btn2 = tk.Button(root, text='+', width=1, height=1, font='Arial 9', command=lambda: p_but2(plus_btn2, links2))
    plus_btn2.place(relx=loc_pls2_x, rely=loc_text2_y)


def p_but1(btn, links):
    btn.destroy()
    global loc_text1_y
    loc_text1_y += 0.05
    txt = tk.Entry(root, width=27, font='Arial 14')
    txt.place(relx=loc_text1_x, rely=loc_text1_y)
    links.append(txt)
    if len(links) < 11:
        btn = tk.Button(root, text='+', width=1, height=1, font='Arial 9', command=lambda: p_but1(btn, links))
        btn.place(relx=loc_pls1_x, rely=loc_text1_y)


def p_but2(btn, links):
    btn.destroy()
    global loc_text2_y
    loc_text2_y += 0.05
    txt = tk.Entry(root, width=27, font='Arial 14')
    txt.place(relx=loc_text2_x, rely=loc_text2_y)
    links.append(txt)
    if len(links) < 11:
        btn = tk.Button(root, text='+', width=1, height=1, font='Arial 9', command=lambda: p_but2(btn, links))
        btn.place(relx=loc_pls2_x, rely=loc_text2_y)


def union_groups(links1, links2):
    global index
    index = 0
    list_of_links1 = []
    for link in links1:
        list_of_links1.append(link.get())

    list_of_links2 = []
    for link in links2:
        list_of_links2.append(link.get())

    members1 = []
    for i in range(len(list_of_links1)):
        tmp = get_members(list_of_links1[i][15:], str(i + 1), str(len(list_of_links1)), 0.4)
        members1 = set(members1)
        tmp = set(tmp)
        members1.update(tmp)

    members2 = []
    for i in range(len(list_of_links2)):
        tmp = get_members(list_of_links2[i][15:], str(i + 1), str(len(list_of_links2)), 0.85)
        members2 = set(members2)
        tmp = set(tmp)
        members2.update(tmp)
    global intersection_of_groups
    intersection_of_groups = union_members(members1, members2)
    save_data(intersection_of_groups, "intersection_of_groups.txt")  # сохраняем пересечение в файл
    global num_of_people
    num_of_people.destroy()
    num_of_people = tk.Label(root, text='Пересечение аудиторий: ' + str(len(intersection_of_groups)) + ' человек',
                             font='Arial 14', bg='cornflower blue')
    num_of_people.place(relx=.1, rely=0.85)


def open_link(members):
    global index
    if index == len(members):
        return
    try:
        yandex_path = path
        webbrowser.register('yandex', None, webbrowser.BackgroundBrowser(yandex_path))
        webbrowser.get(using='yandex').open('vk.com/id' + str(members[index]))
    except webbrowser.Error:
        webbrowser.open_new(str(members[index]))
    index += 1


def take_browser(browser):
    global path
    path = browser.get()
    if len(path) <= 1:
        path = r"C:\Users\dimon\AppData\Local\Yandex\YandexBrowser\Application\browser.exe"


if __name__ == "__main__":
    token = "*********************************************************************************"  # Сервисный ключ доступа
    session = vk.Session(access_token=token)  # Авторизация
    vk_api = vk.API(session)

    root = tk.Tk()
    root.title("Open links")
    root.geometry("800x600")
    root.resizable(width=False, height=False)
    root["bg"] = 'cornflower blue'

    index = 0
    links1 = []
    links2 = []
    create_screen(links1, links2)
    union_groups_btn = tk.Button(root, text='Объединить наборы групп', width=25, height=2, font='Arial 12',
                                 command=lambda: union_groups(links1, links2), bg='gray85')
    union_groups_btn.place(relx=.1, rely=0.65)
    intersection_of_groups = []
    btn = tk.Button(text="Открыть ссылку на страницу", width=25, height=2, font='Arial 12',
                    command=lambda: open_link(intersection_of_groups), bg='gray85')
    btn.place(relx=.1, rely=0.75)
    num_of_people = tk.Label(root)

    label = tk.Label(root, text='Ввести путь к браузеру:', font='Arial 10', bg='cornflower blue').place(relx=.1,
                                                                                                        rely=0.92)
    browser = tk.Entry(root, width=85)
    browser.place(relx=.3, rely=0.925)
    button = tk.Button(root, text='OK', command=lambda: take_browser(browser)).place(relx=.95, rely=0.92)

    root.mainloop()
