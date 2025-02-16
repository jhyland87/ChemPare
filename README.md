# ChemPare
### Intro
Compares prices from chemical vendors that sell to individuals and residential addresses.

> _*Note:* This project is a work in progress, not yet in Beta mode_

---

### How does it work
Magic.

---

### Installation

#### Python Enviroment Setup 

1. Install Python 3.9

2. Checkout this repo
```bash
git clone https://github.com/YourHeatingMantle/ChemPare.git
```

3. Create pyenv environment

Optional. ([documentation here](https://packaging.python.org/en/latest/tutorials/installing-packages/#optionally-create-a-virtual-environment)).
```bash
python3 -m venv ./ChemPare
```

4. Go to the folder and activate the python env

<small>_On Linux/OSX:_</small>

```bash
cd ./ChemPare
source ./bin/activate
```

<small>_On Windows:_</small>

```powershell
# tbd...
```

5. Install project packages
```bash
pip install -e .
```

6. Run main script, and provide a chemical name or CAS.

```
python3 main.py
```

Example output:
![image](assets/images/demo-screenshot-01.png)