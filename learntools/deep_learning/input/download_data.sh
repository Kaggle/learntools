kaggle competitions download dog-breed-identification -p ./dog-breed-identification -f train.zip
unzip ./dog-breed-identification/train.zip -d ./dog-breed-identification/
rm ./dog-breed-identification/train.zip

kaggle datasets download keras/resnet50 -p resnet50

kaggle datasets download -d keras/vgg16 -p vgg16

kaggle datasets download -d keras/inceptionv3 -p inceptionv3

kaggle datasets download dansbecker/hot-dog-not-hot-dog -p hot-dog-not-hot-dog/seefood --unzip

kaggle datasets download dansbecker/dogs-gone-sideways -p dogs-gone-sideways --unzip
unzip dogs-gone-sideways/images.zip -d dogs-gone-sideways/

kaggle datasets download zalando-research/fashionmnist -p fashionmnist --unzip

kaggle competitions download digit-recognizer -p ./digit-recognizer -f train.csv
