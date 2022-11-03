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


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Nombre del producto', max_length=50)
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2)
    stock = models.IntegerField('Stock')
    description = models.TextField('Descripcion', max_length=200)
    image = models.ImageField('Imagen', upload_to='products', null=True, blank=True)

    def __str__(self):
        return self.name

