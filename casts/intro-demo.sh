#$ delay 50

cat csvsum.py
#$ expect \$

#$ delay 50
python -m nuitka --mode=onefile --remove-output csvsum.py
#$ expect \$

#$ delay 80
./csvsum.bin sales.csv --column amount
#$ expect \$
