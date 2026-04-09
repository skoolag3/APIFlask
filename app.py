from flask import Flask, jsonify, request
from flask_migrate import Migrate

from config import Config
from db import db
from models.usuario import Usuario
from models.raridade import Raridade
from models.item import Item
from models.inventario_item import InventarioItem
from models.hotbar import Hotbar

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    return app


app = create_app()


@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.para_dic() for u in usuarios]), 200


@app.route("/usuarios/<int:id_usuario>", methods=["GET"])
def obter_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({"status": 404, "message": "Usuário não encontrado"}), 404
    return jsonify(usuario.para_dic()), 200


@app.route("/usuarios", methods=["POST"])
def criar_usuario():
    data = request.get_json()

    usuario = Usuario(
        nome=data.get("nome"),
        email=data.get("email"),
        senha=data.get("senha")
    )

    db.session.add(usuario)
    db.session.commit()

    return jsonify({"status": 201, "message": "Usuário criado com sucesso", "data": usuario.para_dic()}), 201


@app.route("/usuarios/<int:id_usuario>", methods=["PUT"])
def atualizar_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({"status": 404, "message": "Usuário não encontrado"}), 404

    data = request.get_json()

    usuario.nome = data.get("nome", usuario.nome)
    usuario.email = data.get("email", usuario.email)
    usuario.senha = data.get("senha", usuario.senha)

    db.session.commit()

    return jsonify({"status": 200, "message": "Usuário atualizado com sucesso", "data": usuario.para_dic()}), 200


