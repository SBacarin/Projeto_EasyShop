from flask import Flask, make_response
from markupsafe import escape   
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect

app = Flask(__name__)
## Configurando a ligação com o BD  = 'mysql://USUARIO:SENHA@SERVIDOR:PORTA/DATABASE'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testuser:toledo22@localhost:3306/mydb'

#uso para retirar um warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db = SQLAlchemy(app)


####### MODELS - CLASSES QUE REPRESENTAM AS TABELAS DO BANCO DE DADOS #######
class Usuario(db.Model):
    __tablename__ = "usuario"
    id_usuario = db.Column('id_usuario', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(200)) 
    login = db.Column('login', db.String(50))
    senha = db.Column('senha', db.String(50))
    email = db.Column('email', db.String(150))
    fone = db.Column('fone', db.String(100))
    rua = db.Column('rua', db.String(256))
    numero = db.Column('numero', db.String(20))
    bairro = db.Column('bairro', db.String(80))
    cidade = db.Column('cidade', db.String(100))
    estado = db.Column('estado', db.String(20))
    cep = db.Column('cep', db.String(100))
  
    ## constroe automaticamente um objeto com estes valores
    def __init__(self, nome, login, senha, email, fone, rua, numero, bairro, cidade, estado, cep):
        self.nome = nome
        self.login = login
        self.senha = senha
        self.email = email
        self.fone = fone
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id_anuncio = db.Column('id_anuncio', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(200))  # Nome do Anúncio
    descricao = db.Column('descricao', db.String(500))  # Descrição do Anúncio  
    data = db.Column('data', db.DateTime, nullable=False)  # Data do Anúncio
    quantidade = db.Column('quantidade', db.Integer)   # Quantidade do Anúncio
    valor = db.Column('valor', db.Float) # Valor do Anúncio
    situacao = db.Column('situacao', db.String(45))  # Situação do Anúncio (Ativo, Vendido, Cancelado)
    id_us_prop_anuncio = db.Column('id_us_prop_anuncio', db.ForeignKey('usuario.id_usuario'))
    id_cat = db.Column('id_categoria', db.ForeignKey('categoria.id_categoria'))   
    
    ## constroe automaticamente um objeto com estes valores
    def __init__(self, nome, descricao, data, quantidade, valor, situacao, is_us_prop_anuncio, id_cat):
         self.nome = nome
         self.descricao = descricao
         self.data = data
         self.quantidade = quantidade
         self.valor = valor
         self.situacao = situacao
         self.is_us_prop_anuncio = is_us_prop_anuncio
         self.id_cat = id_cat   

class Perg_resp(db.Model):
    __tablename__ = "perg_resp"
    id_perg_resp = db.Column('id_perg_resp', db.Integer, primary_key=True)
    tipo = db.Column('tipo', db.String(45))  # Pergunta ou Resposta
    data = db.Column('data', db.DateTime, nullable=False)
    descricao = db.Column('descricao', db.String(500))
    id_anuncio = db.Column('id_anuncio', db.ForeignKey('anuncio.id_anuncio'))
    id_usuario = db.Column('id_usuario', db.ForeignKey('usuario.id_usuario'))

    ## constroe automaticamente um objeto com estes valores
    def __init__(self, tipo, data, descricao, id_anuncio, id_usuario):  
        self.tipo = tipo
        self.data = data
        self.descricao = descricao
        self.id_anuncio = id_anuncio
        self.id_usuario = id_usuario

class Categoria(db.Model):
    __tablename__ = "categoria"
    id_categoria = db.Column('id_categoria', db.Integer, primary_key=True)
    descricao = db.Column('descricao', db.String(500))
    
    ## constroe automaticamente um objeto com estes valores
    def __init__(self, descricao):
        self.descricao = descricao

class Anunc_favor(db.Model):   
    __tablename__ = "anunc_favor"
    id_sequencia = db.Column('id_sequencia', db.Integer, primary_key=True)
    id_anuncio_favorito = db.Column('id_anuncio_favorito', db.Integer, nullable=False)
    id_usuario = db.Column('id_usuario', db.ForeignKey('usuario.id_usuario'))

    ## constroe automaticamente um objeto com estes valores
    def __init__(self, data, id_anuncio_favorito, id_usuario):
        self.id_anuncio = id_anuncio
        self.id_usuario = id_usuario   

