from db import db


class Hotbar(db.Model):
    __tablename__ = "hotbar"

    idHotbar = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)
    idInventarioItem = db.Column(db.Integer, db.ForeignKey("inventario_item.idInventarioItem"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("idUsuario", "idInventarioItem", name="uq_usuario_inventario_item"),
    )

    def para_dic(self):
        return {
            "idHotbar": self.idHotbar,
            "idUsuario": self.idUsuario,
            "idInventarioItem": self.idInventarioItem,
            "item": self.inventario_item.item.nome if self.inventario_item and self.inventario_item.item else None
        }
