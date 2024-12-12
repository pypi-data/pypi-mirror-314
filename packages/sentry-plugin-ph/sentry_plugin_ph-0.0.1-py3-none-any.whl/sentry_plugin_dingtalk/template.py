# coding: utf-8

import re
import json

keywordFields = [
    "projectName",
    "projectId",
    "eventId",
    "issuesUrl",
    "title",
    "message",
    "platform",
    "datetime",
    "release",
    "url",
    "environment",
]

defaultConfig = """
[
  {
    "token": "xxxx_access_token1",
    "title": "{title}",
    "condition": {
      "tag": "{environment}",
      "op": "=",
      "value": "prod"
    },
    "markdown": "{#demo-pro#}",
    "remark": "说明字段，可省略，监听环境为 prod 的 issue"
  },
  {
    "token": "xxxx_access_token2",
    "title": "{@loginName} - {@browser}",
    "condition": {
      "tag": "{@browser}",
      "op": "in",
      "value": "Chrome"
    },
    "markdown": "{#chrome-demo#}",
    "remark": "监听 tag 标签 browser 字段包含 Chrome 字符的 issue"
  },
  {
    "token": "xxxx_access_token3",
    "condition": {
      "tag": "{@loginName}",
      "op": "=",
      "value": "18088888888"
    },
    "markdown": "{#user-temp#}",
    "remark": "监听指定用户的 issue，如果 markdown 模板匹配不到，会使用默认模板"
  }
]
""".lstrip()

defaultMarkdown = """
{#demo-pro#}
Sentry项目名: {projectName}
Sentry项目ID: {projectId}
Sentry接入平台: {platform}
事件ID: {eventId}
Issues 地址: {issuesUrl}
环境: {environment}
标题: {title}
上报时间: {datetime}
发布版本: {release}
url: {url}
标签 browser 字段: {@browser}
标签 browser.name 字段: {@browser.name}
标签 level 字段: {@level}

{#chrome-demo#}
用户: {@loginName}
""".lstrip()

defaultContent = """
Sentry项目名: {projectName}
Sentry项目ID: {projectId}
Sentry接入平台: {platform}
事件ID: {eventId}
Issues 地址: {issuesUrl}
环境: {environment}
标题: {title}
上报时间: {datetime}
发布版本: {release}
url: {url}
标签 level 字段: {@level}
""".lstrip()


def parseConfig(options, markdowns):
    configList = json.loads(options)
    # python 3.6 不支持空匹配切割，3.8 开始支持
    blockList = re.split(r"(?=\{#[\w-]+#\}).", markdowns)
    blockDict = {}

    for block in blockList:
        block = block.strip()
        if block == "":
            continue
        ret = re.search(r"(#[\w-]+#\})", block)
        if ret:
            str = re.sub(r"(#[\w-]+#\})", "", block)
            blockDict[ret.group(1)] = str.strip()

    for item in configList:
        key = item.get("markdown", "")
        item["markdown"] = blockDict.get(key[1:], defaultContent)

    return configList
