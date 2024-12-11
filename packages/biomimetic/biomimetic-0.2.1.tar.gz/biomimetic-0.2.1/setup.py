from setuptools import setup, find_packages

setup(
    name='biomimetic',
    version='0.2.1',
    author='Sari Itani and Dr. Ziad Doughan',
    author_email='sariitani101@gmail.com',
    description='A Python library for biomimetic cell models in neural networks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='biomimetic neural networks machine learning',
    install_requires=[line.strip() for line in open("requirements.txt", "r")],
    python_requires='>=3.6',
    package_data={
        'biomimetic': ['data/*.data'],
    },
    include_package_data=True,
    zip_safe=False
)
