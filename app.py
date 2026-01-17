from flask import Flask, render_template, request
from analysis import clean_sequence, sequence_length, gc_content, translate_dna, is_valid_dna, reverse_complement
import threading
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

# --- Global variables ---
latest_results = None
latest_error = None
sequence_history = []  # Store history of sequences

# --- Folder to watch for new DNA files ---
WATCH_FOLDER = "./lab_exports"
os.makedirs(WATCH_FOLDER, exist_ok=True)

# --- Watchdog event handler ---
class DNAFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        global latest_results, latest_error, sequence_history
        if event.is_directory:
            return
        if event.src_path.endswith((".txt", ".csv")):
            try:
                with open(event.src_path, "r") as f:
                    raw_seq = f.read().strip()
                
                seq = clean_sequence(raw_seq)
                filename_or_manual = os.path.basename(event.src_path)

                if not seq:
                    latest_error = f"No DNA sequence found in {filename_or_manual}"
                    latest_results = None
                    return
                if not is_valid_dna(seq):
                    latest_error = f"Invalid DNA sequence in {filename_or_manual}"
                    latest_results = None
                    return
                
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

                # --- Append to history ---
                sequence_history.append({
                    "file": filename_or_manual,
                    "results": latest_results
                })

                latest_error = None
                print(f"Processed sequence from {filename_or_manual}")
            
            except Exception as e:
                latest_error = f"Error processing file {os.path.basename(event.src_path)}: {str(e)}"
                latest_results = None

# --- Start Watchdog in a background thread ---
def start_watcher():
    observer = Observer()
    event_handler = DNAFileHandler()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"Watching folder '{WATCH_FOLDER}' for new DNA files...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

threading.Thread(target=start_watcher, daemon=True).start()

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

            # --- Append to history ---
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
    app.run(host="0.0.0.0", debug=True)
