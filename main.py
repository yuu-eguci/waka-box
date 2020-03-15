import os
import logging
import json
import requests
import dotenv
from pprint import pprint


def get_my_logger():
    """モジュール用のロガーを作成します。
    メインの処理とは別に関係ない。

    Returns:
        Logger -- モジュール用のロガー。
    """
    # ルートロガーを作成します。ロガーはモジュールごとに分けるもの。
    logger = logging.getLogger(__name__)
    # ルートロガーのログレベルは DEBUG。
    logger.setLevel(logging.DEBUG)
    # コンソールへ出力するハンドラを作成。
    handler = logging.StreamHandler()
    # ハンドラもログレベルを持ちます。
    handler.setLevel(logging.DEBUG)
    # ログフォーマットをハンドラに設定します。
    formatter = logging.Formatter(
        # NOTE: 改行は逆に見づらいので E501 を無視します。
        '%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')  # noqa: E501
    handler.setFormatter(formatter)
    # ハンドラをロガーへセットします。
    logger.addHandler(handler)
    # 親ロガーへの(伝播をオフにします。
    logger.propagate = False
    return logger


class WakaBoxException(Exception):
    """waka-box モジュールの基底例外クラス。

    Arguments:
        Exception {[type]} -- [description]
    """
    pass


class EnvNotFoundError(WakaBoxException):
    """特定の環境変数が見つからないことを表す例外クラス。

    Arguments:
        WakaBoxException {[type]} -- [description]
    """


def get_env(keyname: str) -> str:
    """環境変数を取得します。

    Arguments:
        keyname {str} -- 環境変数名。

    Raises:
        EnvNotFoundError: 環境変数が見つからない。

    Returns:
        str -- 環境変数の値。
    """
    try:
        return os.environ[keyname]
    except KeyError as e:
        raise EnvNotFoundError(keyname) from e


# .env で環境変数を取得する場合に対応します。見つからなくてもエラーを起こさない。
dotenv.load_dotenv(dotenv.find_dotenv(raise_error_if_not_found=False))
wakatime_secret_api_key = get_env('WAKATIME_SECRET_API_KEY')

logger = get_my_logger()
logger.info('foobarbaz')

response = requests.get(
    # NOTE: 改行は逆に見づらいので E501 を無視します。
    f'https://wakatime.com/api/v1/users/current/stats/last_7_days?api_key={wakatime_secret_api_key}')  # noqa: E501
response_json = json.loads(response.text)
pprint(response_json['data']['languages'])