class Compra(db.Model):
    __tablename__ = "compra"
    id_transacao = db.Column('id_transacao', db.Integer, primary_key=True)
    tipo = db.Column('tipo', db.String(45))  # Compra ou Venda
    data = db.Column('data', db.DateTime, nullable=False)
    valor = db.Column('valor', db.Float)
    nota_fiscal = db.Column('nota_fiscal', db.String(500))
    ###id_produto = db.Column('id_produto', db.ForeignKey('produto.id_produto'))
    id_usuario = db.Column('id_usuario', db.ForeignKey('usuario.id_usuario'))

    ## constroe automaticamente um objeto com estes valores
    def __init__(self, tipo, data, valor, nota_fiscal, id_anuncio, id_usuario): 
        self.tipo = tipo
        self.data = data
        self.valor = valor
        self.nota_fiscal = nota_fiscal
        self.id_anuncio = id_anuncio
        self.id_usuario = id_usuario

class Produto(db.Model):
    __tablename__ = "produto"  
    id_produto = db.Column('id_produto', db.Integer, primary_key=True)  
    descricao = db.Column('descricao', db.String(500))
    valor = db.Column('valor', db.Float)
    qt_estoque = db.Column('qt_estoque', db.Integer)
    ## constroe automaticamente um objeto com estes valores    
    def __init__(self, descricao, valor, qt_estoque):
        self.descricao = descricao
        self.valor = valor
        self.qt_estoque = qt_estoque       


####################### ROTAS #######################
@app.route("/")
def index():
    return render_template('index.html')

####################### USUARIOS #######################
@app.route("/cad/usuarios")
def cadusuario():
    return render_template('usuarios.html', usuarios = Usuario.query.all(), titulo="Usuarios")

@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
    usuario = Usuario(
        request.form.get('nome'),
        request.form.get('login'),
        request.form.get('senha'),
        request.form.get('email'),
        request.form.get('fone'),
        request.form.get('rua'),
        request.form.get('numero'),
        request.form.get('bairro'),
        request.form.get('cidade'),
        request.form.get('estado'),
        request.form.get('cep')
    )
    db.session.add(usuario)
    db.session.commit() 
    return redirect(url_for('cadusuario'))

@app.route("/usuario/detalhar/<int:id_usuario>")
def detalharusuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if usuario:
        return usuario.nome + "<br>" + \
               usuario.login + "<br>" + \
               usuario.email + "<br>" + \
               usuario.fone + "<br>" + \
               usuario.rua + "<br>" + \
               usuario.numero + "<br>" + \
               usuario.bairro + "<br>" + \
               usuario.cidade + "<br>" + \
               usuario.estado + "<br>" + \
               usuario.cep      
    else:
        return "Usuário não encontrado", 404

@app.route("/usuario/editar/<int:id_usuario>", methods=['GET', 'POST'])
def editarusuario(id_usuario):  
    usuario = Usuario.query.get(id_usuario)
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.login = request.form.get('login')
        usuario.senha = request.form.get('senha')
        usuario.email = request.form.get('email')   
        usuario.fone = request.form.get('fone')
        usuario.rua = request.form.get('rua')
        usuario.numero = request.form.get('numero')
        usuario.bairro = request.form.get('bairro')
        usuario.cidade = request.form.get('cidade')
        usuario.estado = request.form.get('estado')
        usuario.cep = request.form.get('cep')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('cadusuario'))
    return render_template('edit_usuario.html', usuario = usuario, titulo="Usuarios")          

@app.route("/usuario/excluir/<int:id_usuario>")
def excluirusuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for('cadusuario'))
    else:
        return "Usuário não encontrado", 404        


####################### CATEGORIAS #######################
@app.route("/cad/categoria")
def cadcategoria():
    return render_template('categorias.html',categorias = Categoria.query.all(), titulo="Categorias")

@app.route("/categoria/criar", methods=['POST'])
def criarcategoria():
    categoria = Categoria(
        request.form.get('descricao')
    )
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('cadcategoria'))

