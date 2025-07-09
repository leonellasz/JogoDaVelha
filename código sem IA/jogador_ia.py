
from random import randint
from jogador import Jogador
from tabuleiro import Tabuleiro


class JogadorIA(Jogador):
    def __init__(self, tabuleiro: Tabuleiro, tipo: int):
        super().__init__(tabuleiro, tipo)
        # Define o tipo do oponente
        self.oponente = Tabuleiro.JOGADOR_X if tipo == Tabuleiro.JOGADOR_0 else Tabuleiro.JOGADOR_0

    def getJogada(self) -> (int, int):
        # R1: Ganhar ou bloquear (duas em sequência)
        jogada = self._regra_ganhar_ou_bloquear()
        if jogada:
            return jogada

        # R2: Criar duas sequências de duas marcações
        jogada = self._regra_dupla_ameaca()
        if jogada:
            return jogada

        # R3: Marcar o centro se estiver livre
        jogada = self._regra_centro()
        if jogada:
            return jogada

        # R4: Marcar canto oposto se oponente marcou um canto
        jogada = self._regra_canto_oposto()
        if jogada:
            return jogada

        # R5: Marcar um canto vazio
        jogada = self._regra_canto_vazio()
        if jogada:
            return jogada

        # R6: Marcar arbitrariamente um quadrado vazio
        return self._regra_quadrado_vazio()

    def _regra_ganhar_ou_bloquear(self) -> (int, int):

        # Primeiro, tenta ganhar
        jogada = self._encontrar_duas_em_sequencia(self.tipo)
        if jogada:
            return jogada

        # Depois, tenta bloquear o oponente
        jogada = self._encontrar_duas_em_sequencia(self.oponente)
        if jogada:
            return jogada

        return None

    def _encontrar_duas_em_sequencia(self, jogador_tipo: int) -> (int, int):

        # Verifica linhas
        for l in range(3):
            count = 0
            vazio = None
            for c in range(3):
                if self.matriz[l][c] == jogador_tipo:
                    count += 1
                elif self.matriz[l][c] == Tabuleiro.DESCONHECIDO:
                    vazio = (l, c)

            if count == 2 and vazio:
                return vazio

        # Verifica colunas
        for c in range(3):
            count = 0
            vazio = None
            for l in range(3):
                if self.matriz[l][c] == jogador_tipo:
                    count += 1
                elif self.matriz[l][c] == Tabuleiro.DESCONHECIDO:
                    vazio = (l, c)

            if count == 2 and vazio:
                return vazio

        # Verifica diagonal principal
        count = 0
        vazio = None
        for i in range(3):
            if self.matriz[i][i] == jogador_tipo:
                count += 1
            elif self.matriz[i][i] == Tabuleiro.DESCONHECIDO:
                vazio = (i, i)

        if count == 2 and vazio:
            return vazio

        # Verifica diagonal secundária
        count = 0
        vazio = None
        for i in range(3):
            if self.matriz[i][2 - i] == jogador_tipo:
                count += 1
            elif self.matriz[i][2 - i] == Tabuleiro.DESCONHECIDO:
                vazio = (i, 2 - i)

        if count == 2 and vazio:
            return vazio

        return None

    def _regra_dupla_ameaca(self) -> (int, int):

        posicoes_vazias = self._obter_posicoes_vazias()

        for pos in posicoes_vazias:
            l, c = pos
            # Simula a jogada
            self.matriz[l][c] = self.tipo

            # Conta quantas sequências de 2 esta jogada criaria
            sequencias = self._contar_sequencias_de_duas(self.tipo)

            # Desfaz a simulação
            self.matriz[l][c] = Tabuleiro.DESCONHECIDO

            # Se criar duas ou mais sequências de duas, é uma dupla ameaça
            if sequencias >= 2:
                return pos

        return None

    def _contar_sequencias_de_duas(self, jogador_tipo: int) -> int:
        """
        Conta quantas sequências de duas marcações o jogador possui
        """
        count = 0

        # Verifica linhas
        for l in range(3):
            marcacoes = sum(1 for c in range(3) if self.matriz[l][c] == jogador_tipo)
            vazios = sum(1 for c in range(3) if self.matriz[l][c] == Tabuleiro.DESCONHECIDO)
            if marcacoes == 2 and vazios == 1:
                count += 1

        # Verifica colunas
        for c in range(3):
            marcacoes = sum(1 for l in range(3) if self.matriz[l][c] == jogador_tipo)
            vazios = sum(1 for l in range(3) if self.matriz[l][c] == Tabuleiro.DESCONHECIDO)
            if marcacoes == 2 and vazios == 1:
                count += 1

        # Verifica diagonal principal
        marcacoes = sum(1 for i in range(3) if self.matriz[i][i] == jogador_tipo)
        vazios = sum(1 for i in range(3) if self.matriz[i][i] == Tabuleiro.DESCONHECIDO)
        if marcacoes == 2 and vazios == 1:
            count += 1

        # Verifica diagonal secundária
        marcacoes = sum(1 for i in range(3) if self.matriz[i][2 - i] == jogador_tipo)
        vazios = sum(1 for i in range(3) if self.matriz[i][2 - i] == Tabuleiro.DESCONHECIDO)
        if marcacoes == 2 and vazios == 1:
            count += 1

        return count

    def _regra_centro(self) -> (int, int):
        """
        R3: Se o quadrado central estiver livre, marque-o
        """
        if self.matriz[1][1] == Tabuleiro.DESCONHECIDO:
            return (1, 1)
        return None

    def _regra_canto_oposto(self) -> (int, int):
        """
        R4: Se seu oponente tiver marcado um dos cantos, marque o canto oposto
        """
        cantos_opostos = [
            ((0, 0), (2, 2)),  # canto superior esquerdo <-> inferior direito
            ((0, 2), (2, 0)),  # canto superior direito <-> inferior esquerdo
        ]

        for canto1, canto2 in cantos_opostos:
            l1, c1 = canto1
            l2, c2 = canto2

            # Se oponente está no canto1 e canto2 está vazio
            if (self.matriz[l1][c1] == self.oponente and
                    self.matriz[l2][c2] == Tabuleiro.DESCONHECIDO):
                return canto2

            # Se oponente está no canto2 e canto1 está vazio
            if (self.matriz[l2][c2] == self.oponente and
                    self.matriz[l1][c1] == Tabuleiro.DESCONHECIDO):
                return canto1

        return None

    def _regra_canto_vazio(self) -> (int, int):
        """
        R5: Se houver um canto vazio, marque-o
        """
        cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        cantos_vazios = [canto for canto in cantos
                         if self.matriz[canto[0]][canto[1]] == Tabuleiro.DESCONHECIDO]

        if cantos_vazios:
            # Escolhe aleatoriamente entre os cantos vazios
            return cantos_vazios[randint(0, len(cantos_vazios) - 1)]
        return None

    def _regra_quadrado_vazio(self) -> (int, int):
        """
        R6: Marcar arbitrariamente um quadrado vazio
        """
        posicoes_vazias = self._obter_posicoes_vazias()

        if posicoes_vazias:
            return posicoes_vazias[randint(0, len(posicoes_vazias) - 1)]
        return None

    def _obter_posicoes_vazias(self) -> list:
        """
        Retorna uma lista com todas as posições vazias do tabuleiro
        """
        posicoes = []
        for l in range(3):
            for c in range(3):
                if self.matriz[l][c] == Tabuleiro.DESCONHECIDO:
                    posicoes.append((l, c))
        return posicoes