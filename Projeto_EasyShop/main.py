from flask import Flask, make_response
from markupsafe import escape   
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cad/usuarios")
def usuarios():
    return render_template('usuarios.html', titulo="Cadastro de Usuarios")

@app.route("/cad/anuncios")
def anuncios():
    return render_template('anuncios.html', titulo="Cadastro de Anúncios" )

@app.route("/cad/produtos")
def produtos():
    return render_template('produtos.html', titulo="Cadastro de Produtos" )

@app.route("/anuncios/perguntas")
def anun_perguntas():
    return render_template('anun_perguntas.html')

@app.route("/anuncios/respostas")
def anun_respostas():
    return render_template('anun_respostas.html')

@app.route("/anuncios/compra")
def anun_compra():
    print ("anuncio comprado")
    return "<h2> Anuncio comprado <h2>"

@app.route("/anuncios/favoritos")
def anun_favor():
    print('favorito inserido')
    return "<h2> Favorito Inserido <h2>"

@app.route("/rel/vendas")
def rel_vendas():
    return render_template('rel_vendas.html')

@app.route("/rel/compras")
def rel_compras():
    return render_template('rel_compras.html')

@app.route("/config/categorias")
def config_categ():
    return render_template('config_categ.html')



