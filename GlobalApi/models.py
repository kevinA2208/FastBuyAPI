from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, doc, username,password=None):
        if not doc:
            raise ValueError('The user must have a document')

        user = self.model(
            doc = doc,
            username=username,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, doc, username, password):
        user = self.create_user(
            doc = doc,
            username=username,
            password=password,
        )
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser):
    doc = models.CharField('Numero de documento', unique=True, max_length=20, primary_key=True)
    username = models.CharField('Nombre de usuario', max_length=50, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = 'doc'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username},  doc: {self.doc}'

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self, app_label):
        return True


class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    #On delete means that if i delete a client, the user with the same doc as the client i deleted, will be
    #remove too
    doc_client = models.ForeignKey('User', on_delete=models.CASCADE, db_column='doc' )
    name_client = models.CharField(max_length = 50)
    last_name_client = models.CharField(max_length = 100)
    email_client = models.EmailField(null = False)



class Categories(models.Model):
    id_category = models.AutoField(primary_key=True)
    name_category = models.CharField(max_length=50, blank=True, null=True)


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField('Product name', max_length=50)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    #Stock will show how many ProductUnits objets from an specific product is available (views)
    description = models.TextField('Description', max_length=200)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, db_column='id_category')
    image = models.ImageField('Image', upload_to='products', null=True, blank=True)
    stock = models.IntegerField('Stock', default=0)
    available = models.BooleanField(default = True)


    def __str__(self):
        return self.name




#This model is the one that manages the units of the products
class ProductUnits(models.Model):
    product_unit_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey('Products',on_delete = models.CASCADE , db_column = 'id')
    # S for Selled and A for available | if the unit is selled then the stock decrease
    product_unit_state = models.CharField(max_length = 10)

    
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_client_id = models.ForeignKey('Client', on_delete = models.CASCADE, db_column = 'id_client', default = 0)
    order_address = models.CharField('Order Address', max_length = 300)
    order_date = models.DateField(null = True)
    order_product_units = models.ManyToManyField(ProductUnits)
    #I for In process, C for completed, D for delivered, if the client pay the order, the order state will change to C and then to delivered
    order_state = models.CharField(max_length = 10, default = 'I')
    
    

""" El cliente desde el front mira un producto, le da al boton de añadir al carrito, si le da
varias veces añadir al mismo producto, se le stackean varios productos para comprar, el carrito de compras se crea
desde el front con la información de los productos que el agregó, ademas de el precio total y un boton para pagarlo
con diferentes metodos de pago, una vez el cliente haga el pago, se borran los productos del carrito, y se crea un
pedido, este pedido tiene la información de los productos y la información del cliente, la direccion etc, el cliente
podrá darle a pedido completado para que el pedido cambie de estado de activo a entregado"""

    