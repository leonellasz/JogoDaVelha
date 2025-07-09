# -*- coding: utf-8 -*-

class Tabuleiro:
    DESCONHECIDO = 0
    JOGADOR_0 = 1
    JOGADOR_X = 4

    def __init__(self):
        self.matriz = [ [Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO], 
                        [Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO],
                        [Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO]]

    def tem_campeao(self):
        # Verifica linhas para ver se alguém ganhou
        for l in range(3):
            if (self.matriz[l][0] == self.matriz[l][1] == self.matriz[l][2] and
                    self.matriz[l][0] != Tabuleiro.DESCONHECIDO):
                return self.matriz[l][0]

        # Verifica colunas para ver se há vencedores
        for c in range(3):
            if (self.matriz[0][c] == self.matriz[1][c] == self.matriz[2][c] and
                    self.matriz[0][c] != Tabuleiro.DESCONHECIDO):
                return self.matriz[0][c]

        # Verifica diagonal principal afim de ver se existe algum vencedor
        if (self.matriz[0][0] == self.matriz[1][1] == self.matriz[2][2] and
                self.matriz[0][0] != Tabuleiro.DESCONHECIDO):
            return self.matriz[0][0]

        # Verifica diagonal secundária para ver se alguém ganhou
        if (self.matriz[0][2] == self.matriz[1][1] == self.matriz[2][0] and
                self.matriz[0][2] != Tabuleiro.DESCONHECIDO):
            return self.matriz[0][2]

        # Nenhum vencedor encontrado
        return Tabuleiro.DESCONHECIDO