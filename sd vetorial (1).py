#***********ALUNOS*************
#José Alisson Nogueira da Silva
# Wellington de Melo Rodrigues
#******************************

import socket
import pickle
import time
import threading

class Processo:
    def __init__(self, pid: int, total_processos: int = 4) -> None:
        # Inicializa os atributos do processo
        self.pid = pid
        self.total_processos = total_processos
        self.relogio_vetorial = [0] * total_processos
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 5000 + pid))
        self.socket.listen()
        # Inicia uma thread para receber continuamente mensagens
        self.thread_recebimento = threading.Thread(target=self.receber_mensagens)
        self.thread_recebimento.start()

    def enviar_mensagem(self, pid_destinatario: int) -> None:
        # Incrementa o relógio vetorial do remetente
        self.relogio_vetorial[self.pid] += 1
        mensagem = (self.pid, self.relogio_vetorial)
        # Conecta ao socket do destinatário e envia a mensagem
        socket_destinatario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_destinatario.connect(('localhost', 5000 + pid_destinatario))
        socket_destinatario.sendall(pickle.dumps(mensagem))
        socket_destinatario.close()

    def receber_mensagens(self) -> None:
        while True:
            # Aceita conexões recebidas
            conexao = self.socket.accept()[0]
            dados = conexao.recv(4096)
            # Desserializa os dados recebidos (PID do remetente e relógio vetorial)
            pid_remetente, relogio_vetorial_remetente = pickle.loads(dados)
            # Atualiza o relógio vetorial do receptor
            for p in range(self.total_processos):
                self.relogio_vetorial[p] = max(self.relogio_vetorial[p], relogio_vetorial_remetente[p])
            # Exibe a mensagem recebida e o relógio vetorial atualizado
            print(f"Processo {self.pid}: Relógio vetorial recebido do Processo {pid_remetente}: {relogio_vetorial_remetente} com o valor incrementado do evento.")
            print(f"Processo {self.pid}: Relógio vetorial atualizado: {self.relogio_vetorial}")
            conexao.close()

# Cria os processos
quantidade_processos = 4
proc0, proc1, proc2, *_ = [Processo(i, quantidade_processos) for i in range(quantidade_processos)]

# Processo 0 envia uma mensagem para o processo 1 e espera 2 segundos
proc0.enviar_mensagem(1)
time.sleep(2)

# Processo 1 envia uma mensagem para o processo 2 e espera 2 segundos
proc1.enviar_mensagem(2)
time.sleep(2)

# Processo 2 envia mensagens para os processos 3 e 1
proc2.enviar_mensagem(3)
proc2.enviar_mensagem(1)

