import os
import logging
import json
import requests
import dotenv
import math


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


def _generate_bar_chart(percent: float, size: int) -> str:
    """バーチャートを生成します。
    ↓こういうやつです。
    ████████████▍░░

    Arguments:
        percent {float} -- パーセンテージ値。
        size {int} -- バーのマス数。

    Returns:
        str -- バーチャート。
    """
    full = '█'
    semifull = '█▏▎▍▌▋▊▉'
    empty = '░'
    frac = math.ceil(size * 8 * percent / 100)
    barsFull = math.ceil(frac / 8)
    semi = int(frac % 8)
    barsEmpty = size - barsFull
    return ''.join([
        full * (barsFull - 1),
        semifull[semi],
        empty * barsEmpty,
    ])


def generate_file_content_line(raw_data: dict) -> str:
    """fileメインファイルコンテンツの1行を生成します。
    ↓こういうやつです。
    Python      2 hrs 36 mins  ██████▍░░░░░░░░  41.9%

    Arguments:
        raw_data {dict} -- name, text, percent をもつディクショナリ。

    Returns:
        str -- コンテンツの1行。
    """
    return ' '.join([
        # name が言語名。
        raw_data['name'].ljust(11),
        # text が期間。
        raw_data['text'].ljust(14),
        # バーチャート。
        _generate_bar_chart(raw_data['percent'], 15),
        # パーセンテージ。
        str(round(raw_data['percent'], 1)).rjust(5) + '%',
    ])


# .env で環境変数を取得する場合に対応します。見つからなくてもエラーを起こさない。
dotenv.load_dotenv(dotenv.find_dotenv(raise_error_if_not_found=False))
wakatime_secret_api_key = get_env('WAKATIME_SECRET_API_KEY')

logger = get_my_logger()
logger.info('処理開始。')

response = requests.get(
    # NOTE: 改行は逆に見づらいので E501 を無視します。
    f'https://wakatime.com/api/v1/users/current/stats/last_7_days?api_key={wakatime_secret_api_key}')  # noqa: E501
response_json = json.loads(response.text)
logger.info('WakaTime stats 取得完了。')

# ファイルコンテンツを生成します。
# response の内容は https://wakatime.com/developers/#stats
languages_raw_data = response_json['data']['languages']
file_content = '\n'.join((generate_file_content_line(_)
                          for _ in languages_raw_data))
logger.info('gist 更新内容生成完了。')

# 認証は access token で行います。
headers = {
    'Authorization': f'token {get_env("GITHUB_ACCESS_TOKEN")}',
}
# gist を更新します。
data = json.dumps({
    # NOTE: description を更新したいときは有効化。
    # 'description': 'test',
    'files': {
        # 更新ファイル名。
        'file': {
            'content': file_content,
        }
    },
})
response = requests.post(
    f'https://api.github.com/gists/{get_env("GIST_ID")}',
    headers=headers,
    data=data)
logger.info(f'gist 更新完了。ステータスコード:{response.status_code}')
response_json = json.loads(response.text)
logger.info(f'更新内容。\n{response_json["files"]["file"]["content"]}')
logger.info(f'処理終了。')
