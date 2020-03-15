<p align="center">
  <img width="400" src="https://user-images.githubusercontent.com/4658208/60469862-2e40bf00-9c2c-11e9-87f7-afe164648de4.png">
  <h3 align="center">waka-box</h3>
  <p align="center">📊 Update a pinned gist to contain your weekly WakaTime stats</p>
</p>

===

[![Actions Status](https://github.com/yuu-eguci/waka-box/workflows/Python%20application/badge.svg)](https://github.com/yuu-eguci/waka-box/actions)
[![GitHub](https://img.shields.io/github/license/yuu-eguci/waka-box)](https://github.com/yuu-eguci/waka-box/blob/master/LICENSE)

## Description

- Python script
- Converts WakaTime stats to bar charts and publishes on specified gist
- Intended to run by GitHub Actions

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

Register env variables run by GitHub Actions.

![secrets](https://user-images.githubusercontent.com/28250432/76698894-968ede00-669f-11ea-957b-0486d3748e2c.png)
