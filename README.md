# Como importar planilha de excel em algum modelo da aplicação django.

Projeto Inicial

**Github:** https://github.com/djangomy/config-default-simple.git

Planilha teste

[CLIENTES.xlsx](https://prod-files-secure.s3.us-west-2.amazonaws.com/a063a051-4fb5-4b47-ad10-54cee14f4f39/c591e605-f4cb-4cc0-8900-a542bd716e63/CLIENTES.xlsx)

Vamos criar os modelos no seu app.

*models.py* 

```python
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
```

*requirements.txt* 

```python
Django==4.1.13 
numpy==1.26.3
openpyxl==3.1.2
pandas==2.2.0
Pillow==9.3.0 
```

*views.py*

```python
import pandas as pd
from django.shortcuts import render, redirect
from django.views import View
from .forms import ImportarDadosForm
from .models import Cliente, Endereco

class ImportarDadosView(View):
    template_name = 'importar_dados.html'

    def get(self, request):
        clientes = Cliente.objects.all()
        form = ImportarDadosForm()
        return render(request, self.template_name, {
            'form': form,
            'clientes': clientes
        })

    def post(self, request):
        form = ImportarDadosForm(request.POST, request.FILES)

        if form.is_valid():
            arquivo = request.FILES['arquivo']
            df = pd.read_excel(arquivo)

            for _, row in df.iterrows():
                # Itera sobre as linhas do DataFrame lido do arquivo Excel 
                self.criar_cliente_e_endereco(row)

            return redirect('importar_dados')

        return render(request, self.template_name, {'form': form})

    def criar_cliente_e_endereco(self, row):
        # Use get_or_create para evitar a necessidade de verificar a existência antes de criar
        cliente, criado = Cliente.objects.get_or_create(
            documento=row['documento'],
            defaults={
                'nome': row['nome'],
                'profissao': row['profissao'],
                'idade': row['idade']
            }
        )

        if criado:
            # Cria o endereço associado ao cliente
            Endereco.objects.create(
                cliente=cliente,
                cep=row['cep'],
                bairro=row['bairro'],
                rua=row['rua'],
                complemento=row['complemento'],
                numero=row['numero'],
                estado=row['estado'],
                cidade=row['cidade']
            )
```

*forms.py* 

```python
from django import forms

class ImportarDadosForm(forms.Form):
    arquivo = forms.FileField()
```

*importar_dados.html*

```python
{% extends 'base.html' %}

{% block title %}Importar Dados{% endblock %}

{% block content %}
<div class="container">
  <h2>Importar Dados</h2>
  <form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Importar</button>
  </form>
 
  {% comment %} Lista de Clientes Importados {% endcomment %}
  <h2>Lista de Clientes</h2>
  <table class="table">
    <thead>
      <tr>
        <th>Nome</th>
        <th>Documento</th>
        <th>Profissão</th>
        <th>Idade</th>
        <th>CEP</th>
        <th>Bairro</th>
        <th>Rua</th>
        <th>Complemento</th>
        <th>Número</th>
        <th>Estado</th>
        <th>Cidade</th>
      </tr>
    </thead>
    <tbody>
      {% for cliente in clientes %}
        <tr>
          <td>{{ cliente.nome }}</td>
          <td>{{ cliente.documento }}</td>
          <td>{{ cliente.profissao }}</td>
          <td>{{ cliente.idade }}</td>
          <td>{{ cliente.clientes.cep }}</td>
          <td>{{ cliente.clientes.bairro }}</td>
          <td>{{ cliente.clientes.rua }}</td>
          <td>{{ cliente.clientes.complemento }}</td>
          <td>{{ cliente.clientes.numero }}</td>
          <td>{{ cliente.clientes.estado }}</td>
          <td>{{ cliente.clientes.cidade }}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
```