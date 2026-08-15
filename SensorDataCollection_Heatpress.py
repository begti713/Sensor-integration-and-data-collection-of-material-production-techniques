import csv
import time
from datetime import datetime
from pymodbus.client import ModbusSerialClient

SERIAL_PORT = "COM3" 
BAUDRATE = 9600

# Sensor to RS485 bus
THERMOCOUPLE_SLAVE_ID = 1  
HUMIDITY_SLAVE_ID = 2     

CSV_FILENAME = "drying_process_data.csv"
POLL_INTERVAL = 5.0  # seconds

def main():
    # Initialize Modbus RTU 
    client = ModbusSerialClient(
        port=SERIAL_PORT,
        baudrate=BAUDRATE,
        timeout=2.0,
        stopbits=1,
        bytesize=8,
        parity='N'
    )

    # Setup CSV
    with open(CSV_FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Timestamp", 
            "Heatpress Temp (°C)", 
            "Mould Temp (°C)", 
            "Core Temp (°C)", 
            "Core Material Humidity (%)"
        ])

    print(f"Opening Serial Port {SERIAL_PORT}...")
    if not client.connect():
        print(f"Error: Could not open {SERIAL_PORT}. Check your USB-to-RS485 adapter.")
        return

    print("Connected to RS485 bus. Starting data collection...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            current_time = datetime.now().isoformat(timespec='seconds')
            
            # Read temperatures sensors
            temp_response = client.read_holding_registers(address=0, count=3, slave=THERMOCOUPLE_SLAVE_ID)
            
            # Read humidity sensor
            hum_response = client.read_holding_registers(address=1, count=1, slave=HUMIDITY_SLAVE_ID)

            # Process raw data
            if temp_response.isError() or hum_response.isError():
                print(f"[{current_time}] Communication Error.")
            else:

                heatpress_temp = round(temp_response.registers[0] * 0.1, 1)
                mould_temp     = round(temp_response.registers[1] * 0.1, 1)
                core_temp      = round(temp_response.registers[2] * 0.1, 1)
                
                material_humidity = round(hum_response.registers[0] * 0.1, 1)

                print(f"[{current_time}] "
                      f"Press: {heatpress_temp}°C | "
                      f"Mould: {mould_temp}°C | "
                      f"Core: {core_temp}°C | "
                      f"Material Hum: {material_humidity}%")

                with open(CSV_FILENAME, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        current_time, 
                        heatpress_temp, 
                        mould_temp, 
                        core_temp, 
                        material_humidity
                    ])

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nData collection stopped by user.")
    
    finally:
        client.close()
        print("Serial port closed safely.")

if __name__ == "__main__":
    main()