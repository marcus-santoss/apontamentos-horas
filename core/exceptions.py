class DependencyParamError(Exception):

    def __init__(self, *args, provided: str, missing: str):
        super().__init__(*args)
        self.provided = provided
        self.missing = missing

    def __str__(self):
        return (f"Ambos parâmetros {self.provided} e {self.missing} "
                f"são obrigatórios. Somente {self.provided} foi fornecido.")


class PatternNotMatchError(Exception):
    def __init__(self, *args, value: str):
        super().__init__(*args)
        self.value = value if len(value) > 0 else "<vazio>"

    def __str__(self):
        return f"O valor fornecido não parece ser uma data no formato YYYY-mm-dd: {self.value}"
