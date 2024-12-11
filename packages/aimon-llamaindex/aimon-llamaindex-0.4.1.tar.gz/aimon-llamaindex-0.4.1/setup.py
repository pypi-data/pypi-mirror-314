from setuptools import setup, find_packages

setup(name="aimon-llamaindex",
      version="0.4.1",
      packages=find_packages(),
      install_requires=[
          'aimon',
          'llama-index',
          'llama-index-vector-stores-milvus'
      ],
      author="Devvrat Bhardwaj",
      description="aimon-llamaindex package"
      )