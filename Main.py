import csv
from Stakeholder import Stakeholder

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

def main():
    
    archivo_stakeholders = input("Introduzca el archivo de stakeholders (con extensión): ")
    formato_stakeholders = archivo_stakeholders.split('.')[-1]
    stakeholders = cargar_stakeholders_desde_archivo(archivo_stakeholders, formato_stakeholders)
    print(f"Se han cargado {len(stakeholders)} stakeholders: {', '.join([stakeholder.nombre for stakeholder in stakeholders])}")

if __name__ == "__main__":
    main()