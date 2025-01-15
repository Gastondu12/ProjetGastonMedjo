import sys
import time
import csv
from ping3 import ping
import ipaddress

def scan_ip_range(ip_range):
    # Début du scan
    print(f"Début du scan pour la plage d'IP: {ip_range}")
    
    active_ips = []
    for ip in ipaddress.IPv4Network(ip_range).hosts():
        ip_str = str(ip)
        print(f"Scanning {ip_str}...")  # Imprimer l'IP qui est en train d'être scannée
        response_time = ping(ip_str, timeout=1)
        if response_time is not None:
            print(f"{ip_str} Active (Ping: {response_time}ms)")  # Affichage si l'IP est active
            active_ips.append((ip_str, "Active", response_time))
        else:
            print(f"{ip_str} Inactive")  # Affichage si l'IP est inactive
            active_ips.append((ip_str, "Inactive", ""))
    
    return active_ips

def save_results_to_csv(results):
    print("Sauvegarde des résultats dans results.csv...")  # Affichage de la sauvegarde
    with open("results.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["IP", "Status", "Ping (ms)"])
        for result in results:
            writer.writerow(result)
    print("Sauvegarde terminée.")

def main():
    if len(sys.argv) < 3:
        print("Usage: python .\\projetGaston.py scan --file ip_list.txt")
        sys.exit(1)

    option = sys.argv[1]
    if option == "scan":
        # Assurez-vous d'utiliser --file ou --range correctement
        if sys.argv[2] == "--file":
            ip_file = sys.argv[3]
            with open(ip_file, "r") as f:
                ip_list = f.readlines()
            ip_list = [ip.strip() for ip in ip_list]
            for ip in ip_list:
                response_time = ping(ip, timeout=1)
                if response_time is not None:
                    print(f"{ip} Active (Ping: {response_time}ms)")
                else:
                    print(f"{ip} Inactive")
        elif sys.argv[2] == "--range":
            ip_range = sys.argv[3]
            results = scan_ip_range(ip_range)
            save_results_to_csv(results)
        else:
            print("Option invalide. Utilisez --file ou --range.")

if __name__ == "__main__":
    main()
