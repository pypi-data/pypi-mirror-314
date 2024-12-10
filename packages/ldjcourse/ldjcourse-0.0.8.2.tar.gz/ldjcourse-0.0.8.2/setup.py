from setuptools import setup, find_packages

VERSION = '0.0.8.2'

setup(
    name='ldjcourse',
    version=VERSION,
    author='元蓝先生',
    description='该安装包是元蓝先生专门教学而设计，旨在帮助学生更好地理解和掌握相关技术。通过使用本包，用户将能够获得元蓝先生在教学过程中使用的工具和资源。元蓝先生是一位活跃于B站的教育工作者，分享了大量与编程、数据分析、人工智能等领域相关的教学内容。 您可以通过以下链接，找到更多关于元蓝先生的课程和资源：B站：元蓝先生 https://space.bilibili.com/3546564903569609',
    license='MIT',
    packages=find_packages()
)
