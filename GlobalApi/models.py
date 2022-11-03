from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, doc, name,password=None):
        if not doc:
            raise ValueError('The user must have a document')

        user = self.model(
            doc = doc,
            email = self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, doc, name, password):
        user = self.create_user(
            email,
            doc = doc,
            name=name,
            password=password,
        )
        user.user_type = 'A'
        user.save()
        return user

class User(AbstractBaseUser):
    doc = models.CharField('Numero de documento', unique=True, max_length=20, primary_key=True)
    name = models.CharField('Nombre de usuario', max_length=50, blank=True, null=True)
    email = models.CharField('Email',max_length=60, blank=True, null=True)
    user_active = models.BooleanField(default = True)
    user_type = models.CharField('Tipo usuario', max_length=1)
    #[A (Admin) C (Client)]
    objects = UserManager()
    USERNAME_FIELD = 'doc'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return f'{self.name},  doc: {self.doc}'

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.user_type == 'A'

class Client(models.Model):
    id_client = models.AutoField(primary_key=True, unique=True)
    #On delete means that if i delete a client, the user with the same doc as the client i deleted, will be
    #remove too
    doc_client = models.ForeignKey('User', on_delete=models.CASCADE, db_column='doc' )
    name_client = models.CharField(max_length = 50)
    last_name_client = models.CharField(max_length = 100)
    email_client = models.EmailField(null = False)

class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True, unique=True)
    doc_admin = models.ForeignKey('User', on_delete=models.CASCADE, db_column='doc' )
    name_admin = models.CharField(max_length = 50)
    last_name_admin = models.CharField(max_length = 100)
    email_admin = models.EmailField(null = False)

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Product name', max_length=50)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    stock = models.IntegerField('Stock')
    description = models.TextField('Description', max_length=200)
    image = models.ImageField('Image', upload_to='products', null=True, blank=True)
    available = models.BooleanField(default = True)


    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_client_name = models.ForeignKey('Client', on_delete = models.CASCADE ,db_column = 'name_client', related_name = 'client_name_order')
    order_client_lastname = models.ForeignKey('Client',on_delete = models.CASCADE , db_column = 'last_name_client', related_name = 'client_lastname_order')
    order_address = models.CharField('Order Address', max_length = 300)
    order_client_doc = models.ForeignKey('Client', on_delete = models.CASCADE , db_column = 'doc_client')
    order_date = models.DateField(null = True)
    order_product = models.ManyToManyField(Products)
    order_active = models.BooleanField(default = True)
    
    

""" El cliente desde el front mira un producto, le da al boton de añadir al carrito, si le da
varias veces añadir al mismo producto, se le stackean varios productos para comprar, el carrito de compras se crea
desde el front con la información de los productos que el agregó, ademas de el precio total y un boton para pagarlo
con diferentes metodos de pago, una vez el cliente haga el pago, se borran los productos del carrito, y se crea un
pedido, este pedido tiene la información de los productos y la información del cliente, la direccion etc, el cliente
podrá darle a pedido completado para que el pedido cambie de estado de activo a entregado"""

    