from micropython import const
import ubluetooth
from machine import Timer

_UUID_SERVICE = ubluetooth.UUID('12345678-1234-5678-1234-56789abcdef0')
_UUID_CHAR = ubluetooth.UUID('12345678-1234-5678-1234-56789abcdef1')
_FLAG_READ = const(0x0002)
_FLAG_WRITE = const(0x0008)

class BLEServer:
    def __init__(self):
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
        self.timer = Timer(-1)
        self.connections = set()
        self.register_service()
        self.advertise()

    def register_service(self):
        self.service = self.ble.gatts_register_services([
            (_UUID_SERVICE, ((_UUID_CHAR, _FLAG_READ | _FLAG_WRITE),))
        ])
        self.service_handle = self.service[0][0]

    def ble_irq(self, event, data):
        if event == 1:  # _IRQ_CENTRAL_CONNECT
            conn_handle, _, _ = data
            print("Dispositivo conectado:", conn_handle)
            self.connections.add(conn_handle)
        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT
            conn_handle, _, _ = data
            print("Dispositivo desconectado:", conn_handle)
            self.connections.discard(conn_handle)
            self.advertise()

    def advertise(self, name='ESP32_BLE_Server'):
        name_data = bytes(name, 'utf-8')
        adv_data = bytearray(2 + len(name_data))
        adv_data[0] = len(name_data) + 1  # Length of the field
        adv_data[1] = 0x09  # Field type (Complete Local Name)
        adv_data[2:] = name_data
        self.ble.gap_advertise(100000, adv_data=adv_data)

def main():
    ble_server = BLEServer()
    print("Servidor BLE iniciado, esperando conexiones...")
    #try:
    #    while True:
    #        #print("Ejecutando!")
    #        pass  # Mantener el script en ejecución
    #except KeyboardInterrupt:
    #    print("Script detenido manualmente")

if __name__ == "__main__":
    main()


