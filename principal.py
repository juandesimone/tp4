from registro import *
import random

from time import *
import os
from archivos import *

def validateRange(mensaje, ci, cs):
    valor = int(input(mensaje))
    while valor < ci or valor > cs:
        print('ERROR! el valor asignado debe estar entre', ci, 'y', cs)
        valor = int(input(mensaje))
    return valor


def displayVector(vec):
    print('-'*110)
    print('{:<20}'.format('Cod. Publicacion'),'{:<10}'.format('Precio'),'{:<20}'.format('Ubicacion Geo.'),'{:<10}'.format('Estado'),
          '{:<20}'.format('Cant. disponible'),'{:<10}'.format('Puntuacion del vendedor'))
    print('-'*110)
    for i in range(len(vec)):
        write2(vec[i])

def vector_generate(vec, n):
    for i in range(n):
        codigo = i+1
        precio = random.uniform(200, 1500)
        ubicacion= random.randint(0, 22)
        estado = random.choice(['Usado', 'Nuevo'])
        cantidad = random.randrange(300)
        puntos = random.randint(1, 5)
        busq = busqueda(codigo, round(precio, 2), ubicacion,estado, cantidad, puntos)
        vec.append(busq)


def buscar_producto(vec,op_cod):
    izq, der = 0, len(vec) - 1
    while izq <= der:
        c = (izq + der) // 2
        if op_cod == vec[c].codigo:
            return c
        if op_cod < vec[c].codigo:
            der = c - 1
        else:
            izq = c + 1
    return -1


def procesarCompra(vec, ind, cantidad):
    vec[ind].cantidad -= cantidad
    print('Desea que el producto', vec[ind].codigo, ' sea enviado a ', provincias_f(vec[ind].ubicacion), ' (10% de la compra):')
    op_envio=validateRange('1-Envio a domicilio / 0-Retiro en el local: ', 0, 1)
    monto = round(cantidad * vec[ind].precio, 2)
    if op_envio == 1:
        cargo_envio = monto*0.1
    else:
        cargo_envio = 0
    monto_total = round(monto+cargo_envio, 2)

    registro_compra = compra(vec[ind].codigo, cantidad, vec[ind].precio, op_envio, monto_total, strftime("%Y%m%d"))
    registrarCompra(registro_compra)

    ticket_l1 = 'Compra '+str(vec[ind].codigo)+' - '+strftime("%d/%m/%Y")+'\n'
    ticket_l2 = 'Resumen de la compra:'+'\n'+'Producto $'+str(monto)+(' ($ '+str(vec[ind].precio)+' * '+str(cantidad)+')')
    ticket_l3 = 'Cargo envio '+'$'+str(cargo_envio)+'\n'+'Tu pago '+' $'+str(monto_total)
    generarTicket(ticket_l1, ticket_l2, ticket_l3)

def validarMayorCero(men, l):
    x=int(input(men))
    while x <= l:
        print('ERROR, SU COMPRA DEBE SER MAYOR A CERO.')
        x = int(input(men))
    return x


def realizarCompra(vec):
    op_cod = int(input("Ingrese codigo de producto que desea comprar: "))
    ind = buscar_producto(vec, op_cod)
    if ind != -1:
        cantidad = validarMayorCero("Ingrese cantidad a comprar del producto "+str(op_cod)+" :", 0)
        if cantidad <= vec[ind].cantidad:
            procesarCompra(vec, ind, cantidad)
            print("COMPRA ACEPTADA!!!!")
        else:
            print("COMPRA RECHAZADA!!!!")
    else:
        print("PRODUCTO NO ENCONTRADO")

def validateFecha(fi, ff):
    v = []
    while ff < fi:
        print('FECHA FINAL NO PUEDE SER MAYOR A LA INICIAL')
        fi = input('Ingrese fecha de inicio (aaaammdd): ')
        ff = input('Ingrese fecha de fin (aaaammdd): ')
    v.append(fi)
    v.append(ff)
    return v


def displayVectorCompras(v_miscompras,v_date):
    print('-' * 110)
    print('{:<20}'.format('Cod. Publicacion'), '{:<10}'.format('Cantidad'), '{:<20}'.format('Precio'),
          '{:<20}'.format('Envio'), '{:<20}'.format('Monto total'), '{:<10}'.format('Fecha'))
    print('-' * 110)
    for i in range(len(v_miscompras)):
        if v_miscompras[i].fecha >= v_date[0] and v_miscompras[i].fecha <= v_date[1]:
                writeCompra(v_miscompras[i])


def rangoDePrecios(vec, min, max):
   n = len(vec)
   v = []
   for i in range(n):
        if vec[i].precio <= max and vec[i].precio >= min:
            v.append(vec[i])

   return v


def buscarMinimoMaximo(vec):
   min = vec[0].precio
   max = 0
   for i in range(len(vec)):
       if vec[i].precio > max:
           max = vec[i].precio
       elif vec[i].precio < min:
           min = vec[i].precio

   return min, max


