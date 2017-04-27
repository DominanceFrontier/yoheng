import MySQLdb

class DBconfig:
    passwd='travelingisfun'
    db='yoheng$default'
    host='yoheng.mysql.pythonanywhere-services.com'

class DBException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return repr(self.message)

def get_user(username):
    conn = MySQLdb.connect(passwd=DBconfig.passwd, db=DBconfig.db, host=DBconfig.host)
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    sqlcmd = f"Select * from User where username='{username}'"
    num_rows = cursor.execute(sqlcmd)

    if num_rows == 0:
        return None

    if (num_rows > 1):
        raise DBException("More than one user found. Contact admin.")

    user = cursor.fetchall()[0]
    conn.close()

    return user

def get_users():
    conn = MySQLdb.connect(passwd=DBconfig.passwd, db=DBconfig.db, host=DBconfig.host)
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    sqlcmd = "Select * from User"
    num_rows = cursor.execute(sqlcmd)
    users = cursor.fetchall()
    conn.close()

    return users

def insert_user(fullname, username, password):
    try:
        sqlcmd = f'''INSERT INTO
User (fullname, username, password)
VALUES ('{fullname}', '{username}', '{password}')
'''
        conn = MySQLdb.connect(passwd=DBconfig.passwd, db=DBconfig.db, host=DBconfig.host)
        cursor = conn.cursor()
        execval = cursor.execute(sqlcmd)
        conn.commit()
    except Exception as e:
        raise DBException(f"Database error: {e}")
    finally:
        conn.close()
    
def insert(*, table, **kwargs):
    try:
        keys_str = ''
        values_str = ''
        for k, v in kwargs.items():
            keys_str += f'{k}, '
            values_str += f"'{v}', "

        keys_str = keys_str[:-2]
        values_str = values_str[:-2]

        sqlcmd = f'''INSERT INTO
{table} ({keys_str})
VALUES ({values_str})
'''
        conn = MySQLdb.connect(passwd=DBconfig.passwd, db=DBconfig.db, host=DBconfig.host)
        cursor = conn.cursor()
        execval = cursor.execute(sqlcmd)
        conn.commit()

        return search(table=table, **kwargs)[0]
    except Exception as e:
        raise DBException(f"Database error: {e}")
    finally:
        conn.close()

def get(*, table):
    try:
        sqlcmd = f'''Select * from {table}'''
        conn = MySQLdb.connect(passwd=DBconfig.passwd, db=DBconfig.db, host=DBconfig.host)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        num_rows = cursor.execute(sqlcmd)
        items = cursor.fetchall()
        return items
    except Exception as e:
        raise DBException(f"Database error: {e}")
    finally:
        conn.close()

def search(*, table, **kwargs):
    try:
        pred_str = ''
        for k, v in kwargs.items():
            pred_str += f'{k}='
            pred_str += f"'{v}' and "

        pred_str = pred_str[:-5]
        sqlcmd = f'''Select * from {table} where {pred_str}'''
        conn = MySQLdb.connect(passwd=DBconfig.passwd, db=DBconfig.db, host=DBconfig.host)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        num_rows = cursor.execute(sqlcmd)
        items = cursor.fetchall()
        return items
    except Exception as e:
        raise DBException(f"Database error: {e}")
    finally:
        conn.close()

def first_match(*, table, **kwargs):
    matches = search(table=table, **kwargs)
    if matches:
        return matches[0]

    return None

def update(*, table, id, **kwargs):
    try:
        update_str = ''
        for k, v in kwargs.items():
            update_str += f'{k}='
            update_str += f"'{v}', "

        update_str = update_str[:-2]

        sqlcmd = f'''UPDATE {table}
SET {update_str}
WHERE id={id}
'''
        conn = MySQLdb.connect(passwd=DBconfig.passwd, db=DBconfig.db, host=DBconfig.host)
        cursor = conn.cursor()
        execval = cursor.execute(sqlcmd)
        conn.commit()

        return search(table=table, **kwargs)[0]
    except Exception as e:
        raise DBException(f"Database error: {e}")
    finally:
        conn.close()

def delete(*, table, **kwargs):
    try:
        pred_str = ''
        for k, v in kwargs.items():
            pred_str += f'{k}='
            pred_str += f"'{v}' and "

        pred_str = pred_str[:-5]
        sqlcmd = f'''DELETE FROM {table} WHERE {pred_str}'''
        conn = MySQLdb.connect(passwd=DBconfig.passwd, db=DBconfig.db, host=DBconfig.host)
        cursor = conn.cursor()
        execval = cursor.execute(sqlcmd)
        conn.commit()
    except Exception as e:
        raise DBException(f"Database error: {e}")
    finally:
        conn.close()

def get_relationship(User1_id, User2_id):
    if User1_id == User2_id:
        return 'Private'
    
    forward = first_match(table='Friend', User1_id=User1_id, User2_id=User2_id)
    reciprocal = first_match(table='Friend', User1_id=User2_id, User2_id=User1_id)
    if forward and reciprocal:
        return 'Friends'
    elif forward:
        return 'Followers'

    return 'Public'

def filter_articles_with_perm(articles, perm_category):
    perm = first_match(table='Perm', category=perm_category)
    if not perm:
        return articles

    Perm_id = perm['id']
    filtered = []
    for article in articles:
        Article_id = article['id']
        permitted = first_match(table='Article_Perm',
                                Article_id=Article_id,
                                Perm_id=Perm_id)
        if permitted:
            filtered.append(article)

    return filtered

def filter_articles_with_tag(articles, tag_line):
    tag = first_match(table='Tag', line=tag_line)
    if not tag:
        return articles

    Tag_id = tag['id']
    filtered = []
    for article in articles:
        Article_id = article['id']
        tagged = first_match(table='Article_Tag',
                             Article_id=Article_id,
                             Tag_id=Tag_id)
        if tagged:
            filtered.append(article)

    return filtered

def filter_articles_with_dest(articles, dest_title):
    dest = first_match(table='TravelDest', title=dest_title)
    if not dest:
        return articles

    Dest_id = dest['id']
    filtered = []
    for article in articles:
        Article_id = article['id']
        destined = first_match(table='Article_TravelDest',
                               Article_id=Article_id,
                               TravelDest_id=Dest_id)
        if destined:
            filtered.append(article)

    return filtered

def get_articles_with_perm(perm_category):
    perm = first_match(table='Perm', category=perm_category)
    if not perm:
        return []

    Perm_id = perm['id']
    article_perms = search(table='Article_Perm',
                           Perm_id=Perm_id)
    permitted_articles = []
    for article_perm in article_perms:
        article = first_match(table='Article',
                              id=article_perm['Article_id'])
        if article:
            permitted_articles.append(article)

    return permitted_articles

def get_articles_with_tag(tag_line):
    tag = first_match(table='Tag', line=tag_line)
    if not tag:
        return []
    
    Tag_id = tag['id']
    article_tags = search(table='Article_Tag',
                          Tag_id=Tag_id)
    tagged_articles = []
    for article_tag in article_tags:
        article = first_match(table='Article',
                              id=article_tag['Article_id'])
        if article:
            tagged_articles.append(article)

    return tagged_articles    

def get_articles_with_dest(dest_title):
    dest = first_match(table='TravelDest', title=dest_title)
    if not dest:
        return []

    Dest_id = dest['id']
    article_dests = search(table='Article_TravelDest',
                           TravelDest_id=Dest_id)
    dest_articles = []
    for article_dest in article_dests:
        article = first_match(table='Article',
                              id=article_dest['Article_id'])
        if article:
            dest_articles.append(article)

    return dest_articles    

