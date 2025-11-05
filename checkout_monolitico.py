
from abc import ABC, abstractmethod


##interfaces

class Estrategia_pagamento(ABC):
    @abstractmethod
    def processar_pagamento(self, valor: float) -> None:
        pass

class Estrategia_frete(ABC):
    @abstractmethod
    def calcular_frete(self, valor_desconto: float) -> float:
        pass


##pagamentos 
class Pag_Credito(Estrategia_pagamento):
    def processar_pagamento(self, valor_final):
        print(f"Processando pagamento via Cartão de Crédito no valor de R$ {valor_final:.2f}")
        
        if valor_final > 1000:
            print("Pagamento via Cartão de Crédito recusado: valor excede o limite.")
            return False
        
        else:
            print("Pagamento via Cartão de Crédito realizado com sucesso!")
            return True 
        
class Pag_pix(Estrategia_pagamento):
    def processar_pagamento(self, valor_final:float)-> bool:
        print(f"Processando pagamento via Pix no valor de R$ {valor_final:.2f}")
        print("Pagamento via Pix realizado com sucesso!")
        return True
    

class Pag_mana(Estrategia_pagamento):
    def processar_pagamento(self, valor_final: float) -> bool:
        print(f"Processando pagamento via Mana no valor de R$ {valor_final:.2f}")
        print("Pagamento via Mana realizado com sucesso!")
        return True
    

##fretes
class Frete_normal(Estrategia_frete):
    def calcular_frete(self, valor_desconto: float) -> float:
        custo_frete =valor_desconto * 0.05
        print(f"Frete normal calculado: R$ {custo_frete:.2f}")
        return custo_frete
    
class Frete_express(Estrategia_frete):
    def calcular_frete(self, valor_desconto: float) -> float:
        custo_frete =valor_desconto * 0.1 + 15.0
        print(f"Frete expresso calculado: R$ {custo_frete:.2f}")
        return custo_frete
    
class Frete_teletransporte(Estrategia_frete):
    def calcular_frete(self, valor_desconto: float) -> float:
        custo_frete = 50.0
        print(f"Frete por teletransporte calculado: R$ {custo_frete:.2f}")
        return custo_frete
    

##Pedido novo 

class Pedido_novo:
    def __init__(self,itens: list, estrategia_pagamento: Estrategia_pagamento, estrategia_frete: Estrategia_frete):
        self.itens = itens
        self.estrategia_pagamento = estrategia_pagamento
        self.estrategia_frete = estrategia_frete
        self.embalagem="padrão"
        self.valor_total = sum(item['preco'] * item['quantidade'] for item in itens)

    def Aplicar_desconto(self):
        self.valor_desconto = self.valor_total
        nome_estrategia = self.estrategia_pagamento.__class__.__name__

        if nome_estrategia == "Pag_pix":
            self.valor_desconto *= 0.9
            print(f"Desconto de 10% aplicado para pagamento via Pix. Novo valor: R$ {self.valor_desconto:.2f}")

        elif self.valor_total > 500:
            print(f"Desconto de 5% aplicado para pedidos acima de R$ 500. Novo valor: R$ {self.valor_desconto:.2f}")
            self.valor_desconto *= 0.95
            
        return self.valor_desconto
    
    def Compra_final(self):
        valor_com_desconto = self.Aplicar_desconto()
        custo_frete = self.estrategia_frete.calcular_frete(valor_com_desconto)
        valor_final = valor_com_desconto + custo_frete
        print(f"Valor final do pedido (com frete): R$ {valor_final:.2f}")
        sucesso_pagamento = self.estrategia_pagamento.processar_pagamento(valor_final)
        return sucesso_pagamento
    


## pedido base
class Calcular_valor(ABC):
    @abstractmethod
    def Calcular_valor(self) -> float:
        pass

    @abstractmethod
    def Detalhes_pedido(self) -> str:
        pass

class Pedido_base(Calcular_valor):
    def __init__(self, itens: list):
        self.itens = itens
        print("Pedido criado com os itens fornecidos. Valor inicial: R$ {self.__calcular_valor:.2f}")

    def Calcular_valor(self) -> float:
        return sum(item['preco'] * item['quantidade'] for item in self.itens)

    def Obter_detalhes(self) -> str:
        detalhes = "Detalhes do Pedido:\n"
        for item in self.itens:
            detalhes += f"- {item['nome']}: R$ {item['preco']:.2f} x {item['quantidade']}\n"
        detalhes += f"Valor Total: R$ {self.Calcular_valor():.2f}\n"
        return detalhes
    

class Sistema_estoque:

    def atualizar_estoque(self, itens: list) -> bool:
        print("Atualizando estoque: Reduzindo")
        if any(item['nome'] == 'Item Raro Indisponível' for item in itens):
             print("Item indisponível em estoque.")
             return False
        
        print("Estoque atualizado com sucesso.")
        return True
    
    def reverter_estoque(self, itens: list) -> None:
        print("Revertendo estoque: Itens adicionados de volta.")

    
class Gerador_nota:

    def emitir_nota(self, valor_final:float, itens:list):
        print("Emitindo nota fiscal para o pedido R${valor_final:.2f}:")
        print("Nota fiscal emitida com sucesso.")
        

class Sistema_notificacao:
    def enviar_confirmacao(self, sucesso_pagamento: bool) -> None:
        if sucesso_pagamento:
            print("Enviando confirmação de pedido ao cliente.")
            print("Confirmação enviada com sucesso.")
        else:
            print("Não foi possível enviar confirmação: pagamento não realizado.")


class CheckoutFacade:
    def __init__(self):
        self.estoque = Sistema_estoque()
        self.nota = Gerador_nota()
        self.notificacao = Sistema_notificacao()

    def Concluir_pedido(self, pedido: Pedido_novo) -> None:
        print("Iniciando processo de checkout...")
        
        if not self.estoque.atualizar_estoque(pedido.itens):
            print("Checkout cancelado: problemas no estoque.")
            return
        
        sucesso_pagamento = pedido.Compra_final()
        
        if sucesso_pagamento:
            valor_com_desconto = pedido.Aplicar_desconto()
            custo_frete = pedido.estrategia_frete.calcular_frete(valor_com_desconto)
            valor_final = valor_com_desconto + custo_frete
            self.nota.emitir_nota(valor_final, pedido.itens)
        else:
            self.estoque.reverter_estoque(pedido.itens)
            print("Checkout cancelado: pagamento falhou.")
            return
        
        self.notificacao.enviar_confirmacao(sucesso_pagamento)
        print("Checkout concluído com sucesso.")

class Pedido:
    def __init__(self,itens: list, estrategia_pagamento: Estrategia_pagamento, frete:Estrategia_frete ):
        self.itens = itens
        self.estrategia_pagamento = estrategia_pagamento
        self.frete = Estrategia_frete
        self.embalagem="padrão"
        self.valor_total = sum(item['preco'] * item['quantidade'] for item in itens)

    def aplicar_desconto(self):
        valor_apos_desconto = self.valor_total
        if self.valor_total > 500:
            print("Aplicando 10% de desconto para pedidos grandes.")
            valor_apos_desconto *= 0.90
        return valor_apos_desconto