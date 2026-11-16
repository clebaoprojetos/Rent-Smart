from decimal import Decimal, ROUND_HALF_UP


class Contrato:

    TAXA_CONTRATUAL_PADRAO = Decimal("2000.00")
    PARCELAS_MINIMAS = 1
    PARCELAS_MAXIMAS = 5

    def __init__(self, quant_parcelas: int = 1, taxa_contratual: Decimal = TAXA_CONTRATUAL_PADRAO):
        self._validar_parcelamento(quant_parcelas)
        self._quant_parcelas = int(quant_parcelas)
        self._taxa_total = Decimal(str(taxa_contratual))

    @classmethod
    def _validar_parcelamento(cls, quant_parcelas: int) -> None:
        if not isinstance(quant_parcelas, int) or quant_parcelas < cls.PARCELAS_MINIMAS or quant_parcelas > cls.PARCELAS_MAXIMAS:
            raise ValueError(
                f"A quantidade de parcelas deve ser um número inteiro entre "
                f"{cls.PARCELAS_MINIMAS} e {cls.PARCELAS_MAXIMAS} vezes."
            )

    @property
    def taxa_total(self) -> Decimal:
        return self._taxa_total

    @property
    def quant_parcelas(self) -> int:
        return self._quant_parcelas

    def calcular_valor_parcela(self) -> Decimal:
        valor_parcela = self._taxa_total / Decimal(str(self._quant_parcelas))
        return valor_parcela.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def obter_parcela_mes(self, mes: int) -> Decimal:
        if 1 <= mes <= self._quant_parcelas:
            return self.calcular_valor_parcela()
        return Decimal("0.00")
