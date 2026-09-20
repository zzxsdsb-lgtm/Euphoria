#!/usr/bin/env python3
"""把 assets/*.png 内嵌为 data-url 的 JS 文件，使页面在 file:// 协议下也能直接打开。
换用自己的初始图片时：替换 assets/dream.png 后重新运行本脚本。
"""
import base64
import os

os.chdir(os.path.join(os.path.dirname(__file__), '..', 'assets'))
for name in ['noise', 'dream']:
    with open(f'{name}.png', 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    with open(f'{name}.data.js', 'w') as f:
        f.write(f'// 自动生成：python3 tools/encode_assets.py（把 assets/{name}.png 内嵌为 data-url，使 file:// 直开可用）\n')
        f.write(f'window.ASSET_{name.upper()} = "data:image/png;base64,{b64}";\n')
    print(f'{name}.data.js written ({len(b64)} b64 chars)')
