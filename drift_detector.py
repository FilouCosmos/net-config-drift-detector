import difflib
from netmiko import ConnectHandler

# --- Config ---
GOLDEN_CONFIG_FILE = "golden_config.txt"

# A adapter selon l'equipement
TARGET_DEVICE = {
    'device_type': 'cisco_ios',
    'host':   '192.168.1.10',
    'username': 'admin',
    'password': 'SuperPassword123!',
    'secret': 'EnablePassword123!',
}

# Codes couleurs ANSI por le terminal
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def get_local_config(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"[ERROR] Fichier de ref introuvable : {filepath}")
        return None

def get_running_config(device):
    print(f"[INFO] Connexion SSH a {device['host']}...")
    try:
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            return net_connect.send_command("show running-config")
    except Exception as e:
        print(f"[ERROR] SSH failed: {e}")
        return None

def compare_configs(golden, running):
    diff = difflib.unified_diff(
        golden.strip().splitlines(), 
        running.strip().splitlines(), 
        fromfile='Golden', tofile='Running', lineterm=''
    )
    return list(diff)

if __name__ == "__main__":
    golden_cfg = get_local_config(GOLDEN_CONFIG_FILE)
    
    if golden_cfg:
        running_cfg = get_running_config(TARGET_DEVICE)
        
        if running_cfg:
            diff_report = compare_configs(golden_cfg, running_cfg)
            
            if diff_report:
                print("\n[WARN] CONFIG DRIFT DETECTE !\n")
                for line in diff_report:
                    if line.startswith('+') and not line.startswith('+++'):
                        print(f"{GREEN}{line}{RESET}")
                    elif line.startswith('-') and not line.startswith('---'):
                        print(f"{RED}{line}{RESET}")
                    else:
                        print(line)
            else:
                print("\n[OK] Configuration conforme a la baseline.")