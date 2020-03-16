<p align="center">
  <img width="400" src="https://user-images.githubusercontent.com/4658208/60469862-2e40bf00-9c2c-11e9-87f7-afe164648de4.png">
  <h3 align="center">waka-box</h3>
  <p align="center">📊 Update a pinned gist to contain your weekly WakaTime stats</p>
</p>

[![Actions Status](https://github.com/yuu-eguci/waka-box/workflows/Python%20application/badge.svg)](https://github.com/yuu-eguci/waka-box/actions)
[![GitHub](https://img.shields.io/github/license/yuu-eguci/waka-box)](https://github.com/yuu-eguci/waka-box/blob/master/LICENSE)

## Description

- Python script
- Converts WakaTime stats to bar charts and publishes on specified gist
- Intended to run by GitHub Actions

## Use on your own GitHub overview

1. Register WakaTime account at [https://wakatime.com/](https://wakatime.com/).
1. Install WakaTime plugins into your editors following [plugin install instructions](https://wakatime.com/plugins).
1. Create your own waka-box repository by pushing **Use this template** button at [waka-box top page](https://github.com/yuu-eguci/waka-box).
    - GitHub Actions workflow automatically runs and it shows `EnvNotFoundError` this time.
1. Register three env variables as repository secrets.
    - WAKATIME_SECRET_API_KEY: Get your WakaTime Secret API Key from [your account page](https://wakatime.com/settings/account).
    - GIST_ID: Create a public gist with a file named **`file`** and get the gist id. `https://gist.github.com/username/[gist id]`
    - GITHUB_ACCESS_TOKEN: Create a token from GitHub Settings > Developer settings > Personal access tokens > Generate new token > Check gist and generate
    - Set them as repository secrets - Repository settings > Secrets
1. Pin the gist on your GitHub overview.
1. Open Actions tab > Open your workflow result > build > Re-run jobs
    - It is possible that it shows `EmptyWakaTimeDataError` because WakaTime API data can be empty for a while after registration.
1. After that, the jobs automatically run by every 12 hours.

## Installation

### On local

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

### On GitHub Actions

Register env variables and run by GitHub Actions.

![secrets](https://user-images.githubusercontent.com/28250432/76698894-968ede00-669f-11ea-957b-0486d3748e2c.png)

## Gist

[https://gist.github.com/yuu-eguci/10a7031088fb0e783dc92e721c6443c3](https://gist.github.com/yuu-eguci/10a7031088fb0e783dc92e721c6443c3)

## What I learned this time

![what-i-learned](https://user-images.githubusercontent.com/28250432/76726931-85e77200-674a-11ea-826a-c207841ed9f8.png)

- [https://gitmoji.carloscuesta.me/](https://gitmoji.carloscuesta.me/)