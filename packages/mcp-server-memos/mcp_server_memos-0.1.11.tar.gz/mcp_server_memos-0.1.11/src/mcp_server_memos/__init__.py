from .config import Config
from .server import new_server, serve_stdio


def main():
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="Give a model the ability to access Memos Server"
    )
    parser.add_argument(
        "--host", default="localhost", help="The host name to connect to"
    )
    parser.add_argument(
        "--port", default=8080, help="The port number for the Memos Server"
    )
    parser.add_argument(
        "--token", default="", help="The token to use for authentication"
    )
    args = parser.parse_args()

    config = Config(
        host=args.host,
        port=args.port,
        token=args.token,
    )

    asyncio.run(serve_stdio(config=config))


if __name__ == "__main__":
    main()
