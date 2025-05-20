import random
from colorama import Style

def register_commands(console_os):
    """Регистрация команд мода"""
    console_os.commands['game'] = start_game
    console_os.commands['guess'] = guess_number

def unregister_commands(console_os):
    """Удаление команд мода"""
    if 'game' in console_os.commands:
        del console_os.commands['game']
    if 'guess' in console_os.commands:
        del console_os.commands['guess']

# Глобальные переменные для игры
game_active = False
target_number = 0
attempts = 0
max_attempts = 10

def start_game(args):
    """Начать новую игру"""
    global game_active, target_number, attempts
    
    if game_active:
        print(f"{Style.RESET_ALL}Игра уже запущена! Используйте команду 'guess <число>' для угадывания.")
        return
        
    # Устанавливаем диапазон чисел
    min_num = 1
    max_num = 100
    
    # Генерируем случайное число
    target_number = random.randint(min_num, max_num)
    attempts = 0
    game_active = True
    
    print(f"\n{Style.RESET_ALL}Новая игра началась!")
    print(f"Я загадал число от {min_num} до {max_num}")
    print(f"У вас есть {max_attempts} попыток, чтобы угадать")
    print("Используйте команду 'guess <число>' для угадывания")
    print("Например: guess 50")

def guess_number(args):
    """Угадать число"""
    global game_active, target_number, attempts
    
    if not game_active:
        print(f"{Style.RESET_ALL}Сначала начните игру командой 'game'")
        return
        
    if not args:
        print(f"{Style.RESET_ALL}Укажите число для угадывания")
        print("Например: guess 50")
        return
        
    try:
        guess = int(args[0])
    except ValueError:
        print(f"{Style.RESET_ALL}Пожалуйста, введите число")
        return
        
    attempts += 1
    
    if guess < target_number:
        print(f"{Style.RESET_ALL}Загаданное число больше {guess}")
    elif guess > target_number:
        print(f"{Style.RESET_ALL}Загаданное число меньше {guess}")
    else:
        print(f"\n{Style.RESET_ALL}Поздравляем! Вы угадали число {target_number} за {attempts} попыток!")
        game_active = False
        return
        
    if attempts >= max_attempts:
        print(f"\n{Style.RESET_ALL}Игра окончена! Вы использовали все {max_attempts} попыток")
        print(f"Загаданное число было: {target_number}")
        game_active = False
    else:
        print(f"Осталось попыток: {max_attempts - attempts}") 