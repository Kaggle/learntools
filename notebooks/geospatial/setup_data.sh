rm -r ./input
mkdir input
kaggle datasets download alexisbcook/geospatial-learn-course-data -p input
unzip -q input/geospatial-learn-course-data.zip -d input
chmod 644 input/*.csv
