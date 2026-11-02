<p align="center">
  <img width="400" src="https://user-images.githubusercontent.com/4658208/60469862-2e40bf00-9c2c-11e9-87f7-afe164648de4.png">
  <h3 align="center">waka-box</h3>
  <p align="center">📊 Update a pinned gist to contain your weekly WakaTime stats</p>
</p>

<p align="center">
  <a href="https://github.com/yuu-eguci/waka-box/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/yuu-eguci/waka-box/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/yuu-eguci/waka-box/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/yuu-eguci/waka-box"></a>
</p>

## Description

- Python script
- Converts WakaTime stats to bar charts and publishes on specified gist
- Intended to run by GitHub Actions

## Environment

- Python 3.14 + Pipenv
- GitHub Actions
    - `CI`: lint and test on push to master and on pull requests
    - `Update gist`: every 12 hours, or manually with Run workflow
- Docker: not used!

## Quick run

```bash
pipenv install --dev
pipenv run flake8 main.py tests
pipenv run python -m pytest
DRY_RUN=1 pipenv run python main.py
```

`DRY_RUN` set to any non-empty value prints the content instead of updating the gist. The other env variables are still required.

## Use on your own GitHub overview

1. Register WakaTime account at [https://wakatime.com/](https://wakatime.com/).
1. Install WakaTime plugins into your editors following [plugin install instructions](https://wakatime.com/plugins).
1. Create your own waka-box repository with the **Use this template** button at [waka-box top page](https://github.com/yuu-eguci/waka-box).
1. Register three repository secrets at Settings > Secrets and variables > Actions.
    - WAKATIME_SECRET_API_KEY: Get your WakaTime Secret API Key from [your account page](https://wakatime.com/settings/account).
    - GIST_ID: Create a public gist with a file named **`file`** and get the gist id. `https://gist.github.com/username/[gist id]`
    - GITHUB_ACCESS_TOKEN: Create a personal access token that can write gists (classic token: `gist` scope).
1. Pin the gist on your GitHub overview.
1. Open Actions tab > Update gist > Run workflow.
    - WakaTime stats can be empty for a while after registration. Then the job only logs a warning.
1. After that, the job runs every 12 hours.

## Run locally

Create .env and run.

```plaintext
WAKATIME_SECRET_API_KEY=***
GIST_ID=***
GITHUB_ACCESS_TOKEN=***
```

```bash
pipenv install
pipenv run python main.py
```

## Gist

[https://gist.github.com/yuu-eguci/10a7031088fb0e783dc92e721c6443c3](https://gist.github.com/yuu-eguci/10a7031088fb0e783dc92e721c6443c3)

## What I learned this time

<img alt="what-i-learned" src="https://user-images.githubusercontent.com/28250432/76726931-85e77200-674a-11ea-826a-c207841ed9f8.png">

- [https://gitmoji.dev/](https://gitmoji.dev/)
