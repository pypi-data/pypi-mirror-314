# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_xinghuo_api']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.2.1,<3.0.0',
 'nonebot2>=2.0.0rc3,<3.0.0',
 'spark_ai_python>=0.4.4,<0.5.0',
 'websocket-client>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-xinghuo-api',
    'version': '2.3.1',
    'description': 'A nonebot plugin for xinghuo LLM',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-xinghuo-api\n</div>\n\n# 介绍\n- 本插件是适配科大讯飞星火大模型官方API的聊天机器人插件，同时具有上下文记忆回复功能。已适配版本：Ultra，Max，Pro，Pro-128K，V2.0，Lite。\n- 当前版本可能会与LittlePaimon机器人冲突\n# 安装\n\n* 手动安装\n  ```\n  git clone https://github.com/Alpaca4610/nonebot-plugin-xinghuo-api.git\n  ```\n\n  下载完成后在bot项目的pyproject.toml文件手动添加插件：\n\n  ```\n  plugin_dirs = ["xxxxxx","xxxxxx",......,"下载完成的插件路径/nonebot-plugin-xinghuo-api"]\n  ```\n* 使用 pip\n  ```\n  pip install nonebot-plugin-xinghuo-api\n  ```\n\n# 配置文件\n\n必选内容: 在Bot根目录下的.env文件中填入科大讯飞提供的API调用鉴权信息：\n\n```\nxinghuo_app_id = xxxxxxxx\nxinghuo_api_secret = xxxxxxxx\nxinghuo_api_key = xxxxxxxx\n```\n\n可选内容：\n```\nxinghuo_enable_private_chat = True   # 私聊开关，默认开启，改为False关闭\nxinghuo_api_version = ""    #星火大模型的版本，默认为免费的Lite模型，可选填：Ultra，Max，Pro，Pro-128K，V2.0，Lite\n```\n\n# 使用方法\n\n- xh 获取回复，没有上下文回复的能力\n- XH 获取回复，具有上下文回复的能力\n- xh_clear 清除当前用户的聊天记录\n',
    'author': 'Alpaca',
    'author_email': 'admin@alpaca.kim',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
