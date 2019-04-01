rm -r ./input
mkdir input
kaggle datasets download alexisbcook/data-for-datavis -p input
unzip -q input/data-for-datavis.zip -d input
chmod 644 input/*.csv
