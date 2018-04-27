import tensorflow as tf

from tensorflow.python.keras.layers import Dense, Flatten, Conv2D, LeakyReLU

tfgan = tf.contrib.gan
leaky = LeakyReLU(0.2)

def basic_discriminator(img, unused_conditioning):
    """Discriminator network on MNIST digits.

    Args:
        img: Real or generated image. Should be in the range [-1, 1].
        unused_conditioning: The TFGAN API can help with conditional GANs, which
            would require extra `condition` information to both the generator and the
            discriminator. Since this example is not conditional, we do not use this
            argument.

    Returns:
        Logits for the probability that the image is real.
    """
    net = Conv2D(64, kernel_size=4, strides=2)(img)
    net = leaky(net)
    net = Conv2D(64, kernel_size=4, strides=2)(net)
    net = leaky(net)
    net = Conv2D(64, kernel_size=4)(net)
    net = leaky(net)

    net = Flatten()(net)
    net = Dense(1024)(net)
    net = leaky(net)
    net = Dense(1, activation='linear')(net)
    return net

def conditional_discriminator(img, conditioning):
    """Conditional discriminator network on MNIST digits.

    Args:
        img: Real or generated MNIST digits. Should be in the range [-1, 1].
        conditioning: A 2-tuple of Tensors representing (noise, one_hot_labels).

    Returns:
        Logits for the probability that the image is real.
    """

    _, one_hot_labels = conditioning
    net = Conv2D(64, kernel_size=4, strides=2)(img)
    net = leaky(net)
    net = tfgan.features.condition_tensor_from_onehot(net, one_hot_labels)
    net = Conv2D(128, kernel_size=4, strides=2)(net)
    net = leaky(net)
    net = Flatten()(net)
    net = Dense(1024)(net)
    net = leaky(net)
    net = Dense(1, activation='linear')(net)
    return net
