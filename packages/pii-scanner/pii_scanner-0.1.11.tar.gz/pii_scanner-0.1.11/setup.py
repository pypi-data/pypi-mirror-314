from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pii_scanner',
    version='0.1.11',
    packages=find_packages(),
    install_requires=[
        'unstructured==0.15.5',
        'presidio-analyzer==2.2.32',
        'openpyxl==3.1.5',
        'opencv-python==4.10.0.84',
        'pdf2image==1.17.0',
        'pytesseract==0.3.13',
        'PyPDF2==3.0.1',
        'python-docx==1.1.2',
        'python-pptx==1.0.2',
        'xmltodict==0.13.0',
        'scikit-image==0.24.0',
        'deskew==1.5.1',
        'gliner==0.2.10',
        'charset-normalizer==3.3.2',
        'idna==3.7',
        


        
        # add other dependencies here
    ],
    tests_require=['unittest'],
    description='A library for scanning Personally Identifiable Information (PII).',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specifies that the README is in Markdown format
    author='Ankit Gupta',  # Replace with your name
    author_email='devankitgupta01@gmail.com',  # Replace with your email
    url='https://github.com/devankit01/pii_scanner',  # Replace with your GitHub repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # or whichever license you're using
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Specify the minimum Python version required
)
