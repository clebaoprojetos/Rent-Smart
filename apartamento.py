from decimal import Decimal, ROUND_HALF_UP
from imovel import Imovel


class Apartamento(Imovel):

    VALOR_BASE_PADRAO = Decimal("700.00")
    ADICIONAL_2_QUARTOS = Decimal("200.00")
    ADICIONAL_GARAGEM = Decimal("300.00")
    PERCENTUAL_DESCONTO_SEM_CRIANCAS = Decimal("0.05")

    def __init__(self, quant_quartos: int, possui_garagem: bool, possui_criancas: bool):
        super().__init__(categoria="Apartamento", valor_base=self.VALOR_BASE_PADRAO)
        
        if quant_quartos not in (1, 2):
            raise ValueError("A quantidade de quartos para Apartamento deve ser 1 ou 2.")

        self._quant_quartos = quant_quartos
        self._possui_garagem = bool(possui_garagem)
        self._possui_criancas = bool(possui_criancas)

    @property
    def quant_quartos(self) -> int:
        return self._quant_quartos

    @property
    def possui_garagem(self) -> bool:
        return self._possui_garagem

    @property
    def possui_criancas(self) -> bool:
        return self._possui_criancas

    def calcular_adicional_quartos(self) -> Decimal:
        if self._quant_quartos == 2:
            return self.ADICIONAL_2_QUARTOS
        return Decimal("0.00")

    def calcular_adicional_garagem(self) -> Decimal:
        if self._possui_garagem:
            return self.ADICIONAL_GARAGEM
        return Decimal("0.00")

    def calcular_desconto(self) -> Decimal:
        if not self._possui_criancas:
            subtotal = self.calcular_subtotal()
            desconto = subtotal * self.PERCENTUAL_DESCONTO_SEM_CRIANCAS
            return desconto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return Decimal("0.00")

    def obter_detalhes(self) -> dict:
        return {
            "categoria": self.categoria,
            "quartos": self._quant_quartos,
            "garagem": "Sim" if self._possui_garagem else "Não",
            "criancas": "Sim" if self._possui_criancas else "Não",
            "percentual_desconto": "5%" if not self._possui_criancas else "0%",
            "obs_garagem": None,
        }
