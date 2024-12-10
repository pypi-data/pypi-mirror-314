import setuptools
with open('README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='web_console_log',
	version='0.1.0',
	author='Super_Zombi',
	author_email='super.zombi.yt@gmail.com',
	description='Python Web Console',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/SuperZombi/Web-Console',
	packages=['web_console'],
	install_requires=["eventlet", "python-socketio"],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.9',
)