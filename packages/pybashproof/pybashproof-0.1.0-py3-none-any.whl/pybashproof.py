import subprocess
import threading
import datetime
import queue
import readline
import getpass
import socket
import argparse
import hashlib
import os





def calculate_sha256(file_path):
    """
    Calculate the SHA-256 hash of a given file.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def close_case(log_file):
    """
    Close log, calculate sha256.
    """
    if not os.path.exists(log_file):
        print("\nERROR: No logfile to close case!\n")
        return
    write_to_log(log_file, "----------------------------------")
    write_to_log(log_file, "------------ CASE DONE -----------")
    sha256 = calculate_sha256(log_file)
    sha256_log_file = os.path.expanduser("~/bashproof_sha256.log")
    with open(sha256_log_file, "w") as f:
        f.write(sha256)
    print(f"\nSHA-256 hash of log file written to {sha256_log_file}")

    closed_log_file = os.path.expanduser("~/bashproof_closed.log")
    os.rename(log_file, closed_log_file)
    print(f"Log file renamed to {closed_log_file}\n")





def get_time():
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def write_to_log(log_file, message):
    """
    Append a timestamped message to a log file.
    """
    with open(log_file, "a") as f:
        f.write(f"{get_time()} {message}\n")

def read_output(process, log_file, output_queue, marker):
    """
    Continuously read and process the output from a subprocess.
    """
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            if marker in output:
                output_queue.put("DONE")
            else:
                print(output, end="")
                write_to_log(log_file, f"<-- [stdOUT] {output.strip()}")

def flush_stderr(process, log_file):
    """
    Continuously read from a process's standard error stream and log any errors.
    """
    while True:
        error = process.stderr.readline()
        if error == "" and process.poll() is not None:
            break
        if error:
            print(error, end="")
            write_to_log(log_file, f"<-- [stdERR] {error.strip()}")





def main():
    parser = argparse.ArgumentParser(description="Track bash shell activity.")
    parser.add_argument("-c", "--close", action="store_true", help="Close case - work finished.")
    args = parser.parse_args()

    log_file = os.path.expanduser("~/bashproof.log")

    if args.close:
        close_case(log_file)
        return

    current_user = getpass.getuser()
    current_host = socket.gethostname()

    print(f"\n{get_time()} - Your shell is now TRACKED!\n")
    write_to_log(log_file, "")
    write_to_log(log_file, "----------------------------------")
    write_to_log(log_file, "STARTED SHELL-TRACKING")
    write_to_log(log_file, "----------------------------------")
    write_to_log(log_file, f"HOST: {current_host}; USER: {current_user}")
    write_to_log(log_file, "----------------------------------")
    write_to_log(log_file, "")
    
    marker = "END_OF_COMMAND_OUTPUT"

    # run bash
    process = subprocess.Popen(
        ["/bin/bash"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # track command completion
    output_queue = queue.Queue()

    output_thread = threading.Thread(target=read_output, args=(process, log_file, output_queue, marker), daemon=True)
    error_thread = threading.Thread(target=flush_stderr, args=(process, log_file), daemon=True)
    output_thread.start()
    error_thread.start()

    try:
        while True:
            # prompt input
            print("$ ", end="", flush=True)
            user_input = input()

            # in-memory history
            if user_input.strip():
                readline.add_history(user_input)

            # log input
            write_to_log(log_file, f"--> [ stdIN] {user_input}")

            # send input
            print("────────────────────────────────────────────────────")
            write_to_log(log_file, "────────────────────────────────────────────────────")
            process.stdin.write(user_input + f"\necho {marker}\n")
            process.stdin.flush()

            # wait for input-end marker, blocks until "DONE" message is put into queue
            output_queue.get()
            print("────────────────────────────────────────────────────")
            write_to_log(log_file, "────────────────────────────────────────────────────")

    except KeyboardInterrupt:
        write_to_log(log_file, "")
        write_to_log(log_file, "----------------------------------")
        write_to_log(log_file, "TERMINATED SHELL-TRACKING")
        write_to_log(log_file, "----------------------------------")
        print(f"\n{get_time()} - Your shell is now UNTRACKED!\n")
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    main()
