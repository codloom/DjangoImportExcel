from django.db import models

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    documento = models.CharField(max_length=15)
    profissao = models.CharField(max_length=255)
    idade = models.IntegerField()

    def __str__(self):
        return self.nome

class Endereco(models.Model):
    cliente = models.OneToOneField(
        Cliente, on_delete=models.CASCADE, related_name='clientes')
    cep = models.CharField(max_length=10)
    bairro = models.CharField(max_length=255)
    rua = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=255)

    def __str__(self):
        return f"Endereço de {self.cliente.nome}"