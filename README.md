# AES-128 Cryptographic Implementation

## Overview
This repository contains a modular, from-scratch Python implementation of the **Advanced Encryption Standard (AES-128)**. It encrypts a 128-bit (16-byte) block of plaintext using a 128-bit cryptographic key, executing the standard 10 rounds of AES transformations. 

The project is intentionally decoupled into functional modules to clearly demonstrate the underlying mathematics and cryptographic steps involved in both the encryption and decryption pipelines.

---

## Repository Structure

The project separates execution environments, data storage, and core cryptographic logic into distinct files for maintainability.

### Execution Environments
* `Encryption.ipynb`: The main runner script that executes the 10-round encryption process and generates output files.
* `Decryption.ipynb`: The verification script that reads the ciphertext and reverses the AES operations to recover the plaintext.

### Data Files (Inputs & Outputs)
* `plaintext.txt`: User-editable file for the input message.
* `key.txt`: User-editable file for the 32-character Hex key.
* `ciphertext.txt` / `ciphertext_utf.txt`: Generated outputs containing the encrypted data and verification hash.
* `input_output_hex.txt`: A summarized result file for easy validation.
* `encryption_trace.json`: A deep-level debug log tracking the matrix state after every transformation.

### Core Logic Modules
* `aes_*.py`: Isolated Python scripts containing the specific mathematical transformations (e.g., S-Box, ShiftRows, MixColumns, Key Expansion).

---

## Getting Started

### 1. Prerequisites
Ensure you have the following installed on your local machine:
* **Python 3.x**
* **Jupyter Notebook** (can be run via the terminal or using the Jupyter extension in VS Code).

### 2. Configuring Inputs
You do not need to alter the source code to encrypt custom data. Simply open the text files in the root directory to provide your inputs:
1. **`plaintext.txt`**: Enter the exact 16-character (128-bit) string you wish to encrypt.
2. **`key.txt`**: Enter your custom 32-character hexadecimal key.

*(Note: If these files are left empty or deleted, the system will automatically fall back to safe default values to prevent execution errors.)*

### 3. Execution Workflow
The cryptographic process is split into two phases. You must run them sequentially.

**Phase A: Encrypt the Data**
Open `Encryption.ipynb` and run all cells. This script reads your inputs, executes the AES-128 algorithm, and generates the encrypted text alongside a full debugging trace.

**Phase B: Decrypt and Verify**
Open `Decryption.ipynb` and run all cells. This script reads the generated ciphertext, performs the inverse AES transformations, and mathematical confirms that the recovered text matches your original input.

### 4. Viewing Results
Once execution is complete, you can review the outputs without running the code again:
* **Quick Summary:** Open `input_output_hex.txt`. This file neatly logs the Input Hex, Key Hex, and Final Output Hex in one place.
* **Deep Debugging:** Open `encryption_trace.json`. This JSON file tracks the exact state of the $4\times4$ matrix after every single step of the process. Formatting this document in your editor will allow you to see exactly how your data was manipulated round-by-round.

---

## Under the Hood: Code Explanation

This project breaks down the AES-128 algorithm into its fundamental operations. Here is a systematic explanation of how the logic flows.

### 1. State Management (`aes_state.py`)
AES does not process data sequentially as a flat string. It organizes the 16 bytes of data into a $4\times4$ grid known as the "State Matrix". The `aes_state.py` file handles the conversion of linear text arrays into this matrix format and back.

### 2. Key Expansion (`aes_key_expansion.py` & `aes_g_func.py`)

AES-128 requires a unique Round Key for every step of the process. 
* The `expand_key` function takes your single master key and expands it into 11 separate Round Keys (Round 0 through 10).
* It utilizes `aes_g_func.py` to introduce cryptographic non-linearity to these generated keys using byte rotations (`RotWord`) and substitutions (`SubWord`).

### 3. The Encryption Cipher (`Encryption.ipynb`)

The encryption pipeline processes the state matrix through multiple rigorous rounds:
* **Round 0 (Initial Round):** The algorithm performs an initial `AddRoundKey` operation, XORing the raw plaintext matrix with the first Round Key.
* **Rounds 1 to 9 (Main Rounds):** The code loops through four specific, consecutive transformations:
  1. **SubBytes (`aes_sbox.py`):** Replaces each byte with a different byte using a pre-computed lookup table (S-Box) to create confusion.
  2. **ShiftRows (`aes_shift_rows.py`):** Cyclically shifts the rows of the matrix to the left, ensuring bytes spread across different columns.
  3. **MixColumns (`aes_mix_columns.py`):** Uses Galois Field ($GF(2^8)$) matrix multiplication to mix the bytes vertically within each column, providing heavy diffusion.
  4. **AddRoundKey (`aes_xor.py`):** XORs the current matrix with the unique Round Key generated for that specific round.
* **Round 10 (Final Round):** The algorithm executes SubBytes, ShiftRows, and AddRoundKey, but intentionally skips the MixColumns step to adhere strictly to the AES standard.

### 4. The Decryption Cipher (`Decryption.ipynb`)

Decryption is the exact mathematical inverse of the encryption process. The `Decryption.ipynb` notebook reads the ciphertext and applies inverse operations sequentially:
* It utilizes the `INV_S_BOX` to accurately reverse byte substitutions.
* It shifts matrix rows to the right instead of the left.
* It applies an Inverse MixColumns transformation, relying on a different set of Galois Field multipliers to unscramble the columns back to their previous state.

### 5. Integrity Verification (`hash.py`)
To ensure the ciphertext is never accidentally corrupted or tampered with between notebooks, `hash.py` implements a custom Polynomial Rolling Hash. A 6-character hash is generated and appended to `ciphertext.txt` during encryption. The decryption notebook automatically validates this hash before attempting to reverse the cipher.

## Authors

* Aryan Vashishtha: aryan23148@iiitd.ac.in
* Atin Aggarwal: atin23157@iiitd.ac.in
