def clean_sequence(seq):
    """Remove spaces/newlines and make uppercase"""
    return seq.replace(" ", "").replace("\n", "").upper()


def sequence_length(seq):
    return len(seq)


def gc_content(seq):
    if len(seq) == 0:
        return 0
    g = seq.count("G")
    c = seq.count("C")
    return round(((g + c) / len(seq)) * 100, 2)


def translate_dna(seq):
    codon_table = {
        "ATA":"I", "ATC":"I", "ATT":"I", "ATG":"M",
        "ACA":"T", "ACC":"T", "ACG":"T", "ACT":"T",
        "AAC":"N", "AAT":"N", "AAA":"K", "AAG":"K",
        "AGC":"S", "AGT":"S", "AGA":"R", "AGG":"R",
        "CTA":"L", "CTC":"L", "CTG":"L", "CTT":"L",
        "CCA":"P", "CCC":"P", "CCG":"P", "CCT":"P",
        "CAC":"H", "CAT":"H", "CAA":"Q", "CAG":"Q",
        "CGA":"R", "CGC":"R", "CGG":"R", "CGT":"R",
        "GTA":"V", "GTC":"V", "GTG":"V", "GTT":"V",
        "GCA":"A", "GCC":"A", "GCG":"A", "GCT":"A",
        "GAC":"D", "GAT":"D", "GAA":"E", "GAG":"E",
        "GGA":"G", "GGC":"G", "GGG":"G", "GGT":"G",
        "TCA":"S", "TCC":"S", "TCG":"S", "TCT":"S",
        "TTC":"F", "TTT":"F", "TTA":"L", "TTG":"L",
        "TAC":"Y", "TAT":"Y", "TAA":"*", "TAG":"*",
        "TGC":"C", "TGT":"C", "TGA":"*", "TGG":"W",
    }



    protein = ""
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i:i+3]
        protein += codon_table.get(codon, "X")

    return protein

def is_valid_dna(seq):
    return all(base in "ATGC" for base in seq)

