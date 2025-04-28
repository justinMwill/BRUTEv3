Advanced SMB Brute-Force and Spray Tool | Developed by 0dayjay
# BRUTEv3 - SMB Attack Tool

### Developed by 0dayjay

BRUTEv3 is a multi-mode SMB bruteforce and spray tool built for ethical penetration testing and red-team operations.

## Features:
- Classic Bruteforce (1 username, many passwords)
- Username Spray (many usernames, 1 password)
- Password Spray (1 username, many passwords)
- Full Spray (userlist + passwordlist, carefully rotated)
- Threaded attacks with user-controlled speed (`--threads`)
- Timestamped success and failure logs
- Clean professional console output with custom banner

## Usage:
```bash
python smb_bruteforce_v3.py --threads 10

