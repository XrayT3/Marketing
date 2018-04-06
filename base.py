# -*- coding: utf-8 -*- ?
import sqlite3 as sqlite
import config, const, temp


def give_menu():
    db = sqlite.connect('clientbase.db')
    cur = db.cursor()
    cur.execute("SELECT name FROM categories")
    temp_items = cur.fetchall()
    categories = []
    for item in temp_items:
        categories.append(item[0])
    return categories


def get_all_users():
    db = sqlite.connect('clientbase.db')
    cur = db.cursor()
    sql = "SELECT * FROM users"
    cur.execute(sql)
    return cur.fetchall()


def addInvitation(user_id, invited_user_id):
    db = sqlite.connect('clientbase.db')
    cur = db.cursor()
    sql = "SELECT * FROM INVITATIONS WHERE INVITED= ?"
    cur.execute(sql, (str(invited_user_id),))
    if not cur.fetchone():
        sql = "INSERT INTO INVITATIONS (ID, INVITED) VALUES (?, ?)"
        cur.execute(sql, (str(user_id), str(invited_user_id)))
        db.commit()
        sql = 'UPDATE PARTNERS SET TOTAL = TOTAL + 1 WHERE ID = ?'
        cur.execute(sql, (str(user_id),))
        db.commit()

        sql = 'SELECT ID FROM INVITATIONS WHERE INVITED = ?'
        cur.execute(sql, (str(user_id),))
        initial_user = cur.fetchone()
        if initial_user:
            sql = 'UPDATE PARTNERS SET TOTAL = TOTAL + 1 WHERE ID = ?'
            cur.execute(sql, (str(initial_user),))
            db.commit()


