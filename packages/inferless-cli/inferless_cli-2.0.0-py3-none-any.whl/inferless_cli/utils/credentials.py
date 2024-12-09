import os
import base64

import rich
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

try:
    import keyring
    from keyring.backends import null

    keyring_backend = keyring.get_keyring()
except ImportError:
    keyring = None
    keyring_backend = None


# Define a salt and a key derivation function
SALT = b"\xc6\x9a\xf8\xc9\xa9\x1d\xd3\x93\xc8\xf9\x8a\x8a\xd2\xf1\xec\xc8"

INFERLESS_KEY = "SkBya_fdKRnTPSCIKbgrQNOxD8Dp86Csxnhn1hTkS3Y="

KEYRING = keyring


def is_keyring_supported():
    if keyring is None:
        return False
    if keyring_backend is not None and isinstance(keyring_backend, null.Keyring):
        return False
    return True


# Define a function to load the encryption key from an environment variable
def load_key():
    key = INFERLESS_KEY
    if key is None:
        raise ValueError("INFERLESS_KEY environment variable not set")
    return base64.urlsafe_b64decode(key)


# Define a function to encrypt and save the credentials
def save_credentials(
    access_key,
    access_secret,
    token,
    refresh_token,
    user_id,
    workspace_id,
    workspace_name,
    mode,
):
    try:
        home_directory = os.path.expanduser("~")
        # Create the full path to the file
        CREDENTIALS_FILE = os.path.join(home_directory, ".inferless", ".credentials")
        # Load the existing credentials
        (
            access_key,
            access_secret,
            token,
            refresh_token,
            user_id,
            workspace_id,
            workspace_name,
            mode,
        ) = retain_and_get_credentials(
            access_key,
            access_secret,
            token,
            refresh_token,
            user_id,
            workspace_id,
            workspace_name,
            mode,
        )

        # Create the .inferless directory if it doesn't exist
        os.makedirs(os.path.join(home_directory, ".inferless"), exist_ok=True)

        # Load the encryption key
        key, kdf = load_encryption_key()

        # Create a Fernet object with the encryption key
        fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(key)))

        # Encrypt the credentials
        encrypted_access_key = (
            fernet.encrypt(access_key.encode()) if access_key is not None else b""
        )
        encrypted_access_secret = (
            fernet.encrypt(access_secret.encode()) if access_secret is not None else b""
        )
        encrypted_token = fernet.encrypt(token.encode()) if token is not None else b""
        encrypted_refresh_token = (
            fernet.encrypt(refresh_token.encode()) if refresh_token is not None else b""
        )
        encrypted_user_id = (
            fernet.encrypt(user_id.encode()) if user_id is not None else b""
        )
        encrypted_workspace_id = (
            fernet.encrypt(workspace_id.encode()) if workspace_id is not None else b""
        )
        encrypted_workspace_name = (
            fernet.encrypt(workspace_name.encode())
            if workspace_name is not None
            else b""
        )
        encrypted_mode = fernet.encrypt(mode.encode()) if mode is not None else b""
        # Write the encrypted credentials to the .credentials file
        with open(CREDENTIALS_FILE, "wb") as f:
            f.write(encrypted_access_key + b"\n")
            f.write(encrypted_access_secret + b"\n")
            f.write(encrypted_token + b"\n")
            f.write(encrypted_refresh_token + b"\n")
            f.write(encrypted_user_id + b"\n")
            f.write(encrypted_workspace_id + b"\n")
            f.write(encrypted_workspace_name + b"\n")
            f.write(encrypted_mode + b"\n")

    except Exception as e:
        rich.print("Error saving credentials:", e)


def retain_and_get_credentials(
    access_key,
    access_secret,
    token,
    refresh_token,
    user_id,
    workspace_id,
    workspace_name,
    mode,
):
    (
        existing_access_key,
        existing_access_secret,
        existing_token,
        existing_refresh_token,
        existing_user_id,
        existing_workspace_id,
        existing_workspace_name,
        existing_mode,
    ) = load_credentials()
    access_key = access_key if access_key else existing_access_key
    access_secret = access_secret if access_secret else existing_access_secret
    token = token if token else existing_token
    refresh_token = refresh_token if refresh_token else existing_refresh_token
    user_id = user_id if user_id else existing_user_id
    workspace_id = workspace_id if workspace_id else existing_workspace_id
    workspace_name = workspace_name if workspace_name else existing_workspace_name
    mode = mode if mode else existing_mode
    return (
        access_key,
        access_secret,
        token,
        refresh_token,
        user_id,
        workspace_id,
        workspace_name,
        mode,
    )


def load_encryption_key():
    key = load_key()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
    )
    return key, kdf


def load_credentials():
    # Load the encryption key
    home_directory = os.path.expanduser("~")
    # Create the full path to the file
    CREDENTIALS_FILE = os.path.join(home_directory, ".inferless", ".credentials")

    key, kdf = load_encryption_key()

    # Create a Fernet object with the encryption key
    fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(key)))

    # Load the encrypted credentials from the .credentials file
    try:
        with open(CREDENTIALS_FILE, "rb") as f:
            lines = f.readlines()
            encrypted_access_key = lines[0].strip()
            encrypted_access_secret = lines[1].strip()
            encrypted_token = lines[2].strip()
            encrypted_refresh_token = lines[3].strip()
            encrypted_user_id = lines[4].strip()
            encrypted_workspace_id = lines[5].strip()
            encrypted_workspace_name = lines[6].strip()
            encrypted_mode = lines[7].strip()
    except FileNotFoundError:
        return None, None, None, None, None, None, None, None
    except Exception:
        return None, None, None, None, None, None, None, None

    # Decrypt the credentials
    access_key = (
        fernet.decrypt(encrypted_access_key).decode() if encrypted_access_key else None
    )
    access_secret = (
        fernet.decrypt(encrypted_access_secret).decode()
        if encrypted_access_secret
        else None
    )
    token = fernet.decrypt(encrypted_token).decode() if encrypted_token else None
    refresh_token = (
        fernet.decrypt(encrypted_refresh_token).decode()
        if encrypted_refresh_token
        else None
    )
    user_id = fernet.decrypt(encrypted_user_id).decode() if encrypted_user_id else None
    workspace_id = (
        fernet.decrypt(encrypted_workspace_id).decode()
        if encrypted_workspace_id
        else None
    )
    workspace_name = (
        fernet.decrypt(encrypted_workspace_name).decode()
        if encrypted_workspace_name
        else None
    )
    mode = fernet.decrypt(encrypted_mode).decode() if encrypted_mode else None
    return (
        access_key,
        access_secret,
        token,
        refresh_token,
        user_id,
        workspace_id,
        workspace_name,
        mode,
    )


def select_url(url_dev, url_prod):
    mode = "PROD"
    if not is_keyring_supported():
        _, _, _, _, _, _, _, mode = load_credentials()
    else:
        try:
            keyring.get_keyring()
            mode = keyring.get_password("Inferless", "mode")
        except Exception:
            mode = "PROD"
    if mode == "DEV":
        return url_dev
    return url_prod
