import pandas as pd
from scipy import stats
from numpy import nan
import matplotlib.pyplot as plt




class Seletor(object):
    """
        Classe que permite fazer seleção de variáveis em problemas de Ciências dos Dados.
    """
    def __init__(self):
        pass

    def teste_student(self, dataframe, variavel_entrada, variavel_saida):
        """
            Método para checar se de fato uma variável é relevante ao conjunto de atributos disponível ao problema.
            Este método é viável para:
                                      input -> contínuo  | output -> discreto

                                      input -> discreto | output -> contínuo
                                      Levando se em conta uma variável discreta binária.
                O método compara se as médias dos grupos que são formados pelo agrupamento da variável de saída, são de fato, diferentes.
        """
        dataframe = dataframe.replace('?', nan)
        dataframe = dataframe.dropna()
        
        classes_de_saida = list(dataframe[variavel_saida].unique())

        assert len(classes_de_saida) == 2

        # Construção do primeiro grupo: 
        condition_num_1 = dataframe['RESPOND'] == classes_de_saida[0]
        df_num_1 = dataframe[condition_num_1]
        df_num_1 = df_num_1[variavel_entrada].dropna()

        # Construção do segundo grupo: 
        condition_num_2 = dataframe['RESPOND'] == classes_de_saida[1]
        df_num_2 = dataframe[condition_num_2]
        df_num_2 = df_num_2[variavel_entrada].dropna()

        grupo_1_media , grupo_2_media = df_num_1.mean(), df_num_2.mean()

        # A hipótese nula é de que as médias dos dois grupos distintos é a mesma.
        # O objetivo do teste de hipótese é negar esta hipotese, e garantir a hipótese H1:
        # De que a média dos dois grupos é diferente
        if grupo_1_media != grupo_2_media:
            variancia_grupo_1, variancia_grupo_2 = df_num_1.var(), df_num_2.var()
            
            if variancia_grupo_1 != variancia_grupo_2:
                # Cálculo de t e p-value:
                t, p_value = stats.ttest_ind(df_num_1, df_num_2, equal_var = False)
            else:
                # Cálculo de t e p-value:
                t, p_value = stats.ttest_ind(df_num_1, df_num_2)

        # Se observamos um grande valor para o p-value, por exemplo maior que 0.5 ou 0.1,
        # então não podemos rejeitar a hipótese nula de médias idênticas.
        # Se o p-value é menor que o limiar de 0.01, 0.05 ou 0.1
        # então rejeitamos a hipótese nula de médias iguais.
        if p_value > 0.5:
            print("As médias não apresentam diferença estatisticamente significativa")
        else:
            print("As médias apresentam diferença estatisticamente significativa")
    
        return df_num_1, df_num_2, t, p_value




if __name__ == '__main__':
    baseDados = pd.read_excel('base_buy.xlsx')

    testeHipotese = Seletor()
    # grupo_1, grupo_2, t, p_value = testeHipotese.teste_student(baseDados, 'AGE ', 'RESPOND')
    # grupo_1, grupo_2, t, p_value = testeHipotese.teste_student(baseDados, 'INCOME ', 'RESPOND')
    # grupo_1, grupo_2, t, p_value = testeHipotese.teste_student(baseDados, 'FICO ', 'RESPOND')
    grupo_1, grupo_2, t, p_value = testeHipotese.teste_student(baseDados, 'VALUE24 ', 'RESPOND')
