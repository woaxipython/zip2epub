import os
import zipfile
import shutil

def create_epub_from_zip(zip_path, output_epub_path):
    """
    将包含特定文件结构的 ZIP 文件转换为 EPUB 文件。
    
    :param zip_path: 输入的 ZIP 文件路径
    :param output_epub_path: 输出 EPUB 文件路径
    """
    # 解压 ZIP 文件到临时目录
    temp_dir = "temp_epub"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # 创建 EPUB 的目录结构
    mimetype_path = os.path.join(temp_dir, "mimetype")
    meta_inf_path = os.path.join(temp_dir, "META-INF")
    oebps_path = os.path.join(temp_dir, "OEBPS")
    
    os.makedirs(meta_inf_path, exist_ok=True)
    os.makedirs(oebps_path, exist_ok=True)

    # 创建 mimetype 文件
    with open(mimetype_path, 'w') as f:
        f.write("application/epub+zip")
    
    # 创建 META-INF/container.xml 文件
    container_xml = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>
"""
    with open(os.path.join(meta_inf_path, "container.xml"), 'w') as f:
        f.write(container_xml)
    
    # 移动文件到 OEBPS 文件夹
    for item in os.listdir(temp_dir):
        item_path = os.path.join(temp_dir, item)
        if item not in ["mimetype", "META-INF", "OEBPS"]:
            shutil.move(item_path, oebps_path)

    # 创建 content.opf 文件（简单示例）
    content_opf = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>Sample EPUB</dc:title>
        <dc:language>en</dc:language>
    </metadata>
    <manifest>
        <item id="info" href="info.txt" media-type="text/plain"/>
    </manifest>
    <spine>
        <itemref idref="info"/>
    </spine>
</package>
"""
    with open(os.path.join(oebps_path, "content.opf"), 'w') as f:
        f.write(content_opf)
    
    # 打包为 EPUB 文件
    with zipfile.ZipFile(output_epub_path, 'w') as epub:
        # 添加 mimetype 文件（不压缩）
        epub.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)
        # 添加其他文件
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                if arcname != "mimetype":  # mimetype 已添加
                    epub.write(file_path, arcname)
    
    # 清理临时目录
    shutil.rmtree(temp_dir)
    print(f"EPUB 文件已生成：{output_epub_path}")

# 示例用法
zip_path = r"D:\01赵延腾\book\3744274\创新者的窘境.zip"  # 输入 ZIP 文件路径
output_epub_path = "output.epub"  # 输出 EPUB 文件路径
create_epub_from_zip(zip_path, output_epub_path)
