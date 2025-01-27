
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None):
        """
        Creates and saves a User with the given email, name, mobile, and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        if not name:
            raise ValueError('User must have a name')
        if not mobile:
            raise ValueError('User must have a mobile number')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            mobile=mobile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile, password=None):
        """
        Creates and saves a superuser with the given email, name, mobile, and password.
        """
        user = self.create_user(
            email,
            name=name,
            mobile=mobile,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin



class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    productdesc=models.TextField(blank=True)
    productadditonalinformation=models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    products = models.ForeignKey(Product, related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.products.title)


class Cart(models.Model):
    cart_id=models.CharField(max_length=500,null=True,blank=True,db_index=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return str(self.cart_id)



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,db_index=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True,db_index=True,related_name='carts')
    order_id = models.CharField(max_length=100,null=True,blank=True ,db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,db_index=True)
    price=models.IntegerField(null=True,blank=True,db_index=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cart)