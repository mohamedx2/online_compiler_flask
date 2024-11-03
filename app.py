from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import subprocess
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    # Serve the HTML template
    return render_template("index.html")

types = [{"bl": "ENTIER", "c": "int"}, {"bl": "NOMBRE", "c": "float"}]

def inter(program_lines):
    c_code = ""
    inside_condition = False  # Track if we're inside a conditional block
    condition_code = ""  # Holds code within the condition

    for line in program_lines:
        # Remove leading and trailing whitespace (including tabs) from the line
        line = line.strip()
        # Split the line into parts and strip whitespace from each part
        parts = [part.strip() for part in line.split(" ") if part.strip()]
        if not parts:
            continue  # Skip empty lines
        
        opcode = parts[0]
        line_code = ""

        if opcode == "ECRIRE":
            line_code += 'printf("'
            line_code += parts[1]
            for i in range(2, len(parts)):
                line_code += " " + parts[i]
            line_code += '");'
        elif opcode == "LIRE":
            line_code += "scanf("
            line_code += '"%f"' if parts[1] == "NOMBRE" else '"%d"'
            line_code += ",&" + parts[2] + ");"
        elif opcode == "NOMBRE":
            line_code += "float " + parts[1] + ";"
        elif opcode == "ENTIER":
            line_code += "int " + parts[1] + ";"
        elif opcode == "ECHO":
            line_code += "printf("
            line_code += '"%.6f"' if parts[1] == "NOMBRE" else '"%d"'
            line_code += "," + parts[2] + ");"
        elif opcode == "SI" and parts[-1] == "alors":
            # Start of a conditional block
            condition = " ".join(parts[1:-1])  # Exclude 'SI' and 'alors'
            line_code += f"if({condition}){{"
            inside_condition = True
            condition_code = ""  # Reset for new condition block
        elif opcode == "FIN" and "SI" in line:
            # End of the conditional block
            line_code += condition_code + "}"  # Close the 'if' block with accumulated condition code
            inside_condition = False
            condition_code = ""  # Reset after finishing the conditional block
        elif opcode == "POUR":
            line_code += f"for(int {parts[1]} = {parts[3]}; {parts[1]} <= {parts[5]}; {parts[1]}++){{"
        elif opcode == "FIN":
            line_code += "}"
        elif "=" in line:  # Detect assignment
            variable, value = line.split("=")
            variable = variable.strip()
            value = value.strip()
            line_code += f"{variable} = {value};"

        # If we're inside a conditional, accumulate code for that block
        if inside_condition:
            if line_code:
                condition_code += "    " + line_code + "\n"
        else:
            c_code += line_code + "\n"  # Regular lines go directly to c_code if not in a condition

    return c_code

def compile_and_run_code(program_lines):
    c_code = "#include <stdio.h>\nint main() {\n"
    c_code += inter(program_lines)
    c_code += "    return 0;\n}"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as c_file:
        c_file.write(c_code.encode('utf-8'))
        c_file_path = c_file.name

    compiled_program = c_file_path.replace(".c", "")
    return_code = os.system(f"gcc {c_file_path} -o {compiled_program}")

    if return_code != 0:
        return "Compilation failed."

    result = subprocess.run([compiled_program], capture_output=True, text=True)
    return result.stdout

@app.route('/compile', methods=['POST'])
def compile_text():
    code = request.json.get("code")
    if not code:
        return jsonify({"error": "No code provided"}), 400

    # Split the code into lines and strip whitespace from each line
    program_lines = [line.strip() for line in code.splitlines()]

    output = compile_and_run_code(program_lines)
    return jsonify({"output": output})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT from environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)