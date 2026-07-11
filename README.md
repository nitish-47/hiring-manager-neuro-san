# hiring-manager-neuro-san

A hiring manager application powered by Neuro-SAN-studio.

## Quick Start

### 1. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install UV Package Manager

```bash
pip install uv
```

### 3. Install Dependencies

```bash
uv sync
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
```

**Or set as environment variable:**

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GOOGLE_API_KEY=your_api_key_here
```

**Linux/macOS:**
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### 5. Run the Application

```bash
ns run
```

## Requirements

- Python 3.8+
- UV package manager
- Google API Key
