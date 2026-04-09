from db import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    senha = db.Column(db.String(60), nullable=True)

    inventario = db.relationship("InventarioItem", backref="usuario", lazy=True)
    hotbar = db.relationship("Hotbar", backref="usuario", lazy=True)

    def para_dic(self):
        return {
            "idUsuario": self.idUsuario,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha
        }