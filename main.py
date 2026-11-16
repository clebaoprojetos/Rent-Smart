import sys
from apartamento import Apartamento
from casa import Casa
from estudio import Estudio
from contrato import Contrato
from orcamento import Orcamento
from relatorio import RelatorioCSV


def ler_opcao_menu(mensagem: str, opcoes_validas: tuple) -> str:
    while True:
        entrada = input(mensagem).strip()
        if entrada in opcoes_validas:
            return entrada
        print(f"Opção inválida! Escolha entre: {', '.join(opcoes_validas)}")


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        entrada = input(f"{mensagem} (s/n): ").strip().lower()
        if entrada in ("s", "sim"):
            return True
        if entrada in ("n", "nao", "não"):
            return False
        print("Resposta inválida! Digite 's' para Sim ou 'n' para Não.")


def ler_inteiro_faixa(mensagem: str, minimo: int, maximo: int) -> int:
    while True:
        entrada = input(f"{mensagem} ({minimo} a {maximo}): ").strip()
        try:
            valor = int(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f"Valor fora do intervalo permitido! Deve ser entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")


def ler_inteiro_minimo(mensagem: str, minimo: int = 0) -> int:
    while True:
        entrada = input(f"{mensagem} (mínimo {minimo}): ").strip()
        try:
            valor = int(entrada)
            if valor >= minimo:
                return valor
            print(f"Valor inválido! Deve ser no mínimo {minimo}.")
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")


def coletar_dados_apartamento() -> Apartamento:
    print("\n--- Configuração do Apartamento ---")
    quartos = ler_inteiro_faixa("Quantidade de quartos", 1, 2)
    garagem = ler_sim_nao("Deseja vaga de garagem?")
    criancas = ler_sim_nao("Possui crianças?")
    return Apartamento(quant_quartos=quartos, possui_garagem=garagem, possui_criancas=criancas)


def coletar_dados_casa() -> Casa:
    print("\n--- Configuração da Casa ---")
    quartos = ler_inteiro_faixa("Quantidade de quartos", 1, 2)
    garagem = ler_sim_nao("Deseja vaga de garagem?")
    return Casa(quant_quartos=quartos, possui_garagem=garagem)


def coletar_dados_estudio() -> Estudio:
    print("\n--- Configuração do Estúdio ---")
    vagas = ler_inteiro_minimo("Quantidade de vagas de garagem", 0)
    return Estudio(quant_vagas=vagas)


def criar_novo_orcamento() -> None:
    print("\n==========================================")
    print("      CRIAÇÃO DE NOVO ORÇAMENTO           ")
    print("==========================================")
    print("Categorias disponíveis:")
    print("1. Apartamento")
    print("2. Casa")
    print("3. Estúdio")

    categoria_op = ler_opcao_menu("Escolha a categoria do imóvel (1-3): ", ("1", "2", "3"))

    imovel = None
    if categoria_op == "1":
        imovel = coletar_dados_apartamento()
    elif categoria_op == "2":
        imovel = coletar_dados_casa()
    elif categoria_op == "3":
        imovel = coletar_dados_estudio()

    print("\n--- Configuração do Contrato ---")
    parcelas = ler_inteiro_faixa("Quantidade de parcelas da taxa contratual", 1, 5)
    contrato = Contrato(quant_parcelas=parcelas)

    orcamento = Orcamento(imovel=imovel, contrato=contrato)

    print("\n" + orcamento.gerar_resumo_formatado())

    relatorio = RelatorioCSV(orcamento)
    caminho_csv = relatorio.gerar_csv()
    print(f"\n[SUCESSO] Projeção financeira de 12 meses salva em: {caminho_csv}\n")


def menu_principal() -> None:
    while True:
        print("=" * 42)
        print("       RENTSMART - R.M IMÓVEIS            ")
        print("=" * 42)
        print("1. Criar novo orçamento")
        print("2. Sair")
        print("=" * 42)

        opcao = ler_opcao_menu("Selecione uma opção: ", ("1", "2"))

        if opcao == "1":
            try:
                criar_novo_orcamento()
            except Exception as e:
                print(f"\n[ERRO] Ocorreu um erro ao gerar o orçamento: {e}\n")
        elif opcao == "2":
            print("\nObrigado por utilizar o RentSmart. Até logo!")
            sys.exit(0)


if __name__ == "__main__":
    menu_principal()
