kaggle competitions download dog-breed-identification -p ./dog-breed-identification -f train.zip
unzip ./dog-breed-identification/train.zip -d ./dog-breed-identification/
rm ./dog-breed-identification/train.zip

kaggle datasets download keras/resnet50 -p resnet50
unzip resnet50/resnet50.zip -d resnet50


kaggle datasets download dansbecker/hot-dog-not-hot-dog -p hot-dog-not-hot-dog --unzip
unzip hot-dog-not-hot-dog/hot-dog-not-hot-dog.zip -d hot-dog-not-hot-dog/


kaggle datasets download dansbecker/dogs-gone-sideways -p dogs-gone-sideways --unzip
unzip dogs-gone-sideways/images.zip -d dogs-gone-sideways/

kaggle datasets download zalando-research/fashionmnist -p fashionmnist

kaggle competitions download digit-recognizer -p ./digit-recognizer -f train.csv
