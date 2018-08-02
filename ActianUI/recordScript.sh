#whoami
echo ----------------------------------------
echo starting scripts
echo ----------------------------------------
sleep 60
#sleep 5
./flightAnalysis/fullReport_psql/vehicle_state.py &
sleep 20
./flightAnalysis/movidius/analyzeImgs.py &
