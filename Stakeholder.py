class Stakeholder:
    
    def __init__(self, nombre: str, recomendaciones):
        self.nombre = nombre
        if recomendaciones is None:
            recomendaciones = []
        self.recomendaciones = recomendaciones
        self.importancia = len(recomendaciones)

    def agregar_recomendaciones(self, recomendaciones):
        self.recomendaciones.append(recomendaciones)
        self.importancia += len(recomendaciones)

    def comprobar_recomendaciones(self, nombres_stakeholders):
        if self.nombre in self.recomendaciones:
            return False
        return set(self.recomendaciones).issubset(nombres_stakeholders)
    
    def __str__(self):
        return f"Stakeholder: {self.nombre}, Recomendaciones: {self.recomendaciones}"
    
    def mostrar_recomendaciones(self):
        print(f"Stakeholders que han recomendado a {self.nombre}:")
        for recomendacion in self.recomendaciones:
            print(f"  - {recomendacion}")
    