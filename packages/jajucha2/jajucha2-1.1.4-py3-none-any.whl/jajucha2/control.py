# jajucha/control.py
import socket
import time
import keyboard
import re
# Server address and port
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22222
UDP_PORT = 33333


def init_motor():
    send_message('45455009')

def stop_motor():
    send_message('45454500')

def set_motor(left = 0,right = 0,speed = 0):

    #clip the steering
    if(left > 10):
        left = 10
    elif(left < -10):
        left = -10
    
    if(right > 10):
        right = 10  
    elif(right < -10):  
        right = -10

    #clip the speed
    if(speed > 30):
        speed = 30
    elif(speed < -30):
        speed = -30

    left = 45 - left
    right = 45 - right
    speed = 50 - speed 

    message = f"{left}{right}{speed}09"
    send_message(str(message))

def get_voltage():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_ADDRESS, UDP_PORT))
    extracted_numbers = []

    data, addr = sock.recvfrom(1024)
    output = re.findall(r'\d+', data.decode())

    voltage = (int(output[0][:3])/10 + 0.6)  # First 3 characters
    current = int(output[0][3:5])/10 # Next 2 characters
    angle = int(int(output[0][5:7])*(100/99)*3.6) # Last 2 characters

    sock.close()

    return output

def get_batt_percentage():
    voltage = get_voltage()
    batt_percentage = ((voltage/2 - 6.5) / (8.4 - 6.5) * 100)
    return batt_percentage

def get_current():
    extracted_numbers = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_ADDRESS, UDP_PORT))

    data, addr = sock.recvfrom(1024)
    output = re.findall(r'\d+', data.decode())

    voltage = int(output[0][:3])/10  # First 3 characters
    current = int(output[0][3:5])/10 # Next 2 characters
    angle = int(int(output[0][5:7])*(100/99)*3.6) # Last 2 characters

    sock.close()

    return current

def get_angle():
    extracted_numbers = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_ADDRESS, UDP_PORT))

    data, addr = sock.recvfrom(1024)
    output = re.findall(r'\d+', data.decode())

    voltage = int(output[0][:3])/10  # First 3 characters
    current = int(output[0][3:5])/10 # Next 2 characters
    angle = (int(output[0][5:7])*(100/99)*3.6) # Last 2 characters

    sock.close()

    return angle

def send_message(message):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send message to the server
        client_socket.sendto(message.encode(), (SERVER_ADDRESS, SERVER_PORT))
    finally:
        # Close the socket
        client_socket.close()
