class NFeImpostoRetido:
    aliquota: float
    anoCompetencia: float
    codDarf: str
    codReceita: str
    codTributo: str
    dataFatoGerador: str
    dataFimCompetencia: str
    dataIniCompetencia: str
    dataPagamento: str
    dataVencto: str
    espTributo: str
    mesCompetencia: float
    numAp: str
    observacao: str
    valorBruto: float
    valorDedINSSTerceiro: float
    valorIRRetido: float

    def __init__(self, **json):
        if json:
            for key, typeProp in self.__class__.__dict__['__annotations__'].items():
                # str, float, bool, int
                class_name = str(typeProp).split("'")[1].split(".")[-1]

                if key in json:
                    if isinstance(typeProp, list):
                        cls = globals()[class_name]
                        items = []
                        for item_data in json[key]:
                            item = cls(**item_data)
                            items.append(item)
                        setattr(self, key, items)
                    elif class_name not in ('str', 'int', 'float', 'bool'):
                        cls = globals()[class_name]
                        instance = cls(**json[key])
                        setattr(self, key, instance)
                    else:
                        setattr(self, key, str(json[key]))
                else:
                    if isinstance(typeProp, list):
                        # cls = globals()[class_name]
                        items = []
                        setattr(self, key, items)
                    elif class_name not in ('str', 'int', 'float', 'bool'):
                        cls = globals()[class_name]
                        instance = cls()
                        setattr(self, key, instance)
                    else:
                        setattr(self, key, '')
        else:
            for key, typeProp in self.__class__.__dict__['__annotations__'].items():
                class_name = str(typeProp).split("'")[1].split(".")[-1]
                if isinstance(typeProp, list):
                    # cls = globals()[class_name]
                    items = []
                    setattr(self, key, items)
                elif class_name not in ('str', 'int', 'float', 'bool'):
                    cls = globals()[class_name]
                    instance = cls()
                    setattr(self, key, instance)
                else:
                    setattr(self, key, '')

    def get_aliquota(self):
        return self.aliquota

    def get_anoCompetencia(self):
        return self.anoCompetencia

    def get_codDarf(self):
        return self.codDarf

    def get_codReceita(self):
        return self.codReceita

    def get_codTributo(self):
        return self.codTributo

    def get_dataFatoGerador(self):
        return self.dataFatoGerador

    def get_dataFimCompetencia(self):
        return self.dataFimCompetencia

    def get_dataIniCompetencia(self):
        return self.dataIniCompetencia

    def get_dataPagamento(self):
        return self.dataPagamento

    def get_dataVencto(self):
        return self.dataVencto

    def get_espTributo(self):
        return self.espTributo

    def get_mesCompetencia(self):
        return self.mesCompetencia

    def get_numAp(self):
        return self.numAp

    def get_observacao(self):
        return self.observacao

    def get_valorBruto(self):
        return self.valorBruto

    def get_valorDedINSSTerceiro(self):
        return self.valorDedINSSTerceiro

    def get_valorIRRetido(self):
        return self.valorIRRetido