from functools import reduce

# Classe Venda
class Venda:
    def __init__(self, nome_produto, quantidade_vendida, preco_unitario):
        self.nome_produto = nome_produto
        self.quantidade_vendida = quantidade_vendida
        self.preco_unitario = preco_unitario

# Classe HistoricoVendas
class HistoricoVendas:
    def __init__(self):
        self.vendas = []

    def adicionar_venda(self, venda):
        self.vendas.append(venda)

    def total_por_produto(self):
        # Usando reduce e lambda para somar as vendas por produto
        produtos = {venda.nome_produto: venda.quantidade_vendida * venda.preco_unitario for venda in self.vendas}
        total_vendas = reduce(lambda acc, key: {**acc, key: acc.get(key, 0) + produtos[key]}, produtos.keys(), {})
        return total_vendas

    def listar_vendas_acima_de(self, valor):
        for venda in self.vendas:
            if venda.quantidade_vendida * venda.preco_unitario > valor:
                yield venda

# Classe Funcionario
class Funcionario:
    def __init__(self, nome, cargo, salario):
        self.nome = nome
        self.cargo = cargo
        self.salario = salario

# Decorator para autenticar acesso
def autenticar_acesso(funcao):
    def wrapper(self, *args, **kwargs):
        if self.cargo == "Gerente":
            return funcao(self, *args, **kwargs)
        else:
            raise PermissionError("Acesso negado: apenas gerentes podem aumentar salários.")
    return wrapper

# Classe SistemaRH
class SistemaRH:
    def __init__(self):
        self.funcionarios = []

    def adicionar_funcionario(self, funcionario):
        self.funcionarios.append(funcionario)

    @autenticar_acesso
    def aumentar_salario(self, funcionario, aumento):
        funcionario.salario += aumento

# Classe Conta
class Conta:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, tipo, valor):
        self.transacoes.append({'tipo': tipo, 'valor': valor})

    def filtrar_transacoes_por_tipo(self, tipo):
        # Usando filter e lambda para retornar transações de um tipo específico
        return list(filter(lambda t: t['tipo'] == tipo, self.transacoes))

    def aplicar_taxa(self, taxa):
        # Usando map e lambda para aplicar uma taxa a cada transação de tipo "Saque"
        self.transacoes = list(map(lambda t: {**t, 'valor': t['valor'] - taxa} if t['tipo'] == 'Saque' else t, self.transacoes))

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de Vendas
    venda1 = Venda("Produto A", 10, 5.0)
    venda2 = Venda("Produto B", 5, 20.0)
    venda3 = Venda("Produto A", 7, 5.0)

    historico = HistoricoVendas()
    historico.adicionar_venda(venda1)
    historico.adicionar_venda(venda2)
    historico.adicionar_venda(venda3)

    print("Total arrecadado por produto:", historico.total_por_produto())

    print("Vendas acima de R$50:")
    for venda in historico.listar_vendas_acima_de(50):
        print(f"Produto: {venda.nome_produto}, Quantidade: {venda.quantidade_vendida}, Preço Unitário: {venda.preco_unitario}")

    # Exemplo de Funcionários
    funcionario1 = Funcionario("João", "Gerente", 5000)
    funcionario2 = Funcionario("Maria", "Assistente", 3000)

    sistema_rh = SistemaRH()
    sistema_rh.adicionar_funcionario(funcionario1)
    sistema_rh.adicionar_funcionario(funcionario2)

    # Tentativa de aumento de salário
    try:
        sistema_rh.aumentar_salario(funcionario1, 1000)
        print(f"Novo salário de {funcionario1.nome}: R${funcionario1.salario}")
    except PermissionError as e:
        print(e)

    try:
        sistema_rh.aumentar_salario(funcionario2, 500)
    except PermissionError as e:
        print(e)

    # Exemplo de Conta
    conta = Conta()
    conta.adicionar_transacao("Depósito", 100)
    conta.adicionar_transacao("Saque", 50)
    conta.adicionar_transacao("Saque", 30)

    print("Transações do tipo 'Saque':", conta.filtrar_transacoes_por_tipo("Saque"))

    conta.aplicar_taxa(5)  # Aplica uma taxa de R$5 em saques
    print("Transações após aplicar taxa:", conta.transacoes)
