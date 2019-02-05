rm -r input
mkdir input 

kaggle datasets download dansbecker/hospital-readmissions -p input
unzip -q input/hospital-readmissions.zip -d input/hospital-readmissions
chmod 644 input/hospital-readmissions/*

kaggle datasets download dansbecker/new-york-city-taxi-fare-prediction -p input
unzip -q input/new-york-city-taxi-fare-prediction.zip -d input/new-york-city-taxi-fare-prediction
chmod 644 input/new-york-city-taxi-fare-prediction/*

kaggle datasets download mathan/fifa-2018-match-statistics -p input
unzip -q input/fifa-2018-match-statistics.zip -d input/fifa-2018-match-statistics
chmod 644 input/fifa-2018-match-statistics/*

rm input/*.zip

