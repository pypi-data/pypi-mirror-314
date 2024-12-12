# setup.py

from setuptools import setup, find_packages

setup(
    name='aimanual',  # 패키지 이름
    version='0.1',     # 버전
    packages=find_packages(),  # 패키지 자동 탐색
    install_requires=[],  # 외부 의존성 (없으면 빈 리스트)
    author='Zoony',  # 작성자
    author_email='onepage4you@gmail.com',  # 이메일
    description='A manual package for ai beginner',  # 간단한 설명
    long_description=open('README.md').read(),  # 긴 설명 (README.md 파일로부터 읽음)
    long_description_content_type='text/markdown',  # Markdown 형식
    url='https://github.com/',  # 프로젝트 URL
    classifiers=[  # PyPI에서 보여지는 분류
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 지원하는 Python 버전
)
