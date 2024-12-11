### 安装chromium

    playwright install


### 需要版本一致

    https://github.com/microsoft/playwright-python/releases


     playwright --version
     Version 1.47.0

    https://github.com/microsoft/playwright-python/releases 里面Version 1.47.0要求的版本是：

    Browser Versions
    Chromium 129.0.6668.29
    Mozilla Firefox 130.0
    WebKit 18.0

    # 安装对应版本
    https://chromium.googlesource.com/chromium/src/+/refs/tags/129.0.6668.29
    https://chromiumdash.appspot.com/releases?platform=Windows
    https://www.chromedriverdownload.com/zh/download/chromedriver-129.0.6668.29-mac%20arm64#google_vignette

     rm -rf /Users/zouhuigang/Library/Caches/ms-playwright/
     sudo playwright install

     
    node:internal/bootstrap/switches/does_own_process_state:144
    cachedCwd = rawMethods.cwd();
                           ^

Error: ENOENT: no such file or directory, uv_cwd
    at process.wrappedCwd [as cwd] (node:internal/bootstrap/switches/does_own_process_state:144:28)
    at /Users/zouhuigang/anaconda3/envs/py3/lib/python3.10/site-packages/playwright/driver/package/lib/utilsBundleImpl/index.js:35:85156
    at /Users/zouhuigang/anaconda3/envs/py3/lib/python3.10/site-packages/playwright/driver/package/lib/utilsBundleImpl/index.js:1:222
    at Object.<anonymous> (/Users/zouhuigang/anaconda3/envs/py3/lib/python3.10/site-packages/playwright/driver/package/lib/utilsBundleImpl/index.js:44:14541)
    at Module._compile (node:internal/modules/cjs/loader:1469:14)
    at Module._extensions..js (node:internal/modules/cjs/loader:1548:10)
    at Module.load (node:internal/modules/cjs/loader:1288:32)
    at Module._load (node:internal/modules/cjs/loader:1104:12)
    at Module.require (node:internal/modules/cjs/loader:1311:19)
    at require (node:internal/modules/helpers:179:18) {
  errno: -2,
  code: 'ENOENT',
  syscall: 'uv_cwd'
}

Node.js v20.17.0


重新打开terminal

### 使用

        
    
   ```
    
if __name__ == "__main__":
    # 使用示例
    title = "中国选手领奖台上的这个动作刷屏！网友：彰显奥林匹克的意义"
    content = """### CypNest 桥接功能

CypNest中的桥接功能是一项技术，允许在排样时自动将文字转换为曲线，以便更好地处理和展示 。然而，CypNest软件已经引入了一种新的连筋字体功能，旨在替代桥接功能，从而减少手动设置的时间和精力 。

### 连筋字体功能

连筋字体功能的引入是为了提高用户的效率。在没有连筋字体之前，用户需要手动设置桥接功能，这非常耗时。现在，用户可以在零件上已有文字的情况下，使用文字编辑来批量设置文字字体，或者在图纸处理界面添加文字，并使用连筋字体 。这大大简化了操作流程，提升了工作效率。

### 操作方法

要使用连筋字体功能，用户可以在零件编辑界面选择连筋字体，保存并返回即可。具体操作步骤如下：

1. 在排样界面点击“从文件导入并编辑”按钮进入图纸处理界面。
2. 在左侧零件列表零件上“右击-编辑/替换此零件”进入零件编辑界面。
3. 选择连筋字体，保存并返回 。

### 总结

虽然桥接功能仍然存在，但CypNest软件更推荐使用连筋字体功能来替代桥接功能，以提高效率和简化操作。如果您仍然需要使用桥接功能，可以在排样时自动将文字转换为曲线来实现。

希望这些信息对您有所帮助。如果您有更多问题，请随时联系CypNest客服 。"""
    author = """"""
    qrcode_data = "https://fs-oss.fscut.com/wechat/screen/20240806/81cd8ab53cad58104c934b5d591b14d3.png"

    asyncio.run(process_markdown_and_template(title=title, content=content, author=author, qrcode_data=qrcode_data))
   ```