mkdir input

kaggle competitions download dog-breed-identification -p input/dog-breed-identification -f train.zip 
unzip input/dog-breed-identification/train.zip -d input/dog-breed-identification/


kaggle datasets download keras/resnet50 -p input/resnet50 --unzip

kaggle datasets download -d keras/vgg16 -p input/vgg16 --unzip

kaggle datasets download dansbecker/hot-dog-not-hot-dog -p input/hot-dog-not-hot-dog/seefood --unzip

kaggle datasets download dansbecker/dogs-gone-sideways -p input/dogs-gone-sideways --unzip
unzip input/dogs-gone-sideways/images.zip -d input/dogs-gone-sideways

kaggle datasets download zalando-research/fashionmnist -p input/fashionmnist --unzip

kaggle competitions download digit-recognizer -p input/digit-recognizer -f train.csv
