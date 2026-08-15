import csv
import time
from datetime import datetime
from pymodbus.client import ModbusSerialClient

SERIAL_PORT = "COM3" 
BAUDRATE = 9600

# Sensor RS485 Slave IDs
THERMOCOUPLE_SLAVE_ID = 1  # Reads Inlet Temp, Mould Temp, Exhaust Temp
MOULD_HUM_SLAVE_ID = 2     # Reads Mould Humidity
EXHAUST_HUM_SLAVE_ID = 3   # Reads Exhaust Humidity
FLOW_SLAVE_ID = 4          # Reads Inlet Airflow (L/min)

CSV_FILENAME = "hotair_drying_data.csv"
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
            "Inlet Temp (°C)",
            "Inlet Airflow (L/min)",
            "Mould Temp (°C)", 
            "Mould Humidity (%)",
            "Exhaust Temp (°C)",
            "Exhaust Humidity (%)"
        ])

    print(f"Opening Serial Port {SERIAL_PORT}...")
    if not client.connect():
        print(f"Error: Could not open {SERIAL_PORT}. Check your USB-to-RS485 adapter.")
        return

    print("Connected to RS485 bus. Starting hot air data collection...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            current_time = datetime.now().isoformat(timespec='seconds')
            
            # Read 3 temperatures (Inlet, Mould, Exhaust) from the multi-channel thermocouple module
            temp_response = client.read_holding_registers(address=0, count=3, slave=THERMOCOUPLE_SLAVE_ID)
            
            # Read Airflow from the flow sensor
            flow_response = client.read_holding_registers(address=0, count=1, slave=FLOW_SLAVE_ID)
            
            # Read Humidities from two separate sensors
            mould_hum_response = client.read_holding_registers(address=1, count=1, slave=MOULD_HUM_SLAVE_ID)
            exhaust_hum_response = client.read_holding_registers(address=1, count=1, slave=EXHAUST_HUM_SLAVE_ID)

            # Process raw data
            if (temp_response.isError() or flow_response.isError() or 
                mould_hum_response.isError() or exhaust_hum_response.isError()):
                print(f"[{current_time}] Communication Error.")
            else:

                inlet_temp   = round(temp_response.registers[0] * 0.1, 1)
                mould_temp   = round(temp_response.registers[1] * 0.1, 1)
                exhaust_temp = round(temp_response.registers[2] * 0.1, 1)
                
                inlet_airflow    = round(flow_response.registers[0] * 0.1, 1)
                mould_humidity   = round(mould_hum_response.registers[0] * 0.1, 1)
                exhaust_humidity = round(exhaust_hum_response.registers[0] * 0.1, 1)

                print(f"[{current_time}] "
                      f"Inlet: {inlet_temp}°C ({inlet_airflow} L/min) | "
                      f"Mould: {mould_temp}°C ({mould_humidity}%) | "
                      f"Exhaust: {exhaust_temp}°C ({exhaust_humidity}%)")

                with open(CSV_FILENAME, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        current_time, 
                        inlet_temp, 
                        inlet_airflow,
                        mould_temp, 
                        mould_humidity,
                        exhaust_temp,
                        exhaust_humidity
                    ])

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nData collection stopped by user.")
    
    finally:
        client.close()
        print("Serial port closed safely.")

if __name__ == "__main__":
    main()