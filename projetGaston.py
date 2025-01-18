import argparse
import asyncio
import csv
from ping3 import ping
import aiofiles

async def scan_ip(ip: str, timeout: float = 1.0):
    """Ping an IP address and return its status and response time."""
    try:
        response = await asyncio.to_thread(ping, ip, timeout=timeout, unit='ms')
        if response is not None:
            result = (ip, "Active", round(response, 2))
        else:
            result = (ip, "Inactive", None)
    except Exception as e:
        result = (ip, "Error", str(e))
    
    # Affiche le résultat dans le shell en temps réel
    print(f"IP: {result[0]}, Status: {result[1]}, Ping: {result[2]}")
    return result

async def write_csv(filename: str, results: list):
    """Write scan results to a CSV file."""
    # Ouvre le fichier de manière synchrone pour éviter des erreurs avec csv.writer
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["IP", "Status", "Ping (ms)"])  # Écrit l'en-tête
        for result in results:
            writer.writerow(result)  # Écrit chaque ligne des résultats

async def scan_file(filename: str):
    """Scan IPs listed in a file."""
    tasks = []
    async with aiofiles.open(filename, mode='r') as file:
        async for line in file:
            ip = line.strip()
            tasks.append(scan_ip(ip))  # Lance le scan pour chaque IP
    return await asyncio.gather(*tasks)  # Attends que tous les scans soient terminés

def main():
    parser = argparse.ArgumentParser(description="Network Scanner")
    parser.add_argument("--file", type=str, required=True, help="File containing a list of IPs")
    parser.add_argument("--output", type=str, default="results.csv", help="Output CSV file")

    args = parser.parse_args()

    if args.file:
        file = args.file
        results = asyncio.run(scan_file(file))  # Exécute la fonction de scan pour tous les IPs du fichier
        print("Scan complete. Writing results to CSV...")
        asyncio.run(write_csv(args.output, results))  # Écrit les résultats dans le fichier CSV
        print(f"Results saved to {args.output}")
    else:
        print("Please specify a valid --file option.")

if __name__ == "__main__":
    main()
