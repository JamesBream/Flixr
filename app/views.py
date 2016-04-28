# System imports
import re, json
# Third party imports
import bleach, requests
from flask import render_template, redirect, request, session
from flask.ext.mysqldb import MySQL
from werkzeug import generate_password_hash, check_password_hash
from app import application

mysql = MySQL()
mysql.init_app(application)

@application.route('/')
@application.route('/index')
def index():
    if session.get('user'):
        return redirect('/discover')
    return render_template('index.html')


@application.route('/register', methods=['GET', 'POST'])
def register():
    title = "Flixr - Register"
    if request.method == "GET":
        return render_template('register.html',
                                title=title)
    
    elif request.method == "POST":
        try:
            # Request POST values and sanitise input of HTML where necessary
            _firstname = bleach.clean(request.form['inputFirstName'])
            _lastname = bleach.clean(request.form['inputLastName'])
            _email = bleach.clean(request.form['inputEmail'])
            _password = request.form['inputPassword']
            _passconfirm = request.form['inputPassConfirm']

            if _firstname and _lastname and _email and _password and _passconfirm:
                if re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", _email):
                    if _password == _passconfirm:
                        cur = mysql.connection.cursor()

                        # Generate a hash of the password
                        _hashed_password = generate_password_hash(_password)
                        cur.callproc('sp_createUser', (_email, _firstname, _lastname, _hashed_password))

                        rv = cur.fetchall()
                        cur.close()

                        if len(rv) is 0:
                            # Commit changes to database
                            mysql.connection.commit()
                            return render_template('login.html',
                                                    title=title,
                                                    error="Registration success! You may now login.")
                        else:
                            # Return error from db, likely user already exists
                            error = str(rv[0][0]    )
                            return render_template('register.html',
                                                    title=title,
                                                    error=error)
                    else:
                        error = "Passwords do not match."
                        return render_template('register.html',
                                                title=title,
                                                error=error)
                else:
                    error = "Email address is invalid."
                    return render_template('register.html',
                                            title=title,
                                            error=error)
            else:
                error = "Please enter all fields."
                return render_template('register.html',
                                        title=title,
                                        error=error)
        except Exception as e:
            return render_template('register.html',
                                    title=title,
                                    error=str(e))
        

@application.route('/login', methods=['GET', 'POST'])
def login():
    title = "Flixr - Log In"
    error_incorrect = "Sorry, your details were incorrect."
    
    if request.method == "GET":
        return render_template('login.html',
                                title=title)
    
    elif request.method == "POST":
        try:
            _email = request.form['inputEmail']
            _password = request.form['inputPassword']

            cur = mysql.connection.cursor()
            cur.callproc('sp_validateLogin', (_email,))
            rv = cur.fetchall()
            
            # If there's an entry, check password matches stored hash
            if len(rv) > 0:
                if check_password_hash(str(rv[0][4]), _password):
                    
                    #Set session to user id and redirect
                    session['user'] = rv[0][0]
                    return redirect('/discover')
                else:
                    return render_template('login.html',
                                            title=title,
                                            error=error_incorrect)
            else:
                return render_template('login.html',
                                        title=title,
                                        error=error_incorrect)
        except Exception as e:
            return render_template('login.html',
                                    title=title,
                                    error=str(e))


@application.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@application.route('/discover')
def discover():
    if session.get('user'):
        return render_template('home.html',
                                title='Discover')
    else:
        return redirect('/login')


@application.route('/bookmarks')
def bookmarks():
    if session.get('user'):
        return render_template('bookmarks.html',
                                title='Bookmarks')
    else:
        return redirect('/login')


### API ###
@application.route('/getPopularMovies/<int:page>')
def getPopularMovies(page):
    if session.get('user'):
        try:
            # Configure the parameter payload
            payload = {'api_key': application.config['API_KEY'], 'sort_by': 'popularity.desc', 'page': page}
            r = requests.get('https://api.themoviedb.org/3/discover/movie', params=payload)
            data = r.json()

            # Construct new serialised data structure
            base_url = application.config['API_CONFIG']['images']['base_url']
            poster_size = application.config['API_CONFIG']['images']['poster_sizes'][3] #w342
            movies_dict = []
            for i in data['results']:
                movie_dict = {
                    'Id': i['id'],
                    'Title': i['title'],
                    'Overview': i['overview'],
                    'Poster_Path': (base_url + poster_size + i['poster_path'])
                }
                movies_dict.append(movie_dict)

            return json.dumps(movies_dict)
        
        except Exception as e:
            return json.dumps({'error': str(e)})


@application.route('/getMovieDetails/<int:mid>')
def getMovieDetails(mid):
    if session.get('user'):
        try:
            _user = session.get('user')
            # Configure the parameter payload
            payload = {'api_key': application.config['API_KEY']}
            r = requests.get('https://api.themoviedb.org/3/movie/' + str(mid), params=payload)
            data = r.json()
            
            # Query database for a bookmark
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM tbl_bookmark WHERE user_id = %s AND movie_id = %s", (_user, str(mid)))
            rv = cur.fetchall()
            
            if len(rv) > 0:
                existsBookmark = True
            else:
                existsBookmark = False
            
            movie_dict = {
                'Id': data['id'],
                'Title': data['title'],
                'Overview': data['overview'],
                'Rating': data['vote_average'],
                'Release': data['release_date'],
                'ExistsBookmark': existsBookmark
            }
            
            return json.dumps(movie_dict)

        except Exception as e:
            return json.dumps({'error': str(e)})



@application.route('/getBookmarks')
def getBookmarks():
    if session.get('user'):
        #REMEMBER TRY STATEMENT
        _user = session.get('user')
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id, movie_id FROM tbl_bookmark WHERE user_id = %s", (_user,))
        
        rv = cur.fetchall()
        
        bookmarks_dict = []
        if len(rv) > 0:
            base_url = application.config['API_CONFIG']['images']['base_url']
            poster_size = application.config['API_CONFIG']['images']['poster_sizes'][3] #w342
            
            for movie in rv:
                
                # Configure the parameter payload
                payload = {'api_key': application.config['API_KEY']}
                r = requests.get('https://api.themoviedb.org/3/movie/' + str(movie[1]), params=payload)
                data = r.json()
                
                movie_dict = {
                    'Id_User': movie[0],
                    'Id_Movie': movie[1],
                    'Title': data['title'],
                    'Overview': data['overview'],
                    'Poster_Path': (base_url + poster_size + data['poster_path'])
                }
                bookmarks_dict.append(movie_dict)
        return json.dumps(bookmarks_dict) 


@application.route('/bookmark/<int:mid>')
def bookmark(mid):
    if session.get('user'):
        try:
            _user = session.get('user')

            cur = mysql.connection.cursor()
            cur.callproc('sp_toggleBookmark', (_user, mid))

            # Check for MySQL errors
            rv = cur.fetchall()
            cur.close()
            if len(rv) is 0:
                mysql.connection.commit()
                return json.dumps({'success': 'Toggle succeeded!'})
            else:
                return json.dumps({'error': str(rv)})
        except Exception as e:
            return json.dumps({'error': str(e)})