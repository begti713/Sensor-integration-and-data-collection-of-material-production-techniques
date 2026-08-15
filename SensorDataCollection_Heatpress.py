import csv
import time
from pymodbus.client import ModbusSerialClient

SERIAL_PORT = "COM3" 
BAUDRATE = 9600

# Sensor to RS485 bus
THERMOCOUPLE_SLAVE_ID = 1  
HUMIDITY_SLAVE_ID = 2      

CSV_FILENAME = "heatpress_rawdata.csv"
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

    with open(CSV_FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Time (min)", 
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

    start_time = time.time()

    try:
        while True:
            # Calculate elapsed minutes
            elapsed_seconds = time.time() - start_time
            current_minute = round(elapsed_seconds / 60.0, 2)
            
            # Read temperatures sensors
            temp_response = client.read_holding_registers(address=0, count=3, slave=THERMOCOUPLE_SLAVE_ID)
            
            # Read humidity sensor
            hum_response = client.read_holding_registers(address=1, count=1, slave=HUMIDITY_SLAVE_ID)

            # Process raw data
            if temp_response.isError() or hum_response.isError():
                print(f"[Min: {current_minute}] Communication Error.")
            else:

                heatpress_temp = round(temp_response.registers[0] * 0.1, 1)
                mould_temp     = round(temp_response.registers[1] * 0.1, 1)
                core_temp      = round(temp_response.registers[2] * 0.1, 1)
                
                material_humidity = round(hum_response.registers[0] * 0.1, 1)

                print(f"[Min: {current_minute}] "
                      f"Press: {heatpress_temp}°C | "
                      f"Mould: {mould_temp}°C | "
                      f"Core: {core_temp}°C | "
                      f"Material Hum: {material_humidity}%")

                with open(CSV_FILENAME, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    # Write the numerical current_minute instead of a timestamp
                    writer.writerow([
                        current_minute, 
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