amino_acid_map = {
    # T
    'TTT': {'name': 'Phenylalanine', '3-letter': 'Phe', '1-letter': 'F'},
    'TTC': {'name': 'Phenylalanine', '3-letter': 'Phe', '1-letter': 'F'},
    'TTA': {'name': 'Leucine', '3-letter': 'Leu', '1-letter': 'L'},
    'TTG': {'name': 'Leucine', '3-letter': 'Leu', '1-letter': 'L'},
    'TCT': {'name': 'Serine', '3-letter': 'Ser', '1-letter': 'S'},
    'TCC': {'name': 'Serine', '3-letter': 'Ser', '1-letter': 'S'},
    'TCA': {'name': 'Serine', '3-letter': 'Ser', '1-letter': 'S'},
    'TCG': {'name': 'Serine', '3-letter': 'Ser', '1-letter': 'S'},
    'TAT': {'name': 'Tyrosine', '3-letter': 'Tyr', '1-letter': 'Y'},
    'TAC': {'name': 'Tyrosine', '3-letter': 'Tyr', '1-letter': 'Y'},
    'TAA': {'name': 'STOP', '3-letter': 'Stop', '1-letter': '*'},
    'TAG': {'name': 'STOP', '3-letter': 'Stop', '1-letter': '*'},
    'TGT': {'name': 'Cysteine', '3-letter': 'Cys', '1-letter': 'C'},
    'TGC': {'name': 'Cysteine', '3-letter': 'Cys', '1-letter': 'C'},
    'TGA': {'name': 'STOP', '3-letter': 'Stop', '1-letter': '*'},
    'TGG': {'name': 'Tryptophan', '3-letter': 'Trp', '1-letter': 'W'},

    # C
    'CTT': {'name': 'Leucine', '3-letter': 'Leu', '1-letter': 'L'},
    'CTC': {'name': 'Leucine', '3-letter': 'Leu', '1-letter': 'L'},
    'CTA': {'name': 'Leucine', '3-letter': 'Leu', '1-letter': 'L'},
    'CTG': {'name': 'Leucine', '3-letter': 'Leu', '1-letter': 'L'},
    'CCT': {'name': 'Proline', '3-letter': 'Pro', '1-letter': 'P'},
    'CCC': {'name': 'Proline', '3-letter': 'Pro', '1-letter': 'P'},
    'CCA': {'name': 'Proline', '3-letter': 'Pro', '1-letter': 'P'},
    'CCG': {'name': 'Proline', '3-letter': 'Pro', '1-letter': 'P'},
    'CAT': {'name': 'Histidine', '3-letter': 'His', '1-letter': 'H'},
    'CAC': {'name': 'Histidine', '3-letter': 'His', '1-letter': 'H'},
    'CAA': {'name': 'Glutamine', '3-letter': 'Gln', '1-letter': 'Q'},
    'CAG': {'name': 'Glutamine', '3-letter': 'Gln', '1-letter': 'Q'},
    'CGT': {'name': 'Arginine', '3-letter': 'Arg', '1-letter': 'R'},
    'CGC': {'name': 'Arginine', '3-letter': 'Arg', '1-letter': 'R'},
    'CGA': {'name': 'Arginine', '3-letter': 'Arg', '1-letter': 'R'},
    'CGG': {'name': 'Arginine', '3-letter': 'Arg', '1-letter': 'R'},

    # A
    'ATT': {'name': 'Isoleucine', '3-letter': 'Ile', '1-letter': 'I'},
    'ATC': {'name': 'Isoleucine', '3-letter': 'Ile', '1-letter': 'I'},
    'ATA': {'name': 'Isoleucine', '3-letter': 'Ile', '1-letter': 'I'},
    'ATG': {'name': 'Methionine (START)', '3-letter': 'Met', '1-letter': 'M'},
    'ACT': {'name': 'Threonine', '3-letter': 'Thr', '1-letter': 'T'},
    'ACC': {'name': 'Threonine', '3-letter': 'Thr', '1-letter': 'T'},
    'ACA': {'name': 'Threonine', '3-letter': 'Thr', '1-letter': 'T'},
    'ACG': {'name': 'Threonine', '3-letter': 'Thr', '1-letter': 'T'},
    'AAT': {'name': 'Asparagine', '3-letter': 'Asn', '1-letter': 'N'},
    'AAC': {'name': 'Asparagine', '3-letter': 'Asn', '1-letter': 'N'},
    'AAA': {'name': 'Lysine', '3-letter': 'Lys', '1-letter': 'K'},
    'AAG': {'name': 'Lysine', '3-letter': 'Lys', '1-letter': 'K'},
    'AGT': {'name': 'Serine', '3-letter': 'Ser', '1-letter': 'S'},
    'AGC': {'name': 'Serine', '3-letter': 'Ser', '1-letter': 'S'},
    'AGA': {'name': 'Arginine', '3-letter': 'Arg', '1-letter': 'R'},
    'AGG': {'name': 'Arginine', '3-letter': 'Arg', '1-letter': 'R'},

    # G
    'GTT': {'name': 'Valine', '3-letter': 'Val', '1-letter': 'V'},
    'GTC': {'name': 'Valine', '3-letter': 'Val', '1-letter': 'V'},
    'GTA': {'name': 'Valine', '3-letter': 'Val', '1-letter': 'V'},
    'GTG': {'name': 'Valine', '3-letter': 'Val', '1-letter': 'V'},
    'GCT': {'name': 'Alanine', '3-letter': 'Ala', '1-letter': 'A'},
    'GCC': {'name': 'Alanine', '3-letter': 'Ala', '1-letter': 'A'},
    'GCA': {'name': 'Alanine', '3-letter': 'Ala', '1-letter': 'A'},
    'GCG': {'name': 'Alanine', '3-letter': 'Ala', '1-letter': 'A'},
    'GAT': {'name': 'Aspartic Acid', '3-letter': 'Asp', '1-letter': 'D'},
    'GAC': {'name': 'Aspartic Acid', '3-letter': 'Asp', '1-letter': 'D'},
    'GAA': {'name': 'Glutamic Acid', '3-letter': 'Glu', '1-letter': 'E'},
    'GAG': {'name': 'Glutamic Acid', '3-letter': 'Glu', '1-letter': 'E'},
    'GGT': {'name': 'Glycine', '3-letter': 'Gly', '1-letter': 'G'},
    'GGC': {'name': 'Glycine', '3-letter': 'Gly', '1-letter': 'G'},
    'GGA': {'name': 'Glycine', '3-letter': 'Gly', '1-letter': 'G'},
    'GGG': {'name': 'Glycine', '3-letter': 'Gly', '1-letter': 'G'}
}


