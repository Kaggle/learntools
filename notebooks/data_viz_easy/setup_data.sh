mkdir input
kaggle datasets download alexisbcook/datavizeasy -p input
unzip -q input/datavizeasy.zip -d input
chmod 644 input/*.csv
