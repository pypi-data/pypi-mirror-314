# coding: utf-8

import re
import aiohttp
import time
import markdown

from typing import Dict, Any, Optional
from sentry.plugins.bases.notify import NotificationPlugin
from sentry_plugin_dingtalk import VERSION
from .forms import OptionsForm
from .template import parseConfig


class DingtalkPlugin(NotificationPlugin):
    """钉钉通知插件,用于发送错误信息到钉钉"""

    author = "ding"
    version = VERSION
    description = "DingTalk integrations for sentry."
    slug = "DingTalk-EX"
    title = "DingTalk-EX"
    conf_key = slug
    conf_title = title
    project_conf_form = OptionsForm

    def is_configured(self, project) -> bool:
        """检查插件是否已配置"""
        return bool(self.get_option("options", project))

    def notify_users(self, group, event, *args, **kwargs) -> None:
        """通知用户"""
        self.post_process(group, event, *args, **kwargs)

    def get_tag_data(self, group, event) -> Dict[str, str]:
        """获取基础数据,用于标签渲染"""
        return {
            "projectName": event.project.slug,
            "projectId": str(event.project_id or "--"),
            "eventId": event.event_id,
            "issuesUrl": group.get_absolute_url(event_id=event.event_id),
            "title": event.title,
            "message": event.message or event.title,
            "platform": event.platform,
            "datetime": event.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "release": event.release or "--",
            "url": event.get_tag("url") or "--", 
            "environment": event.get_tag("environment") or "--",
        }

    def render_tag(self, event, tag_data: Dict[str, str], template: str) -> str:
        """渲染模板"""
        def replace_tag(pattern):
            op = pattern.group("op")
            tag = pattern.group("tag")
            return event.get_tag(tag) or "--" if op == "@" else tag_data.get(tag, "--")

        return re.sub(r"\{(?P<op>[@#])?(?P<tag>[^}]+)\}", replace_tag, template)

    def parse_config(self, group):
        """解析配置和模板"""
        options = self.get_option("options", group.project)
        markdowns = self.get_option("markdowns", group.project)
        return parseConfig(options, markdowns)

    def check_condition(self, tag: str, op: str, value: str) -> bool:
        """条件判定"""
        if op in ("=", "=="): 
            return tag == value
        if op == "!=":
            return tag != value
        if op == "in":
            return value in tag
        if op == "not in":
            return value not in tag
        if op == "reg":
            return bool(re.search(value, tag))
        if op == "not reg":
            return not bool(re.search(value, tag))
        return False

    async def send_msg(self, title: str, text: str, item: dict) -> None:
        """发送消息到钉钉"""
        # 将markdown转换为HTML
        html_content = markdown.markdown(text)
        
        timestamp = int(time.time() * 1000)
        secret = 'f7f61059f236433ba21f0f50c5c5a0a0'
        app_id = 'PuHuiDeaknUIOJjkmndSER'
        base_url = "http://feature-oa-2-0.oa.inclution.com"

        async with aiohttp.ClientSession() as session:
            # 获取签名
            sign_resp = await session.post(base_url + '/api/open/getSign', json={
                'timestamp': timestamp,
                'appId': app_id,
                'secret': secret,
                'url': '/api/open/api/auth'
            })
            sign_data = await sign_resp.json()

            # 获取token
            token_resp = await session.post(base_url + '/api/open/api/auth', json={
                'timestamp': timestamp,
                'appId': app_id,
                'secretKey': secret,
                'sign': sign_data['data']
            })
            token_data = await token_resp.json()
            token = token_data['data']['token']
            
            # 从 item 中获取 recipientCodes
            recipient_codes = item.get('recipientCodes', 'AAA')

            # 获取推送签名
            push_sign_resp = await session.post(base_url + '/api/open/getSign', json={
                'timestamp': timestamp,
                'token': token,
                'secret': secret,
                'url': '/api/open/api/push'
            })
            push_sign = await push_sign_resp.json()

            # 发送消息
            await session.post(base_url + '/api/open/api/push', json={
                'data': {
                    'msgSource': '前端团队',
                    'msgTitle': title,
                    'msgText': html_content,
                    'recipientCodes': recipient_codes,
                    'recipientType': 2,
                },
                'apiCode': 'phmsg.message.send',
                'sign': push_sign['data'],
                'timestamp': timestamp,
                'token': token
            })

    async def post_process(self, group, event, *args, **kwargs) -> None:
        """处理错误并发送通知"""
        if not self.is_configured(group.project) or group.is_ignored():
            return

        tag_data = self.get_tag_data(group, event)
        config_list = self.parse_config(group)

        # 调试功能
        try:
            debug_url = config_list[0].get("debug")
            if debug_url and re.search(r"https?:", debug_url):
                debug_data = {
                    "type": "debug",
                    "environment": tag_data.get("environment", "-"),
                    "title": tag_data.get("title", "-"),
                    "url": tag_data.get("url", "-"),
                    "datetime": tag_data.get("datetime", "-"),
                }
                async with aiohttp.ClientSession() as session:
                    await session.post(
                        url=debug_url,
                        headers={"Content-Type": "application/json"},
                        json=debug_data
                    )
        except Exception:
            pass

        # 遍历配置列表,满足条件发送消息
        for item in config_list:
            title = item.get("title", "")
            markdown = item.get("markdown", "")
            condition = item.get("condition", {})
            
            if self.check_condition(
                self.render_tag(event, tag_data, condition.get("tag", "")),
                condition.get("op", ""),
                condition.get("value", "")
            ):
                rendered_title = (
                    self.render_tag(event, tag_data, title)
                    if title
                    else tag_data.get("title", "--")
                )
                rendered_text = self.render_tag(event, tag_data, markdown)
                await self.send_msg(rendered_title, rendered_text, item)
