# Future Interns - Cyber Security Internship
## Task 3: Secure File Sharing System

**Domain:** Web Application Security & Cryptography
**Tech Stack:** Python (Flask), PyCryptodome, HTML/CSS
**Encryption:** AES-256 (EAX Mode)

### 📌 Project Description
In this task, I developed a secure file sharing application that prioritizes data confidentiality and integrity. Unlike standard file uploaders, this system encrypts every file immediately upon upload using **AES-256 encryption**. The server never stores raw files, ensuring data remains secure even if the server storage is compromised.

### 🚀 Key Features
* **AES-256 Encryption:** Uses the Advanced Encryption Standard with a 256-bit key for robust security.
* **Authenticated Encryption:** Implements **AES-EAX mode** to verify both data confidentiality and integrity (preventing tampering).
* **Secure Key Management:** Generates a cryptographically strong random key on startup.
* **On-the-Fly Decryption:** Files are only decrypted temporarily when a user requests a download.

### 🛠️ How to Run
1. **Install Dependencies:**
   ```bash
   pip install flask pycryptodome
   
2. **Start the Server:**
   python app.py
   
3. **Access the Portal:**
   Open your browser and navigate to http://localhost:5000.

### 📂 Repository Structure
   
   **app.py:** The main application logic handling upload, encryption, and decryption.
   
   **templates/index.html:** The frontend user interface.
   
   **Security_Overview.txt:**  Documentation explaining the cryptographic approach and key management strategy

# Developed by Milind M Patil for Future Interns Task 3
