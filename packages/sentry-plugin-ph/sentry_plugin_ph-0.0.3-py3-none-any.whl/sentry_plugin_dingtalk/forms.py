# coding: utf-8

from django import forms
from .template import keywordFields, defaultMarkdown, defaultConfig


class OptionsForm(forms.Form):
    # access_token = forms.CharField(
    #     max_length=255,
    #     help_text='DingTalk robot access_token'
    # )

    # keyword = forms.CharField(
    #     max_length=255,
    #     help_text='DingTalk robot key-word',
    #     required=False
    # )

    options = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6, "class": "span9"}),
        initial=defaultConfig,
        required=True,
        label="消息配置",
        help_text="<br>".join(
            [
                "字段 title 为标题，不在模板中显示，默认支持自定义变量，可忽略默认使用 <code>event.title</code>",
                "字段 condition 为条件，其中 op 字段支持的条件有 <code>{op}</code>",
                "字段 markdown 为模板，会匹配消息“消息模板”配置的内容，如果匹配不到会使用默认模板",
            ]
        ).format(
            op="</code>, <code>".join(["=", "!=", "in", "not in", "reg", "not reg"])
        ),
    )

    markdowns = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6, "class": "span9"}),
        initial=defaultMarkdown,
        required=True,
        label="消息模板",
        help_text="<br>".join(
            [
                "支持 markdown 格式，并且扩展自定义变量，用法为：<code>{{自定义变量}}</code> <code>{{@tag}}</code>",
                "自定义变量：<code>{var}</code>",
                "标签变量：<code>{{@tag}}</code> 取上报的 tag 字段，如：<code>{{@browser.name}}</code> 会显示为 Chrome",
            ]
        ).format(var="</code>, <code>".join(keywordFields)),
    )
