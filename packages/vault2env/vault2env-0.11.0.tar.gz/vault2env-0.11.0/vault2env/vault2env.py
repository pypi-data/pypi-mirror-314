# -*- coding: utf-8 -*-
import sys
import os

from requests.exceptions import RequestException
import hvac

"""Main module."""

class Vault2EnvException(Exception):
  def __init__(self, returnCode):
    super().__init__()
    self.returnCode = returnCode

def read_env(vault_address, vault_token, engine_path, secret_path):
  client = hvac.Client(url=vault_address, token=vault_token)

  # Attempt to read the secret from the given path
  try:
      result = client.read(f'{engine_path}/data/{secret_path}')
  except RequestException:
    print("Issue connecting to the specified Vault address")
    raise Vault2EnvException(1)

  except hvac.exceptions.Forbidden:
    print("The provided token is not authenticated to access the secrets in Vault")
    raise Vault2EnvException(2)

  if not result:
    print("No secrets found")
    raise Vault2EnvException(3)

  secrets = result['data']['data']

  # Update the environment with the secrets
  for key, value in secrets.items():
    os.environ[key] = value

  return secrets

def generate_env(vault_address, vault_token, engine_path, secret_path, output_filename):
  secrets = read_env(vault_address, vault_token, engine_path, secret_path)

  with open(output_filename, 'w+') as filed:
    for key, value in secrets.items():
      new_line = f'{key}="{value}"'
      filed.write(f'{new_line}\n')
