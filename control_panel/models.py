from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True, unique=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_created=True, null=True, blank=True)

    def __str__(self):
        return self.name;

    @classmethod
    def create(cls, name, phone, email, date_created):
        customer = cls(name=name, phone=phone, email=email, date_created=date_created)
        return customer


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name;


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    buying_price = models.FloatField(null=False)
    price = models.FloatField(null=True)
    category = models.ForeignKey(Category, null=False, on_delete=models.SET("ABCD"))
    description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_created=True, null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name;


class PaymentMethod(models.Model):
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name


class TransactionCredentials(models.Model):
    method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_created=True, null=False)
    phone_number = models.CharField(max_length=200, null=True)
    from_destination = models.CharField(max_length=200, null=True)
    amount = models.FloatField(null=False)

    def __str__(self):
        return self.phone_number.__str__() + ' with an amount of ' + self.amount.__str__()

    @classmethod
    def create(cls, method, date_created, phone_number, from_destination, amount):
        transaction_credential = cls(method=method, date_created=date_created, phone_number=phone_number, from_destination=from_destination, amount=amount)
        return transaction_credential


class Transaction(models.Model):
    credentials = models.ForeignKey(TransactionCredentials, null=False, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_created=True, null=False)
    verified = models.BooleanField(null=False)

    def __str__(self):
        return self.id.__str__();

    @classmethod
    def create(cls, credentials, date_created, verified):
        transaction = cls(credentials=credentials, verified=verified, date_created=date_created)
        return transaction


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_created=True, null=True)
    quantity = models.IntegerField(null=False)
    status = models.CharField(max_length=200, null=True, default='Delivered', choices=STATUS)
    transaction = models.OneToOneField(Transaction, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.product.name + ' #' + self.id.__str__()

    @classmethod
    def create(cls, customer, product, date_created, quantity, status, transaction):
        order = cls(customer=customer, product=product, date_created=date_created, quantity=quantity, status=status, transaction=transaction)
        return order


class GiftCard(models.Model):
    date_created = models.DateTimeField(auto_created=True, null=True)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    code = models.CharField(max_length=200, null=False)
    serial = models.CharField(max_length=200, null=True)
    used = models.BooleanField(default=False)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Card #" + self.serial
