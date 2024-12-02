import socket
import random
import threading

host = "127.0.0.1"
port = 5000

operators = ["+", "-", "*"]

op_func = {
    '+': lambda a, b: a + b, 
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b, 
}

tasks = 10
flag = 'flag{123_calc_flag_456}'
timeout_duration = 5  

def handle_client(conn, address):
    print(f"Connected from: {str(address)}")
    sol_count = 0

    while sol_count < tasks:
        var1 = random.randint(1000, 10000)
        var2 = random.randint(1000, 10000)
        operator = random.choice(operators)
        solution = op_func[operator](var1, var2)

        conn.send(f'\nSolve this: {var1} {operator} {var2} (you have {timeout_duration} seconds): '.encode())
        
        
        answer_received = [False]
        user_answer = None

        def receive_answer():
            nonlocal user_answer
            try:
                user_answer = int(conn.recv(1024).decode())
                answer_received[0] = True
            except ValueError:
                answer_received[0] = True  
            except OSError:
                answer_received[0] = True  

        
        answer_thread = threading.Thread(target=receive_answer)
        answer_thread.start()

        
        answer_thread.join(timeout=timeout_duration)

        if not answer_received[0]:
            conn.send("\nTime's up! See you later!\n".encode())
            conn.close()
            return  

        
        if answer_thread.is_alive():
            answer_thread.join()  

        if user_answer is not None and user_answer == solution:
            sol_count += 1
            conn.send(f"\nGreat! Solved: {sol_count} of {tasks} tasks!\n".encode())
        else:
            conn.send('\nNope!\n'.encode())

    try:
        conn.send(f"\nCongrats!\nYour flag: {flag}".encode())
    except OSError:
        print("Client has disconnected before receiving the flag.")
    finally:
        conn.close()
        print(f"Connection with {address} closed.")

if __name__ == "__main__":    
    server = socket.socket()
    server.bind((host, port))
    server.listen(5)

    print(f"Server is listening on {host}:{port}")

    while True:
        try:
            conn, address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, address))
            client_thread.start()
        except KeyboardInterrupt:
            print("\nBye!")
            server.close()
        except: break
