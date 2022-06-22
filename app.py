from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'


#Configuração de conexão PostgreSQL
engine = create_engine("postgresql://qyaidplwokxgaf:59be526e18d66accd0441832ab9add1fa1c56fdcf4b586ee14a26bb0f30ddaca@ec2-52-22-136-117.compute-1.amazonaws.com:5432/d99ce040bt6uck")
db = scoped_session(sessionmaker(bind=engine))
app.secret_key = '123456789'
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"


#Função para encontrar ID de postagens individuais
def get_post(post_id):
    conn = db.execute()
    with conn:
        with conn.cursor() as curs:
            curs.execute('SELECT * FROM d99ce040bt6uck.public.posts WHERE post_id = id').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/teste')
def get_geo():
    geo = db.execute('SELECT row_to_json(row(geo, contato, dt)) FROM d99ce040bt6uck.public.geo').fetchall()
    db.close()
    return json

#Página inicial
@app.route('/')
def index():
    exibe = db.execute('SELECT * FROM d99ce040bt6uck.public.retornos').fetchall()
    geo = db.execute('select json_build_array(geo_lat::numeric,geo_long::numeric,id) from posts_geo').fetchall()
    db.close()
    return render_template('index.html', Res=exibe, Geo_pontos=geo)


#Página tipos de contato
@app.route('/db')
def tipo():
    exibe = db.execute('SELECT * FROM d99ce040bt6uck.public.tipos').fetchall()
    return render_template('db.html', tipos=exibe)


#Página de informação do grupo
@app.route('/sobre')
def sobreNos():
    return render_template('sobre.html')


#Página de aprofundamento do tema
@app.route('/aprofundando')
def aprofundando():
    return render_template('aprofundando.html')


#Retorno individual de postagens
@app.route('/<int:id>')
def post():
    post = get_post()
    return render_template('post.html', post=post)


#Criação de postagens
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        contato = request.form.get('contato')
        bairro = request.form.get('bairro')
        geo = request.form.get('geo')
        db.execute("INSERT INTO posts (contato, bairro,geo) VALUES (:contato, :bairro, :geo)" , {"contato": contato, "bairro": bairro, "geo": geo})
        db.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

#geojson
