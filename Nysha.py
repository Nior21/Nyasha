# Библиотека для работы с платой Troyka HAT.
import troykahat
import time

# Назначаем константные имена пинам из группы "Analog IO"
# Подключаю манипулятор к следующим пинам.
PIN_AP_SW = 5   # SW
PIN_AP_VRY = 6  # VRY
PIN_AP_VRX = 7  # VRX
# Подключаем сервоприводы к следующим пинам.
PIN_AP_SVY = 1  # Cерва ось X
PIN_AP_SVX = 2  # Cерва ось Y

# Инициируем переменные для работы servo
VRXTask = 0
VRYTask = 0

# Назначаем константные има пинам из группы "Wiring PI IO"
# PIN_WP_XXX

# Создаём объект ap для работы с пинами,
# помеченными как «Analog IO» на плате Troyka HAT.
# Это пины, подключенные к встроенному на плате I²C расширителю
# на микроконтроллере STM32F030F4P6.
ap = troykahat.analog_io()

# Создаём объект wp для работы с пинами,
# помеченными как «Wiring Pi IO» на плате Troyka HAT.
# Это пины, подключенные напрямую к Raspberry Pi через его GPIO-разъём.
#wp = troykahat.wiringpi_io()

# Конфигурируем контакты в режим выхода или выхода.
# ap.pinMode(PIN_AP_XXX, ap.INPUT)
# wp.pinMode(PIN_WP_XXX, wp.OUTPUT)
ap.pinMode(PIN_AP_SW, ap.INPUT)
ap.pinMode(PIN_AP_SW, ap.INPUT)
ap.pinMode(PIN_AP_SW, ap.INPUT)

ap.pinMode(PIN_AP_SVX, ap.OUTPUT)
ap.pinMode(PIN_AP_SVY, ap.OUTPUT)

# Получаем от пользователя значение коллибровочной константы. Если пропустить, то будет значение по-умолчанию
CC = float(input("Введите зачение колибровочной константы: ") or 0.025)
print("Каллибровочная константа = ", CC)

while True:
    # Считываем данные с манипулятора по осям X и Y
    VRXValue = ap.analogRead(PIN_AP_VRX)    
    VRYValue = ap.analogRead(PIN_AP_VRY)

    
    # Задаем значения константам
    marginOfError = 0.1 # Потенциальная погрешность манипулятора (чувствительность)
    
    MID_X = float (48 / 100) # Среднее значение манипулятора по X
    LEFT = float (85 / 100)
    RIGHT = float (0 / 100)
    
    MID_Y = float (49 / 100) # Среднее значение манипулятора по Y
    TOP = float (0 / 100)
    BOTTOM = float (84 / 100)
    
    
    # Оцениваем значения с манипулятора и определяем направление поворота
    if (VRXValue > (MID_X  + marginOfError)):
        VRXTask = VRXTask + CC
        
    if (VRXValue < (MID_X - marginOfError)):
        VRXTask = VRXTask - CC
        
    # Передаем значение на серву Y  
    ap.analogWrite(PIN_AP_SVX, VRXTask)
    
    
    # Выводим значения в консоль получаемые данные
    print('X:', VRXTask, '(', CC, ')', '(', 'X:', int(VRXValue * 100),  'Y:', int(VRYValue * 100), ')')
    
    # Передаем целевые значения по осям X и Y на сервопривод "PIN_AP_SV*"
    ap.analogWrite(PIN_AP_SVX, VRXTask)
    ap.analogWrite(PIN_AP_SVY, VRYTask)
    time.sleep(0.5)
    
    # Отключаем сервоприводы "PIN_AP_SV*" по осям X и Y    
    ap.analogWrite(PIN_AP_SVX, 0)
    ap.analogWrite(PIN_AP_SVY, 0)
    
    time.sleep(0.5)
