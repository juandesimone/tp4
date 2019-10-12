provincias = ['Jujuy', 'Catamarca', 'Corrientes', 'Formosa', 'Salta', 'Misiones', 'Tucuman','Chaco',
            'Santiago del Estero','La Rioja','Santa Fe', 'Entre rios', 'Buenos Aires', 'Mendoza', 'San Juan',
              'San Luis','Cordoba', 'La Pampa','Rio Negro','Chubut', 'Neuquen', 'Santa Cruz', 'Tierra del Fuego']

envios=['Retiro en local','Envio a Domicilio']

class busqueda():
    def __init__(self, codigo, precio, ubicacion ,estado, cantidad, puntos):
        self.codigo = codigo
        self.precio = precio
        self.ubicacion = ubicacion
        self.estado = estado
        self.cantidad = cantidad
        self.puntos = puntos


class compra():
    def __init__(self,codigo,cantidad,precio,envio,monto_total,fecha):
        self.codigo=codigo
        self.cantidad=cantidad
        self.precio=precio
        self.envio=envio
        self.monto_total=monto_total
        self.fecha=fecha

def writeCompra(compra):
    print('{:<20}'.format(compra.codigo), '{:<10}'.format(compra.cantidad),
          '{:<20}'.format(compra.precio), '{:<20}'.format(envios_f(compra.envio)),
          '{:<20}'.format(compra.monto_total), '{:<10}'.format(compra.fecha))

def write(busqueda):
    print('-'*60)
    print('Codigo de la publicacion:  ', busqueda.codigo)
    print('Precio: $ ', busqueda.precio)
    print('Ubicacion geografica:  ', busqueda.ubicacion)
    print('Estado: ', busqueda.estado)
    print('Cantidad disponible:  ', busqueda.cantidad)
    print('Puntuacion del vendedor:  ', busqueda.puntos)
    print('-'*60)

def provincias_f(num):
    return provincias[num]

def envios_f(num):
    return envios[num]

def write2(busqueda):
    print('{:<20}'.format(busqueda.codigo),'{:<10}'.format(busqueda.precio),'{:<20}'.format(provincias_f(busqueda.ubicacion)),'{:<10}'.format(busqueda.estado),
          '{:<20}'.format(busqueda.cantidad),'{:<10}'.format(busqueda.puntos))
