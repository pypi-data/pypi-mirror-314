""" This file runs the server and two app instances. """
import subprocess

import util


if __name__ == '__main__':
    server_port = util.read_config('src/config.yaml')['server']['port']
    client_port1 = util.read_config('src/config.yaml')['client']['port1']
    client_port2 = util.read_config('src/config.yaml')['client']['port2']

    ## Start FastAPI server
    # os.system("uvicorn server:app --reload --port 8000")
    # os.system("uvicorn server:app --reload --port 8000 --workers 4")
    command_0 = ["uvicorn", "src.server:app", "--reload", "--port", server_port]
    process_0 = subprocess.Popen(command_0)

    ## Command to run the two Streamlit instances
    print('reaching streamlit')
    command_1 = ["streamlit", "run", "src/app.py", "--server.port", client_port1, server_port]
    command_2 = ["streamlit", "run", "src/app.py", "--server.port", client_port2, server_port]

    # Start both Streamlit instances as separate processes
    process_1 = subprocess.Popen(command_1)
    process_2 = subprocess.Popen(command_2)
    # Optional: Wait for both processes to complete (will keep main.py running)
    process_0.wait()
    process_1.wait()
    process_2.wait()
