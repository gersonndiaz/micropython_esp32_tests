import network

# Configuración WiFi
ssid = 'SSID'
password = 'PASSWORD'

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    pass

def main():
    print('Conexión WiFi establecida')
    print(wifi.ifconfig())

if __name__ == "__main__":
    main()