import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from analysis import clean_sequence, sequence_length, gc_content, translate_dna, is_valid_dna, reverse_complement

# --- FLASK APP SETUP ---
app = Flask(__name__)

# --- CONFIG ---
UPLOAD_FOLDER = "lab_exports"
ALLOWED_EXTENSIONS = {"txt"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- HELPERS ---
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_history_files():
    """Return TXT files in lab_exports sorted newest first"""
    files = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)), reverse=True)
    return files

# --- DNA ANALYSIS FUNCTION ---
def analyze_sequence(seq):
    """Return all computed DNA/protein info as dict"""
    protein_data = translate_dna(seq)
    protein_string = "".join([item['name'][0] if item['name'] != 'STOP' else '*' for item in protein_data])
    rev_comp_seq = reverse_complement(seq)
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    comp_pairs = [{"original": base, "complement": complement_map.get(base, base)} for base in seq]
    rev_comp_pairs = comp_pairs[::-1]

    return {
        "length": sequence_length(seq),
        "gc": gc_content(seq),
        "protein_length": len(protein_data),
        "protein": protein_data,
        "protein_str": protein_string,
        "rev_comp": rev_comp_seq,
        "rev_comp_pairs": rev_comp_pairs,
    }

# --- ROUTES ---
@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    error = None
    raw_seq = ""

    if request.method == "POST":
        # --- FILE UPLOAD ---
        file = request.files.get("file")
        raw_seq = ""
        if file and file.filename != "":
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                file.seek(0)
                raw_seq = file.read().decode("utf-8")
            else:
                error = "Invalid file type. Only TXT files are allowed."

        # --- FALLBACK TO MANUAL INPUT ---
        if not raw_seq:
            raw_seq = request.form.get("sequence", "")

        # --- PROCESS SEQUENCE ---
        seq = clean_sequence(raw_seq)
        if not seq:
            error = "Please enter a DNA sequence."
        elif not is_valid_dna(seq):
            error = "Invalid DNA sequence. Use only A, T, G, and C."
        else:
            results = analyze_sequence(seq)

    history_files = get_history_files()
    return render_template("index.html", results=results, error=error, history_files=history_files)


@app.route("/history/<filename>")
def history(filename):
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(filepath):
        return f"File {filename} not found", 404

    with open(filepath, "r") as f:
        raw_seq = f.read()

    seq = clean_sequence(raw_seq)
    if not seq or not is_valid_dna(seq):
        results = {"error": "Invalid DNA sequence in file."}
    else:
        results = analyze_sequence(seq)

    history_files = get_history_files()
    return render_template("index.html", results=results, history_files=history_files, selected_file=filename)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
