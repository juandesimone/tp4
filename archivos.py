from pickle import *
from os.path import *

def generarTicket(ticket_l1,ticket_l2,ticket_l3):
    if not exists('ticket.txt'):
        n = open('ticket.txt', 'wt')
        n.write('-' * 60 + '\n')
        n.write(ticket_l1)
        n.write(ticket_l2 + '\n')
        n.write(ticket_l3 + '\n')
        n.write('-' * 60)
        n.close()
    else:
        n = open('ticket.txt', 'a+t')
        n.write('-' * 60 + '\n')
        n.write(ticket_l1)
        n.write(ticket_l2 + '\n')
        n.write(ticket_l3 + '\n')
        n.write('-' * 60)
        n.close()

def registrarCompra(registro_compra):
    m=open('miscompras.dat','a+b')
    dump(registro_compra,m)
    m.close()


def archivo_fav(vec, fd):
    m = open(fd, 'wb')
    for i in range(len(vec)):
        dump(vec[i],m)

#FUNCION DEL TP4
def deserializar(fd):
    if not exists(fd):
        print('ARCHIVO INEEXISTENTE')
        return
    m=open(fd,'rb')
    v=[]
    tam=getsize(fd)
    while m.tell()<tam:
        registro=load(m)
        v.append(registro)
    m.close()
    return v

