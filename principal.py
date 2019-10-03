from registro import *
import random
from pickle import *
from time import *
from os.path import *

def validateRange(mensaje, ci, cs):
    valor = int(input(mensaje))
    while valor < ci or valor > cs:
        print('ERROR!')
        valor = int(input(mensaje))
    return valor

def ordenarPorPrecio(vec):
    n = len(vec)
    for i in range(n-1):
        for j in range(i + 1, n):
            if vec[i].precio > vec[j].precio:
                vec[i], vec[j] = vec[j], vec[i]

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


def nuevosPorPrecio(vec):
    vecNuevo=[]
    for i in range(len(vec)):
        if vec[i].estado =='Nuevo':
            vecNuevo.append(vec[i])
    return vecNuevo


def usadosPorPuntos(v):
    con =[0]* len(v)
    for i in range(len(v)):
        c = v[i].puntos
        if v[i].estado == 'Usado':
            con[c-1] += 1

    return con

def distribucionGeografica(vec):
    mat = [[0]*5 for i in range(23)]
    for j in range(len(vec)):
        p = vec[j].ubicacion
        v = vec[j].puntos - 1
        mat[p][v] += vec[j].cantidad
    return mat

def ValidarProvincia(men):
    prov=input(men)
    ban_encontrado=False
    while ban_encontrado==False:
        for j in range(len(provincias)):
            if prov==provincias[j].lower() or prov == provincias[j].upper() or prov == provincias[j]:
                prov=j
                return prov
        else:
                print("ERROR! PROVINCIA NO ENCONTRADA!!!")
                prov = input(men)

def sumarTotalPorProvincia(mat):

    prov=ValidarProvincia('Ingrese la provincia a totalizar: ')
    total=0

    for i in range(len(mat[0])):
        total += mat[prov][i]
    print('El total de productos en', provincias_f(prov), 'es de', total, 'productos.')


def mostrarUsados(vec):
    num,den=0,0
    v=[]
    for i in range(len(vec)):
        if vec[i].estado == 'Usado':
            num+=vec[i].precio
            den+=1
    if den!=0:
        prom=num/den
    else:
        prom=0
    for i in range(len(vec)):
        if vec[i].estado == 'Usado' and vec[i].precio>=prom:
            v.append(vec[i])
    displayVector(v)

def compraIdeal(vec):
    v=[]
    for i in range(len(vec)):
        if vec[i].estado == 'Nuevo' and vec[i].puntos>1:
            v.append(vec[i])

    menor=v[0]
    for i in range(len(v)):
        if v[i].precio<menor.precio:
            menor=v[i]

    v2=[]
    v2.append(menor)
    displayVector(v2)

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

#FUNCION DEL TP4
def procesarCompra(vec,ind,cantidad):
    vec[ind].cantidad -= cantidad
    print('Desea que el producto',vec[ind].codigo,' sea enviado a ',vec[ind].ubicacion,' (10% de la compra):')
    op_envio=validateRange('1-Envio a domicilio / 0-Retiro en el local: ',0,1)
    monto = round(cantidad * vec[ind].precio,2)
    if op_envio==1:
        cargo_envio=monto*0.1
    else:
        cargo_envio=0
    monto_total=round(monto+cargo_envio,2)

    registro_compra=compra(vec[ind].codigo,cantidad,vec[ind].precio,op_envio,monto_total,strftime("%Y%m%d"))
    m=open('miscompras.dat','a+b')
    dump(registro_compra,m)
    m.close()

    n=open('ticket.txt','wt')
    ticket_l1='Compra '+str(vec[ind].codigo)+' - '+strftime("%d/%m/%Y")+'\n'
    ticket_l2='Resumen de la compra:'+'\n'+'Producto $'+str(monto)+(' ($ '+str(vec[ind].precio)+' * '+str(cantidad)+')')
    ticket_l3='Cargo envio '+'$'+str(cargo_envio)+'\n'+'Tu pago '+' $'+str(monto_total)
    n.write('-'*60+'\n')
    n.write(ticket_l1)
    n.write(ticket_l2+'\n')
    n.write(ticket_l3+'\n')
    n.write('-'*60)
    n.close()
#FUNCION DEL TP4
def realizarCompra(vec):
    op_cod=int(input("Ingrese codigo de producto que desea comprar: "))
    ind=buscar_producto(vec,op_cod)
    if ind!=-1:
        cantidad=int(input("Ingrese cantidad a comprar del producto "+str(op_cod)+" :"))
        if cantidad<=vec[ind].cantidad:
            procesarCompra(vec,ind,cantidad)
            print("COMPRA ACEPTADA!!!!")
        else:
            print("COMPRA RECHAZADA!!!!")
    else:
        print("PRODUCTO NO ENCONTRADO")
#FUNCION DEL TP4
def deserializarMisCompras():
    if not exists('miscompras.dat'):
        print('ARCHIVO INEEXISTENTE')
        return
    m=open('miscompras.dat','rb')
    v_miscompras=[]
    tam=getsize('miscompras.dat')
    while m.tell()<tam:
        registro=load(m)
        v_miscompras.append(registro)
    m.close()

    fecha_i=input('Ingrese fecha de inicio: ')
    fecha_f=input('Ingrese fecha de fin: ')
    for i in range(len(v_miscompras)):
        if v_miscompras[i].fecha>=fecha_i and v_miscompras[i].fecha<=fecha_f:
            print(v_miscompras[i])

def mostrarMatriz(mat):
    n = len(mat)
    m = len(mat[0])
    ban = False
    for i in range(n):
        for j in range(m):
            if mat[i][j]!= 0:
                if not ban:
                    print('En', provincias_f(i), ':' )
                    ban = True
                print('\t Para vendedores de', j + 1 , 'estrellas hay', mat[i][j], 'productos.')
        ban = False


def test():
    vec=[]
    op = -1
    n = int(input('Ingrese la cantidad de elementos devueltos de la busqueda: '))
    vector_generate(vec, n)
    banM = False
    displayVector(vec)
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
            deserializarMisCompras()
        elif op == 3:
            mat = distribucionGeografica(vec)
            mostrarMatriz(mat)
            banM = True
        elif op == 4:
            if banM:
                sumarTotalPorProvincia(mat)
            else:
                print('No se encuentra ninguna dato cargado. Por favor, seleccione la opcion 3 primero.')
        elif op == 5:
            mostrarUsados(vec)
        elif op == 0:
           print('FIN DEL PROGRAMA')

test()
