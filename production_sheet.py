from typing import List

class ProductionSheet:
    _sheet:List[List]

    def __init__(self,sheet) -> None:
        self.sheet=sheet

    def __repr__(self) -> str:
        return f'ProductionSheet({self.sheet!r})'
    
    def __getitem__(self,index):
        if isinstance(index, tuple):
            row_index,col_index = self._process_ellipsis(index)
            return [row[col_index] for row in self.sheet[row_index]]
        return self.sheet[index]
    
    def _process_ellipsis(self,index):
        if Ellipsis in index:
            ellipsis_pos = index.index(Ellipsis)
            if ellipsis_pos == 0:
                col_index = index[1]
                return slice(None),col_index
            elif ellipsis_pos == 1:
                row_index = index[0]
                return row_index,slice(None)
        else:
            return index

    @property
    def sheet(self) -> List[List[int]]:
        return self._sheet
    
    @sheet.setter
    def sheet(self,new:List[List[int]]):
        if all(isinstance(sublist,list) and len(sublist)==3 and all(isinstance(item,int) for item in sublist) for sublist in new):
            self._sheet = new
        else:
            raise ValueError(
                f"Invalid value for sheet: {new}. Expected structure: [[int(prod1),int(prod2),int(prod3)],...]"
            )
        
    def analyze(self,type_analize):
        match type_analize:
            case 'soma_total':
                return sum(item for sublist in self.sheet for item in sublist)
            case 'media_diaria':
                return [sum(row)/len(row) for row in self.sheet]
            case 'maximo_produto':
                return max(item for sublist in self.sheet for item in sublist)
            case _:
                raise ValueError(
                    f"Invalid value for type_analize: {type_analize}. Expected any: 'soma_total','media_diaria','maximo_produto'"
                )
            
if __name__=='__main__':
    # Criando uma instância da classe ProductionSheet
    sheet = ProductionSheet([
        [100, 200, 300],  # Dia 1
        [150, 180, 250],  # Dia 2
        [120, 210, 310],  # Dia 3
    ])

    # Acessando todas as produções do primeiro produto
    print(sheet[1:, 1:])

    # Acessando produções dos dias 2 e 3
    print(sheet[..., :2])

    # Analisando a planilha usando match/case
    print(sheet.analyze("soma_total"))     # Saída: 1820
    print(sheet.analyze("media_diaria"))   # Saída: [200.0, 193.33, 213.33]
    print(sheet.analyze("maximo_produto")) # Saída: [150, 210, 310]
