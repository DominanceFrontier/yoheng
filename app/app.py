import random

from functools import wraps
from flask import *

import db

app = Flask(__name__)
app.secret_key = '\xeb\xaeRf\xa7\x8e\xf4u.\x14\x18\xa6\xd0\xd6\xdd<\xe5\xa0\xb1QJ\xcd\x1bU'

PERM_LEVELS = {'Private': 0, 'Friends': 1, 'Followers': 2, 'Public': 3}

def unique(seq, transform=None): 
   if transform is None:
       def transform(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = transform(item)
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user'):
            flash('You must be logged in to view that page.', 'info')
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return wrapper

def validate_json(*expected_args):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            json_object = request.get_json()
            for expected_arg in expected_args:
                if expected_arg not in json_object:
                    abort(400)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def handle_error(error_message):
    flash(str(error_message), 'error')
    return redirect(url_for('login'))

@app.route('/')
@app.route('/index')
def index():
    articles = db.get_articles_with_perm('public')
    articles = random.sample(articles, min(20, len(articles)))
    return render_template('index.djhtml',
                           page_title='Home',
                           articles=articles)

@app.route('/signup')
def signup():
    return render_template('signup.djhtml',
                           page_title='Registration')

@app.route('/search', methods=['GET', 'POST'])
def search():
    tags = db.get(table='Tag')
    destinations = db.get(table='TravelDest')
    articles = {}

    if request.method == 'POST':
        search_text = request.form.get('text')
        if search_text:
            search_param = request.form.get('param')
            if search_param == 'title':
                articles = db.search(table='Article', title=search_text)
            elif search_param == 'author':
                author = db.get_user(search_text)
                if author:
                    articles = db.search(table='Article', User_id=author['id'])
        else:
            articles = db.get(table='Article')

        articles = db.filter_articles_with_perm(articles, 'public')
        articles = db.filter_articles_with_tag(articles, request.form.get('tag'))
        articles = db.filter_articles_with_dest(articles, request.form.get('dest'))

    return render_template('search.djhtml',
                           page_title='Search',
                           tags=tags,
                           destinations=destinations,
                           articles=articles)

@app.route('/confirm-signup', methods=['POST'])
def confirm_signup():
    fullname = request.form.get('fullname').strip()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    cpassword = request.form.get('cpassword').strip()

    if not username:
        return handle_error("Please enter a username.")

    if not password:
        return handle_error("Please enter a password.")

    if password != cpassword:
        return handle_error("Password doesn't match confirmation.")

    try:
        user = db.get_user(username=username)
    except db.DBException as e:
        return handle_error(e.message)

    if user is not None:
        return handle_error("Username already taken. Please try again.")

    try:
        user = db.insert_user(fullname=fullname, username=username, password=password)
    except db.DBException as e:
        return handle_error(e.message)

    flash(f'Thank you, {username}, for signing up. You can now log in.', 'success')
    return render_template('login.djhtml',
                           page_title='Login')

@app.route('/login')
def login():
    return render_template('login.djhtml',
                           page_title='Registration',
                           user='user')

@app.route('/logout')
@authenticated
def logout():
    session.pop('user')
    return redirect(url_for('index'))

@app.route('/users', methods=['GET', 'POST'])
def users():
    users = db.get_users()
    return render_template('users.djhtml',
                           page_title='Yoheng users',
                           users=users)

@app.route('/users/<int:user_id>')
def user(user_id=None):
    user = db.first_match(table='User', id=user_id)

    if session.get('user'):
        user_rel = db.get_relationship(session['user']['id'], user['id'])
    else:
        user_rel = 'Public'
    
    articles = db.search(table='Article', User_id=user['id'])
    permitted_articles = []
    for perm, level in PERM_LEVELS.items():
        if level >= PERM_LEVELS[user_rel]:
            permitted_articles.extend(db.filter_articles_with_perm(articles, perm))
    
    return render_template('user.djhtml',
                           page_title=f"{user['username']}",
                           user=user,
                           user_rel=user_rel,
                           articles=permitted_articles)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    articles = db.get_articles_with_perm('public')
    authors = []
    for article in articles:
        authors.append(db.first_match(table='User', id=article['User_id']))

    return render_template('articles.djhtml',
                           page_title='Yoheng articles',
                           authors=authors,
                           articles=articles)

@app.route('/articles/create/', methods=['GET', 'POST'])
@authenticated
def create_article():
    author = session['user']
    article = {}
    tags = db.get(table='Tag')
    perms = db.get(table='Perm')
    destinations = db.get(table='TravelDest')

    if request.method == 'POST':
        article_data = {
            'title': request.form.get('title'),
            'body': request.form.get('body'),
            'User_id': author['id']
        }
        article = db.insert(table='Article', **article_data)

        tag = db.first_match(table='Tag', id=request.form.get('tag'))
        article_tag = db.insert(table='Article_Tag',
                                Article_id=article['id'],
                                Tag_id=tag['id'])

        perm = db.first_match(table='Perm', id=request.form.get('perm'))
        article_perm = db.insert(table='Article_Perm',
                                 Article_id=article['id'],
                                 Perm_id=perm['id'])

        traveldest = db.first_match(table='TravelDest',
                                    id=request.form.get('TravelDest'))
        article_traveldest = db.insert(table='Article_TravelDest',
                                       Article_id=article['id'],
                                       TravelDest_id=traveldest['id'])

        return redirect(url_for('article', article_id=article['id']))
    
    return render_template('create-article.djhtml',
                           page_title=f"Writing a new story",
                           article=article,
                           author=author,
                           tags=tags,
                           perms=perms,
                           destinations=destinations)

@app.route('/articles/<int:article_id>/update', methods=['GET', 'POST'])
@authenticated
def update_article(article_id):
    user = session['user']
    article = db.first_match(table='Article', id=article_id)
    author = db.first_match(table='User', id=article['User_id'])

    tags = db.get(table='Tag')
    perms = db.get(table='Perm')
    destinations = db.get(table='TravelDest')

    article_tag = db.first_match(table='Article_Tag', Article_id=article_id)
    original_tag = db.first_match(table='Tag', id=article_tag['Tag_id'])
    
    article_perm = db.first_match(table='Article_Perm', Article_id=article_id)
    original_perm = db.first_match(table='Perm', id=article_perm['Perm_id'])
    
    article_traveldest = db.first_match(table='Article_TravelDest', Article_id=article_id)
    original_dest = db.first_match(table='TravelDest', id=article_traveldest['TravelDest_id'])

    if user['id'] != author['id']:
        flash("You don't own that article.", "error")
        return redirect(url_for('profile'))

    if request.method == 'POST':
        if request.form.get('delete'):
            db.delete(table='Article', id=article_id)
            return redirect(url_for('profile'))

        article_data = {
            'title': request.form.get('title'),
            'body': request.form.get('body'),
            'User_id': author['id']
        }
        article = db.update(table='Article', id=article_id, **article_data)

        tag = db.first_match(table='Tag', id=request.form.get('tag'))
        article_tag = db.update(table='Article_Tag',
                                id=article_tag['id'],
                                Article_id=article['id'],
                                Tag_id=tag['id'])

        perm = db.first_match(table='Perm', id=request.form.get('perm'))
        article_perm = db.update(table='Article_Perm',
                                 id=article_perm['id'],
                                 Article_id=article['id'],
                                 Perm_id=perm['id'])

        traveldest = db.first_match(table='TravelDest',
                                    id=request.form.get('TravelDest'))
        article_traveldest = db.update(table='Article_TravelDest',
                                       id=article_traveldest['id'],
                                       Article_id=article['id'],
                                       TravelDest_id=traveldest['id'])

        return redirect(url_for('article', article_id=article['id']))

    return render_template('edit-article.djhtml',
                           page_title=f"Writing a new story",
                           article=article,
                           author=author,
                           tags=tags,
                           perms=perms,
                           destinations=destinations,
                           original_tag=original_tag,
                           original_perm=original_perm,
                           original_dest=original_dest)

    
    
@app.route('/articles/<int:article_id>')
def article(article_id=None):
    article = db.first_match(table='Article', id=article_id)
    author = db.first_match(table='User', id=article['User_id'])

    article_perm = db.first_match(table='Article_Perm', Article_id=article_id)
    if article_perm:
        perm_level = db.first_match(table='Perm', id=article_perm['Perm_id'])
        if perm_level:
            perm_level = perm_level['category']
        else:
            perm_level = 'Private'
    else:
        perm_level = 'Private'

    if session.get('user'):
        user_rel = db.get_relationship(session['user']['id'], author['id'])
    else:
        user_rel = 'Public'
        
    if PERM_LEVELS[perm_level] < PERM_LEVELS[user_rel]:
        flash("You don't have permissions to see this article.", "error")
        return redirect(url_for('articles'))

    article_tag = db.first_match(table='Article_Tag', Article_id=article_id)
    tag = db.first_match(table='Tag', id=article_tag['Tag_id'])

    article_traveldest = db.first_match(table='Article_TravelDest', Article_id=article_id)
    dest = db.first_match(table='TravelDest', id=article_traveldest['TravelDest_id'])

        
    return render_template('article.djhtml',
                           page_title=f"{article['title']}",
                           author=author,
                           article=article,
                           tag=tag,
                           dest=dest)

@app.route('/friends/add/<int:target_id>', methods=['POST'])
@authenticated
def add_friend(target_id):
    try:
        user = session.get('user')
        target = db.first_match(table='User', id=target_id)
        friend = db.insert(table='Friend', User1_id=user['id'], User2_id=target_id)
    except db.DBException as e:
        return handle_error(e.message)

    flash(f"You added {target['username']} as a friend.", 'success')
    return redirect(url_for('user', user_id=target_id))

@app.route('/profile/')
@authenticated
def profile():
    user = session.get('user')
    articles = db.search(table='Article', User_id=user['id'])
    return render_template('user.djhtml',
                           page_title=f"{user['username']}",
                           user=user,
                           articles=articles)

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()

    if not username:
        return handle_error("Please enter a username.")

    if not password:
        return handle_error("Please enter a password.")
    
    try:
        user = db.get_user(username)
    except db.DBException as e:
        return handle_error(e.message)

    if (user['password'] != password):
        return handle_error("Incorrect Password.")

    session['user'] = user
    
    return redirect(url_for('profile'))

@app.route('/about')
def about():
    return render_template('about.djhtml',
                           page_time="About us")

@app.route('/contact')
def contact():
    return render_template('contact.djhtml',
                           page_time="Contact us")

if __name__ == "__main__":
    app.run(debug=True)

