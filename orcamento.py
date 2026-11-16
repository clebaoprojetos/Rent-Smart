from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Any
from imovel import Imovel, formatar_moeda
from contrato import Contrato


class Orcamento:

    def __init__(self, imovel: Imovel, contrato: Contrato):
        if not isinstance(imovel, Imovel):
            raise TypeError("O imóvel deve ser uma instância válida de Imovel.")
        if not isinstance(contrato, Contrato):
            raise TypeError("O contrato deve ser uma instância válida de Contrato.")

        self._imovel = imovel
        self._contrato = contrato

    @property
    def imovel(self) -> Imovel:
        return self._imovel

    @property
    def contrato(self) -> Contrato:
        return self._contrato

    @property
    def aluguel_mensal(self) -> Decimal:
        return self._imovel.calcular_aluguel_mensal()

    def gerar_projecao_12_meses(self) -> List[Dict[str, Any]]:
        projecao = []
        aluguel = self.aluguel_mensal

        for mes in range(1, 13):
            parcela = self._contrato.obter_parcela_mes(mes)
            total = (aluguel + parcela).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            projecao.append({
                "mes": mes,
                "aluguel_mensal": aluguel,
                "parcela_contratual": parcela,
                "total_mensal": total,
            })

        return projecao

    def gerar_resumo_formatado(self) -> str:
        detalhes = self._imovel.obter_detalhes()
        valor_base = self._imovel.valor_base
        adicional_quarto = self._imovel.calcular_adicional_quartos()
        adicional_garagem = self._imovel.calcular_adicional_garagem()
        subtotal = self._imovel.calcular_subtotal()
        desconto = self._imovel.calcular_desconto()
        aluguel_mensal = self.aluguel_mensal
        taxa_total = self._contrato.taxa_total
        quant_parcelas = self._contrato.quant_parcelas
        valor_parcela = self._contrato.calcular_valor_parcela()

        linhas = [
            "========== RESUMO DO ORÇAMENTO ==========",
            "",
            f"Imóvel: {detalhes['categoria']}",
        ]

        if detalhes["categoria"] in ("Apartamento", "Casa"):
            linhas.append(f"Quartos: {detalhes['quartos']}")
            linhas.append(f"Garagem: {detalhes['garagem']}")
            if detalhes["categoria"] == "Apartamento":
                linhas.append(f"Crianças: {detalhes['criancas']}")
                linhas.append(f"Desconto: {detalhes['percentual_desconto']}")
        else:
            linhas.append(f"Vagas de Garagem: {detalhes['garagem']}")
            if detalhes.get("obs_garagem"):
                linhas.append(f"Observação Garagem: {detalhes['obs_garagem']}")

        linhas.append("")
        linhas.append(f"Aluguel-base: {formatar_moeda(valor_base)}")

        if adicional_quarto > Decimal("0.00"):
            linhas.append(f"Adicional de quarto: {formatar_moeda(adicional_quarto)}")

        if adicional_garagem > Decimal("0.00"):
            linhas.append(f"Adicional de garagem: {formatar_moeda(adicional_garagem)}")

        linhas.append(f"Subtotal: {formatar_moeda(subtotal)}")

        if desconto > Decimal("0.00"):
            linhas.append(f"Desconto ({detalhes['percentual_desconto']}): {formatar_moeda(desconto)}")
        elif detalhes["categoria"] == "Apartamento":
            linhas.append("Desconto: R$ 0,00 (0%)")

        linhas.append("")
        linhas.append(f"ALUGUEL MENSAL: {formatar_moeda(aluguel_mensal)}")
        linhas.append("")
        linhas.append(f"Taxa contratual: {formatar_moeda(taxa_total)}")
        linhas.append(f"Parcelamento: {quant_parcelas} {'vez' if quant_parcelas == 1 else 'vezes'}")
        linhas.append(f"Parcela contratual: {formatar_moeda(valor_parcela)}")
        linhas.append("")
        linhas.append("=========================================")

        return "\n".join(linhas)
