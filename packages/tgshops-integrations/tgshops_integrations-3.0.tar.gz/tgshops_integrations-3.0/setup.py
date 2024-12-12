from setuptools import setup,find_packages

setup(
    name='tgshops_integrations',
    version='3.0',
    packages=find_packages(),
    install_requires=[
        # List your library's dependencies here
        # 'some_package',
    ],
    include_package_data=True,
    description='Library is intended to provide the integration of the external service or CRM system with the TelegramShops/'
                'It allows to configure the relationship between NocoDB list of the products used further to display in the shop/'
                'As a resultss the products can be synchronized and updated uppon the request.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://git.the-devs.com/virtual-shops/shop-system/shop-backend-integrations/integration-library/integration-library',  # Update with your URL
    author='Dimi Latoff',
    author_email='drpozd@gmail.com',
    license='MIT',  # Update with your chosen license
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)