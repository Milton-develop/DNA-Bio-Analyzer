import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from analysis import clean_sequence, is_valid_dna, translate_dna

# Folder to watch
WATCH_FOLDER = "./lab_exports"

class DNAFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        # Only process CSV or TXT files
        if event.src_path.endswith((".txt", ".csv")):
            print(f"New file detected: {event.src_path}")
            self.process_file(event.src_path)

    def process_file(self, filepath):
        with open(filepath, "r") as f:
            raw_seq = f.read().strip()
        
        seq = clean_sequence(raw_seq)
        if not seq or not is_valid_dna(seq):
            print("Invalid DNA sequence in file.")
            return
        
        protein_data = translate_dna(seq)
        protein_string = "".join([item['name'][0] if item['name'] != 'STOP' else '*' for item in protein_data])
        
        print(f"Sequence length: {len(seq)}")
        print(f"Protein: {protein_string}")
        print("--- Done processing ---\n")

# Observer
observer = Observer()
event_handler = DNAFileHandler()
observer.schedule(event_handler, WATCH_FOLDER, recursive=False)

observer.start()
print(f"Watching folder: {WATCH_FOLDER} for new DNA files...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
