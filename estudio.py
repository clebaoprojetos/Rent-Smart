from decimal import Decimal
from imovel import Imovel, formatar_moeda


class Estudio(Imovel):

    VALOR_BASE_PADRAO = Decimal("1200.00")
    PACOTE_DUAS_VAGAS = Decimal("250.00")
    VALOR_VAGA_ADICIONAL = Decimal("60.00")

    def __init__(self, quant_vagas: int = 0):
        super().__init__(categoria="Estúdio", valor_base=self.VALOR_BASE_PADRAO)

        if quant_vagas < 0:
            raise ValueError("A quantidade de vagas de garagem não pode ser negativa.")

        self._quant_vagas = int(quant_vagas)

    @property
    def quant_vagas(self) -> int:
        return self._quant_vagas

    def calcular_adicional_quartos(self) -> Decimal:
        return Decimal("0.00")

    def calcular_adicional_garagem(self) -> Decimal:
        if self._quant_vagas == 0:
            return Decimal("0.00")
        elif self._quant_vagas <= 2:
            return self.PACOTE_DUAS_VAGAS
        else:
            vagas_extras = self._quant_vagas - 2
            return self.PACOTE_DUAS_VAGAS + (Decimal(str(vagas_extras)) * self.VALOR_VAGA_ADICIONAL)

    def calcular_desconto(self) -> Decimal:
        return Decimal("0.00")

    def obter_detalhes(self) -> dict:
        if self._quant_vagas == 0:
            obs = "Nenhuma vaga selecionada"
        elif self._quant_vagas <= 2:
            obs = f"Pacote promocional de 2 vagas utilizado ({self._quant_vagas} vaga(s) por R$ 250,00)"
        else:
            vagas_extras = self._quant_vagas - 2
            adicional_extras = Decimal(str(vagas_extras)) * self.VALOR_VAGA_ADICIONAL
            obs = f"Pacote 2 vagas (R$ 250,00) + {vagas_extras} vaga(s) extra(s) ({formatar_moeda(adicional_extras)})"

        return {
            "categoria": self.categoria,
            "quartos": "Integrado (não aplicável)",
            "garagem": f"{self._quant_vagas} vaga(s)",
            "criancas": "Não aplicável",
            "percentual_desconto": "0%",
            "obs_garagem": obs,
        }