@app.route("/usuarios/<int:id_usuario>", methods=["DELETE"])
def excluir_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({"status": 404, "message": "Usuário não encontrado"}), 404

    try:
        itens = InventarioItem.query.filter_by(idUsuario=id_usuario).all()
        for item in itens:
            db.session.delete(item)

        slots = Hotbar.query.filter_by(idUsuario=id_usuario).all()
        for slot in slots:
            db.session.delete(slot)

        db.session.delete(usuario)
        db.session.commit()

        return jsonify({"status": 200, "message": "Usuário deletado com sucesso"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": 400, "message": str(e)}), 400


@app.route("/usuarios/<int:id_usuario>/inventario", methods=["GET"])
def inventario_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({"status": 404, "message": "Usuário não encontrado"}), 404

    itens = InventarioItem.query.filter_by(idUsuario=id_usuario).all()
    return jsonify([i.para_dic() for i in itens]), 200


@app.route("/usuarios/<int:id_usuario>/hotbar", methods=["GET"])
def hotbar_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({"status": 404, "message": "Usuário não encontrado"}), 404

    slots = Hotbar.query.filter_by(idUsuario=id_usuario).all()
    return jsonify([h.para_dic() for h in slots]), 200


@app.route("/raridades", methods=["GET"])
def listar_raridades():
    return jsonify([r.para_dic() for r in Raridade.query.all()]), 200


@app.route("/raridades/<int:id_raridade>", methods=["GET"])
def obter_raridade(id_raridade):
    r = Raridade.query.get(id_raridade)
    if not r:
        return jsonify({"status": 404, "message": "Raridade não encontrada"}), 404
    return jsonify(r.para_dic()), 200


@app.route("/raridades", methods=["POST"])
def criar_raridade():
    data = request.get_json()

    r = Raridade(nome=data.get("nome"))
    db.session.add(r)
    db.session.commit()

    return jsonify({"status": 201, "message": "Raridade criada com sucesso", "data": r.para_dic()}), 201


@app.route("/raridades/<int:id_raridade>", methods=["PUT"])
def atualizar_raridade(id_raridade):
    r = Raridade.query.get(id_raridade)
    if not r:
        return jsonify({"status": 404, "message": "Raridade não encontrada"}), 404

    data = request.get_json()
    r.nome = data.get("nome", r.nome)

    db.session.commit()
    return jsonify({"status": 200, "message": "Raridade atualizada com sucesso", "data": r.para_dic()}), 200


@app.route("/raridades/<int:id_raridade>", methods=["DELETE"])
def excluir_raridade(id_raridade):
    r = Raridade.query.get(id_raridade)
    if not r:
        return jsonify({"status": 404, "message": "Raridade não encontrada"}), 404

    db.session.delete(r)
    db.session.commit()

    return jsonify({"status": 200, "message": "Raridade deletada com sucesso"}), 200


@app.route("/raridades/<int:id_raridade>/itens", methods=["GET"])
def itens_por_raridade(id_raridade):
    r = Raridade.query.get(id_raridade)
    if not r:
        return jsonify({"status": 404, "message": "Raridade não encontrada"}), 404

    itens = Item.query.filter_by(idRaridade=id_raridade).all()
    return jsonify([i.para_dic() for i in itens]), 200


@app.route("/itens", methods=["GET"])
def listar_itens():
    return jsonify([i.para_dic() for i in Item.query.all()]), 200


@app.route("/itens/<int:id_item>", methods=["GET"])
def obter_item(id_item):
    item = Item.query.get(id_item)
    if not item:
        return jsonify({"status": 404, "message": "Item não encontrado"}), 404
    return jsonify(item.para_dic()), 200


@app.route("/itens", methods=["POST"])
def criar_item():
    data = request.get_json()

    item = Item(
        idRaridade=data.get("idRaridade"),
        nome=data.get("nome"),
        descr=data.get("descr"),
        imagem_url=data.get("imagem_url"),
        qtd=data.get("qtd")
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({"status": 201, "message": "Item criado com sucesso", "data": item.para_dic()}), 201


@app.route("/itens/<int:id_item>", methods=["PUT"])
def atualizar_item(id_item):
    item = Item.query.get(id_item)
    if not item:
        return jsonify({"status": 404, "message": "Item não encontrado"}), 404

    data = request.get_json()

    item.idRaridade = data.get("idRaridade", item.idRaridade)
    item.nome = data.get("nome", item.nome)
    item.descr = data.get("descr", item.descr)
    item.imagem_url = data.get("imagem_url", item.imagem_url)
    item.qtd = data.get("qtd", item.qtd)

    db.session.commit()
    return jsonify({"status": 200, "message": "Item atualizado com sucesso", "data": item.para_dic()}), 200


@app.route("/itens/<int:id_item>", methods=["DELETE"])
def excluir_item(id_item):
    item = Item.query.get(id_item)
    if not item:
        return jsonify({"status": 404, "message": "Item não encontrado"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"status": 200, "message": "Item deletado com sucesso"}), 200


@app.route("/itens/busca", methods=["GET"])
def buscar_itens():
    nome = request.args.get("nome", "")
    itens = Item.query.filter(Item.nome.ilike(f"%{nome}%")).all()
    if not itens:
        return jsonify({"status": 404, "message": "Nenhum item encontrado"}), 404
    return jsonify([i.para_dic() for i in itens]), 200


@app.route("/inventario", methods=["GET"])
def listar_inventario():
    return jsonify([i.para_dic() for i in InventarioItem.query.all()]), 200


@app.route("/inventario", methods=["POST"])
def add_inventario():
    data = request.get_json()

    inv = InventarioItem(
        idItem=data.get("idItem"),
        idUsuario=data.get("idUsuario"),
        qtd=data.get("qtd", 1)
    )

    db.session.add(inv)
    db.session.commit()

    return jsonify({"status": 201, "message": "Item adicionado ao inventário", "data": inv.para_dic()}), 201


@app.route("/inventario/<int:id>", methods=["PUT"])
def atualizar_inventario(id):
    inv = InventarioItem.query.get(id)
    if not inv:
        return jsonify({"status": 404, "message": "Item do inventário não encontrado"}), 404

    data = request.get_json()
    inv.qtd = data.get("qtd", inv.qtd)

    db.session.commit()
    return jsonify({"status": 200, "message": "Inventário atualizado com sucesso", "data": inv.para_dic()}), 200


@app.route("/inventario/<int:id>", methods=["DELETE"])
def deletar_inventario(id):
    inv = InventarioItem.query.get(id)
    if not inv:
        return jsonify({"status": 404, "message": "Item do inventário não encontrado"}), 404

    db.session.delete(inv)
    db.session.commit()

    return jsonify({"status": 200, "message": "Item removido do inventário"}), 200


@app.route("/hotbar", methods=["GET"])
def listar_hotbar():
    return jsonify([h.para_dic() for h in Hotbar.query.all()]), 200


@app.route("/hotbar", methods=["POST"])
def add_hotbar():
    data = request.get_json()

    h = Hotbar(
        idUsuario=data.get("idUsuario"),
        idInventarioItem=data.get("idInventarioItem")
    )

    db.session.add(h)
    db.session.commit()

    return jsonify({"status": 201, "message": "Adicionado à hotbar com sucesso", "data": h.para_dic()}), 201


@app.route("/hotbar/<int:id>", methods=["PUT"])
def atualizar_hotbar(id):
    h = Hotbar.query.get(id)
    if not h:
        return jsonify({"status": 404, "message": "Slot da hotbar não encontrado"}), 404

    data = request.get_json()
    h.idInventarioItem = data.get("idInventarioItem", h.idInventarioItem)

    db.session.commit()
    return jsonify({"status": 200, "message": "Hotbar atualizada com sucesso", "data": h.para_dic()}), 200


@app.route("/hotbar/<int:id>", methods=["DELETE"])
def deletar_hotbar(id):
    h = Hotbar.query.get(id)
    if not h:
        return jsonify({"status": 404, "message": "Slot da hotbar não encontrado"}), 404

    db.session.delete(h)
    db.session.commit()

    return jsonify({"status": 200, "message": "Removido da hotbar com sucesso"}), 200


if __name__ == "__main__":
    app.run(debug=True)