from curia.session import Session


def create_session(env: str, api_token: str, debug: bool = False) -> Session:
    """Utility function for formatting of new session

    Args:
        env (str): Production, development, or staging environment.
        api_token (str): Generated API token. Run `dbutils.secrets.get(scope='your_id', key='ALEDADE_PROD_API_KEY')` to get the API token.
        debug (bool, optional): Whether to have a debug session Defaults to False.

    Returns:
        Session: The new session.
    """
    insert_stage = f"{env}." if env in ["stage", "dev"] else ""
    host = f"https://api.{insert_stage}curia.ai"
    session = Session(
        api_token=api_token,
        host=host,
        debug=debug,
    )
    return session