from db import db


class InventarioItem(db.Model):
    __tablename__ = "inventario_item"

    idInventarioItem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idItem = db.Column(db.Integer, db.ForeignKey("item.idItem"), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)
    qtd = db.Column(db.Integer)

    hotbar = db.relationship("Hotbar", backref="inventario_item", lazy=True)

    def para_dic(self):
        return {
            "idInventarioItem": self.idInventarioItem,
            "idItem": self.idItem,
            "item": self.item.nome if self.item else None,
            "idUsuario": self.idUsuario,
            "qtd": self.qtd
        }
