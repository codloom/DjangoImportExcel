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
