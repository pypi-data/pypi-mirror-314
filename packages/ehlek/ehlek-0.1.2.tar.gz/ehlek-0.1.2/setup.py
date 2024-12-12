from setuptools import setup, find_packages
# twine upload dist/*
setup(
    name='ehlek',  # 패키지 이름
    version='0.1.2',   # 버전
    packages=find_packages(),  # 패키지 자동 검색
    install_requires=[  # 필수 의존성 패키지
        'numpy', 
        'pandas',
        'ccxt',
        'ta',
        'pytz'
    ],
)
