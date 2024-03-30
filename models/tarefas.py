class Tarefa:
    def __init__(self, id, nome, descricao, completada=False) -> None:
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.completada = completada

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "completada": self.completada,
        }