def who_invited(user_id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    sql = "SELECT ID FROM INVITATIONS WHERE INVITED = ?"
    cur.execute(sql, (str(user_id), ))
    id = cur.fetchone()
    if id:
        sql = "SELECT username FROM users WHERE user_id = ?"
        cur.execute(sql, (id[0], ))
        return cur.fetchone()[0]
    return False


def true_pay(username):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    sql = 'SELECT * FROM users WHERE username = ?'
    cur.execute(sql, (username,))
    if cur.fetchone():
        sql = 'UPDATE users SET pay = "TRUE" WHERE username = ?'
        try:
            cur.execute(sql, (username,))
            print('\nadded\n')
            db.commit()
        except Exception as e:
            config.log(Error=e, Text='ADDING_CLIENT')
        return True
    else:
        return False


def false_pay(username):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    sql = 'SELECT * FROM users WHERE username = ?'
    cur.execute(sql, (username,))
    if cur.fetchone():
        sql = 'UPDATE users SET pay = "FALSE" WHERE username = ?'
        try:
            cur.execute(sql, (username,))
            print('\nadded\n')
            db.commit()
        except Exception as e:
            config.log(Error=e, Text='ADDING_CLIENT')
        return True
    else:
        return False


def getValuesPartnership(user_id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    sql = 'SELECT TOTAL FROM PARTNERS WHERE ID = ?'
    cur.execute(sql, (str(user_id),))
    total = cur.fetchone()
    return total[0], user_id


def defineType(item_type):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * id FROM categories WHERE name = ?", (item_type,))
    type1 = cur.fetchone()
    return type1[0]


def type_finder(item_type, city):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    data = item_type+' '+ city
    cur.execute('SELECT id FROM items WHERE ("type" || " " || "city") = (?)', (data,))
    temp_items = cur.fetchall()
    print(temp_items)
    items = []
    for item in temp_items:
        items.append(item_finder(item[0]))
    print(items)
    return items


def item_finder(item_id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = temp.Item()
    item.set_full_data(*cur.fetchone())
    print("\n\n\n")
    print(item.get_data())
    return item


def is_seller(user_id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute('SELECT user_id FROM clients WHERE user_id = (?)', (str(user_id),))
    if cur.fetchone():
        return True
    else:
        return False


def is_admin(id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute('SELECT * FROM admins WHERE id = (?)', (id,))
    if cur.fetchone():
        return True
    else:
        return False


def is_in_base(id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = (?)", (id,))
    if cur.fetchone():
        return True
    else: return False


def real_name(message):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT real_name FROM users WHERE user_id = (?)", (message.from_user.id,))
    #return cur.fetchall()
    if cur.fetchone():
        return cur.fetchall()
    else:
        return ""


def add_user(message):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE user_id = (?)", (message.from_user.id,))
    except Exception as e:
        config.log(Error=e, Text="DBTESTING ERROR")
    if not cur.fetchone():
        try:
            cur.execute("INSERT INTO users (user_id, first_name, last_name, username) VALUES (?,?,?,?)", (
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username))
            cur.execute('INSERT INTO PARTNERS (ID) VALUES (?)', (message.chat.id,))
            config.log(Text="User successfully added",
                       user=str(message.from_user.first_name + " " + message.from_user.last_name))
        except Exception as e:
            config.log(Error=e, Text="USER_ADDING_ERROR")
        db.commit()
    else:
        config.log(Error="IN_THE_BASE_YET",
                   id=message.from_user.id,
                   info=str(message.from_user.last_name) + " " + str(message.from_user.first_name),
                   username=message.from_user.username)


def add_client(message):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    login = message.text[1:]
    try:
        cur.execute("SELECT * FROM clients WHERE user_id = (?)", (message.from_user.id,))
    except Exception as e:
        config.log(Error=e, Text="DBTESTING ERROR")
    if not cur.fetchone():
        try:
            cur.execute("INSERT INTO clients (user_id, name, surname, phone_number) VALUES (?,?,?,?)", (
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
                message.text))
            config.log(Text="Client successfully added",
                       user=str(message.from_user.first_name + " " + message.from_user.last_name))
        except Exception as e:
            config.log(Error=e, Text="CLIENT_ADDING_ERROR")
        db.commit()
    else:
        config.log(Error="IN_THE_BASE_YET",
                   id=message.from_user.id,
                   info=str(message.from_user.last_name) + " " + str(message.from_user.first_name),
                   username=message.from_user.username)


def add_item(item, user):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user.id,))
    print(cur.fetchone())
    if not cur.fetchone():
        try:
            cur.execute("INSERT INTO users "
                        "(user_id, first_name, last_name, username, phone, real_name, city, who, doing) "
                        "VALUES (?,?,?,?,?,?,?,?,?)",
                        (
                            user.id,
                            user.first_name,
                            user.last_name,
                            user.username,
                            item.phone,
                            item.real_name,
                            item.city,
                            item.who,
                            item.doing))
            print('\nadded\n')
            db.commit()
        except Exception as e:
            config.log(Error=e, Text='ADDING_NEW_ITEM_ERROR')


def get_user_step(user_id):
    if user_id in const.user_adding_item_step.keys():
        return const.user_adding_item_step[user_id]
    else:
        return False


def add_item_phone(message, phone):
    new_item = const.new_items_user_adding[message.chat.id]
    new_item.phone = phone


def add_item_name(message):
    new_item = const.new_items_user_adding[message.chat.id]
    new_item.real_name = message.text


def add_item_city(message):
    new_item = const.new_items_user_adding[message.chat.id]
    new_item.city = message.text


def add_item_who(message):
    new_item = const.new_items_user_adding[message.chat.id]
    new_item.who = message.text


def add_item_doing(message):
    new_item = const.new_items_user_adding[message.chat.id]
    new_item.doing = message.text
    add_item(new_item, message.chat)
    new_item.delete()


def find_users_items(user_id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE hash = ?", (str(user_id),))
    result = cur.fetchall()
    return result


def get_all_ids():
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT user_id FROM users")
    result = [id[0] for id in cur.fetchall()]
    cur.execute("SELECT user_id FROM clients")
    for id in cur.fetchall():
        if id[0] not in result:
            result.append(id[0])
    return result


def count_clients():
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT user_id FROM clients")
    return len(cur.fetchall())


def count_users():
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT user_id FROM users")
    return len(cur.fetchall())
