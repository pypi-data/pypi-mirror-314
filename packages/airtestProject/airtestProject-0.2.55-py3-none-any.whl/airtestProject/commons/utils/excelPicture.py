import os
import re
from xml.etree.ElementTree import fromstring
from io import BytesIO
from zipfile import ZipFile
from lxml import etree

from openpyxl.packaging.relationship import get_rels_path, get_dependents
from openpyxl.xml.constants import SHEET_DRAWING_NS, REL_NS, IMAGE_NS
from openpyxl.drawing.image import *

"""
author liuhuatong
des 获取图片路径，把excel表内嵌的图片另存起来，返回图片路径信息
date 2024/4/29
"""

def parse_element(element):
    """
    获取指定节点数据
    """
    data = {}
    xdr_namespace = "{%s}" % SHEET_DRAWING_NS
    targets = level_order_traversal(element, xdr_namespace + "nvPicPr")

    for target in targets:
        # 是一个cellimage
        cNvPr = embed = ""
        for child in target:
            if child.tag == xdr_namespace + "nvPicPr":
                cNvPr = child[0].attrib["name"]
            elif child.tag == xdr_namespace + "blipFill":
                _rel_embed = "{%s}embed" % REL_NS
                embed = child[0].attrib[_rel_embed]

        if cNvPr:
            data[cNvPr] = embed

    return data


def level_order_traversal(root, flag):
    """
    层次遍历，查找目标节点
    """
    queue = [root]
    targets = []
    while queue:
        node = queue.pop(0)
        children = [child.tag for child in node]
        if flag in children:
            targets.append(node)
            continue

        for child in node:
            queue.append(child)

    return targets


def handle_images(deps, archive, project, dir_name) -> []:
    """
    将图片二进制内容另存为
    """
    images = {}
    # if not PILImage:  # Pillow not installed, drop img
    #     return img

    for dep in deps:
        if dep.Type != IMAGE_NS:
            msg = "{0} 不支持的图像格式".format(dep.Type)
            print(msg)
            continue

        try:
            image_io = archive.read(dep.target)
            image = Image(BytesIO(image_io))
        except OSError:
            msg = "图像 {0} 将被删除，因为它无法读取".format(dep.target)
            print(msg)
            continue
        if image.format.upper() == "WMF":  # cannot save
            msg = "不支持 ｛0｝ 图像格式，因此正在删除该图像d".format(image.format)
            print(msg)
            continue
        image.embed = dep.id  # 文件rId
        image.target = dep.target  # 文件地址

        # 找到图片对象后，获取图片数据
        image_data = image_io

        image_name = image.target.split("/")[-1]
        # 使用文件名和'wb'模式写入图片数据
        images_path = "..//images//{}//{}".format(project, dir_name)
        if not os.path.exists(images_path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(images_path)

        with open("{}//{}".format(images_path, image_name), 'wb') as img_file:
            img_file.write(image_data)

        images.setdefault(image.embed, os.path.abspath("{}//{}".format(images_path, image_name)))

    return images


def parseElement(element):
    """
    获取指定节点数据
    """
    et = etree.fromstring(element)
    workSheets = et.findall("{*}sheetData")
    table = {}
    tablePlus = {}
    workSheetNames = []
    for workSheet in workSheets:
        # @*[local-name() = 'Name']获取当前节点下属性为Name的值
        rowName = workSheet.findall("{*}row")  # 返回的是个列表，用索引取出值
        workSheetNames.append(rowName)
        c = workSheet.xpath(".//*[local-name() = 'c']")
        for cell in c:
            v = cell.findall("{*}f")
            if len(v) != 0:
                match = re.search(r'\((.*?)\)', cell.findall("{*}f")[0].text)
                if match:
                    content_inside_brackets = match.group(1)
                    ID = content_inside_brackets.split(",")[0].strip('"')
                    table.setdefault(cell.attrib['r'], ID)
                    tablePlus.setdefault(cell.findall("{*}f")[0].text, ID)

    return table, tablePlus


def get_id_name(project="zg", PARSE_FILE_PATH = 'ZgTestCases1.xlsx', page=1):
    """获取excel表图片，id与文件路径的对应信息
    :param project: 项目
    :param PARSE_FILE_PATH: excel路径
    :param page: excel工坐表下标索引
    :return:
    """
    CELLIMAGE_PATH = "xl/cellimages.xml"
    sheetName = "xl/worksheets/sheet{}.xml".format(page+1)
    archive = ZipFile(PARSE_FILE_PATH, "r")

    sheet = archive.read(sheetName)
    src = archive.read(CELLIMAGE_PATH)  # 打开cellImage.xml文件
    deps = get_dependents(archive, get_rels_path(CELLIMAGE_PATH))  # 解析cellImage.xml._rel文件
    image_rels = handle_images(deps=deps.Relationship, archive=archive, project=project, dir_name=PARSE_FILE_PATH.split("\\")[-1].split(".")[0])

    node = fromstring(src)
    tabel, tabelPlus = parseElement(sheet)
    cellimages_xml = parse_element(node)

    for cnvpr, embed in cellimages_xml.items():
        cellimages_xml[cnvpr] = image_rels.get(embed)

    for ln, embed in tabel.items():
        tabel[ln] = cellimages_xml.get(embed)

    for ln, embed in tabelPlus.items():
        tabelPlus[ln] = cellimages_xml.get(embed)
    archive.close()  # 关闭压缩文件对象，防止内存泄漏
    return tabelPlus

if __name__ == '__main__':

    # 这个数字传入是sheet的下标，第一个sheet，第二个
    get_id_name(project="zg", PARSE_FILE_PATH='ZgTestCases.xlsx', page=0)
