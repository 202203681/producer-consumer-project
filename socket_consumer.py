import socket
import sys
import os

# --- FIX START: Dynamic Import Path ---
# Get the absolute path to the folder containing this file (the 'src' folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add this folder to sys.path so Python looks here for modules
sys.path.append(current_dir)

# Now we can import ITStudent directly without the 'src.' prefix
from ITStudent import ITStudent
# --- FIX END ---

def recv_all(sock, n):
    """Helper to ensure we receive exactly n bytes from the TCP stream."""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def run_client(host='127.0.0.1', port=9009):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print(f"[Socket Consumer] Connected to {host}:{port}")
        except ConnectionRefusedError:
            print(f"[Socket Consumer] Could not connect to {host}:{port}. Is the server running?")
            return

        try:
            while True:
                # 1. Read length prefix (first 4 bytes)
                raw_len = recv_all(s, 4)
                if not raw_len:
                    break
                length = int.from_bytes(raw_len, byteorder='big')
                
                # 2. Read the actual XML data based on the length
                data = recv_all(s, length)
                if not data:
                    break
                
                xml = data.decode('utf-8')
                
                # 3. Write XML to a temporary file so we can use the parsing method
                # Note: We save this in the current directory
                temp_filename = os.path.join(current_dir, "socket_received.xml")
                
                with open(temp_filename, "w", encoding="utf-8") as f:
                    f.write(xml)
                
                # 4. Parse the file back into an object
                student = ITStudent.from_xml_file(temp_filename)
                
                print("--- Socket Consumer Received ---")
                print(f"Name: {student.name}")
                print(f"Student ID: {student.student_id}")
                print(f"Programme: {student.programme}")
                for c, m in zip(student.courses, student.marks):
                    print(f"  {c}: {m}")
                print(f"Average: {student.average():.2f}")
                print(f"Result: {'PASS' if student.passed() else 'FAIL'}")
                print("-" * 30)
                
        except KeyboardInterrupt:
            print("[Socket Consumer] Interrupted by user.")
        except Exception as e:
            print(f"[Socket Consumer] Error: {e}")

if __name__ == "__main__":
    run_client()