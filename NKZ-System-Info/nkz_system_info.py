"""
NKZ System Info
Ferramenta de informações do sistema usando somente a biblioteca padrão do Python.
A consulta de RAM via ctypes está disponível no Windows.
"""

import os
import sys
import platform
import getpass
import socket
import shutil
from datetime import datetime


def format_bytes(value):
    """Converte bytes para uma unidade legível."""
    if value is None:
        return "Não disponível"

    value = float(value)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.2f} {unit}"
        value /= 1024


def get_windows_memory():
    """Retorna (total, disponível) em bytes no Windows; caso contrário, (None, None)."""
    if os.name != "nt":
        return None, None

    try:
        import ctypes

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        memory = MEMORYSTATUSEX()
        memory.dwLength = ctypes.sizeof(MEMORYSTATUSEX)

        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
            return int(memory.ullTotalPhys), int(memory.ullAvailPhys)
    except (AttributeError, OSError, ValueError):
        pass

    return None, None


def get_local_ip():
    """Tenta descobrir o IP local sem enviar dados para nenhum serviço externo."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except OSError:
        return "Não disponível"


def collect_info():
    """Coleta informações básicas do sistema."""
    info = {
        "Computador": platform.node() or "Não disponível",
        "Usuário": getpass.getuser(),
        "Sistema operacional": platform.system(),
        "Versão do sistema": platform.version(),
        "Versão do Python": platform.python_version(),
        "Arquitetura": platform.architecture()[0],
        "Processador": platform.processor() or "Não identificado",
        "Núcleos lógicos": os.cpu_count() or "Não disponível",
        "Endereço IP local": get_local_ip(),
        "Pasta atual": os.getcwd(),
    }

    total_ram, available_ram = get_windows_memory()
    info["RAM total"] = format_bytes(total_ram)

    if total_ram is not None and available_ram is not None:
        used_ram = total_ram - available_ram
        info["RAM em uso"] = format_bytes(used_ram)
        info["Uso da RAM"] = f"{used_ram / total_ram * 100:.1f}%" if total_ram else "Não disponível"
    else:
        info["RAM em uso"] = "Não disponível nesta plataforma"
        info["Uso da RAM"] = "Não disponível nesta plataforma"

    try:
        disk = shutil.disk_usage(os.getcwd())
        info["Armazenamento total"] = format_bytes(disk.total)
        info["Armazenamento usado"] = format_bytes(disk.used)
        info["Armazenamento livre"] = format_bytes(disk.free)
        info["Uso do armazenamento"] = f"{disk.used / disk.total * 100:.1f}%" if disk.total else "Não disponível"
    except OSError:
        info["Armazenamento total"] = "Não disponível"
        info["Armazenamento usado"] = "Não disponível"
        info["Armazenamento livre"] = "Não disponível"
        info["Uso do armazenamento"] = "Não disponível"

    info["Data e hora"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return info


def show_info(info):
    print("=" * 58)
    print("                    NKZ SYSTEM INFO")
    print("=" * 58)
    for label, value in info.items():
        print(f"{label:<27}: {value}")
    print("=" * 58)


def save_report(info):
    filename = "nkz_system_report.txt"
    try:
        with open(filename, "w", encoding="utf-8") as report:
            report.write("NKZ SYSTEM INFO\n")
            report.write("=" * 58 + "\n")
            for label, value in info.items():
                report.write(f"{label}: {value}\n")
        print(f"\nRelatório salvo em: {os.path.abspath(filename)}")
    except OSError as error:
        print(f"\nNão foi possível salvar o relatório: {error}")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    while True:
        print(
            "\n"
            "+------------------------------------------+\n"
            "|              NKZ SYSTEM INFO             |\n"
            "+------------------------------------------+\n"
            "|  1. Consultar informações                |\n"
            "|  2. Salvar relatório TXT                 |\n"
            "|  3. Sair                                 |\n"
            "+------------------------------------------+"
        )
        choice = input("NKZ > ").strip()

        if choice == "1":
            show_info(collect_info())
        elif choice == "2":
            info = collect_info()
            show_info(info)
            save_report(info)
        elif choice == "3":
            print("NKZ System Info encerrado.")
            break
        else:
            print("Opção inválida. Escolha 1, 2 ou 3.")

        try:
            input("\nPressione ENTER para voltar ao menu...")
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma encerrado.")
            break
        clear_screen()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nNKZ System Info encerrado.")
