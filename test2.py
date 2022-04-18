# 添加 accessToken

import yaml


xxx = {
    'JSESSIONID' : '222'
}
with open('config1.yaml', 'a', encoding="utf-8") as config:
    yaml.dump(data=xxx, stream=config, allow_unicode=True)