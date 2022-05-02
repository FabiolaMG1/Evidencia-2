import datetime
import csv
def leer_csv(articulos):
    try:
        with open("datos.csv", "r") as archivo:
            lector = csv.reader(archivo, delimiter=",")
            registros = 0
            if lector:
                for clave, nombreCliente, descripcion, descripcionEq, cantidad, precio, total, fechan in lector:
                    if registros == 0:
                        registros = registros + 1
                    else:
                        clave = int(clave)
                        if clave in articulos:
                            articulos[clave].append((clave,nombreCliente, descripcion,descripcionEq, int(
                                cantidad), float(precio), float(total), fechan))
                        else:
                            articulos[clave] = [(clave, descripcion, int(
                                cantidad), float(precio), float(total), fechan)]
    except Exception as e:
        print("\n\n\tVerificando Almacenamiento..")
        input("<<ENTER>>")
        print("Memoria sincronizada\n")
    finally:
        archivo.close()

    return articulos


def generar(articulos):
    try:
        with open("datos.csv", "w", newline="") as archivo:
            registrador = csv.writer(archivo)
            registrador.writerow(
                ("Clave","Cliente", "Descripcion servicio","Descripcion equipo", "Cantidad", "Precio", "Total", "Fecha de Venta"))
            for i in articulos.keys():
                registrador.writerows(articulos[i])
    except Exception as e:
        print(f"Ocurrio un Error {e}\nVuelve a intentarlo\n")
    finally:
        archivo.close()
    return articulos

# Este diccionario sera usa para alacenar los datos de los servicios
articulos = {}
if not articulos:
    with open("datos.csv", "a") as archivo:
        archivo.close()

leer_csv(articulos)

while True:
    print("\n\tMenu Soporte Tecnico")
    print("1-Registrar una venta")
    print("2-Consultar una venta")
    print("3-Obtener un reporte de ventas para una fecha en específico")
    print("4-Obtener un reporte de ventas por rango de fechas")
    print("X-Salir y guardar ventas")
    opcion = input("Elige una opcion: ")
    if opcion == '1':
        monto_total = 0
        print("\n\tRegistrar")
        contador = max(articulos, default=0)+1
        articulos[contador] = []
        while opcion != '0':
            while True:
                try:
                    nombreCliente = input(
                        f"Escribe el nombre del cliente: ")
                    descripcion = input(
                        f"Escribe la descripción del servicio {contador} para este equipo: ")
                    descripcionEq = input(
                        f"Escribe la descripción del/los equipo(s): ")
                    cantidad = int(
                        input("Escribe la cantidad de equipos que requieren este servicios: "))
                    precio = float(input(f"Escribe el cargo del equipo: "))
                    fecha = input("Dime la fecha (dd/mm/aaaa): \n")
                    fecha_datetime = datetime.datetime.strptime(
                        fecha, "%d/%m/%Y").date()
                    fecha_procesada = fecha_datetime.strftime('%d/%m/%Y')
                    break
                except Exception as e:
                    print(f'Error vuelve a intentarlo\t{e}')
            compra = (contador,nombreCliente.upper(), descripcion.upper(), descripcionEq.upper(), cantidad,
                    precio, cantidad*precio, fecha_procesada)
            monto_total = monto_total+cantidad*precio
            Iva = monto_total*0.16
            montoTotal=monto_total+Iva
            articulos[contador].append(compra)
            opcion = input(
                "Escribe si deseas continuar 1-Continuar registrando/0-Dejar de registar: ")
        print(f"N° DE VENTA: {contador}")
        #El for va ir procesando los datos  del diccionario prara poderlos imprimir
        for i in articulos[contador]:
            print(
                f"Descripcion: {i[1]}\t {i[2]}\t {i[3]}\t {i[4]}X ${i[5]}\tMonto: {i[6]}\n")
        print("\nSubtotal: ", monto_total)
        print("\nIva: ", Iva)
        print("\nMonto Total: ", montoTotal)
        input("<<ENTER>>")
    elif opcion == '2':
        total = 0
        print("\n\tConsulta tus ventas\n")
        buscar = int(input("Introduce el numero de venta a buscar: "))
        if buscar in articulos:
            for consulta in articulos[buscar]:
                print(
                    f"Descripcion: {consulta[1]}\t {consulta[2]}\t {consulta[3]}\t {consulta[4]}X ${consulta[5]}\tMonto: {consulta[6]}\n")
                total = total+consulta[6]
            print("\nSubtotal: ", total)
            iva=total*0.16
            print("\nIva: ", iva)
            print("\nMonto Total: ", total+iva)
        else:
            print("\n\tNo se ha encontrado dicho numero de venta")
        input("<<ENTER>>")
    elif opcion == '3':
        print("\tObtener un reporte de ventas para una fecha en específico\n")
        while True:
            try:
                reporte_f = input(
                    "Dime la fecha ha encontrar (dd/mm/aaaa): \n")
                reporte_fecha = datetime.datetime.strptime(
                    reporte_f, "%d/%m/%Y").date()
                print(f"Fecha {reporte_fecha}\n")
                # Del diccionario sacamos los datos que necesitamos  con el .values
                for i in articulos.values():
                    iva=0
                    gran=0
                    for j in i:
                        if reporte_fecha.strftime('%d/%m/%Y') == j[7]:
                            iva=iva + j[6] * 0.16
                            gran= gran + j[6]
                            print(
                                f"\tFolio: {j[0]}\tCliente: {j[1]}\tDescripción de servicio: {j[2]}\tDescripción de equipo: {j[3]}\tCantidad: {j[4]}\tPrecio: {j[5]}\tSubtotal:{gran}\tiva:{iva}\tGran Total:{gran + iva}\n")
                break
            except Exception as e:
                print(f"Error Vuelve a intentar\t{e}\n")
                input("<<Enter>>")
    elif opcion == '4':
        print("\tObtener un reporte de ventas con un rango de fechas\n")
        while True:
            try:
                reporte_i = input("Dime desde que fecha buscar(dd/mm/aaaa): \n")
                reporte_f = input("Dime hasta que fecha buscar(dd/mm/aaaa): \n")
                reporte_fecha = datetime.datetime.strptime(reporte_i, "%d/%m/%Y").date()
                reportefecha = datetime.datetime.strptime(reporte_f, "%d/%m/%Y").date()
                print(f"Fecha {reporte_fecha} hasta {reportefecha}\n")
                # Del diccionario sacamos los datos que necesitamos  con el .values
                for i in articulos.values():
                    for j in i:
                        if reporte_fecha.strftime('%d/%m/%Y')<j[7]<reportefecha.strftime('%d/%m/%Y'):
                            print(f"\tFolio: {j[0]}\tCliente: {j[1]}\n")
                break
            except Exception as e:
                print(f"Error Vuelve a intentar\t{e}\n")
                input("<<Enter>>")
    elif opcion == 'X':
        generar(articulos)
        print("\n\t\t**---Almacenando cambios del sistema--**\n")
        print("\nSaliendo...\n")
        break
    else:
        print("\n\nError vuelve a intentarlo\n\n")
        input("<<ENTER>>")
