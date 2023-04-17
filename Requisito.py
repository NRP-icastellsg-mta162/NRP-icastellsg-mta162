class Requisito:
    def __init__(self, id, descripcion, dependencias):
        self.id = id
        self.descripcion = descripcion
        if dependencias is None:
            dependencias = []
        self.dependencias = dependencias
        self.satisfaccion_total = 0
        self.coste = 1

# I: Implicacion // J: Combinacion // X : Exclusion

    def agregar_satisfaccion(self, satisfaccion):
        self.satisfaccion_total += satisfaccion

    def comprobar_dependencias(self, nombres_requisitos):
        dependencias_sin_tipo = [dependencia.split('.')[0] for dependencia in self.dependencias]
        if self.id in dependencias_sin_tipo:
            return False
        return set(dependencias_sin_tipo).issubset(nombres_requisitos)