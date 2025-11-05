from checkout_monolitico import Pedido_novo, Frete_normal, Frete_express, CheckoutFacade, Pag_pix, Pag_Credito
if __name__ == "__main__":
    
    
    fachada = CheckoutFacade()


    itens_sucesso = [
        {'nome': 'Poção de Vida', 'preco': 100.0, 'quantidade': 2},
        {'nome': 'Capa Comum', 'preco': 50.0, 'quantidade': 1}
    ] 
    print("\n\n*********************************************************")
    print("CENÁRIO 1: SUCESSO (PIX, Frete Normal, Desconto PIX 10%)")
    print("*********************************************************")

    pedido1 = Pedido_novo(
        itens=itens_sucesso, 
        estrategia_pagamento=Pag_pix(), 
        estrategia_frete=Frete_normal()
    )
    fachada.Concluir_pedido(pedido1)
    
   
    itens_falha = [
        {'nome': 'Castelo Mágico', 'preco': 1200.0, 'quantidade': 1},
        {'nome': 'Item Raro Indisponível', 'preco': 5.0, 'quantidade': 1} 
    ] 
    
    print("\n\n*********************************************************")
    print("CENÁRIO 2: FALHA (Crédito > Limite OU Item Indisponível)")
    print("*********************************************************")

    pedido2 = Pedido_novo(
        itens=itens_falha, 
        estrategia_pagamento=Pag_Credito(), 
        estrategia_frete=Frete_express()
    )
  
    fachada.Concluir_pedido(pedido2)