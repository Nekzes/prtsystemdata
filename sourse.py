import os
import sys
import time
import datetime
import shutil
from colorama import init, Fore, Style
import platform
import subprocess
import json
from pathlib import Path
import importlib.util

init(autoreset=True)

class ConsoleOS:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.path = os.getcwd()
        self.username = os.getenv('USERNAME')
        self.hostname = platform.node()
        self.load_theme()
        self.load_custom_apps()
        self.mods = {}  # Словарь для хранения загруженных модов
        self.commands = {
            'help': self.help,
            'clear': self.clear,
            'exit': self.exit,
            'ls': self.list_files,
            'cd': self.change_dir,
            'mkdir': self.make_dir,
            'rm': self.remove,
            'rmdir': self.remove_dir,
            'cat': self.read_file,
            'echo': self.echo,
            'date': self.show_date,
            'time': self.show_time,
            'whoami': self.whoami,
            'pwd': self.print_working_dir,
            'cp': self.copy_file,
            'mv': self.move_file,
            'sysinfo': self.system_info,
            'prtinfo': self.prtinfo,
            'calcapp': self.open_calculator,
            'touch': self.create_file,
            'theme': self.change_theme,
            'note': self.open_notepad,
            'paint': self.open_paint,
            'exp': self.open_explorer,
            'cmd': self.open_cmd,
            'ctrl': self.open_control_panel,
            'task': self.open_task_manager,
            'app': self.manage_custom_apps,
            'restart': self.restart,
            'open': self.open_custom_app_command,
            'write': self.write_file,
            'rename': self.rename_file,
            'mod': self.manage_mods  # Новая команда для управления модами
        }
        self.load_mods()  # Загружаем моды при инициализации

    def load_theme(self):
        try:
            with open('themes.json', 'r') as f:
                self.themes = json.load(f)
            
            # Загрузка текущей темы из конфигурации
            try:
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    theme_name = config.get('current_theme', 'default')
            except FileNotFoundError:
                theme_name = 'default'
                # Создаем файл конфигурации с настройками по умолчанию
                with open('config.json', 'w') as f:
                    json.dump({'current_theme': 'default'}, f, indent=4)
            
            self.current_theme = self.themes.get(theme_name, self.themes['default'])
        except FileNotFoundError:
            self.themes = {}
            self.current_theme = {
                'primary': 'CYAN',
                'secondary': 'YELLOW',
                'text': 'WHITE',
                'error': 'RED',
                'success': 'GREEN'
            }
            # Создаем файл конфигурации с настройками по умолчанию
            with open('config.json', 'w') as f:
                json.dump({'current_theme': 'default'}, f, indent=4)

    def get_color(self, color_name):
        return getattr(Fore, self.current_theme.get(color_name, 'WHITE'))

    def change_theme(self, args):
        if not args:
            print(f"{self.get_color('error')}Укажите название темы: {', '.join(self.themes.keys())}{Style.RESET_ALL}")
            return
        theme_name = args[0]
        if theme_name in self.themes:
            self.current_theme = self.themes[theme_name]
            # Сохраняем выбранную тему в конфигурацию
            with open('config.json', 'w') as f:
                json.dump({'current_theme': theme_name}, f, indent=4)
            print(f"{self.get_color('success')}Тема успешно изменена на {theme_name}{Style.RESET_ALL}")
        else:
            print(f"{self.get_color('error')}Тема не найдена. Доступные темы: {', '.join(self.themes.keys())}{Style.RESET_ALL}")

    def print_banner(self):
        banner = f"""
{self.get_color('primary')}╭───────────────────────────────────────────────────────────────────────────────────────────╮
║  ██████╗ ██████╗ ████████╗    ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗  {self.get_color('secondary')}v1.2{self.get_color('primary')} ║
║  ██╔══██╗██╔══██╗╚══██╔══╝    ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║       ║
║  ██████╔╝██████╔╝   ██║       ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║       ║
║  ██╔═══╝ ██╔══██╗   ██║       ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║       ║
║  ██║     ██║  ██║   ██║       ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║       ║
║  ╚═╝     ╚═╝  ╚═╝   ╚═╝       ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝       ║
╰───────────────────────────────────────────────────────────────────────────────────────────╯{Style.RESET_ALL}
"""
        print(banner)

    def print_prompt(self):
        username_color = self.get_color('primary')
        hostname_color = self.get_color('secondary')
        path_color = self.get_color('primary')
        prompt_color = self.get_color('text')
        
        print(f"{username_color}{self.username}{Style.RESET_ALL}@{hostname_color}{self.hostname}{Style.RESET_ALL}:{path_color}{self.current_dir}{Style.RESET_ALL}{prompt_color}$ {Style.RESET_ALL}", end='')

    def help(self, args):
        primary_color = self.get_color('primary')
        secondary_color = self.get_color('secondary')
        text_color = self.get_color('text')
        success_color = self.get_color('success')
        
        print(f"""
{secondary_color}Доступные команды:{Style.RESET_ALL}
{primary_color}help{Style.RESET_ALL} - Показать это сообщение
{primary_color}clear{Style.RESET_ALL} - Очистить экран
{primary_color}exit{Style.RESET_ALL} - Выйти из системы
{primary_color}restart{Style.RESET_ALL} - Перезапустить ОС
{primary_color}ls{Style.RESET_ALL} - Показать содержимое директории
{primary_color}cd{Style.RESET_ALL} - Сменить директорию (используйте -m для создания директории)
{primary_color}mkdir{Style.RESET_ALL} - Создать директорию
{primary_color}rm{Style.RESET_ALL} - Удалить файл или директорию
{primary_color}rmdir{Style.RESET_ALL} - Удалить директорию
{primary_color}cat{Style.RESET_ALL} - Показать содержимое файла
{primary_color}echo{Style.RESET_ALL} - Вывести текст
{primary_color}date{Style.RESET_ALL} - Показать дату
{primary_color}time{Style.RESET_ALL} - Показать время
{primary_color}whoami{Style.RESET_ALL} - Показать текущего пользователя
{primary_color}pwd{Style.RESET_ALL} - Показать текущую директорию
{primary_color}cp{Style.RESET_ALL} - Копировать файл
{primary_color}mv{Style.RESET_ALL} - Переместить файл
{primary_color}sysinfo{Style.RESET_ALL} - Показать информацию о системе
{primary_color}prtinfo{Style.RESET_ALL} - Показать информацию о PRT системе
{primary_color}calcapp{Style.RESET_ALL} - Калькулятор
{primary_color}touch{Style.RESET_ALL} - Создать файл
{primary_color}theme{Style.RESET_ALL} - Изменить тему оформления (default, dark, light, matrix, red)

{secondary_color}Стандартные приложения Windows:{Style.RESET_ALL}
{primary_color}note{Style.RESET_ALL} - Запустить Блокнот
{primary_color}calcapp{Style.RESET_ALL} - Запустить Калькулятор
{primary_color}paint{Style.RESET_ALL} - Запустить Paint
{primary_color}exp{Style.RESET_ALL} - Запустить Проводник
{primary_color}cmd{Style.RESET_ALL} - Запустить Командную строку
{primary_color}ctrl{Style.RESET_ALL} - Запустить Панель управления
{primary_color}task{Style.RESET_ALL} - Запустить Диспетчер задач

{secondary_color}Кастомные приложения:{Style.RESET_ALL}""")
        
        if self.custom_apps:
            for name, path in self.custom_apps.items():
                print(f"{primary_color}{name}{Style.RESET_ALL} - {text_color}{path}{Style.RESET_ALL}")
        else:
            print(f"{secondary_color}Нет добавленных приложений{Style.RESET_ALL}")
            
        print(f"""
{secondary_color}Управление приложениями:{Style.RESET_ALL}
{primary_color}app add <имя> <путь>{Style.RESET_ALL} - Добавить новое приложение
{primary_color}app remove <имя>{Style.RESET_ALL} - Удалить приложение
{primary_color}app list{Style.RESET_ALL} - Показать список добавленных приложений
{primary_color}app find <имя_файла>{Style.RESET_ALL} - Найти приложение в системе
{primary_color}open <имя_приложения>{Style.RESET_ALL} - Открыть кастомное приложение
{primary_color}write <имя_файла> <текст>{Style.RESET_ALL} - Записать текст в файл
{primary_color}rename <старое_имя> <новое_имя>{Style.RESET_ALL} - Переименовать файл или директорию
""")

    def clear(self, args):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()

    def exit(self, args):
        print(f"\n{self.get_color('success')}До свидания!{Style.RESET_ALL}")
        sys.exit(0)

    def list_files(self, args):
        try:
            path = args[0] if args else self.current_dir
            items = os.listdir(path)
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    print(f"{self.get_color('primary')}{item}/{Style.RESET_ALL}")
                else:
                    print(f"{self.get_color('text')}{item}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка: {str(e)}{Style.RESET_ALL}")

    def change_dir(self, args):
        if not args:
            return
        try:
            # Объединяем все аргументы в один путь, если их несколько
            new_dir = ' '.join(args[:-1] if len(args) > 1 and args[-1] == '-m' else args)
            create_if_not_exists = len(args) > 1 and args[-1] == '-m'
            
            # Удаляем кавычки, если они есть
            new_dir = new_dir.strip('"\'')
            
            if new_dir == "..":
                self.current_dir = str(Path(self.current_dir).parent)
            else:
                # Преобразуем пути в Path объекты
                current_path = Path(self.current_dir)
                new_path = Path(new_dir)
                
                print(f"{self.get_color('secondary')}Текущий путь: {current_path}{Style.RESET_ALL}")
                print(f"{self.get_color('secondary')}Новый путь: {new_path}{Style.RESET_ALL}")
                
                # Если путь не абсолютный, объединяем с текущей директорией
                if not new_path.is_absolute():
                    new_path = current_path / new_path
                
                print(f"{self.get_color('secondary')}Объединенный путь: {new_path}{Style.RESET_ALL}")
                
                # Преобразуем в абсолютный путь
                new_path = new_path.resolve()
                
                print(f"{self.get_color('secondary')}Абсолютный путь: {new_path}{Style.RESET_ALL}")
                print(f"{self.get_color('secondary')}Существует ли директория: {new_path.is_dir()}{Style.RESET_ALL}")
                
                # Проверка существования директории
                if new_path.is_dir():
                    self.current_dir = str(new_path)
                else:
                    if create_if_not_exists:
                        try:
                            new_path.mkdir(parents=True, exist_ok=True)
                            self.current_dir = str(new_path)
                            print(f"{self.get_color('success')}Директория создана и открыта{Style.RESET_ALL}")
                        except Exception as e:
                            print(f"{self.get_color('error')}Ошибка при создании директории: {str(e)}{Style.RESET_ALL}")
                    else:
                        print(f"{self.get_color('error')}Директория не существует. Используйте 'cd <путь> -m' для создания директории{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка: {str(e)}{Style.RESET_ALL}")

    def make_dir(self, args):
        if not args:
            return
        try:
            os.makedirs(os.path.join(self.current_dir, args[0]))
            print(f"{self.get_color('success')}Директория создана{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка: {str(e)}{Style.RESET_ALL}")

    def remove(self, args):
        if not args:
            return
        try:
            path = os.path.join(self.current_dir, args[0])
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            print(f"{self.get_color('success')}Удалено успешно{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка: {str(e)}{Style.RESET_ALL}")

    def read_file(self, args):
        if not args:
            return
        try:
            with open(os.path.join(self.current_dir, args[0]), 'r', encoding='utf-8') as f:
                print(f"{self.get_color('text')}{f.read()}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка: {str(e)}{Style.RESET_ALL}")

    def echo(self, args):
        if not args:
            return
        print(f"{self.get_color('text')}{' '.join(args)}{Style.RESET_ALL}")

    def show_date(self, args):
        print(f"{self.get_color('text')}{datetime.datetime.now().strftime('%Y-%m-%d')}{Style.RESET_ALL}")

    def show_time(self, args):
        print(f"{self.get_color('text')}{datetime.datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}")

    def whoami(self, args):
        print(f"{self.get_color('text')}{self.username}{Style.RESET_ALL}")

    def print_working_dir(self, args):
        print(f"{self.get_color('text')}{self.current_dir}{Style.RESET_ALL}")

    def copy_file(self, args):
        if len(args) != 2:
            print(f"{self.get_color('error')}Использование: cp <источник> <назначение>{Style.RESET_ALL}")
            return
        try:
            shutil.copy2(
                os.path.join(self.current_dir, args[0]),
                os.path.join(self.current_dir, args[1])
            )
            print(f"{self.get_color('success')}Файл скопирован{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка: {str(e)}{Style.RESET_ALL}")

    def move_file(self, args):
        if len(args) != 2:
            print(f"{self.get_color('error')}Использование: mv <источник> <назначение>{Style.RESET_ALL}")
            return
        try:
            shutil.move(
                os.path.join(self.current_dir, args[0]),
                os.path.join(self.current_dir, args[1])
            )
            print(f"{self.get_color('success')}Файл перемещен{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка: {str(e)}{Style.RESET_ALL}")

    def system_info(self, args):
        """Показать подробную информацию о системе"""
        try:
            # Основная информация о системе
            system_info = {
                "Операционная система": platform.system(),
                "Версия ОС": platform.version(),
                "Архитектура": platform.machine(),
                "Процессор": platform.processor(),
                "Имя компьютера": self.hostname,
                "Текущий пользователь": self.username,
                "Python версия": platform.python_version(),
                "Python путь": sys.executable,
                "Текущая директория": self.current_dir,
                "Время запуска": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Количество ядер CPU": str(os.cpu_count()),
                "Общий объем RAM": "N/A (требуется psutil)",
                "Доступно RAM": "N/A (требуется psutil)",
                "Используется RAM": "N/A (требуется psutil)",
                "Процент использования RAM": "N/A (требуется psutil)"
            }

            # Вывод информации с цветовым оформлением
            print(f"\n{self.get_color('primary')}╭───────────────────────────────────────────────────────────────────────────────────────────╮")
            print(f"║ {self.get_color('secondary')}Информация о системе{self.get_color('primary')}                                                                 ║")
            print(f"╰───────────────────────────────────────────────────────────────────────────────────────────╯{Style.RESET_ALL}\n")

            for key, value in system_info.items():
                print(f"{self.get_color('secondary')}{key}:{Style.RESET_ALL} {self.get_color('text')}{value}{Style.RESET_ALL}")

            # Информация о дисках
            print(f"\n{self.get_color('primary')}╭───────────────────────────────────────────────────────────────────────────────────────────╮")
            print(f"║ {self.get_color('secondary')}Информация о дисках{self.get_color('primary')}                                                                  ║")
            print(f"╰───────────────────────────────────────────────────────────────────────────────────────────╯{Style.RESET_ALL}\n")

            # Получаем информацию о дисках без psutil
            drives = []
            for drive in range(ord('A'), ord('Z') + 1):
                drive_letter = chr(drive) + ':\\'
                if os.path.exists(drive_letter):
                    try:
                        total, used, free = shutil.disk_usage(drive_letter)
                        print(f"{self.get_color('secondary')}Диск {drive_letter}{Style.RESET_ALL}")
                        print(f"  Общий объем: {total / (1024**3):.2f} GB")
                        print(f"  Использовано: {used / (1024**3):.2f} GB")
                        print(f"  Свободно: {free / (1024**3):.2f} GB")
                        print(f"  Использовано: {(used/total)*100:.1f}%")
                    except Exception:
                        continue

        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при получении информации о системе: {str(e)}{Style.RESET_ALL}")

    def prtinfo(self, args):
        """Показать информацию о PRT системе"""
        try:
            # Получаем информацию о файле
            file_size = os.path.getsize(__file__)
            file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(__file__))
            
            # Собираем информацию
            prt_info = {
                "Версия PRT": "1.2",
                "Путь к файлу": __file__,
                "Размер файла": f"{file_size / 1024:.2f} KB",
                "Последнее изменение": file_modified.strftime("%Y-%m-%d %H:%M:%S"),
                "Текущая директория": self.current_dir,
                "Пользователь": self.username,
                "Имя компьютера": self.hostname,
                "Операционная система": platform.system(),
                "Версия ОС": platform.version(),
                "Архитектура": platform.machine(),
                "Python версия": platform.python_version()
            }

            # Вывод информации с цветовым оформлением
            print(f"\n{self.get_color('primary')}╭───────────────────────────────────────────────────────────────────────────────────────────╮")
            print(f"║ {self.get_color('secondary')}Информация о PRT системе{self.get_color('primary')}                                                                  ║")
            print(f"╰───────────────────────────────────────────────────────────────────────────────────────────╯{Style.RESET_ALL}\n")

            for key, value in prt_info.items():
                print(f"{self.get_color('secondary')}{key}:{Style.RESET_ALL} {self.get_color('text')}{value}{Style.RESET_ALL}")

        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при получении информации о PRT системе: {str(e)}{Style.RESET_ALL}")

    def open_calculator(self, args):
        try:
            subprocess.Popen(['calc.exe'])
            print(f"{self.get_color('success')}Калькулятор запущен{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при запуске калькулятора: {str(e)}{Style.RESET_ALL}")

    def create_file(self, args):
        if not args:
            print(f"{self.get_color('error')}Укажите имя файла{Style.RESET_ALL}")
            return
        try:
            file_path = os.path.join(self.current_dir, args[0])
            with open(file_path, 'w') as f:
                pass
            print(f"{self.get_color('success')}Файл создан: {args[0]}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при создании файла: {str(e)}{Style.RESET_ALL}")

    def open_notepad(self, args):
        try:
            subprocess.Popen(['notepad.exe'])
            print(f"{self.get_color('success')}Блокнот запущен{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при запуске блокнота: {str(e)}{Style.RESET_ALL}")

    def open_paint(self, args):
        try:
            subprocess.Popen(['mspaint.exe'])
            print(f"{self.get_color('success')}Paint запущен{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при запуске Paint: {str(e)}{Style.RESET_ALL}")

    def open_explorer(self, args):
        try:
            path = args[0] if args else self.current_dir
            subprocess.Popen(['explorer.exe', path])
            print(f"{self.get_color('success')}Проводник запущен{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при запуске проводника: {str(e)}{Style.RESET_ALL}")

    def open_cmd(self, args):
        try:
            subprocess.Popen(['cmd.exe'])
            print(f"{self.get_color('success')}Командная строка запущена{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при запуске командной строки: {str(e)}{Style.RESET_ALL}")

    def open_control_panel(self, args):
        try:
            subprocess.Popen(['control.exe'])
            print(f"{self.get_color('success')}Панель управления запущена{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при запуске панели управления: {str(e)}{Style.RESET_ALL}")

    def open_task_manager(self, args):
        try:
            if platform.system() == 'Windows':
                # Запуск через shell с повышенными привилегиями
                subprocess.Popen('powershell -Command "Start-Process taskmgr.exe -Verb RunAs"', shell=True)
                print(f"{self.get_color('success')}Диспетчер задач запущен с правами администратора{Style.RESET_ALL}")
            else:
                subprocess.Popen(['taskmgr.exe'])
                print(f"{self.get_color('success')}Диспетчер задач запущен{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при запуске диспетчера задач: {str(e)}{Style.RESET_ALL}")

    def load_custom_apps(self):
        try:
            with open('custom_apps.json', 'r') as f:
                self.custom_apps = json.load(f)
        except FileNotFoundError:
            self.custom_apps = {}
            with open('custom_apps.json', 'w') as f:
                json.dump(self.custom_apps, f, indent=4)

    def save_custom_apps(self):
        with open('custom_apps.json', 'w') as f:
            json.dump(self.custom_apps, f, indent=4)

    def find_application(self, app_name):
        """Поиск приложения в системе"""
        if platform.system() == 'Windows':
            search_paths = [
                os.environ.get('ProgramFiles', 'C:\\Program Files'),
                os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'),
                os.environ.get('LOCALAPPDATA', os.path.expanduser('~\\AppData\\Local')),
                os.environ.get('APPDATA', os.path.expanduser('~\\AppData\\Roaming'))
            ]
            
            print(f"{self.get_color('secondary')}Поиск '{app_name}' в следующих директориях:{Style.RESET_ALL}")
            for path in search_paths:
                print(f"  - {path}")
            
            found_paths = []
            for base_path in search_paths:
                try:
                    for root, dirs, files in os.walk(base_path):
                        for file in files:
                            if file.lower() == app_name.lower():
                                full_path = os.path.join(root, file)
                                found_paths.append(full_path)
                                print(f"{self.get_color('success')}Найден путь: {full_path}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{self.get_color('error')}Ошибка при поиске в {base_path}: {str(e)}{Style.RESET_ALL}")
            
            if found_paths:
                return found_paths[0]  # Возвращаем первый найденный путь
            return None
        return None

    def manage_custom_apps(self, args):
        if not args:
            print(f"{self.get_color('error')}Укажите действие: add, remove, list, find{Style.RESET_ALL}")
            return

        action = args[0].lower()
        
        if action == 'add':
            if len(args) < 3:
                print(f"{self.get_color('error')}Использование: app add <имя_команды> <путь_к_приложению>{Style.RESET_ALL}")
                return
            command_name = args[1]
            # Объединяем все оставшиеся аргументы в один путь
            app_path = ' '.join(args[2:])
            
            if command_name in self.commands:
                print(f"{self.get_color('error')}Команда '{command_name}' уже существует{Style.RESET_ALL}")
                return
                
            # Проверяем существование файла
            if not os.path.exists(app_path):
                # Пробуем найти файл в стандартных местах
                if platform.system() == 'Windows':
                    # Проверяем Program Files
                    program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
                    program_files_x86 = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
                    local_appdata = os.environ.get('LOCALAPPDATA', os.path.expanduser('~\\AppData\\Local'))
                    
                    # Создаем список возможных путей
                    possible_paths = [
                        app_path,
                        os.path.join(program_files, app_path),
                        os.path.join(program_files_x86, app_path),
                        os.path.join(local_appdata, app_path)
                    ]
                    
                    # Проверяем каждый путь
                    for path in possible_paths:
                        # Нормализуем путь
                        normalized_path = os.path.normpath(path)
                        if os.path.exists(normalized_path):
                            app_path = normalized_path
                            break
                    else:
                        # Если путь не найден, пробуем найти файл по имени
                        file_name = os.path.basename(app_path)
                        print(f"{self.get_color('secondary')}Поиск файла '{file_name}'...{Style.RESET_ALL}")
                        found_path = self.find_application(file_name)
                        if found_path:
                            app_path = found_path
                        else:
                            print(f"{self.get_color('error')}Указанный путь не существует. Проверьте правильность пути.{Style.RESET_ALL}")
                            print(f"{self.get_color('secondary')}Используйте 'app find <имя_файла>' для поиска приложения{Style.RESET_ALL}")
                            return
                else:
                    print(f"{self.get_color('error')}Указанный путь не существует{Style.RESET_ALL}")
                    return
                
            # Сохраняем путь в формате raw string
            self.custom_apps[command_name] = app_path
            self.commands[command_name] = lambda args: self.open_custom_app(command_name, args)
            self.save_custom_apps()
            print(f"{self.get_color('success')}Приложение '{command_name}' успешно добавлено{Style.RESET_ALL}")
            print(f"{self.get_color('secondary')}Путь: {app_path}{Style.RESET_ALL}")
            
        elif action == 'remove':
            if len(args) < 2:
                print(f"{self.get_color('error')}Использование: app remove <имя_команды>{Style.RESET_ALL}")
                return
            command_name = args[1]
            
            if command_name not in self.custom_apps:
                print(f"{self.get_color('error')}Приложение '{command_name}' не найдено{Style.RESET_ALL}")
                return
                
            del self.custom_apps[command_name]
            del self.commands[command_name]
            self.save_custom_apps()
            print(f"{self.get_color('success')}Приложение '{command_name}' успешно удалено{Style.RESET_ALL}")
            
        elif action == 'list':
            if not self.custom_apps:
                print(f"{self.get_color('secondary')}Нет добавленных приложений{Style.RESET_ALL}")
                return
                
            print(f"{self.get_color('secondary')}Добавленные приложения:{Style.RESET_ALL}")
            for name, path in self.custom_apps.items():
                print(f"{self.get_color('success')}{name}{Style.RESET_ALL}: {path}")
                
        elif action == 'find':
            if len(args) < 2:
                print(f"{self.get_color('error')}Использование: app find <имя_файла>{Style.RESET_ALL}")
                return
            app_name = args[1]
            found_path = self.find_application(app_name)
            if not found_path:
                print(f"{self.get_color('error')}Приложение '{app_name}' не найдено{Style.RESET_ALL}")
                
        else:
            print(f"{self.get_color('error')}Неизвестное действие. Используйте: add, remove, list, find{Style.RESET_ALL}")

    def open_custom_app(self, command_name, args):
        try:
            app_path = self.custom_apps[command_name]
            # Используем shell=True для корректной обработки путей с пробелами
            subprocess.Popen(app_path, shell=True)
            print(f"{self.get_color('success')}Приложение '{command_name}' запущено{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при запуске приложения '{command_name}': {str(e)}{Style.RESET_ALL}")

    def restart(self, args):
        """Перезапуск ОС"""
        primary_color = self.get_color('primary')
        print(f"\n{primary_color}Перезапуск ОС...{Style.RESET_ALL}")
        time.sleep(1)  # Небольшая задержка для визуального эффекта
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        
        # Получаем путь к текущему скрипту
        script_path = os.path.abspath(sys.argv[0])
        
        # Запускаем новый процесс
        if os.name == 'nt':  # Windows
            subprocess.Popen([sys.executable, script_path])
        else:  # Unix-like systems
            os.execv(sys.executable, [sys.executable, script_path])
        
        # Завершаем текущий процесс
        sys.exit(0)

    def open_custom_app_command(self, args):
        """Открыть кастомное приложение"""
        if not args:
            print(f"{self.get_color('error')}Укажите название приложения для открытия{Style.RESET_ALL}")
            print(f"{self.get_color('secondary')}Доступные приложения:{Style.RESET_ALL}")
            if self.custom_apps:
                for name in self.custom_apps.keys():
                    print(f"{self.get_color('primary')}{name}{Style.RESET_ALL}")
            else:
                print(f"{self.get_color('secondary')}Нет добавленных приложений{Style.RESET_ALL}")
            return

        app_name = args[0]
        if app_name in self.custom_apps:
            try:
                app_path = self.custom_apps[app_name]
                subprocess.Popen(app_path, shell=True)
                print(f"{self.get_color('success')}Приложение '{app_name}' запущено{Style.RESET_ALL}")
            except Exception as e:
                print(f"{self.get_color('error')}Ошибка при запуске приложения '{app_name}': {str(e)}{Style.RESET_ALL}")
        else:
            print(f"{self.get_color('error')}Приложение '{app_name}' не найдено{Style.RESET_ALL}")
            print(f"{self.get_color('secondary')}Используйте 'app list' для просмотра доступных приложений{Style.RESET_ALL}")

    def write_file(self, args):
        """Записать данные в файл"""
        if len(args) < 2:
            print(f"{self.get_color('error')}Использование: write <имя_файла> <текст>{Style.RESET_ALL}")
            print(f"{self.get_color('secondary')}Пример: write test.txt 'Привет, мир!'{Style.RESET_ALL}")
            return

        try:
            file_path = os.path.join(self.current_dir, args[0])
            text = ' '.join(args[1:])
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"{self.get_color('success')}Текст успешно записан в файл '{args[0]}'{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при записи в файл: {str(e)}{Style.RESET_ALL}")

    def rename_file(self, args):
        """Переименовать файл или директорию"""
        if len(args) != 2:
            print(f"{self.get_color('error')}Использование: rename <старое_имя> <новое_имя>{Style.RESET_ALL}")
            print(f"{self.get_color('secondary')}Пример: rename old.txt new.txt{Style.RESET_ALL}")
            return

        try:
            old_path = os.path.join(self.current_dir, args[0])
            new_path = os.path.join(self.current_dir, args[1])
            
            if not os.path.exists(old_path):
                print(f"{self.get_color('error')}Файл или директория '{args[0]}' не существует{Style.RESET_ALL}")
                return
                
            if os.path.exists(new_path):
                print(f"{self.get_color('error')}Файл или директория '{args[1]}' уже существует{Style.RESET_ALL}")
                return
                
            os.rename(old_path, new_path)
            print(f"{self.get_color('success')}Успешно переименовано из '{args[0]}' в '{args[1]}'{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при переименовании: {str(e)}{Style.RESET_ALL}")

    def remove_dir(self, args):
        """Удалить директорию"""
        if not args:
            print(f"{self.get_color('error')}Укажите имя директории для удаления{Style.RESET_ALL}")
            return
        try:
            dir_path = os.path.join(self.current_dir, args[0])
            if not os.path.isdir(dir_path):
                print(f"{self.get_color('error')}'{args[0]}' не является директорией{Style.RESET_ALL}")
                return
            shutil.rmtree(dir_path)
            print(f"{self.get_color('success')}Директория '{args[0]}' успешно удалена{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при удалении директории: {str(e)}{Style.RESET_ALL}")

    def load_mods(self):
        """Загрузка модов из директории mods"""
        mods_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mods')
        if not os.path.exists(mods_dir):
            os.makedirs(mods_dir)
            return

        for filename in os.listdir(mods_dir):
            if filename.endswith('.py'):
                try:
                    mod_name = filename[:-3]  # Убираем расширение .py
                    mod_path = os.path.join(mods_dir, filename)
                    
                    # Загружаем модуль
                    spec = importlib.util.spec_from_file_location(mod_name, mod_path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    
                    # Регистрируем команды из мода
                    if hasattr(mod, 'register_commands'):
                        mod.register_commands(self)
                        self.mods[mod_name] = mod
                        print(f"{self.get_color('success')}Мод '{mod_name}' успешно загружен{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{self.get_color('error')}Ошибка при загрузке мода '{filename}': {str(e)}{Style.RESET_ALL}")

    def manage_mods(self, args):
        """Управление модами"""
        if not args:
            print(f"{self.get_color('error')}Укажите действие: load, unload, list, reload{Style.RESET_ALL}")
            return

        action = args[0].lower()
        
        if action == 'load':
            if len(args) < 2:
                print(f"{self.get_color('error')}Укажите имя мода для загрузки{Style.RESET_ALL}")
                return
            mod_name = args[1]
            self.load_mod(mod_name)
            
        elif action == 'unload':
            if len(args) < 2:
                print(f"{self.get_color('error')}Укажите имя мода для выгрузки{Style.RESET_ALL}")
                return
            mod_name = args[1]
            self.unload_mod(mod_name)
            
        elif action == 'list':
            if not self.mods:
                print(f"{self.get_color('secondary')}Нет загруженных модов{Style.RESET_ALL}")
                return
            print(f"{self.get_color('secondary')}Загруженные моды:{Style.RESET_ALL}")
            for mod_name in self.mods.keys():
                print(f"{self.get_color('primary')}{mod_name}{Style.RESET_ALL}")
                
        elif action == 'reload':
            if len(args) < 2:
                print(f"{self.get_color('error')}Укажите имя мода для перезагрузки{Style.RESET_ALL}")
                return
            mod_name = args[1]
            self.reload_mod(mod_name)
            
        else:
            print(f"{self.get_color('error')}Неизвестное действие. Используйте: load, unload, list, reload{Style.RESET_ALL}")

    def load_mod(self, mod_name):
        """Загрузка конкретного мода"""
        # Убираем расширение .py, если оно есть
        if mod_name.endswith('.py'):
            mod_name = mod_name[:-3]
            print(f"{self.get_color('secondary')}Примечание: расширение .py не нужно указывать{Style.RESET_ALL}")
            
        mods_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mods')
        mod_path = os.path.join(mods_dir, f"{mod_name}.py")
        
        if not os.path.exists(mod_path):
            print(f"{self.get_color('error')}Мод '{mod_name}' не найден в директории mods{Style.RESET_ALL}")
            print(f"{self.get_color('secondary')}Проверьте, что файл {mod_name}.py существует в директории mods{Style.RESET_ALL}")
            return
            
        try:
            spec = importlib.util.spec_from_file_location(mod_name, mod_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            
            if hasattr(mod, 'register_commands'):
                mod.register_commands(self)
                self.mods[mod_name] = mod
                print(f"{self.get_color('success')}Мод '{mod_name}' успешно загружен{Style.RESET_ALL}")
                print(f"{self.get_color('secondary')}Доступные команды:{Style.RESET_ALL}")
                # Показываем список новых команд
                for cmd in [k for k, v in self.commands.items() if v.__module__ == mod.__name__]:
                    print(f"{self.get_color('primary')}{cmd}{Style.RESET_ALL}")
            else:
                print(f"{self.get_color('error')}Мод '{mod_name}' не содержит функцию register_commands{Style.RESET_ALL}")
                print(f"{self.get_color('secondary')}Убедитесь, что в файле мода есть функция register_commands{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при загрузке мода '{mod_name}': {str(e)}{Style.RESET_ALL}")
            print(f"{self.get_color('secondary')}Проверьте синтаксис файла мода и наличие всех необходимых зависимостей{Style.RESET_ALL}")

    def unload_mod(self, mod_name):
        """Выгрузка мода"""
        if mod_name not in self.mods:
            print(f"{self.get_color('error')}Мод '{mod_name}' не загружен{Style.RESET_ALL}")
            return
            
        try:
            # Удаляем команды, зарегистрированные модом
            if hasattr(self.mods[mod_name], 'unregister_commands'):
                self.mods[mod_name].unregister_commands(self)
            del self.mods[mod_name]
            print(f"{self.get_color('success')}Мод '{mod_name}' успешно выгружен{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self.get_color('error')}Ошибка при выгрузке мода '{mod_name}': {str(e)}{Style.RESET_ALL}")

    def reload_mod(self, mod_name):
        """Перезагрузка мода"""
        self.unload_mod(mod_name)
        self.load_mod(mod_name)

    def run(self):
        self.print_banner()
        while True:
            try:
                self.print_prompt()
                command = input().strip()
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0]
                args = parts[1:] if len(parts) > 1 else []
                
                if cmd in self.commands:
                    self.commands[cmd](args)
                else:
                    print(f"{self.get_color('error')}Команда '{cmd}' не найдена. Введите 'help' для списка команд.{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{self.get_color('text')}Для выхода введите 'exit'{Style.RESET_ALL}")
            except Exception as e:
                print(f"{self.get_color('error')}Ошибка: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    console_os = ConsoleOS()
    console_os.run() 