@app.route("/categoria/detalhar/<int:id_categoria>")
def detalharcategoria(id_categoria):
    categoria = Categoria.query.get(id_categoria)
    if categoria:
        return categoria.descricao
    else:
        return "Categoria não encontrada", 404

@app.route("/categoria/editar/<int:id_categoria>", methods=['GET', 'POST'])
def editarcategoria(id_categoria):
    categoria = Categoria.query.get(id_categoria)
    if request.method == 'POST':
        categoria.descricao = request.form.get('descricao')
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('cadcategoria'))    
    return render_template('edit_categoria.html', categoria = categoria, titulo="Categorias")   

@app.route("/categoria/excluir/<int:id_categoria>")
def excluircategoria(id_categoria):     
    categoria = Categoria.query.get(id_categoria)
    if categoria:
        db.session.delete(categoria)
        db.session.commit()
        return redirect(url_for('cadcategoria'))
    else:
        return "Categoria não encontrada", 404


####################### ANUNCIOS #######################
@app.route("/cad/anuncio")
def cadanuncio():
    return render_template('anuncios.html',
    anuncios=Anuncio.query.all(),
    usuarios=Usuario.query.all(),
    categorias=Categoria.query.all(),
    titulo="Anúncios" )

@app.route("/anuncio/criar", methods=['POST'])
def criaranuncio(): 
    anuncio = Anuncio(
        request.form.get('nome'),
        request.form.get('descricao'),
        request.form.get('data'),
        request.form.get('quantidade'),
        request.form.get('valor'),
        request.form.get('situacao'),
        request.form.get('id_us_prop_anuncio' ),  # ID do Usuário Proprietário do Anúncio
        request.form.get('id_cat')  # ID da Categoria          
    )
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('cadanuncio'))

@app.route("/anuncio/detalhar/<int:id_anuncio>")
def detalharanuncio(id_anuncio):
    anuncio = Anuncio.query.get(id_anuncio)
    if anuncio:
        return anuncio.id_anuncio + "<br>" + \
               anuncio.nome + "<br>" + \
               anuncio.descricao + "<br>" + \
               str(anuncio.data) + "<br>" + \
               str(anuncio.quantidade) + "<br>" + \
               str(anuncio.valor) + "<br>" + \
               anuncio.situacao + "<br>" + \
               str(anuncio.is_us_prop_anuncio) + "<br>" + \
               str(anuncio.id_cat) + "<br>"                
    else:
        return "Anúncio não encontrado", 404

@app.route("/anuncio/editar/<int:id_anuncio>", methods=['GET', 'POST'])
def editaranuncio(id_anuncio):
    anuncio = Anuncio.query.get(id_anuncio)
    if request.method == 'POST':
        anuncio.nome = request.form.get('nome')
        anuncio.descricao = request.form.get('descricao')
        anuncio.data = request.form.get('data')
        anuncio.quantidade = request.form.get('quantidade')
        anuncio.valor = request.form.get('valor')
        anuncio.situacao = request.form.get('situacao')
        anuncio.id_us_prop_anuncio = request.form.get('id_us_prop_anuncio')
        anuncio.id_cat = request.form.get('id_cat')
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('cadanuncio'))
    return render_template('edit_anuncio.html', anuncio = anuncio, titulo="Anúncios")

@app.route("/anuncio/excluir/<int:id_anuncio>")
def excluiranuncio(id_anuncio):
    anuncio = Anuncio.query.get(id_anuncio)
    if anuncio:
        db.session.delete(anuncio)
        db.session.commit()
        return redirect(url_for('cadanuncio'))
    else:
        return "Anúncio não encontrado", 404


####################### PRODUTOS #######################
@app.route("/cad/produto")
def cadproduto():
    return render_template('produtos.html', produtos = Produto.query.all(), titulo="Produtos")

@app.route("/produto/novo", methods=['POST']) 
def novoproduto():
    produto = Produto(
        request.form.get('descricao'),
        request.form.get('valor'),
        request.form.get('qt_estoque')
    )
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('cadproduto'))  

############## DEPOIS DESTE PONTO, SÓ SÃO ROTAS PARA TESTE, NÃO FORAM IMPLEMENTADAS AS FUNÇÕES DE CADASTRO
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

if __name__ =='main':
    print("Criando tabelas...")
    with app.app_context():
         db.create_all()
