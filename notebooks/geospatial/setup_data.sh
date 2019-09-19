rm -r ./input
mkdir input
kaggle datasets download alexisbcook/geospatial-learn-course-data -p input
unzip -q input/geospatial-learn-course-data.zip -d input/geospatial-learn-course-data
chmod 644 input/geospatial-learn-course-data/*.csv
