import os
import zipfile
import shutil


class zip2epub(object):
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.temp_dir = "temp_epub"
        """
        将微信读书下载下的zip文件，转换为epub文件
        : param zip_path: 微信读书下载下的zip文件
        """

    def zip2dir(self):
        "将zip文件转换到临时目录"
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)

        with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
            zip_ref.extractall(self.temp_dir)

    def epub_path(self):
        "创建epub的目录结构"
        mimetype_path = os.path.join(self.temp_dir, "mimetype")
        meta_inf_path = os.path.join(self.temp_dir, "META-INF")
        oebps_path = os.path.join(self.temp_dir, "OEBPS")

        os.makedirs(meta_inf_path, exist_ok=True)
        os.makedirs(oebps_path, exist_ok=True)

        with open(mimetype_path, "w") as f:
            f.write("application/epub+zip")
