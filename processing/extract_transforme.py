import re
from logger import logger

# 1. Cherche les échecs de mot de passe et extrait l'IP
RE_FAILED_IP = re.compile(r"(?:Failed password|authentication failure).*?(?:from|rhost=)([\d\.]+)")

# 2. Cherche les connexions réussies (Accepted password ou publickey)
RE_SUCCESS_USER = re.compile(r"Accepted (?:password|publickey) for (\S+) from")

# 3. Cherche les "Invalid user" et extrait le nom d'utilisateur (groupe 1) et l'IP (groupe 2)
RE_INVALID_USER = re.compile(r"(?:Invalid user|Failed password for invalid user)\s+(\S+)?\s*from ([\d\.]+)")


def extract_failed_ip_counts(lines):
    failed_ips = []
    for line in lines:
        match = RE_FAILED_IP.search(line)
        if match:
            failed_ips.append(match.group(1))
    return failed_ips


def extract_successful_users(lines):
    successful_users = []
    for line in lines:
        match = RE_SUCCESS_USER.search(line)
        if match:
            successful_users.append(match.group(1))
    return successful_users


def extract_invalid_user_attempts(lines):
    invalid_users = []
    for line in lines:
        # On filtre d'abord pour accélérer la recherche
        if "Invalid user" in line or "invalid user" in line:
            match = RE_INVALID_USER.search(line)
            if match:
                # group(1) est le nom. S'il est vide (ex: "Invalid user  from ..."), on met <EMPTY>
                username = match.group(1) if match.group(1) else "<EMPTY>"
                invalid_users.append(username)
    return invalid_users