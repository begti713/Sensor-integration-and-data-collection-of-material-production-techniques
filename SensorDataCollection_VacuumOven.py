import csv
import time
from pymodbus.client import ModbusSerialClient

SERIAL_PORT = "COM3" 
BAUDRATE = 9600

# Sensor to RS485 bus
THERMOCOUPLE_SLAVE_ID = 1  
VACUUM_SLAVE_ID = 2        

CSV_FILENAME = "vacuum_drying_data.csv"
POLL_INTERVAL = 5.0  # seconds

def main():
    client = ModbusSerialClient(...)

    # Setup CSV with the updated "Time (min)" header
    with open(CSV_FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Time (min)", 
            "Oven Temp (°C)", 
            "Shelf Temp (°C)", 
            "Core Temp (°C)", 
            "Vacuum Level (mBar)"
        ])

    print(f"Opening Serial Port {SERIAL_PORT}...")
    if not client.connect():
        return

    print("Connected to RS485 bus. Starting data collection...")
    
    # RECORD START TIME HERE
    start_time = time.time()

    try:
        while True:
            # Calculate elapsed minutes
            elapsed_seconds = time.time() - start_time
            current_minute = round(elapsed_seconds / 60.0, 2)
            
            temp_response = client.read_holding_registers(address=0, count=3, slave=THERMOCOUPLE_SLAVE_ID)
            vacuum_response = client.read_holding_registers(address=1, count=1, slave=VACUUM_SLAVE_ID)

            if temp_response.isError() or vacuum_response.isError():
                print(f"[Min: {current_minute}] Communication Error.")
            else:
                oven_temp  = round(temp_response.registers[0] * 0.1, 1)
                shelf_temp = round(temp_response.registers[1] * 0.1, 1)
                core_temp  = round(temp_response.registers[2] * 0.1, 1)
                vacuum_level = round(vacuum_response.registers[0] * 0.1, 1)

                print(f"[Min: {current_minute}] "
                      f"Oven: {oven_temp}°C | "
                      f"Shelf: {shelf_temp}°C | "
                      f"Core: {core_temp}°C | "
                      f"Vacuum: {vacuum_level} mBar")

                with open(CSV_FILENAME, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    # Write the current_minute instead of the datetime string
                    writer.writerow([
                        current_minute, 
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

if __name__ == "__main__":
    main()
