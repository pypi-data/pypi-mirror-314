def get_des_cap():
    des_cap = {
        "platformName": "Android",
        "appium:platformVersion": "11",  # Versión de Android del emulador
        "appium:deviceName": "emulator-5554",  # Nombre del dispositivo emulador
        "appium:automationName": "UiAutomator2",  # Motor de automatización
        "appium:appPackage": "com.example.florales",  # Paquete de la aplicación
        "appium:appActivity": ".MainActivity",  # Actividad principal de la aplicación
        "app": "C:\\Users\\Usuario\\UniversidadLabs\\proyecto-si8811a-2024-ii-u1-desarrollomovil_corrales_viveros\\build\\app\\outputs\\flutter-apk\\app-debug.apk",
        "noReset": "false",  # No reiniciar la aplicación entre sesiones
        "appWaitForLaunch": "false",
        "newCommandTimeout": "120",  # Tiempo de espera para comandos
        "autoAcceptAlerts": "true"  # Aceptar alertas automáticamente
    }
    return des_cap