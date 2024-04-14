#$ delay 50

python -m nuitka Nuitka-Tests/onefile/HelloWorldTest.py
#$ expect \$

#$ delay 100
./HelloWorldTest.bin
#$ expect \$