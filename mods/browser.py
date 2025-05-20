import os
import webbrowser
import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Style

def register_commands(console_os):
    """Регистрация команд для мода браузера"""
    console_os.commands['browser'] = browser_command
    console_os.commands['search'] = search_command
    console_os.commands['download'] = download_command
    console_os.commands['view'] = view_command

def unregister_commands(console_os):
    """Удаление команд мода браузера"""
    del console_os.commands['browser']
    del console_os.commands['search']
    del console_os.commands['download']
    del console_os.commands['view']

def browser_command(args):
    """Основная команда браузера"""
    if not args:
        print(f"{Fore.CYAN}Доступные команды браузера:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}browser open <url>{Style.RESET_ALL} - Открыть URL в системном браузере")
        print(f"{Fore.YELLOW}browser search <запрос>{Style.RESET_ALL} - Поиск в интернете")
        print(f"{Fore.YELLOW}browser download <url> [имя_файла]{Style.RESET_ALL} - Скачать файл")
        print(f"{Fore.YELLOW}browser view <url>{Style.RESET_ALL} - Просмотр текстового содержимого страницы")
        return

    subcommand = args[0].lower()
    
    if subcommand == 'open':
        if len(args) < 2:
            print(f"{Fore.RED}Укажите URL для открытия{Style.RESET_ALL}")
            return
        url = args[1]
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        webbrowser.open(url)
        print(f"{Fore.GREEN}Открываю {url} в браузере{Style.RESET_ALL}")
        
    elif subcommand == 'search':
        if len(args) < 2:
            print(f"{Fore.RED}Укажите поисковый запрос{Style.RESET_ALL}")
            return
        query = ' '.join(args[1:])
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        print(f"{Fore.GREEN}Выполняю поиск: {query}{Style.RESET_ALL}")
        
    elif subcommand == 'download':
        if len(args) < 2:
            print(f"{Fore.RED}Укажите URL для скачивания{Style.RESET_ALL}")
            return
        url = args[1]
        filename = args[2] if len(args) > 2 else url.split('/')[-1]
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"{Fore.GREEN}Файл успешно скачан: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Ошибка при скачивании: {str(e)}{Style.RESET_ALL}")
            
    elif subcommand == 'view':
        if len(args) < 2:
            print(f"{Fore.RED}Укажите URL для просмотра{Style.RESET_ALL}")
            return
        url = args[1]
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Удаляем скрипты и стили
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Получаем текст
            text = soup.get_text()
            
            # Разбиваем на строки и удаляем пустые
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Выводим первые 1000 символов
            print(f"{Fore.CYAN}Содержимое страницы:{Style.RESET_ALL}")
            print(text[:1000])
            if len(text) > 1000:
                print(f"{Fore.YELLOW}... (показаны первые 1000 символов){Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}Ошибка при получении содержимого страницы: {str(e)}{Style.RESET_ALL}")
            
    else:
        print(f"{Fore.RED}Неизвестная команда браузера{Style.RESET_ALL}")

def search_command(args):
    """Команда поиска (альтернативный синтаксис)"""
    if not args:
        print(f"{Fore.RED}Укажите поисковый запрос{Style.RESET_ALL}")
        return
    search_url = f"https://www.google.com/search?q={' '.join(args)}"
    webbrowser.open(search_url)
    print(f"{Fore.GREEN}Выполняю поиск: {' '.join(args)}{Style.RESET_ALL}")

def download_command(args):
    """Команда скачивания (альтернативный синтаксис)"""
    if not args:
        print(f"{Fore.RED}Укажите URL для скачивания{Style.RESET_ALL}")
        return
    browser_command(['download'] + args)

def view_command(args):
    """Команда просмотра (альтернативный синтаксис)"""
    if not args:
        print(f"{Fore.RED}Укажите URL для просмотра{Style.RESET_ALL}")
        return
    browser_command(['view'] + args)
