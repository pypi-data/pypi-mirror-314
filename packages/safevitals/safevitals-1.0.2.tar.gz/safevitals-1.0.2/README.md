# Safe Vitals

**Safe Vitals** is a Python-based APK vulnerability scanner that decompiles APKs, runs security scans, and generates detailed PDF reports.

## Features
- Decompiles APKs
- Runs MobSF scans
- Generates a PDF vulnerability report

## Requirements

This project requires the following external tools to be installed and available in the system's `PATH`:

1. **apktool**
   - Used for reverse-engineering APK files.
   - Installation:
     ```bash
     sudo apt install apktool  # On Linux
     brew install apktool      # On macOS
     ```
     For other platforms, follow the instructions [here](https://ibotpeaches.github.io/Apktool/).

2. **dex2jar**
   - Converts DEX files into JAR format for decompilation.
   - Installation:
     - Download the latest release from [GitHub](https://github.com/pxb1988/dex2jar).
     - Extract the files and add the directory to your `PATH`.
     ```bash
     export PATH=$PATH:/path/to/dex2jar
     ```
## Install
     pip install safebitals

## How To Run
     safebitals -a file.apk
    
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
