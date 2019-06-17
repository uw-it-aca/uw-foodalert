. bin/activate
cd docs
pip install sphinx
pip install sphinx_rtd_theme
sphinx-apidoc -o ./source ..
mkdir build
make html
cd build/html
python -m http.server 8000
