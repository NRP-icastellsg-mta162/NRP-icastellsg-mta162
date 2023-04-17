class Stakeholder:
    
    def __init__(self, nombre, recomendaciones=[]):
        self.nombre = nombre
        self.recomendaciones = recomendaciones
        self.importancia = len(recomendaciones)

    def agregar_recomendaciones(self, recomendaciones):
        self.recomendaciones.append(recomendaciones)
        self.importancia += len(recomendaciones)

    def comprobar_recomendaciones(self, nombres_stakeholders):
        if self.nombre in self.recomendaciones:
            return False
        return set(self.recomendaciones).issubset(nombres_stakeholders)