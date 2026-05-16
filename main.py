from flask import Flask, render_template, request, redirect, url_for, flash

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# =========================
# CONFIGURAÇÃO FLASK
# =========================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'


engine = create_engine(
    "mysql+pymysql://root:@localhost:3306/projeto_flask", 
    echo=True
)

Session = sessionmaker(bind=engine)

Base = declarative_base()

# =========================
# TABELAS
# =========================

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    email = Column(String(100))
    telefone = Column(String(20))


class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    descricao = Column(String(200))
    preco = Column(Float)
    quantidade = Column(Integer)


class Fornecedor(Base):
    __tablename__ = 'fornecedores'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    cnpj = Column(String(30))
    telefone = Column(String(20))
    email = Column(String(100))
    endereco = Column(String(200))


class Venda(Base):
    __tablename__ = 'vendas'

    id = Column(Integer, primary_key=True)
    produto_nome = Column(String(100))
    quantidade = Column(Integer)
    valor_total = Column(Float)
    cliente_nome = Column(String(100))

# =========================
# CRIAR TABELAS
# =========================

Base.metadata.create_all(engine)

# =========================
# LISTAS TEMPORÁRIAS
# =========================

lista_usuarios = []
lista_produtos = []
lista_fornecedores = []
lista_vendas = []

contador_id = 1

# =========================
# ROTA PRINCIPAL
# =========================

@app.route('/')
def index():

    return render_template(
        'index.html',
        total_usuarios=len(lista_usuarios),
        total_produtos=len(lista_produtos),
        total_fornecedores=len(lista_fornecedores),
        total_vendas=len(lista_vendas)
    )

# =========================
# USUÁRIOS
# =========================

@app.route('/usuarios')
def usuarios():

    return render_template(
        'usuarios.html',
        usuarios=lista_usuarios
    )


@app.route('/usuarios/novo', methods=['POST'])
def novo_usuario():

    global contador_id

    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')

    if nome and email:

        for u in lista_usuarios:
            if u['email'] == email:

                flash('Email já cadastrado!', 'danger')

                return redirect(url_for('usuarios'))

        novo = {
            'id': contador_id,
            'nome': nome,
            'email': email,
            'telefone': telefone
        }

        lista_usuarios.append(novo)

        # SALVAR NO MYSQL
        session = Session()

        usuario_db = Usuario(
            nome=nome,
            email=email,
            telefone=telefone
        )

        session.add(usuario_db)

        session.commit()

        session.close()

        contador_id += 1

        flash('Usuário cadastrado com sucesso!', 'success')

    return redirect(url_for('usuarios'))


@app.route('/usuarios/deletar/<int:id>')
def deletar_usuario(id):

    global lista_usuarios

    lista_usuarios = [
        u for u in lista_usuarios if u['id'] != id
    ]

    flash('Usuário removido com sucesso!', 'success')

    return redirect(url_for('usuarios'))

# =========================
# PRODUTOS
# =========================

@app.route('/produtos')
def produtos():

    return render_template(
        'produtos.html',
        produtos=lista_produtos
    )


@app.route('/produtos/novo', methods=['POST'])
def novo_produto():

    global contador_id

    nome = request.form.get('nome')

    if nome:

        preco = float(request.form.get('preco', 0))
        quantidade = int(request.form.get('quantidade', 0))

        novo = {
            'id': contador_id,
            'nome': nome,
            'descricao': request.form.get('descricao'),
            'preco': preco,
            'quantidade': quantidade
        }

        lista_produtos.append(novo)

        # SALVAR MYSQL
        session = Session()

        produto_db = Produto(
            nome=nome,
            descricao=request.form.get('descricao'),
            preco=preco,
            quantidade=quantidade
        )

        session.add(produto_db)

        session.commit()

        session.close()

        contador_id += 1

        flash('Produto cadastrado com sucesso!', 'success')

    return redirect(url_for('produtos'))


@app.route('/produtos/deletar/<int:id>')
def deletar_produto(id):

    global lista_produtos

    lista_produtos = [
        p for p in lista_produtos if p['id'] != id
    ]

    flash('Produto removido com sucesso!', 'success')

    return redirect(url_for('produtos'))

# =========================
# FORNECEDORES
# =========================

@app.route('/fornecedores')
def fornecedores():

    return render_template(
        'fornecedores.html',
        fornecedores=lista_fornecedores
    )


@app.route('/fornecedores/novo', methods=['POST'])
def novo_fornecedor():

    global contador_id

    nome = request.form.get('nome')

    if nome:

        novo = {
            'id': contador_id,
            'nome': nome,
            'cnpj': request.form.get('cnpj'),
            'telefone': request.form.get('telefone'),
            'email': request.form.get('email'),
            'endereco': request.form.get('endereco')
        }

        lista_fornecedores.append(novo)

        # SALVAR MYSQL
        session = Session()

        fornecedor_db = Fornecedor(
            nome=nome,
            cnpj=request.form.get('cnpj'),
            telefone=request.form.get('telefone'),
            email=request.form.get('email'),
            endereco=request.form.get('endereco')
        )

        session.add(fornecedor_db)

        session.commit()

        session.close()

        contador_id += 1

        flash('Fornecedor cadastrado com sucesso!', 'success')

    return redirect(url_for('fornecedores'))


@app.route('/fornecedores/deletar/<int:id>')
def deletar_fornecedor(id):

    global lista_fornecedores

    lista_fornecedores = [
        f for f in lista_fornecedores if f['id'] != id
    ]

    flash('Fornecedor removido com sucesso!', 'success')

    return redirect(url_for('fornecedores'))

# =========================
# VENDAS
# =========================

@app.route('/venda')
def venda():

    return render_template(
        'venda.html',
        produtos=lista_produtos
    )


@app.route('/venda/finalizar', methods=['POST'])
def finalizar_venda():

    global contador_id

    produto_id = int(request.form.get('produto_id'))

    quantidade = int(request.form.get('quantidade', 0))

    cliente_nome = request.form.get('cliente_nome')

    produto = None

    for p in lista_produtos:

        if p['id'] == produto_id:

            produto = p

            break

    if produto and quantidade > 0 and quantidade <= produto['quantidade']:

        valor_total = produto['preco'] * quantidade

        venda = {
            'id': contador_id,
            'produto_nome': produto['nome'],
            'quantidade': quantidade,
            'valor_total': valor_total,
            'cliente_nome': cliente_nome
        }

        lista_vendas.append(venda)

        produto['quantidade'] -= quantidade

        # SALVAR MYSQL
        session = Session()

        venda_db = Venda(
            produto_nome=produto['nome'],
            quantidade=quantidade,
            valor_total=valor_total,
            cliente_nome=cliente_nome
        )

        session.add(venda_db)

        session.commit()

        session.close()

        contador_id += 1

        flash(
            f'Venda finalizada com sucesso! Total: R$ {valor_total:.2f}',
            'success'
        )

    else:

        flash(
            'Erro: Produto não encontrado ou quantidade insuficiente!',
            'danger'
        )

    return redirect(url_for('venda'))


@app.route('/venda/historico')
def historico_vendas():

    return render_template(
        'historico_vendas.html',
        vendas=lista_vendas
    )

# =========================
# EXECUTAR FLASK
# =========================

if __name__ == '__main__':

    app.run(debug=True, port=5000)