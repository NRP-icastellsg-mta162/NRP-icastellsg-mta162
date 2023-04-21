from NRP import NRP

def main():
    print(" _   _ ____  ____  ")
    print("| \\ | |  _ \\|  _ \\ ")
    print("|  \\| | |_) | |_) |")
    print("| |\\  |  _ <|  __/")
    print("|_| \\_|_| \\_\\_|   \n")

    nrp = NRP()
    archivo_stakeholders = input("Introduzca el archivo de stakeholders (con extensión): ")
    formato_stakeholders = archivo_stakeholders.split('.')[-1]
    stakeholders = nrp.cargar_stakeholders_desde_archivo(archivo_stakeholders, formato_stakeholders)
    
    archivo_requisitos = input("Introduzca el archivo de requisitos (con extensión): ")
    formato_requisitos = archivo_requisitos.split('.')[-1]
    requisitos = nrp.cargar_requisitos_desde_archivo(archivo_requisitos, formato_requisitos, stakeholders)

    cerrar_menu = False

    while not cerrar_menu:
        print("\nSeleccione una opción:")
        print("1. Mostrar stakeholders recomendados para un nombre concreto")
        print("2. Calcular la planificación de sprints")
        print("3. Salir")
        print("")

        option = int(input())

        print()

        if option == 1:
            nombre_stakeholder = input("Introduzca el nombre del stakeholder para saber quién lo ha recomendado: ")
            stakeholder = nrp.obtener_stakeholder_por_nombre(stakeholders, nombre_stakeholder)
            if stakeholder is None:
                print("Error: No se ha encontrado el stakeholder especificado")
            else:
                stakeholder.mostrar_recomendaciones()
        elif option == 2:
            coste_maximo = int(input("Introduzca el coste máximo por sprint: "))
            if (coste_maximo <= 0):
                print(f"El coste máximo debe de ser mayor que 0")
                exit(1)
            sprints = nrp.planificar_sprints(requisitos, coste_maximo)
            nrp.mostrar_solucion(sprints)
        elif option == 3:
            cerrar_menu = True
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()