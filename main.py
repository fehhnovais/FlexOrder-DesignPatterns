from checkout_monolitico import Pedido_novo, Frete_normal, Frete_express, CheckoutFacade, Pag_pix, Pag_Credito
if __name__ == "__main__":
    
    # Inicializa a Fachada (O ponto de entrada para o cliente)
    fachada = CheckoutFacade()

    # --- CENÁRIO 1: SUCESSO (PIX + Frete Normal) ---
    itens_sucesso = [
        {'nome': 'Poção de Vida', 'preco': 100.0, 'quantidade': 2},
        {'nome': 'Capa Comum', 'preco': 50.0, 'quantidade': 1}
    ] # Valor Total: R$ 250.00
    
    print("\n\n*********************************************************")
    print("CENÁRIO 1: SUCESSO (PIX, Frete Normal, Desconto PIX 10%)")
    print("*********************************************************")

    pedido1 = Pedido_novo(
        itens=itens_sucesso, 
        estrategia_pagamento=Pag_pix(), 
        estrategia_frete=Frete_normal()
    )
    fachada.Concluir_pedido(pedido1)
    
    # --- CENÁRIO 2: FALHA (Crédito > Limite + Frete Expresso) ---
    itens_falha = [
        {'nome': 'Castelo Mágico', 'preco': 1200.0, 'quantidade': 1},
        {'nome': 'Item Raro Indisponível', 'preco': 5.0, 'quantidade': 1} # Item que causa falha no estoque
    ] # Valor Total: R$ 1205.00
    
    print("\n\n*********************************************************")
    print("CENÁRIO 2: FALHA (Crédito > Limite OU Item Indisponível)")
    print("*********************************************************")

    pedido2 = Pedido_novo(
        itens=itens_falha, 
        estrategia_pagamento=Pag_Credito(), 
        estrategia_frete=Frete_express()
    )
    # A Fachada tentará coordenar a transação
    fachada.Concluir_pedido(pedido2)