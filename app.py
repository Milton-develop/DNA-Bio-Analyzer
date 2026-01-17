from flask import Flask, render_template, request, session
from analysis import clean_sequence, sequence_length, gc_content, translate_dna, is_valid_dna, reverse_complement
import threading
import time
import os
import uuid

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for sessions

# --- Folder to watch for new DNA files (optional, demo only) ---
WATCH_FOLDER = "./lab_exports"
os.makedirs(WATCH_FOLDER, exist_ok=True)

# --- Initialize session-specific storage ---
def init_session():
    if "sequence_history" not in session:
        session["sequence_history"] = []

# --- Process a DNA sequence (manual or file) ---
def process_sequence(raw_seq, source="Manual Input"):
    seq = clean_sequence(raw_seq)
    if not seq or not is_valid_dna(seq):
        return None, f"Invalid or empty DNA sequence from {source}"

    protein_data = translate_dna(seq)
    rev_comp_seq = reverse_complement(seq)
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    comp_pairs = [{"original": base, "complement": complement_map.get(base, base)} for base in seq]
    rev_comp_pairs = comp_pairs[::-1]
    protein_string = "".join([item['name'][0] if item['name'] != 'STOP' else '*' for item in protein_data])

    results = {
        "length": sequence_length(seq),
        "gc": gc_content(seq),
        "protein_length": len(protein_data),
        "protein": protein_data,
        "protein_str": protein_string,
        "rev_comp": rev_comp_seq,
        "rev_comp_pairs": rev_comp_pairs,
        "source": source
    }
    return results, None

# --- Flask routes ---
@app.route("/", methods=["GET", "POST"])
def home():
    init_session()
    latest_results = None
    latest_error = None

    if request.method == "POST":
        raw_seq = request.form.get("sequence", "")
        results, error = process_sequence(raw_seq, source="Manual Input")

        if error:
            latest_error = error
        else:
            latest_results = results
            # Save only in session (memory)
            session["sequence_history"].append({
                "id": str(uuid.uuid4()),
                "file": "Manual Input",
                "results": results
            })
            session.modified = True

    return render_template("index.html", results=latest_results, error=latest_error)

@app.route("/history")
def history():
    init_session()
    last_sequences = session["sequence_history"][-10:][::-1]  # Show last 10
    return render_template("history.html", history=last_sequences)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
