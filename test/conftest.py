import pytest
import socket
import subprocess
import time
import os

@pytest.fixture(scope="module")
def erp_server():
    """Starts and stops the ERP server for the test module."""
    # Ensure the port is free before starting the server
    port = 8000
    try:
        if os.name == 'nt':
            # This command is more complex to avoid reliance on non-standard Windows tools like awk
            command = f"for /f \"tokens=5\" %a in ('netstat -ano ^| findstr :{port}') do taskkill /F /PID %a"
            subprocess.run(command, shell=True, check=True, capture_output=True)
        else:
            subprocess.run(f"lsof -t -i:{port} | xargs kill -9", shell=True, check=True)
        print(f"\n--- Killed existing process on port {port} ---")
    except (subprocess.CalledProcessError, FileNotFoundError):
        # No process was running on the port, which is fine
        pass

    # Command to run the ERP server
    command = ["uv", "run", "python", "app/mcp/erp_server.py"]
    
    # Start the server as a background process
    server_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Quick check to see if the process terminated immediately
    time.sleep(2) # Give it a moment to potentially fail
    if server_process.poll() is not None:
        stdout, stderr = server_process.communicate()
        pytest.fail(f"Failed to start ERP server. Error: {stderr.decode(errors='ignore')}", pytrace=False)

    # Poll the server to see if it's up
    for _ in range(10):  # Try for 10 seconds
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                break
        except (socket.timeout, ConnectionRefusedError):
            time.sleep(1)
    else:
        pytest.fail(f"Server on port {port} did not start within 10 seconds.")
    
    # Check if the server started successfully
    if server_process.poll() is not None:
        # The process terminated early, read error output
        stdout, stderr = server_process.communicate()
        pytest.fail(f"Failed to start ERP server. Error: {stderr.decode(errors='ignore')}", pytrace=False)
        
    print("\n--- ERP Server Started ---")
    
    # Yield control to the tests
    yield server_process
    
    # After tests are done, terminate the server
    print("\n--- Shutting down ERP Server ---")
    # Use taskkill on Windows for a more forceful shutdown of the process tree
    if os.name == 'nt':
        subprocess.run(f"taskkill /F /PID {server_process.pid} /T", check=True)
    else:
        server_process.terminate()
    server_process.wait()
    print("--- ERP Server Shut Down ---")