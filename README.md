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

##### Try using the Makefile

1. Checkout this repo
```bash
git clone https://github.com/YourHeatingMantle/ChemPare.git
```

2. Go to repo directory and run Makefile
```bash
cd ChemPare
make install
```

3. Run script
```bash
make run
```

##### Manual setup

1. Install Python 3.9

2. Checkout this repo
```bash
git clone https://github.com/YourHeatingMantle/ChemPare.git
```

3. Create pyenv environment

Optional. ([documentation here](https://packaging.python.org/en/latest/tutorials/installing-packages/#optionally-create-a-virtual-environment)).
```bash
cd ./ChemPare
python3 -m venv venv
```

4. Go to the folder and activate the python env

<small>_On Linux/OSX:_</small>

```bash
source ./venv/bin/activate
```

<small>_On Windows:_</small>

```powershell
# tbd...
```

5. Install project packages
```bash
./venv/bin/pip install -r requirements.txt
```

6. Run main script, and provide a chemical name or CAS.

```
python3 main.py
```

Example output:
![image](assets/images/demo-screenshot-01.png)