def translate_dna(sequence):
    protein_info = []
    for i in range(0, len(sequence) - 2, 3):
        codon = sequence[i:i+3].upper()
        # Fetch the dict from your amino_acid_map
        aa_data = amino_acid_map.get(codon, {"name": "Unknown"}) 
        
        protein_info.append({
            "codon": codon, 
            "name": aa_data['name'] # This ensures 'item.name' works in HTML
        })
    return protein_info

# analysis.py

amino_acid_map = {
    'ATA':'Isoleucine', 'ATC':'Isoleucine', 'ATT':'Isoleucine', 'ATG':'Methionine (START)',
    'ACA':'Threonine', 'ACC':'Threonine', 'ACG':'Threonine', 'ACT':'Threonine',
    'AAC':'Asparagine', 'AAT':'Asparagine', 'AAA':'Lysine', 'AAG':'Lysine',
    'AGC':'Serine', 'AGT':'Serine', 'AGA':'Arginine', 'AGG':'Arginine',
    'CTA':'Leucine', 'CTC':'Leucine', 'CTG':'Leucine', 'CTT':'Leucine',
    'CCA':'Proline', 'CCC':'Proline', 'CCG':'Proline', 'CCT':'Proline',
    'CAC':'Histidine', 'CAT':'Histidine', 'CAA':'Glutamine', 'CAG':'Glutamine',
    'CGA':'Arginine', 'CGC':'Arginine', 'CGG':'Arginine', 'CGT':'Arginine',
    'GTA':'Valine', 'GTC':'Valine', 'GTG':'Valine', 'GTT':'Valine',
    'GCA':'Alanine', 'GCC':'Alanine', 'GCG':'Alanine', 'GCT':'Alanine',
    'GAC':'Aspartic Acid', 'GAT':'Aspartic Acid', 'GAA':'Glutamic Acid', 'GAG':'Glutamic Acid',
    'GGA':'Glycine', 'GGC':'Glycine', 'GGG':'Glycine', 'GGT':'Glycine',
    'TCA':'Serine', 'TCC':'Serine', 'TCG':'Serine', 'TCT':'Serine',
    'TTC':'Phenylalanine', 'TTT':'Phenylalanine', 'TTA':'Leucine', 'TTG':'Leucine',
    'TAC':'Tyrosine', 'TAT':'Tyrosine', 'TGC':'Cysteine', 'TGT':'Cysteine',
    'TGG':'Tryptophan', 'TAA':'STOP', 'TAG':'STOP', 'TGA':'STOP'
}

def clean_sequence(seq):
    return seq.strip().upper().replace(" ", "").replace("\n", "").replace("\r", "")

def is_valid_dna(seq):
    return all(base in "ATGC" for base in seq)

def sequence_length(seq):
    return len(seq)

def gc_content(seq):
    if not seq: return 0
    g = seq.count('G')
    c = seq.count('C')
    return round(((g + c) / len(seq)) * 100, 2)

def translate_dna(seq):
    protein_data = []
    # Loop through sequence in steps of 3
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i:i+3]
        name = amino_acid_map.get(codon, "Unknown")
        # Creating a dictionary for each codon to match your HTML keys
        protein_data.append({
            "codon": codon,
            "name": name
        })
    return protein_data

def reverse_complement(seq):
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    # 1. Get the complement (swap letters)
    complement = "".join(complement_map.get(base, base) for base in seq)
    # 2. Reverse the string
    return complement[::-1]

