import socket
import re

host = '127.0.0.1'
port = 5000

op_func = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
}

client = socket.socket()
client.connect((host, port))

while True:
    server_response = client.recv(1024).decode()
    
    if not server_response:
        print("Server has closed the connection.")
        break

    match = re.search(r'Solve this: (\d+) ([\+\-\*]) (\d+):', server_response)
    if match:
        var1 = int(match.group(1))
        var2 = int(match.group(3))
        operator = match.group(2)
        solution = op_func[operator](var1, var2)
        print(f"Solving: {var1} {operator} {var2} = {solution}")
        client.send(str(solution).encode())
    else:
        print(server_response)

print("All tasks completed.")
