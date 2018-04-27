
import tensorflow as tf

from tensorflow.python.keras.layers import Conv2D, Conv2DTranspose, Conv3D, Dense, Reshape

tfgan = tf.contrib.gan

def basic_generator(noise):
    """Simple generator to produce MNIST images.

    Args:
        noise: A single Tensor representing noise.

    Returns:
        A generated image in the range [-1, 1].
    """
    channels_after_reshape = 256

    net = Dense(1024, activation='elu')(noise)
    net = Dense(7 * 7 * channels_after_reshape, activation='elu')(net)
    net = Reshape([7, 7, channels_after_reshape])(net)
    net = Conv2DTranspose(64, kernel_size=4, strides=2, padding="same", activation='elu')(net)
    net = Conv2DTranspose(32, kernel_size=4, strides=2, padding="same", activation='elu')(net)
    # Make sure that generator output is in the same range as `inputs`
    # ie [-1, 1].
    net = Conv2D(1, kernel_size=4, activation = 'tanh', padding='same')(net)
    return net

def conditional_generator(inputs):
    """Generator to produce MNIST images.

    Args:
        inputs: A 2-tuple of Tensors (noise, one_hot_labels).

    Returns:
        A generated image in the range [-1, 1].
    """

    noise, one_hot_labels = inputs
    channels_after_reshape = 128

    net = Dense(1024, activation='elu')(noise)
    net = tfgan.features.condition_tensor_from_onehot(net, one_hot_labels)
    net = Dense(7 * 7 * channels_after_reshape, activation='elu')(net)
    net = Reshape([7, 7, channels_after_reshape])(net)
    net = Conv2DTranspose(64, kernel_size=4, strides=2, padding="same", activation='elu')(net)
    net = Conv2DTranspose(32, kernel_size=4, strides=2, padding="same", activation='elu')(net)
    # Make sure that generator output is in the same range as `inputs`
    # ie [-1, 1].
    net = Conv2D(1, kernel_size=4, activation = 'tanh', padding='same')(net)
    return net


def encoder_decoder_generator(start_img):
    """
    """

    layer1 = Conv2D(64, kernel_size=4, strides=2, activation='elu', padding='same')(start_img)
    layer2 = Conv2D(64, kernel_size=4, strides=2, activation='elu', padding='same')(layer1)
    layer3 = Conv2D(64, kernel_size=4, strides=1, activation='elu', padding='same')(layer2)
    layer4 = Conv2DTranspose(64, kernel_size=4, strides=2, activation='elu', padding="same")(layer3)
    layer5 = Conv2DTranspose(64, kernel_size=4, strides=2, activation='elu', padding="same")(layer4)
    layer6 = Conv2D(64, kernel_size=2, strides=1, activation='elu', padding='same')(layer5)
    # Make sure that generator output is in the same range as `inputs`
    # ie [-1, 1].
    net = Conv2D(3, kernel_size=1, activation = 'tanh', padding='same')(layer6)
    return net
