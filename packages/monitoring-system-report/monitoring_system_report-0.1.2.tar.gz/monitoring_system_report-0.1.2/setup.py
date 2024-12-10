# from setuptools import setup, find_packages
# import subprocess
#
# def open_port():
#     port = 5000
#     print(f"Opening port {port}")
#     try:
#         # Using the `ufw` command to open port (Linux firewall tool)
#         subprocess.run(["ufw", "allow", str(port)], check=True)
#         print(f"Port {port} opened successfully.")
#     except Exception as e:
#         print(f"Failed to open port {port}. {e}")
#
# setup(
#     name='server_report',
#     version='1.0.0',
#     author='Your Name',
#     description='A simple CPU monitoring agent with Flask integration',
#     install_requires=[
#         'psutil',
#         'Flask',
#     ],
#     entry_points={
#         'console_scripts': [
#             'cpu-monitor = main:main'
#         ]
#     },
#     cmdclass={
#         'install': open_port
#     }
# )

from setuptools import setup, find_packages

setup(
    name='monitoring_system_report',               # Name of the package
    version='0.1.2',                         # Version number
    author='Your Name',
    author_email='your.email@example.com',
    description='A monitoring system with an agent and a server.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/monitoring_systems',  # GitHub or project URL
    packages=find_packages(),                # Finds all subpackages automatically
    include_package_data=True,               # Includes files specified in MANIFEST.in
    install_requires=[
        # List your dependencies here
        'flask',  # Example dependency
    ],
    entry_points={
        'console_scripts': [
            'start-agent=monitoring_system_report.agent.agent:main',  # Command to run agent
            'start-server=monitoring_system_report.server.server:main',  # Command to run server
            'start-http-bridge=monitoring_system_report.server.http_bridge:main',  # Command to run HTTP bridge
            'config_loader=monitoring_system_report.server.config_loader:load_config',  # Command to show config
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
