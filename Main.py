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

def asignar_satisfaccion(requisito, solicitudes, stakeholders):
    for solicitud in solicitudes:
        stackeholder = [stakeholder for stakeholder in stakeholders if stakeholder.nombre == solicitud]
        if len(stackeholder) > 0:
            importancia = stackeholder[0].importancia
            requisito.agregar_satisfaccion(importancia)
        else:
            print(f"Error: Las solicitudes del requisito {requisito.id} no son correctas")
            exit(1)

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

def obtener_stakeholder_por_nombre(array_stakeholders, nombre_buscado):
    for stakeholder in array_stakeholders:
        if stakeholder.nombre == nombre_buscado:
            return stakeholder
    return None

def mostrar_solucion(sprints):
    print(f"Se han planificado {len(sprints)} sprints:")
    for i, sprint in enumerate(sprints):
        print(f"Sprint {i + 1}:")
        for requisito in sprint:
            print(f"  - {requisito}")

def main():
    print(" _   _ ____  ____  ")
    print("| \\ | |  _ \\|  _ \\ ")
    print("|  \\| | |_) | |_) |")
    print("| |\\  |  _ <|  __/")
    print("|_| \\_|_| \\_\\_|   \n")

    archivo_stakeholders = input("Introduzca el archivo de stakeholders (con extensión): ")
    formato_stakeholders = archivo_stakeholders.split('.')[-1]
    stakeholders = cargar_stakeholders_desde_archivo(archivo_stakeholders, formato_stakeholders)
    
    archivo_requisitos = input("Introduzca el archivo de requisitos (con extensión): ")
    formato_requisitos = archivo_requisitos.split('.')[-1]
    requisitos = cargar_requisitos_desde_archivo(archivo_requisitos, formato_requisitos, stakeholders)

    cerrar_menu = False

    while not cerrar_menu:
        print("\nSeleccione una opción:")
        print("1. Mostrar stakeholders recomendados para un nombre concreto")
        print("2. Calcular la planificación de sprints")
        print("3. Salir")

        option = int(input())

        print()

        if option == 1:
            nombre_stakeholder = input("Introduzca el nombre del stakeholder para saber quién lo ha recomendado: ")
            stakeholder = obtener_stakeholder_por_nombre(stakeholders, nombre_stakeholder)
            if stakeholder is None:
                print("Error: No se ha encontrado el stakeholder especificado")
            else:
                stakeholder.mostrar_recomendaciones()
        elif option == 2:
            coste_maximo = int(input("Introduzca el coste máximo por sprint: "))
            sprints = planificar_sprints(requisitos, coste_maximo)
            mostrar_solucion(sprints)
        elif option == 3:
            cerrar_menu = True
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()