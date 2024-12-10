from setuptools import setup, find_packages

setup(
    name='ketacli',
    version='0.33',
    packages=find_packages(),
    package_data={
        'ketacli': ['charts/*'],  # 使用 * 通配符来包含 charts 目录下所有内容
    },
    include_package_data=True,
    license='MIT',
    description='KetaDB Client',
    long_description=open('README.md', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    author='lvheyang',
    author_email='cuiwenzheng@ymail.com',
    url='https://xishuhq.com',
    install_requires=[
        "requests~=2.31.0",
        "prettytable~=3.10.0",
        "pyyaml~=6.0.1",
        "mando~=0.7.1",
        "argcomplete~=3.3.0",
        "faker~=24.11.0",
        "jinja2~=3.1.3",
        "rich~=13.7.1",
        "plotext~=5.2.8",
        "pynput~=1.7.7",
        "pygetwindow~=0.0.9",
        "pyperclip~=1.8.2"
    ],
    entry_points={
        'console_scripts': [
            'ketacli=ketacli.ketacli:start',
        ],
    },
)
