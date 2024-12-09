import paramiko # type: ignore
import sys
import mmap
from tqdm import tqdm # type: ignore
import json

def count_lines_mmap(file_path):
    with open(file_path, 'r+b') as file_handle:
        mm = mmap.mmap(file_handle.fileno(), 0)
        lines = 0
        while mm.readline():
            lines += 1
        mm.close()
        return lines

def stream_trace_file(remote_host, username, password, server_script_path, cache_params):
    """
    Streams a trace file to a remote server using Paramiko and processes it with the server script.

    Args:
        remote_host (str): IP or hostname of the remote server.
        username (str): SSH username.
        password (str): SSH password.
        server_script_path (str): Path to the server script on the remote server
        cache_params (dictionary): Dictionary with all the cache parameters
    """
    try:
        # Establish an SSH connection
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname = remote_host, username = username, password = password)
        print(f"Connected to {remote_host}.")

        # Open a session and execute the server script
        transport = client.get_transport()
        if not transport:
            print("Transport could not be established. The connection might have been closed.")
            return
        else:
            print("Transport established successfully.")


        transport.set_keepalive(30)
        session = transport.open_session()

        if not session:
            print("session could not be established. The connection might have been closed.")
            return
        else:
            print("session established successfully.")

        command = "python3 {server_script_path} {cache_size} {line_size} {ways} {replacement_policy}"
        session.exec_command(command.format(
            server_script_path = server_script_path, 
            cache_size = cache_params.get("cache_size"), 
            line_size = cache_params.get("line_size"), 
            ways = cache_params.get("ways"),
            replacement_policy = cache_params.get("replacement_policy")
        ))

        total_line_count = count_lines_mmap(cache_params.get("trace_file"))

        # Stream the trace file to the remote server
        with open(cache_params.get("trace_file"), "r") as trace_file:
            progress_bar = tqdm(total = total_line_count, desc = "Streaming Trace File", unit = "lines")
            for line in trace_file:
                session.send(line)
                progress_bar.update(1)  # Update progress bar
            progress_bar.close()
        session.shutdown_write()  # Signal that the stream is complete

        # Read output from the server script
        stdout = session.makefile("rb", -1).read().decode()
        stderr = session.makefile_stderr("rb", -1).read().decode()

        print("Server Output:")
        print(stdout)
        if stderr:
            print("Server Errors:")
            print(stderr)

        # Close the session
        session.close()
        client.close()
        print("Connection Closed")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":

    if len(sys.argv) < 6:
        print("Usage: python3 cache_simulator.py <trace_file> <cache_size> <line_size> <ways> <replacement_policy>")
        sys.exit(1)
    try:
        trace_file = sys.argv[1]
        cache_size = int(sys.argv[2])
        line_size = int(sys.argv[3])
        ways = int(sys.argv[4])
        replacement_policy = sys.argv[5]
    except ValueError:
        print("Error: Cache size, line size, and ways must be integers.")
        sys.exit(1)

    with open("credentials.json", "r") as file_handle:
        credentials = json.load(file_handle)

    remote_hosts = credentials.get("remote_hosts")

    print("Available remote hosts: ")
    for index, remote_host in enumerate(remote_hosts):
        print("{index} ==> {remote_host}".format(index = index, remote_host = remote_host))
    remote_host_choice = int(input("Enter your choice: "))

    # Credentials
    remote_host = remote_hosts[remote_host_choice]              # Replace with the Fox server's IP or hostname
    username = credentials.get("username")                      # Replace with your SSH username
    password = credentials.get("password")                      # Replace with your SSH password
    server_script_path = credentials.get("server_script_path")  # Path to the server script on the server. should end with *.py

    cache_params = {
        "trace_file": trace_file,
        "cache_size": cache_size, 
        "line_size": line_size, 
        "ways": ways,
        "replacement_policy": replacement_policy
    }

    stream_trace_file(remote_host, username, password, server_script_path, cache_params)
