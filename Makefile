output_dir = dist

cleandir:
	- cmd //C "rmdir /S /Q ${output_dir}"

wheel:
	make cleandir
	python setup.py sdist --formats=gztar  bdist_wheel

upload:
	twine upload dist/*.tar.gz dist/*.whl
