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

# 仮のファイルコンテンツ。
temporary_file_content = '\n'.join([
    'YAML        9 hrs 22 mins  ██████░░░░░░░░░░░░░░  31.1%',
    'TypeScript  6 hrs 50 mins  ████░░░░░░░░░░░░░░░░  22.7%',
    'JSON        5 hrs 42 mins  ███░░░░░░░░░░░░░░░░░  18.9%',
    'Markdown    3 hrs 12 mins  ██░░░░░░░░░░░░░░░░░░  10.7%',
    'Other       2 hrs 4 mins   █░░░░░░░░░░░░░░░░░░░   6.9%',
    'JavaScript  58 mins        ░░░░░░░░░░░░░░░░░░░░   3.3%',
    'Docker      56 mins        ░░░░░░░░░░░░░░░░░░░░   3.1%',
    'Git Config  22 mins        ░░░░░░░░░░░░░░░░░░░░   1.2%',
    'Go          13 mins        ░░░░░░░░░░░░░░░░░░░░   0.8%',
    'GraphQL     12 mins        ░░░░░░░░░░░░░░░░░░░░   0.7%',
    'TOML        9 mins         ░░░░░░░░░░░░░░░░░░░░░   0.6%',
    'INI         1 min          ░░░░░░░░░░░░░░░░░░░░░   0.1%',
    'XML         1 min          ░░░░░░░░░░░░░░░░░░░░░   0.1%',
    'Bash        0 secs         ░░░░░░░░░░░░░░░░░░░░░   0.0%',
    'CSS         0 secs         ░░░░░░░░░░░░░░░░░░░░░   0.0%',
    'HTML        0 secs         ░░░░░░░░░░░░░░░░░░░░░   0.0%',
    'Text        0 secs         ░░░░░░░░░░░░░░░░░░░░░   0.0%',
])

# 認証は access token で行います。
headers = {
    'Authorization': f'token {get_env("GITHUB_ACCESS_TOKEN")}',
}
# gist を更新します。
data = json.dumps({
    # NOTE: なくても良い。
    # 'description': 'test',
    'files': {
        # 更新ファイル名。
        'file': {
            'content': temporary_file_content,
        }
    },
})
response = requests.post(
    f'https://api.github.com/gists/{get_env("GIST_ID")}',
    headers=headers,
    data=data)
response_json = json.loads(response.text)
pprint(response_json)
