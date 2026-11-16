from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP


def formatar_moeda(valor: Decimal) -> str:
    quantizado = valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    partes = f"{quantizado:.2f}".split(".")
    inteiro = partes[0]
    decimal = partes[1]
    
    inteiro_formatado = ""
    for i, digito in enumerate(reversed(inteiro)):
        if i > 0 and i % 3 == 0:
            inteiro_formatado = "." + inteiro_formatado
        inteiro_formatado = digito + inteiro_formatado
        
    return f"R$ {inteiro_formatado},{decimal}"


class Imovel(ABC):

    def __init__(self, categoria: str, valor_base: Decimal):
        self._categoria = categoria
        self._valor_base = Decimal(str(valor_base))

    @property
    def categoria(self) -> str:
        return self._categoria

    @property
    def valor_base(self) -> Decimal:
        return self._valor_base

    @abstractmethod
    def calcular_adicional_quartos(self) -> Decimal:
        pass

    @abstractmethod
    def calcular_adicional_garagem(self) -> Decimal:
        pass

    def calcular_subtotal(self) -> Decimal:
        return (
            self._valor_base
            + self.calcular_adicional_quartos()
            + self.calcular_adicional_garagem()
        )

    @abstractmethod
    def calcular_desconto(self) -> Decimal:
        pass

    def calcular_aluguel_mensal(self) -> Decimal:
        subtotal = self.calcular_subtotal()
        desconto = self.calcular_desconto()
        return (subtotal - desconto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @abstractmethod
    def obter_detalhes(self) -> dict:
        pass
