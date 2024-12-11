import asyncio
import hashlib
import os
from datetime import datetime

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from jinja2 import Template
import markdown
from PIL import Image
import io

from xhm_html2image.MinIOClient import xhm_oss


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def markdown_to_html(markdown_content):
    return markdown.markdown(markdown_content, extensions=['extra', 'codehilite'])


def render_template(template_string, context):
    template = Template(template_string)
    return template.render(context)


async def html_to_image(html_content, width=1242):  # 使用iPhone 8 Plus的宽度作为默认值
    url = None
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': width, 'height': 100})  # 初始高度不重要

        image_file_name = hashlib.md5(html_content.encode('utf-8')).hexdigest()
        output_file = f"{image_file_name}.png"

        try:
            await page.set_content(html_content, wait_until='networkidle')
            # 使用 JavaScript 增加页面缩放比例以提高细节
            # page.evaluate('document.body.style.zoom = "1.0"')

            # 获取页面的实际高度
            height = await page.evaluate('document.documentElement.scrollHeight')
            await page.set_viewport_size({'width': width, 'height': height})

            # 截取整个页面
            screenshot = await page.screenshot(full_page=True)

            # 使用 Pillow 处理和保存图像
            image = Image.open(io.BytesIO(screenshot))
            image.save(output_file)

            date_str = datetime.now().strftime("%Y%m%d")

            object_name = xhm_oss.upload(
                object_name=xhm_oss.auto_object_name(file_path=output_file, object_dir=f"screen/{date_str}"),
                file_path=output_file)
            url = xhm_oss.get_url(object_name=object_name)

            print(f"Image saved as {output_file} url: {url}")
        finally:
            await browser.close()
            # 判断路径是否为文件
            if os.path.isfile(output_file):  # 如果是文件
                # 删除文件
                os.remove(output_file)

    return url


def mkqrcode(data: str):
    import qrcode
    import base64
    from io import BytesIO

    # 生成二维码图像
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )

    # 添加数据
    qr.add_data(data)
    qr.make(fit=True)

    # 生成二维码图像
    img = qr.make_image(fill='black', back_color='white')

    # 将图像转换为Base64编码的字符串
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


async def process_markdown_and_template(title: str, content: str, width=1242,
                                        author: str = "",
                                        qrcode_data: str = "",
                                        qrcode_url: str = "",
                                        template_file: str = "template_rich.html"):
    if not title or not content:
        return ""
    template_file = os.path.join(os.path.dirname(__file__), template_file)
    html_content = markdown_to_html(content)
    html_template = read_file(template_file)
    qrcode = ""
    if not qrcode_url and qrcode_data:
        qrcode = mkqrcode(qrcode_data)
    full_html = render_template(html_template,
                                {'content': html_content, "title": title, "author": author, "qrcode": qrcode,
                                 "qrcode_url": qrcode_url})
    return await html_to_image(full_html, width)


if __name__ == "__main__":
    # 使用示例
    title = "中国选手领奖台上的这个动作刷屏！网友：彰显奥林匹克的意义"
    content = """### 中国选手领奖台上的这个动作刷屏4"""
    author = """"""
    qrcode_data = "https://fs-oss.fscut.com/wechat/screen/20240806/81cd8ab53cad58104c934b5d591b14d3.png"
    qrcode_url = "https://fs-oss.fscut.com/wechat/robot/cypnest_qrcode.png"

    asyncio.run(process_markdown_and_template(title=title, content=content, author=author, qrcode_data=qrcode_data,
                                              qrcode_url=qrcode_url))
