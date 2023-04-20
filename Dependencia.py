from TipoDependencia import TipoDependencia

class Dependencia:
    def __init__(self, id_requisito, tipo: TipoDependencia):
        self.id_requisito = id_requisito
        self.tipo = tipo
    
    def __str__(self):
        return f"{self.id_requisito}: {self.tipo}"

