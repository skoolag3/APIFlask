from db import db


class Item(db.Model):
    __tablename__ = "item"

    idItem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idRaridade = db.Column(db.Integer, db.ForeignKey("raridade.idRaridade"), nullable=False)
    nome = db.Column(db.String(60), nullable=False)
    descr = db.Column(db.String(120), nullable=False)
    imagem_url = db.Column(db.String(100))
    qtd = db.Column(db.Integer)

    inventario = db.relationship("InventarioItem", backref="item", lazy=True)

    def para_dic(self):
        return {
            "idItem": self.idItem,
            "idRaridade": self.idRaridade,
            "raridade": self.raridade.nome if self.raridade else None,
            "nome": self.nome,
            "descr": self.descr,
            "imagem_url": self.imagem_url,
            "qtd": self.qtd
        }
