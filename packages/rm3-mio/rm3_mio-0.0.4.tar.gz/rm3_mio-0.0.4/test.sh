rm -rf virt
python3.9 -m venv virt
source virt/bin/activate
pip install twine
pip install --upgrade pip
pip install .
python -i -c "print('>>> import mio');import mio"