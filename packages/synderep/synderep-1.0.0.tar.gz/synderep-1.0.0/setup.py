from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
    name="synderep",
    version="1.0.0",
    description="stress tester for website",
    author="alfie",
    author_email="alfiehart481@gmail.com",
    url="",
    packages=find_packages(),  # Automatically finds the `synderep` folder
    python_requires=">=3.6",
)
