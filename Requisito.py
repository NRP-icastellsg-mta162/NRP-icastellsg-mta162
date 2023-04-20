from Dependencia import Dependencia
from typing import List

class Requisito:
    def __init__(self, id: str, descripcion: str, dependencias: List[Dependencia]):
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

    def comprobar_dependencias(self, ids_requisitos):
        dependencias_sin_tipo = [dependencia.id_requisito for dependencia in self.dependencias]
        if self.id in dependencias_sin_tipo:
            return False
        return set(dependencias_sin_tipo).issubset(ids_requisitos)
    
    def __str__(self):
        return f"{self.id}: {self.descripcion} (sat: {self.satisfaccion_total}, coste: {self.coste})"