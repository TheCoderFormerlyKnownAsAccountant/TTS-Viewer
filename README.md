```markdown
# TTS Viewer - Hockey League Stats Viewer

This project is designed to fetch and display team standings and player statistics for hockey leagues from the Sharks Ice league website. The application is built using Python and provides a graphical user interface (GUI) for viewing stats.

## Features
- Fetch and display team standings.
- Fetch and display player statistics by division.
- Assign badges based on player performance.
- Aggregate and display all-time top players.

---

## How to Use

### Running the Python Script

1. **Clone the repository:**

   ```bash
   git clone https://github.com/TheCoderFormerlyKnownAsAccountant/tts-viewer.git
   ```

2. **Install the required dependencies:**

   Make sure you have Python 3.x installed, and then install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   The key dependencies are:
   - `beautifulsoup4`
   - `requests`
   - `tkinter` (comes bundled with Python)

3. **Run the Python script:**

   Once you’ve installed the dependencies, you can run the Python script directly:

   ```bash
   python tracker.py
   ```

---

### Generating the Executable (.exe) File (Windows)

If you prefer to have an executable version of the program:

1. **Install PyInstaller:**

   If you don’t have it installed already, you can install PyInstaller with:

   ```bash
   pip install pyinstaller
   ```

2. **Generate the executable:**

   Use PyInstaller to generate a single-file executable:

   ```bash
   pyinstaller --onefile tracker.py
   ```

3. **Find your executable:**

   After running the above command, you’ll find the `.exe` file in the `dist` directory. The executable will contain the entire app, which you can run without Python.

---

### Downloading the Executable (Precompiled for Windows)

If you don't want to run the Python script and prefer to use the executable, download the precompiled `.exe` file from the [Releases](https://github.com/TheCoderFormerlyKnownAsAccountant/tts-viewer/releases) section.

**Note:** The executable is for Windows users only. If you are on another operating system, please follow the steps to run the Python script.

---

## Requirements

To run the Python script, you need the following:
- Python 3.x
- The packages listed in `requirements.txt` (install with `pip install -r requirements.txt`)

If you are creating the executable, you’ll need:
- PyInstaller (installed via `pip`)

---

## Contact

For any questions or issues, feel free to open an issue on GitHub:
- **GitHub**: [TheCoderFormerlyKnownAsAccountant](https://github.com/TheCoderFormerlyKnownAsAccountant)
```
