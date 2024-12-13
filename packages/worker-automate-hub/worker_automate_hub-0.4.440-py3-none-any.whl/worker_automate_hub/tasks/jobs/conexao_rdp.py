import asyncio
import platform
import subprocess
import socket
import pyautogui
import pygetwindow as gw
from rich.console import Console
import pygetwindow as gw
from pywinauto import Application
from worker_automate_hub.models.dto.rpa_historico_request_dto import RpaHistoricoStatusEnum, RpaRetornoProcessoDTO
from worker_automate_hub.models.dto.rpa_processo_rdp_dto import RpaProcessoRdpDTO
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import worker_sleep

console = Console()


class RDPConnection:
    def __init__(self, task: RpaProcessoRdpDTO):
        self.task = task
        self.ip = task.configEntrada.get("ip")
        self.user = task.configEntrada.get("user")
        self.password = task.configEntrada.get("password")
        self.processo = task.configEntrada.get("processo")
        self.uuid_robo = task.configEntrada.get("uuid_robo")
    
    async def verificar_conexao(self) -> bool:
        sistema_operacional = platform.system().lower()
        console.print(f"Sistema operacional detectado: {sistema_operacional}")
        if sistema_operacional == "windows":
            comando_ping = ["ping", "-n", "1", "-w", "1000", self.ip]
        else:
            comando_ping = ["ping", "-c", "1", "-W", "1", self.ip]
        console.print(f"Executando comando de ping: {' '.join(comando_ping)}")
        try:
            resposta_ping = subprocess.run(comando_ping, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            ping_alcancado = resposta_ping.returncode == 0
            console.print(f"Ping {'sucesso' if ping_alcancado else 'falhou'}")
        except Exception as e:
            logger.error(f"Erro ao executar ping: {e}")
            ping_alcancado = False
        
        porta_aberta = False
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10)
                console.print(f"Verificando porta 3389 em {self.ip}")
                resposta_porta = sock.connect_ex((self.ip, 3389))
                porta_aberta = resposta_porta == 0
                console.print(f"Porta 3389 {'aberta' if porta_aberta else 'fechada'}")
        except Exception as e:
            logger.error(f"Erro ao verificar a porta RDP: {e}")
            porta_aberta = False
        
        return ping_alcancado and porta_aberta
    
    async def clicar_no_titulo(self):
        """
        Função para clicar no título das janelas de Conexão de Área de Trabalho Remota
        com o botão direito do mouse e executar comandos.
        """
        janelas_rdp = [
            win
            for win in gw.getAllTitles()
            if "Ligação ao Ambiente de Trabalho Remoto" in win
            or "Remote Desktop Connection" in win
            or "Conexão de Área de Trabalho Remota" in win
        ]

        for titulo in janelas_rdp:
            janela = gw.getWindowsWithTitle(titulo)[0]
            if not janela:
                console.print(f"Erro ao localizar a janela: {titulo}")
                continue

            console.print(f"Processando janela: {titulo}")

            # Obtém as coordenadas da janela
            x, y = janela.left, janela.top

            try:
                # Move o mouse para o título da janela e clica com o botão direito
                pyautogui.moveTo(x + 10, y + 10)  # Ajuste para alinhar ao título da janela
                pyautogui.click(button="right")
                
                await worker_sleep(5)
                pyautogui.press("down", presses=7, interval=0.1)
                await worker_sleep(5)
                pyautogui.hotkey("enter")
                await worker_sleep(5)
                pyautogui.hotkey("enter")
                break

            except Exception as e:
                console.print(f"Erro ao interagir com a janela {titulo}: {e}")
    
    async def conectar(self):
        console.print(f"Iniciando cliente RDP para {self.ip}")
        try:
            pyautogui.hotkey("win", "d")
            await worker_sleep(5)  # Tempo para garantir que todas as janelas sejam minimizadas
            console.print("Todas as janelas minimizadas com sucesso.")
        
            subprocess.Popen(["mstsc", f"/v:{self.ip}"], close_fds=True, start_new_session=True)
            await worker_sleep(10)  # Tempo aumentado para garantir abertura
            
            console.print("Procurando janela 'Ligação ao ambiente de trabalho remoto'")
            try:
                windows = gw.getWindowsWithTitle("Ligação ao ambiente de trabalho remoto")
            except:
                windows = gw.getWindowsWithTitle("Conexão de Área de Trabalho Remota")
                
            if not windows:
                logger.warning("Tentando encontrar janela com título em inglês 'Remote Desktop Connection'")
                windows = gw.getWindowsWithTitle("Remote Desktop Connection")
            
            if not windows:
                logger.error("Janela de RDP não encontrada.")
                return False
            
            rdp_window = windows[0]
            console.print(f"Janela '{rdp_window.title}' encontrada. Focando na janela.")
            
            # Restaurar janela se estiver minimizada
            if rdp_window.isMinimized:
                rdp_window.restore()
                await worker_sleep(5)
            
            # Redimensionar para 50% da tela
            screen_width, screen_height = pyautogui.size()
            new_width = screen_width // 2
            new_height = screen_height // 2
            rdp_window.resizeTo(new_width, new_height)
            rdp_window.moveTo(screen_width // 4, screen_height // 4)
            console.print(f"Janela redimensionada para {new_width}x{new_height}.")
            
            rdp_window.activate()
            await worker_sleep(5)  # Tempo extra para garantir que a janela está ativa
            
            # Clique para garantir o foco
            pyautogui.click(rdp_window.left + 50, rdp_window.top + 50)
            await worker_sleep(3)
            
            # Inserir credenciais
            
            try:
                app = Application(backend="uia").connect(title="Segurança do Windows")
                dialog = app.window(title="Segurança do Windows")

                edit_field = dialog.child_window(auto_id="EditField_1", control_type="Edit")

                if edit_field.exists():
                    console.print("Inserindo usuário.")
                    pyautogui.write(self.user, interval=0.1)
                    pyautogui.press("tab")
                    await worker_sleep(5)
            except:
                pass
           
            console.print("Inserindo senha.")
            pyautogui.write(self.password, interval=0.1)
            pyautogui.press("enter")
            await worker_sleep(5)
            pyautogui.press("left")
            await worker_sleep(5)
            pyautogui.press("enter")
            console.print("Credenciais inseridas.")
            await worker_sleep(5)  # Tempo para conexão ser concluída
            
            console.print("Conexão RDP ativa. Mantendo o script em execução.")
            return True
        except Exception as e:
            logger.error(f"Erro ao tentar conectar via RDP: {e}")
            return False

async def conexao_rdp(task: RpaProcessoRdpDTO) -> RpaRetornoProcessoDTO:
    try:
        console.print("Iniciando processo de conexão RDP.")
        rdp = RDPConnection(task)
        conectado = await rdp.verificar_conexao()
        if not conectado:
            logger.warning("Não foi possível estabelecer conexão RDP. Verifique o IP e a disponibilidade da porta.")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Não foi possível estabelecer conexão RDP. Verifique o IP e a disponibilidade da porta.",
                status=RpaHistoricoStatusEnum.Falha,
            )
        sucesso_conexao = await rdp.conectar()
        if sucesso_conexao:
            console.print("Processo de conexão RDP executado com sucesso.")
            
            await rdp.clicar_no_titulo()
            
            # Mantém o script ativo para manter a conexão RDP aberta
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Conexão RDP estabelecida com sucesso.",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        else:
            logger.error("Falha ao tentar conectar via RDP.")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Falha ao tentar conectar via RDP.",
                status=RpaHistoricoStatusEnum.Falha,
            )
    except Exception as ex:
        err_msg = f"Erro ao executar conexao_rdp: {ex}"
        logger.error(err_msg)
        console.print(err_msg, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=err_msg,
            status=RpaHistoricoStatusEnum.Falha,
        )
