import os
import logging
import json
import requests
import dotenv
import math
import typing
import functools


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


# logger を取得します。
logger = get_my_logger()


class WakaBoxException(Exception):
    """waka-box モジュールの基底例外クラス。

    Arguments:
        Exception {[type]} -- [description]
    """


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
        # GitHub Actions では環境変数が設定されていなくても yaml 内で空文字列が入ってしまう。空欄チェックも行います。
        _ = os.environ[keyname]
        if not _:
            raise KeyError(f'{keyname} is empty.')
        return _
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


def function_execution_announcer_decorator(
        logger: logging.Logger) -> typing.Callable:
    """functools.wraps を使ってみたいがために作ってみたデコレータです。
    これを付与した関数の最初と最後で「処理開始」「処理終了」をアナウンス(logger.info)します。
    ロギングのためのロガーインスタンスを渡してください。

    Arguments:
        logger {logging.Logger} -- アナウンスのためのロガーインスタンス。

    Returns:
        typing.Callable -- デコレータなので関数を返します。
    """
    def _function_execution_announcer_decorator(func: typing.Callable):
        # デコレータ定義するときは functools.wraps を使います。(Effective Python で覚えた。)
        # @functools.wraps(func)
        def __function_execution_announcer_decorator(*args, **kwargs):
            logger.info('処理開始。')
            result = func(*args, **kwargs)
            logger.info('処理終了。')
            return result
        return __function_execution_announcer_decorator
    return _function_execution_announcer_decorator


@function_execution_announcer_decorator(logger)
def run():
    """メインメソッドです。

    Raises:
        EnvNotFoundError: 環境変数が見つからない。
    """
    # .env で環境変数を取得する場合に対応します。
    # raise_error_if_not_found: .env が見つからなくてもエラーを起こさない。
    dotenv.load_dotenv(dotenv.find_dotenv(raise_error_if_not_found=False))

    # 必要な環境変数を取得します。
    WAKATIME_SECRET_API_KEY = get_env('WAKATIME_SECRET_API_KEY')
    GITHUB_ACCESS_TOKEN = get_env('GITHUB_ACCESS_TOKEN')
    GIST_ID = get_env('GIST_ID')
    # DRY_RUN のみデフォルト値 False で取得します。
    DRY_RUN = bool(os.environ.get('DRY_RUN', False))

    # データソース WakaTime stats を取得します。
    # response の内容は https://wakatime.com/developers/#stats
    response = requests.get(
        # NOTE: 改行は逆に見づらいので E501 を無視します。
        f'https://wakatime.com/api/v1/users/current/stats/last_7_days?api_key={WAKATIME_SECRET_API_KEY}')  # noqa: E501
    logger.info('WakaTime stats 取得完了。')

    # データソースを検証します。データがなければ処理終了です。
    response_json = json.loads(response.text)
    languages_raw_data = response_json['data']['languages']
    if not languages_raw_data:
        logger.warning(
            'stats の languages データが空っぽです。'
            'このエラーは一晩おくことで解消する可能性があります。')
        return

    # gist 用ファイルコンテンツを生成します。
    file_content = '\n'.join((generate_file_content_line(_)
                              for _ in languages_raw_data))
    logger.info('gist 更新内容生成完了。')

    # DRY_RUN 時は更新内容を表示して終了します。
    if DRY_RUN:
        logger.info('DRY_RUN')
        logger.info(f'更新内容。\n{file_content}')
        return

    # gist の更新データを作成します。
    headers = {
        # 認証はパスワードでなく access token で行います。
        'Authorization': f'token {GITHUB_ACCESS_TOKEN}',
    }
    data = json.dumps({
        'description': '📊 Weekly development breakdown',
        'files': {
            # 更新ファイル名。
            'file': {
                'content': file_content,
            }
        },
    })
    # gist を更新します。
    response = requests.post(
        f'https://api.github.com/gists/{GIST_ID}',
        headers=headers,
        data=data)
    logger.info(f'gist 更新完了。ステータスコード:{response.status_code}')

    # 更新内容のロギングです。
    response_json = json.loads(response.text)
    logger.info(f'更新内容。\n{response_json["files"]["file"]["content"]}')


if __name__ == "__main__":
    run()
