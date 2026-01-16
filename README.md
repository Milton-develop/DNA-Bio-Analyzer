# BioSeq Analyzer 🧬

**A professional-grade DNA and Protein Sequence Interface.**

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/Milton-develop/DNA-Bio-Analyzer)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Table of Contents
- [🔬 Project Overview](#-project-overview)
- [✨ Features](#-features)
- [🧬 How to Run Locally](#-how-to-run-locally)
- [🧪 Testing the Analysis](#-testing-the-analysis)
- [🎯 Purpose](#-purpose)
- [👤 Author](#-author)
- [📄 License](#-license)

## 🔬 Project Overview

BioSeq Analyzer is a bioinformatics dashboard designed to bridge the gap between raw genetic data and functional protein analysis. Unlike static UI mockups, this platform features a robust **Python (Flask) backend** that performs real-time biological computations, translating genetic blueprints into structural and chemical protein profiles.

## ✨ Features

* **Intelligent Sequence Processing:** Automatically cleans sequences and validates DNA/RNA inputs.
* **DNA Strand Mapping:** Generates complementary antisense strands with color-coded nucleotide visualization (A, T, G, C).
* **Codon Translation:** Converts DNA into amino acid chains, featuring accurate detection of **STOP codons** (Opal, Ochre, Amber).
* **Dynamic Dashboard UI:** Includes a "Dark Mode" toggle and responsive data tables.
* **Export System:** Generate and download professional **PDF and TXT reports** directly from the browser.

## 🧬 How to Run This Project Locally

If you have downloaded the code or cloned the repository, follow these steps to launch the BioSeq Analyzer on your computer.

### 1. Prerequisites

Ensure you have **Python 3.8+** installed on your system. You can check this by typing `python --version` in your terminal.

### 2. Set Up a Virtual Environment (Recommended)

This keeps the project dependencies isolated from your other Python projects.

```bash
# Create the environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

```

### 3. Install Requirements

Install the necessary libraries (like Flask) using the `requirements.txt` file you downloaded.

```bash
pip install -r requirements.txt

```

### 4. Start the Application

Run the main script to start the local web server:

```bash
python app.py

```

### 5. Access the Site

Once the terminal says `Running on http://127.0.0.1:5000`, open your web browser and paste the address:


---

## 🧪 Testing the Analysis

To verify everything is working correctly, try entering this DNA sequence into the input field:
`ATGGGCTTAGCGTGA`

**Expected Results:**

* **Translation:** Methionine (START), Glycine, Leucine, Alanine, STOP.
* **GC Content:** Calculated automatically to show thermal stability.

## 🎯 Purpose

This project serves as a portfolio piece at the intersection of **Biological Sciences and Software Development**, demonstrating the ability to build functional, research-ready tools with a high emphasis on UI/UX and data integrity.

## 👤 Author

**MiltonPixel** *Biological Sciences | Bioinformatics | Full-Stack Development*

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

