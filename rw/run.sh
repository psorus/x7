./clear.sh
cd raw
./run.sh
cd ..
cd ae
./run.sh
cd ..
cd fin
./run.sh
cd ..
cd mfin
./run.sh
cd ..
python3 summarize.py
python3 cat.py
