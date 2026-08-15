import csv
import time
from datetime import datetime
from pymodbus.client import ModbusSerialClient

SERIAL_PORT = "COM3" 
BAUDRATE = 9600

# Sensor to RS485 bus
THERMOCOUPLE_SLAVE_ID = 1  
VACUUM_SLAVE_ID = 2        

CSV_FILENAME = "vacuum_drying_data.csv"
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
            "Oven Temp (°C)", 
            "Shelf Temp (°C)", 
            "Core Temp (°C)", 
            "Vacuum Level (mBar)"
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
            
            # Read vacuum sensor
            vacuum_response = client.read_holding_registers(address=1, count=1, slave=VACUUM_SLAVE_ID)

            # Process raw data
            if temp_response.isError() or vacuum_response.isError():
                print(f"[{current_time}] Communication Error.")
            else:

                oven_temp  = round(temp_response.registers[0] * 0.1, 1)
                shelf_temp = round(temp_response.registers[1] * 0.1, 1)
                core_temp  = round(temp_response.registers[2] * 0.1, 1)
                
                vacuum_level = round(vacuum_response.registers[0] * 0.1, 1)

                print(f"[{current_time}] "
                      f"Oven: {oven_temp}°C | "
                      f"Shelf: {shelf_temp}°C | "
                      f"Core: {core_temp}°C | "
                      f"Vacuum: {vacuum_level} mBar")

                with open(CSV_FILENAME, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        current_time, 
                        oven_temp, 
                        shelf_temp, 
                        core_temp, 
                        vacuum_level
                    ])

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nData collection stopped by user.")
    
    finally:
        client.close()
        print("Serial port closed safely.")

if __name__ == "__main__":
    main()