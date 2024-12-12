from setuptools import find_packages, setup

ESP_PPQ_VERSION = "v0.2.1"

def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content

setup(author='esp-dl',
      author_email='dcp-ppq@sensetime.com',
      description='PPQ is an offline quantization tools',
      long_description=readme(),
      long_description_content_type='text/markdown',
      install_requires=open('requirements.txt').readlines(),
      python_requires='>=3.6',
      name='esp-ppq',
      package_dir={'ppq': 'ppq'},
      packages=find_packages(where='ppq'),
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
      license='Apache License 2.0',
      include_package_data=True,
      version=ESP_PPQ_VERSION,
      zip_safe=False
    )
