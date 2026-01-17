from flask import Flask, render_template, request
from analysis import clean_sequence, sequence_length, gc_content, translate_dna, is_valid_dna, reverse_complement

app = Flask(__name__)

# --- Global variables (memory-only) ---
latest_results = None
latest_error = None
sequence_history = []  # history stored only in memory

# --- Flask routes ---
@app.route("/", methods=["GET", "POST"])
def home():
    global latest_results, latest_error, sequence_history

    if request.method == "POST":
        raw_seq = request.form.get("sequence", "")
        seq = clean_sequence(raw_seq)
        filename_or_manual = "Manual Input"

        if not seq:
            latest_error = "Please enter a DNA sequence."
            latest_results = None
        elif not is_valid_dna(seq):
            latest_error = "Invalid DNA sequence. Use only A, T, G, and C."
            latest_results = None
        else:
            # --- Process DNA ---
            protein_data = translate_dna(seq)
            rev_comp_seq = reverse_complement(seq)
            complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
            comp_pairs = [{"original": base, "complement": complement_map.get(base, base)} for base in seq]
            rev_comp_pairs = comp_pairs[::-1]
            protein_string = "".join([item['name'][0] if item['name'] != 'STOP' else '*' for item in protein_data])

            latest_results = {
                "length": sequence_length(seq),
                "gc": gc_content(seq),
                "protein_length": len(protein_data),
                "protein": protein_data,
                "protein_str": protein_string,
                "rev_comp": rev_comp_seq,
                "rev_comp_pairs": rev_comp_pairs,
                "source": filename_or_manual
            }

            # --- Append to memory-only history ---
            sequence_history.append({
                "file": filename_or_manual,
                "results": latest_results
            })

            latest_error = None

    return render_template("index.html", results=latest_results, error=latest_error)


@app.route("/history")
def history():
    # Show last 10 sequences (newest first)
    last_sequences = sequence_history[-10:][::-1]
    return render_template("history.html", history=last_sequences)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    # App runs entirely in memory; nothing saved to disk
    app.run(host="0.0.0.0", debug=True)
