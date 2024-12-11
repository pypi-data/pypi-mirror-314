# -*- coding: utf-8 -*-

"""Console script for vault2env."""
import argparse
import sys

from vault2env.vault2env import generate_env, Vault2EnvException


def main():
    """Console script for vault2env."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', metavar="URL", help="Vault Address (https://vault.myco.com)", required=True)
    parser.add_argument('-t', metavar="Token", help="Vault Token - Token with enough access to read the KV-2 pairs for the .env", required=True)
    parser.add_argument('-m', metavar="'KV-2 Engine Mount Path'", help="Path the KV-2 secret engine is mounted to in Vault", required=True)
    parser.add_argument('-p', metavar="'Secret Path'", help="Path under the engine mount path that the env secrets are mounted to", required=True)
    parser.add_argument('-o', metavar="'Output File'", help="Output filename", default=".env")
    args = parser.parse_args()

    try:
        generate_env(args.a, args.t, args.m, args.p, args.o)
    except Vault2EnvException as e:
        return e.returnCode

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
