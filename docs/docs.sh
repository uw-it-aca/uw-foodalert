cd docs
pip install sphinx
pip install sphinx_rtd_theme
sphinx-apidoc -o . ..
make html
