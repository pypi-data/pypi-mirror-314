from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

class WordUtils:
    """
    Word工具类，用于填充Word模板并生成新的文档
    """

    @staticmethod
    def fill_template(template_path, data, output_path):
        """
        填充Word模板并生成新的文档

        :param template_path: Word模板文件路径
        :param data: 需要填充的数据，格式为字典
        :param output_path: 输出文档路径
        :return: None
        """
        doc = Document(template_path)

        # 替换文本内容
        for paragraph in doc.paragraphs:
            for key, value in data.items():
                if key in paragraph.text:
                    paragraph.text = paragraph.text.replace(key, str(value))

        # 保存文档
        doc.save(output_path)


if __name__ == '__main__':
    # 定义模板路径、输出路径和要填充的数据
    template_path = 'template.docx'
    output_path = 'output.docx'
    data = {
        '{{name}}': '张三',
        '{{age}}': 30,
        '{{city}}': '北京'
    }

    # 填充模板并生成新的文档
    WordUtils.fill_template(template_path, data, output_path)
