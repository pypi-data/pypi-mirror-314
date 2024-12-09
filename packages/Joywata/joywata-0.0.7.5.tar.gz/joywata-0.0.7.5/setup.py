from setuptools import setup, find_packages

'''
any: 适用于任何平台的通用版本。
manylinux1_x86_64: 适用于符合ManyLinux规范的x86_64 Linux系统。
win_amd64: 适用于64位Windows系统。
macosx_10_9_x86_64: 适用于OS X 10.9及以上版本的x86_64 Mac系统
'''

setup(
    name='Joywata', # 包名
    version='0.0.7.5',  # 版本
    description="wata tools",  # 包简介
    platforms=['Windows', 'Linux'],
    long_description=open('README.md').read(),  # 读取文件中介绍包的详细内容
    include_package_data=True,  # 是否允许上传资源文件
    author='wangtao',  # 作者
    author_email='1083719817@qq.com',  # 作者邮件
    maintainer='wangtao',  # 维护者
    maintainer_email='1083719817@qq.com',  # 维护者邮件
    license='MIT License',  # 协议
    url='',  # github或者自己的网站地址
    packages=find_packages(),  # 包的目录
    package_data={'': ['*.yaml', '*.txt', '*.bin', '*.pcd', '*.png', '*.gif', '*.ui','*.sh']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # 设置编写时的python版本
    ],
    options={
        'bdist_wheel': {
            'python_tag': 'None',
            'plat_name': 'any',
            'build_number': None,
            'dist_dir': None,
        }
    },
    # python_requires='>=3.6',  # 设置python版本要求
    install_requires=["tabulate"],  # 安装所需要的库
    entry_points={
        'console_scripts': [
            'wata=Joywata.console:wata_console',
        ],
    },  # 设置命令行工具(可不使用就可以注释掉)
)
