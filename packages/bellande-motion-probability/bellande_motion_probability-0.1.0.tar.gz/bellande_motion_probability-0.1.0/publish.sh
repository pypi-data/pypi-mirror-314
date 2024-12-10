cp ../../README.md ./
python setup.py sdist
twine upload dist/*
rm -r ./README.md
