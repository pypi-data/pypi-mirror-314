from colorama import Fore, Style  # Pastikan colorama diimpor jika menggunakan warna

class ASCIITools:
    _displayed = False  # Defaultnya di-set False, artinya ASCII belum pernah ditampilkan

    @staticmethod
    def print_ascii_intro():
        if not ASCIITools._displayed:
            ascii_art = r"""
███████╗██╗  ██╗ █████╗ ██████╗ ███████╗    ██╗████████╗    ██╗  ██╗██╗   ██╗██████╗ 
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔════╝    ██║╚══██╔══╝    ██║  ██║██║   ██║██╔══██╗
███████╗███████║███████║██████╔╝█████╗      ██║   ██║       ███████║██║   ██║██████╔╝
╚════██║██╔══██║██╔══██║██╔══██╗██╔══╝      ██║   ██║       ██╔══██║██║   ██║██╔══██╗
███████║██║  ██║██║  ██║██║  ██║███████╗    ██║   ██║       ██║  ██║╚██████╔╝██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝   ╚═╝       ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ 

Telegram Channel : @SHAREITHUB_COM
Youtube Channel : @SHAREITHUB_COM
"""
            print(f"{Fore.GREEN}{ascii_art}{Style.RESET_ALL}")
            ASCIITools._displayed = True
