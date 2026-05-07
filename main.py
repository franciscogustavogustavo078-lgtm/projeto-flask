from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'

# Dados em memória (simulando banco de dados)
lista_usuarios = []
lista_produtos = []
lista_fornecedores = []
lista_vendas = []
contador_id = 1

# ROTAS PRINCIPAIS
@app.route('/')
def index():
    return render_template('index.html', 
                         total_usuarios=len(lista_usuarios),
                         total_produtos=len(lista_produtos),
                         total_fornecedores=len(lista_fornecedores),
                         total_vendas=len(lista_vendas))

# USUÁRIOS
@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', usuarios=lista_usuarios)

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
            'telefone': telefone,
            'data_cadastro': '2025-04-04'
        }
        lista_usuarios.append(novo)
        contador_id += 1
        flash('Usuário cadastrado com sucesso!', 'success')
    
    return redirect(url_for('usuarios'))

@app.route('/usuarios/editar/<int:id>', methods=['POST'])
def editar_usuario(id):
    for usuario in lista_usuarios:
        if usuario['id'] == id:
            usuario['nome'] = request.form.get('nome')
            usuario['email'] = request.form.get('email')
            usuario['telefone'] = request.form.get('telefone')
            flash('Usuário atualizado com sucesso!', 'success')
            break
    return redirect(url_for('usuarios'))

@app.route('/usuarios/deletar/<int:id>')
def deletar_usuario(id):
    global lista_usuarios
    lista_usuarios = [u for u in lista_usuarios if u['id'] != id]
    flash('Usuário removido com sucesso!', 'success')
    return redirect(url_for('usuarios'))

# PRODUTOS
@app.route('/produtos')
def produtos():
    return render_template('produtos.html', produtos=lista_produtos)

@app.route('/produtos/novo', methods=['POST'])
def novo_produto():
    global contador_id
    nome = request.form.get('nome')
    if nome:
        novo = {
            'id': contador_id,
            'nome': nome,
            'descricao': request.form.get('descricao'),
            'preco': float(request.form.get('preco', 0)),
            'quantidade': int(request.form.get('quantidade', 0))
        }
        lista_produtos.append(novo)
        contador_id += 1
        flash('Produto cadastrado com sucesso!', 'success')
    return redirect(url_for('produtos'))

@app.route('/produtos/editar/<int:id>', methods=['POST'])
def editar_produto(id):
    for produto in lista_produtos:
        if produto['id'] == id:
            produto['nome'] = request.form.get('nome')
            produto['descricao'] = request.form.get('descricao')
            produto['preco'] = float(request.form.get('preco', 0))
            produto['quantidade'] = int(request.form.get('quantidade', 0))
            flash('Produto atualizado com sucesso!', 'success')
            break
    return redirect(url_for('produtos'))

@app.route('/produtos/deletar/<int:id>')
def deletar_produto(id):
    global lista_produtos
    lista_produtos = [p for p in lista_produtos if p['id'] != id]
    flash('Produto removido com sucesso!', 'success')
    return redirect(url_for('produtos'))

# FORNECEDORES
@app.route('/fornecedores')
def fornecedores():
    return render_template('fornecedores.html', fornecedores=lista_fornecedores)

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
        contador_id += 1
        flash('Fornecedor cadastrado com sucesso!', 'success')
    return redirect(url_for('fornecedores'))

@app.route('/fornecedores/editar/<int:id>', methods=['POST'])
def editar_fornecedor(id):
    for fornecedor in lista_fornecedores:
        if fornecedor['id'] == id:
            fornecedor['nome'] = request.form.get('nome')
            fornecedor['cnpj'] = request.form.get('cnpj')
            fornecedor['telefone'] = request.form.get('telefone')
            fornecedor['email'] = request.form.get('email')
            fornecedor['endereco'] = request.form.get('endereco')
            flash('Fornecedor atualizado com sucesso!', 'success')
            break
    return redirect(url_for('fornecedores'))

@app.route('/fornecedores/deletar/<int:id>')
def deletar_fornecedor(id):
    global lista_fornecedores
    lista_fornecedores = [f for f in lista_fornecedores if f['id'] != id]
    flash('Fornecedor removido com sucesso!', 'success')
    return redirect(url_for('fornecedores'))

# VENDAS
@app.route('/venda')
def venda():
    return render_template('venda.html', produtos=lista_produtos)

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
            'produto_id': produto_id,
            'produto_nome': produto['nome'],
            'quantidade': quantidade,
            'valor_total': valor_total,
            'cliente_nome': cliente_nome,
            'data_venda': '2025-04-04'
        }
        lista_vendas.append(venda)
        produto['quantidade'] -= quantidade
        contador_id += 1
        flash(f'Venda finalizada com sucesso! Total: R$ {valor_total:.2f}', 'success')
    else:
        flash('Erro: Produto não encontrado ou quantidade insuficiente!', 'danger')
    
    return redirect(url_for('venda'))

@app.route('/venda/historico')
def historico_vendas():
    return render_template('historico_vendas.html', vendas=lista_vendas)

if __name__ == '__main__':
    app.run(debug=True, port=5000)