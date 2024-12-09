import os


def auth_header():
    try:
        access_token = os.getenv("INFERLESS_ACCESS_TOKEN")
        token_header = {"Authorization": f"Bearer {access_token}"}
        return token_header
    except Exception as e:
        print("Unable to fetch the credentials. Please login with inferless-cli. Follow instructions at "
              "https://docs.inferless.com/model-import/cli-import")
        raise SystemExit