def add_in_order_bin(p, nuevo):
    n = len(p)
    pos = n
    izq, der = 0, n - 1
    while izq <= der:
        c = (izq + der) // 2
        if p[c].codigo == nuevo.codigo:
            pos = c
            break
        if nuevo.codigo < p[c].codigo:
            der = c - 1
        else:
            izq = c + 1
    if izq > der:
        pos = izq
    p[pos:pos] = [nuevo]


def busqueda_bin_fav(FD, codigo):
    m=open(FD,'rb')
    t = os.path.getsize(FD)
    fp_inicial = m.tell()
    m.seek(0, io.SEEK_SET)
    posicion = -1
    while m.tell() < t:
        fp = m.tell()
        est = load(m)
        if est.codigo == codigo:
            posicion = fp
            break
    m.seek(fp_inicial, io.SEEK_SET)
    return posicion


def test():
    vec = []
    vec_fav = []
    op = -1
    n = int(input('Ingrese la cantidad de elementos devueltos de la busqueda: '))
    vector_generate(vec, n)
    displayVector(vec)
    if exists('ticket.txt'):
        os.remove('ticket.txt')
    while op != 0:
        print('-'*110)
        print('Menu de Opciones')
        print('1. Comprar.')
        print('2. Mis compras.')
        print('3. Rango de precios.')
        print('4. Agregar favorito.')
        print('5. Actualizar Favoritos.')
        print('0. Salir y terminar.')
        print('-'*110)
        op = int(input('Seleccione la opcion deseada: '))

        if op == 1:
            realizarCompra(vec)
        elif op == 2:
            fd_compras = 'miscompras.dat'
            vec_compras = deserializar(fd_compras)

            fecha_i=input('Ingrese fecha de inicio (aaaammdd): ')
            fecha_f=input('Ingrese fecha de fin (aaaammdd): ')

            v_date=validateFecha(fecha_i,fecha_f)
            displayVectorCompras(vec_compras,v_date)

        elif op == 3:
            min, max = buscarMinimoMaximo(vec)
            print('El menor precio es: \n$', min)
            print('El mayor precio es: \n$', max)
            op2 = 0
            while op2 != 3:
                print('Desea modificar alguno de los valores topes de busqueda?')
                print('\t Presione 1 si desea modificar el valor minimo de busqueda.')
                print('\t Presione 2 si desea modificar el valor maximo de busqueda.')
                print('\t Presione 3 si no desea modificar ningun otro valor.')
                op2 = int(input('Ingrese una opcion:'))
                if op2 == 1:
                    min = validateRange('Ingrese el nuevo valor minimo: $', min, max)
                    input('Su valor se ha modificado correctamente. Presione <ENTER> para continuar')
                elif op2 == 2:
                    max = validateRange('Ingrese el nuevo valor maximo: $', min, max)
                    input('Su valor se ha modificado correctamente. Presione <ENTER> para continuar')
            vRangoPrecios = rangoDePrecios(vec, min, max)
            print('Los productos encontrados en ese rango son: ')
            displayVector(vRangoPrecios)

        elif op == 4:

            busq = int(input('\nIngrese el codigo de la publicacion a buscar, '
                                 'cuando quiera dejar de ingresar elementos favoritos, presione el 0: '))
            while busq != 0:
                index = buscar_producto(vec, busq)
                if index == -1:
                    print('El registro buscado no existe, por favor intente nuevamente.')
                else:
                    if vec[index] in vec_fav:
                        print('El registro ya existe en el arreglo.')
                    else:
                        add_in_order_bin(vec_fav, vec[index])
                        displayVector(vec_fav)
                busq = int(input('\nIngrese el codigo de la publicacion a buscar, '
                                 'cuando quiera dejar de ingresar elementos favoritos, presione el 0: '))
        elif op == 5:
            if len(vec_fav) == 0:
                print('El arreglo de los favoritos esta vacio, por favor, ingrese en el punto 4 primero.')
            else:
                fd_fav = 'favoritos.dat'
                #SI EXISTE EL ARCHIVO
                if exists(fd_fav):
                    vec_fav_act = deserializar(fd_fav)
                    for i in range(len(vec_fav)):
                        codigo = vec_fav[i].codigo
                        r=busqueda_bin_fav(fd_fav,codigo)
                        if r==-1:
                            add_in_order_bin(vec_fav_act,vec_fav[i])
                    archivo_fav(vec_fav_act,fd_fav)
                #SI NO EXISTE EL ARCHIVO
                else:
                    archivo_fav(vec_fav,fd_fav)
                print('\n...LISTADO ACTUALIZADO DE FAVORITOS...')
                vec_fav_final=deserializar(fd_fav)
                displayVector(vec_fav_final)
        elif op == 0:
           print('FIN DEL PROGRAMA')

test()
