import serial
import numpy as np
import time
import subprocess
import json
from bluetooth import *

serial_port = "/dev/ttyUSB0"
baud_rate = 115200
enlarge = 50
header = r"00fe80b7"
tail = r"ffff68ff"

# make raspberry bluetooth discoverable
subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])

# make raspberry USB reset
subprocess.call(['sudo', 'usbreset', '10c4:ea60'])
time.sleep(1)

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)  # set timeout, aviod long wait
except serial.SerialException as e:
    print(f"Error: {e}")
    exit()

# raspberry bluetooth sock connect
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                    service_id = uuid,
                    service_classes = [ uuid, SERIAL_PORT_CLASS ],
                    profiles = [ SERIAL_PORT_PROFILE ],  
                    )
                       
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

def get_yoga_mat_data():
    data = ['']
    pre_data = ""
    next_data = ""
    
    try:
        # clean the buffer
        ser.reset_input_buffer()

        data = ser.read(237).hex()
        print(data)
        
        if header in data:
            arr = data.split(header, 1)
            pre_data = arr[0]
            next_data = arr[1]
            a = next_data + pre_data
            a = a[26:-8]
            a = [int("0x" + a[i:i+2], base=16) for i in range(0, 432, 2)]
            a = np.array(a).reshape((12, 18))
            # diffuse 
            dir = [[0,1],[1,0],[-1,0],[0,-1]]
            for (x, y), value in np.ndenumerate(a):
                if value> 100:
                    for addx,addy in dir:
                        if x+addx>=0 and x+addx<12 and y+addy>=0 and y+addy<18 and a[x+addx][y+addy]<60:
                            a[x+addx][y+addy]=a[x+addx][y+addy]+value/4

            a = (a > 60) * a
            return a
    except serial.SerialTimeoutException as e:
        print(f"Timeout Error: {e}")
        return None
    except serial.SerialException as e:
        print(f"Serial Error: {e}")
        return None

if __name__ == "__main__":
    while True:
        while True:
            flag = False
            try:
                mat_data = get_yoga_mat_data()
                
                if mat_data is not None:
                    client_sock.send(json.dumps(mat_data.tolist()) + "!")
                    time.sleep(0.1)

                    rdata = client_sock.recv(1024)
                
                    while(len(rdata) < 3):
                        time.sleep(0.1)
                        print("none")
                    print(rdata)
            except OSError as e:
                print("connect loss")
                flag = True
            except KeyboardInterrupt:
                print("KeyboardInterrupt: Stopping the program")
                flag = True
            except Exception:
                pass
            finally:
                if (flag):
                    client_sock.close()
                    server_sock.close()
                    if ser.is_open:
                        ser.close()
                    subprocess.call(['sudo', 'usbreset', '10c4:ea60'])
                    time.sleep(1)
                    print("Program terminated")
                    break

        # raspberry bluetooth sock connect
        server_sock=BluetoothSocket( RFCOMM )
        server_sock.bind(("",PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        advertise_service( server_sock, "SampleServer",
                            service_id = uuid,
                            service_classes = [ uuid, SERIAL_PORT_CLASS ],
                            profiles = [ SERIAL_PORT_PROFILE ],  
                            )
                               
        print("Waiting for connection on RFCOMM channel %d" % port)

        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)
        
        ser.open()
