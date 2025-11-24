import socket
import time
import random
import sys
import os

# --- FIX START: Dynamic Import Path ---
# Get the absolute path to the folder containing this file (the 'src' folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add this folder to sys.path so Python looks here for modules
sys.path.append(current_dir)

# Now we can import ITStudent directly
from ITStudent import ITStudent
# --- FIX END ---

PROGRAMMES = ["BSc IT", "Computer Science", "BSC", "BEng"]
COURSES = ["CS101", "CS102", "MATH101", "ENG101", "DS201", "NET301"]

def generate_student_xml():
    name = random.choice(['Lungelo','Michael','Aisha','Sipho','Nokuthula','Thabo'])
    student_id = ''.join(str(random.randint(0,9)) for _ in range(8))
    programme = random.choice(PROGRAMMES)
    num_courses = random.randint(3,5)
    courses = random.sample(COURSES, num_courses)
    marks = [random.randint(0,100) for _ in range(num_courses)]
    
    student = ITStudent(name, student_id, programme, courses, marks)
    return student.to_xml_string()

def run_server(host='127.0.0.1', port=9009, delay=1.0):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allow reusing the address to avoid "Address already in use" errors
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        s.bind((host, port))
        s.listen(1)
        print(f"[Socket Producer] Listening on {host}:{port}")
        
        conn, addr = s.accept()
        with conn:
            print(f"[Socket Producer] Connection from {addr}")
            try:
                while True:
                    xml = generate_student_xml()
                    data = xml.encode('utf-8')
                    
                    # Send length prefix (4 bytes, big endian) then the data
                    conn.sendall(len(data).to_bytes(4, byteorder='big'))
                    conn.sendall(data)
                    
                    print("[Socket Producer] Sent one student XML")
                    time.sleep(delay)
            except (BrokenPipeError, ConnectionResetError):
                print("[Socket Producer] Connection closed by client.")
            except Exception as e:
                print(f"[Socket Producer] Error: {e}")

if __name__ == "__main__":
    run_server()