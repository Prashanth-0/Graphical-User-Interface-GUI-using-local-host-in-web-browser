from flask import Flask, render_template, request
import subprocess
import threading

app = Flask(__name__)

# This variable will store the real-time output
real_time_output = ""

# Function to run any Nmap command
def run_nmap_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            global real_time_output
            real_time_output += output.strip() + '\n'

# Flask route to display the real-time output and execute Nmap commands
@app.route('/', methods=['GET', 'POST'])
def index():
    global real_time_output

    if request.method == 'POST':
        # Get the Nmap command from the user input
        command = request.form['nmap_command']

        # Start the Nmap command execution in a separate thread
        tool_thread = threading.Thread(target=run_nmap_command, args=(command.split(),))
        tool_thread.start()

    return render_template('index.html', output=real_time_output)

if __name__ == '__main__':
    app.run(debug=True)
