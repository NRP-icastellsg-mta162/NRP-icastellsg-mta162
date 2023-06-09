import csv
from Stakeholder import Stakeholder
from Requisito import Requisito
from Dependencia import Dependencia, TipoDependencia
from typing import List

class NRP:
    def cargar_requisitos_desde_archivo(self, archivo: str, formato, stakeholders: List[Stakeholder]):
        requisitos = []
        ids_requisitos = set()
        if formato == 'csv':
            with open(archivo, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    dependencias_archivo = row.get('dependencias', '').split(';')
                    dependencias = self.cargar_dependencias(dependencias_archivo)
                    requisito = Requisito(row['id'], row['descripcion'], dependencias)
                    requisitos.append(requisito)
                    ids_requisitos.add(row['id'])
                    solicitudes = row.get('solicitudes', '').split(';')
                    self.asignar_satisfaccion(requisito, solicitudes, stakeholders)
        else:
            print("Error: Formato de archivo no soportado. Solo se puede trabajar con archivos .csv")
            exit(1)
        
        for requisito in requisitos:
            if len(requisito.dependencias) > 0:
                if not requisito.comprobar_dependencias(ids_requisitos):
                    print(f"Error: Dependencias del requisito {requisito.id} no son correctas")
                    exit(1)
        return requisitos
    
    def cargar_dependencias(self, dependencias_archivo):
        dependencias = []
        if dependencias_archivo != ['']:
            for dependencia in dependencias_archivo:
                requisito_tipo = dependencia.split('.')
                dependencias.append(Dependencia(requisito_tipo[0], requisito_tipo[1]))
        return dependencias

    def cargar_stakeholders_desde_archivo(self,archivo, formato):
        stakeholders = []
        nombres_stakeholders = set()
        if formato == 'csv':
            with open(archivo, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    recomendaciones = row.get('recomendaciones', '').split(';')
                    stakeholders.append(Stakeholder(row['nombre'], recomendaciones))
                    nombres_stakeholders.add(row['nombre'])
        else:
            print("Error: Formato de archivo no soportado. Solo se puede trabajar con archivos .csv")
            exit(1)
        
        for stakeholder in stakeholders:
            if len(stakeholder.recomendaciones[0]) > 0 and not stakeholder.comprobar_recomendaciones(nombres_stakeholders):
                print(f"Error: Recomendaciones del stakeholder {stakeholder.nombre} no son correctas")
                exit(1)
        return stakeholders

    def asignar_satisfaccion(self,requisito, solicitudes, stakeholders):
        for solicitud in solicitudes:
            stackeholder = [stakeholder for stakeholder in stakeholders if stakeholder.nombre == solicitud]
            if len(stackeholder) > 0:
                importancia = stackeholder[0].importancia
                requisito.agregar_satisfaccion(importancia)
            else:
                print(f"Error: Las solicitudes del requisito {requisito.id} no son correctas")
                exit(1)

    def planificar_sprints(self,requisitos, coste_maximo):
        sprints = []
        requisitos_pendientes = sorted(requisitos, key=lambda r: r.satisfaccion_total, reverse=True)

        while requisitos_pendientes:
            sprint = []
            coste_actual = 0

            for requisito in requisitos_pendientes:
                if coste_actual + requisito.coste <= coste_maximo:
                    sprint.append(requisito)
                    coste_actual += requisito.coste

            for requisito in sprint:
                requisitos_pendientes.remove(requisito)

            sprints.append(sprint)

        return sprints

    def obtener_stakeholder_por_nombre(self, array_stakeholders, nombre_buscado):
        for stakeholder in array_stakeholders:
            if stakeholder.nombre == nombre_buscado:
                return stakeholder
        return None

    def mostrar_solucion(self, sprints):
        print(f"Se han planificado {len(sprints)} sprints:")
        for i, sprint in enumerate(sprints):
            print(f"Sprint {i + 1}:")
            for requisito in sprint:
                print(f"  - {requisito}")