from db import db


class Raridade(db.Model):
    __tablename__ = "raridade"

    idRaridade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(60), nullable=False)

    itens = db.relationship("Item", backref="raridade", lazy=True)

    def para_dic(self):
        return {
            "idRaridade": self.idRaridade,
            "nome": self.nome
        }
