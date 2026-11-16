from decimal import Decimal
from imovel import Imovel


class Casa(Imovel):

    VALOR_BASE_PADRAO = Decimal("900.00")
    ADICIONAL_2_QUARTOS = Decimal("250.00")
    ADICIONAL_GARAGEM = Decimal("300.00")

    def __init__(self, quant_quartos: int, possui_garagem: bool):
        super().__init__(categoria="Casa", valor_base=self.VALOR_BASE_PADRAO)

        if quant_quartos not in (1, 2):
            raise ValueError("A quantidade de quartos para Casa deve ser 1 ou 2.")

        self._quant_quartos = quant_quartos
        self._possui_garagem = bool(possui_garagem)

    @property
    def quant_quartos(self) -> int:
        return self._quant_quartos

    @property
    def possui_garagem(self) -> bool:
        return self._possui_garagem

    def calcular_adicional_quartos(self) -> Decimal:
        if self._quant_quartos == 2:
            return self.ADICIONAL_2_QUARTOS
        return Decimal("0.00")

    def calcular_adicional_garagem(self) -> Decimal:
        if self._possui_garagem:
            return self.ADICIONAL_GARAGEM
        return Decimal("0.00")

    def calcular_desconto(self) -> Decimal:
        return Decimal("0.00")

    def obter_detalhes(self) -> dict:
        return {
            "categoria": self.categoria,
            "quartos": self._quant_quartos,
            "garagem": "Sim" if self._possui_garagem else "Não",
            "criancas": "Não aplicável",
            "percentual_desconto": "0%",
            "obs_garagem": None,
        }
