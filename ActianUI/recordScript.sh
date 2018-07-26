#whoami
echo ----------------------------------------
echo starting scripts
echo ----------------------------------------
sleep 60
python ./vehicle_state.py &
sleep 20
python ./analyzeImgs.py &
