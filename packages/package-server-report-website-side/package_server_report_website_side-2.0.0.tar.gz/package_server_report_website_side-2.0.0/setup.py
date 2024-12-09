from setuptools import setup, find_packages

setup(
    name='package_server_report_website_side',  # Choose a unique name for your package
    version='2.0.0',                           # Use semantic versioning
    description='A web application for monitoring and reporting',
    author='Nishal',
    author_email='your.email@example.com',
    # url='https://github.com/yourusername/package_server_report_website_side',  # Replace with your project URL
    packages=find_packages(),  # Automatically discover all packages (e.g., monitor, report)
    include_package_data=True,  # Include additional files like templates in the distribution
    install_requires=[
        # List any dependencies here, e.g., Flask, requests, etc.
        'flask',  # Example if you're using Flask
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version
)
