import serial
import time
import matplotlib.pyplot as plt

port = 'COM6'
baudrate = 115200
data_x = []  
data_y = []  

plt.ion()  
fig, ax = plt.subplots()
line, = ax.plot(data_x, data_y, label='RPM')
ax.set_ylim(0, 9000) 
plt.legend()
plt.xlabel("SEGUNDOS")
plt.ylabel("RPM")
plt.title("RPM del disco")

try:
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(2) 

    print(f"Conectado al puerto {port}")

    while True:
        if ser.in_waiting > 0:
            # Leer datos binarios
            data = ser.read(7)
            BIT1_R = data[2]
            BIT2_R = data[3]
            BIT1_T = data[4]
            CHK = data[5]
            if (BIT1_R ^ BIT2_R ^ BIT1_T ^ 15) == CHK:
                RPM = (BIT2_R << 8) | BIT1_R
                SEGUNDOS = BIT1_T
            
            print(f"RPM: {RPM} y TIEMPO: {SEGUNDOS}")
            data_x.append(SEGUNDOS)
            data_y.append(RPM)

            if SEGUNDOS == 1:
                data_x.clear()  
                data_y.clear()  


            line.set_xdata(data_x)
            line.set_ydata(data_y)

    
            ax.relim()
            ax.autoscale_view()

            plt.draw()
            plt.pause(0.01)  # Pausar para actualizar la gráfica

except serial.SerialException as e:
    print(f"No se pudo conectar al puerto {port}: {e}")


finally:
    if ser.is_open:
        ser.close()
        print(f"Puerto {port} cerrado.")
