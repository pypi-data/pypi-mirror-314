# sentry-plugin-dingtalk

> Sentry 钉钉通知插件

## 安装

新版本在 self-hosted 目录的 `sentry/enhance-image.sh` 中加入 `pip install sentry-plugin-dingtalk`  
老版本在 onpremise 目录的 `sentry/requirements.txt` 中添加 `sentry-plugin-dingtalk`  

**如果新版本中已经在使用 requirements.txt 配置了，那保持原状，在 requirements.txt 添加即可**

然后执行:

```sh
docker-compose down
./install.sh
docker-compose up -d
```

## 使用

在项目的所有集成页面找到 `DingTalk-EX` 插件，启用，并设置模板