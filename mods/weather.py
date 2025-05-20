def register_commands(console_os):
    """Регистрация команд мода"""
    console_os.commands['weather'] = show_weather

def unregister_commands(console_os):
    """Удаление команд мода"""
    if 'weather' in console_os.commands:
        del console_os.commands['weather']

def show_weather(args):
    """Показывает текущую погоду"""
    from colorama import Style
    import requests
    import json
    
    try:
        # Получаем погоду с OpenWeatherMap API
        api_key = "NONE"  # Замените на ваш API ключ с сайта openweathermap.org
        
        if api_key == "NONE":
            print(f"\n{Style.RESET_ALL}Для использования команды погоды нужно получить API ключ:")
            print("1. Зарегистрируйтесь на https://openweathermap.org/")
            print("2. Войдите в свой аккаунт")
            print("3. Перейдите в раздел 'My API Keys'")
            print("4. Скопируйте ваш API ключ")
            print("5. Откройте файл mods/weather.py")
            print("6. Замените 'YOUR_API_KEY' на ваш ключ")
            print("7. Перезагрузите мод командой: mod reload weather")
            return
            
        city = " ".join(args) if args else "Moscow"
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
        response = requests.get(url)
        data = json.loads(response.text)
        
        if response.status_code == 200:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            
            print(f"\nПогода в городе {city}:")
            print(f"Температура: {temp}°C")
            print(f"Влажность: {humidity}%")
            print(f"Описание: {description}")
            print(f"Скорость ветра: {wind_speed} м/с")
        else:
            print(f"Ошибка при получении данных о погоде: {data['message']}")
            if response.status_code == 401:
                print("Неверный API ключ. Проверьте правильность ключа в файле mods/weather.py")
            
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        print("Убедитесь, что у вас есть доступ к интернету и установлен модуль requests")
        print("Установите его командой: pip install requests") 