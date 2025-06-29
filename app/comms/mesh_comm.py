import asyncio
import platform
from bleak import BleakScanner, BleakAdvertisementData
from bleak.backends.scanner import AdvertisementData

BROADCAST_PREFIX = "RESQNET_ALERT:"

class MeshComm:
    def __init__(self):
        self.platform = platform.system()

    async def broadcast_alert(self, message: str):
        full_message = f"{BROADCAST_PREFIX}{message}"

        print(f"[Broadcasting] {full_message}")
        # NOTE: BLE advertising from Python is limited to Linux
        if self.platform != "Linux":
            raise NotImplementedError("BLE advertising works best on Linux/Raspberry Pi for now.")

        # Use 'bluetooth-advertising' utility like BlueZ tools or custom workaround
        os.system(f"sudo hcitool -i hci0 cmd 0x08 0x0008 {full_message.encode().hex()}")

    async def listen_for_alerts(self):
        def callback(device, advertisement_data: AdvertisementData):
            data_str = advertisement_data.local_name or ""
            if data_str.startswith(BROADCAST_PREFIX):
                print(f"[Received Alert] From {device.address}: {data_str[len(BROADCAST_PREFIX):]}")

        scanner = BleakScanner()
        scanner.register_detection_callback(callback)
        print("[Listening for alerts over BLE]")

        await scanner.start()
        await asyncio.sleep(15)  # Scans for 15 seconds
        await scanner.stop()
