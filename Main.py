import csv
from Stakeholder import Stakeholder
from Requisito import Requisito

def cargar_requisitos_desde_archivo(archivo, formato, stakeholders):
    requisitos = []
    ids_requisitos = set()
    if formato == 'csv':
        with open(archivo, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dependencias = row.get('dependencias', '').split(';')
                requisito = Requisito(row['id'], row['descripcion'], dependencias)
                requisitos.append(requisito)
                ids_requisitos.add(row['id'])
                solicitudes = row.get('solicitudes', '').split(';')
                asignar_satisfaccion(requisito, solicitudes, stakeholders)
    else:
        print("Error: Formato de archivo no soportado. Solo se puede trabajar con archivos .csv")
        exit(1)
    
    for requisito in requisitos:
      if len(requisito.dependencias[0]) > 0:
        if not requisito.comprobar_dependencias(ids_requisitos):
            print(f"Error: Dependencias del requisito {requisito.id} no son correctas")
            exit(1)
    return requisitos

def asignar_satisfaccion(requisito, solicitudes, stakeholders):
    for solicitud in solicitudes:
        stackeholder = [stakeholder for stakeholder in stakeholders if stakeholder.nombre == solicitud]
        if len(stackeholder) > 0:
            importancia = stackeholder[0].importancia
            requisito.agregar_satisfaccion(importancia)
        else:
            print(f"Error: Las solicitudes del requisito {requisito.id} no son correctas")
            exit(1)

def cargar_stakeholders_desde_archivo(archivo, formato):
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

def planificar_sprints(requisitos, coste_maximo):
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

def main():
    
    archivo_stakeholders = input("Introduzca el archivo de stakeholders (con extensión): ")
    formato_stakeholders = archivo_stakeholders.split('.')[-1]
    stakeholders = cargar_stakeholders_desde_archivo(archivo_stakeholders, formato_stakeholders)
    print(f"Se han cargado {len(stakeholders)} stakeholders: {', '.join([stakeholder.nombre for stakeholder in stakeholders])}")

    archivo_requisitos = input("Introduzca el archivo de requisitos (con extensión): ")
    formato_requisitos = archivo_requisitos.split('.')[-1]
    requisitos = cargar_requisitos_desde_archivo(archivo_requisitos, formato_requisitos, stakeholders)
    print(f"Se han cargado {len(requisitos)} requisitos: {', '.join([f'{requisito.id}: {requisito.descripcion} (sat: {requisito.satisfaccion_total})' for requisito in requisitos])}")

    coste_maximo = int(input("Introduzca el coste máximo por sprint: "))
    sprints = planificar_sprints(requisitos, coste_maximo)

    print(f"Se han planificado {len(sprints)} sprints:")
    for i, sprint in enumerate(sprints):
        print(f"Sprint {i + 1}:")
        for requisito in sprint:
            print(f"  - {requisito.id}: {requisito.descripcion} (sat: {requisito.satisfaccion_total}, coste: {requisito.coste})")

if __name__ == "__main__":
    main()