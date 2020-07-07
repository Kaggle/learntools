from learntools.core import *
import tensorflow as tf

class Q1(CodingProblem):
    _vars = ['image_condense', 'image_detect', 'image_filter', 'image']
    _hint = """
Your solution should look something like:
```python
image_condense = tf.nn.pool(
    input=____,
    window_shape=____,
    pooling_type=____,
    strides=____,
    padding=____,
)
```
"""
    _solution = CS("""
image_condense = tf.nn.pool(
    input=image_detect,
    window_shape=(2, 2),
    pooling_type='MAX',
    strides=(2, 2),
    padding='SAME',
)
""")
    def check(self, image_condense, image_detect, image_filter, image):
        image_condense_ = tf.nn.pool(
            input=image_detect,
            window_shape=(2, 2),
            pooling_type='MAX',
            strides=(2, 2),
            padding='SAME',
        )
        assert ((image_condense_ == image_condense),
                ("Something went wrong. The image you produced doesn't match the " +
                 "image I was expecting. Are your parameter values okay?"))


        
class Q2(ThoughtExperiment):
    _hint = "If you only had the final output to look at, would you be able to pick which circle originally produced it?"
    _solution ="""It would not be helpful. This exercise illustrates how maximum pooling creates the *translation invariance over small distances* we discussed in the tutorial. The maximum pooling operations reduce each of the inputs to an identical output. There wouldn't be any extra information being passed on to the head for classification.

Note, however, that this invariance only applies over *small* distances. Translating the circle by a larger amount actually could improve the classification. In fact, this method of transforming an image in random ways whenever it's used in training is known as **data augmentation**. Data augmentation is a common way of improving a classifier. You'll learn how to use it in Keras in Lesson 6.
"""

class Q3(ThoughtExperiment):
    _solution = """All else being equal, we might guess that average pooling would not be an improvement over maximum pooling, since maximum pooling attempts to retain only the *most important* pixels (those with greatest activation), while average pooling mixes together all kinds of pixels indiscriminantly.

On the other hand, with average pooling, high activation pixels grouped together would retain most of their activation, while isolated pixels would tend to vanish. Maximum pooling would tend to destroy this information. 

Which of these behaviors is desireable would depend on circumstances. With classification problems, experience has show that the combination of convolution, ReLU (or a variation), and maximum pooling produce the best results. With another problem, some other combination might work better. Intuition can be a valuble guide, but the parts of a machine learning model can interact in ways that are hard to predict. The surest way to know if something works? Try it and find out!
"""


# Free
class Q4A(CodingProblem):
    _hint = ""
    _solution = ""
    def check(self):
        pass
    
class Q4B(ThoughtExperiment):
    _hint = """VGG16 creates 512 features maps from an image, which might represent something like a wheel or a window. Each square in *Pooled Feature Maps* represents a feature. What would a large value for a feature mean?"""
    _solution = """The VGG16 base produces 512 feature maps. We can think of each feature map as representing some high-level visual feature in the original image -- maybe a wheel or window. Pooling a map gives us a single number, which we could think of as a *score* for that feature: large if the feature is present, small if it is absent. Cars tend to score high with one set of features, and Trucks score high with another. Now, instead of trying to map raw features to classes, the head only has to work with these scores that `GlobalAvgPool2D` produced, a much easier problem for it to solve.
"""

Q4 = MultipartProblem(Q4A, Q4B)


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3, Q4,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
