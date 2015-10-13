. venv/bin/activate
echo "Checking dependencies"
pip freeze |sort > tmp2.txt
cat requirements.txt|sort > tmp1.txt
file=`comm -23 <(sort tmp1.txt) <(sort tmp2.txt)`
rm tmp1.txt
rm tmp2.txt
if [ "$file" == "" ];
	then
	echo "No changes occur"
else
	echo "Downloading dependencies..."
	pip install -r requirements.txt
	echo "Finish"
fi