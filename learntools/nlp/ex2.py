import random

import numpy as np
import pandas as pd
import spacy
from spacy.util import minibatch
import textwrap
from spacy.training.example import Example


from learntools.core import *

def load_data(csv_file, split=0.8):
    data = pd.read_csv(csv_file)
    
    # Shuffle data
    train_data = data.sample(frac=1, random_state=7)
    
    texts = train_data.text.values
    labels = [{"POSITIVE": bool(y), "NEGATIVE": not bool(y)}
              for y in train_data.sentiment.values]
    split = int(len(train_data) * split)
    
    train_labels = [{"cats": labels} for labels in labels[:split]]
    val_labels = [{"cats": labels} for labels in labels[split:]]
    
    return texts[:split], train_labels, texts[split:], val_labels

train_texts, train_labels, val_texts, val_labels = load_data('../input/nlp-course/yelp_ratings.csv')

def create_model():
    # Create an empty model
    nlp = spacy.blank("en")

    # Add the TextCategorizer to the empty model
    textcat = nlp.add_pipe("textcat")

    # Add NEGATIVE and POSITIVE labels to text classifier
    textcat.add_label("NEGATIVE")
    textcat.add_label("POSITIVE")

    return nlp

def train_func(model, train_data, optimizer, batch_size=8):
    losses = {}
    random.seed(1)
    random.shuffle(train_data)
    for batch in minibatch(train_data, size=batch_size):
        for text, labels in batch:
            doc = model.make_doc(text)
            example = Example.from_dict(doc, labels)
            # Update model with texts and labels
            model.update([example], sgd=optimizer, losses=losses)
        
    return losses

class EvaluateFeedbackFormApproach(ThoughtExperiment):
    _solution = ("Any way of setting up an ML problem will have multiple strengths and weaknesses.  "
                 "So you may have thought of different issues than listed here.\n\nThe strength of this "
                 "approach is that it allows you to distinguish positive email messages from negative emails "
                 "even though you don't have historical emails that you have labeled as positive or negative.\n\n"
                 "The weakness of this approach is that emails may be systematically different from Yelp reviews "
                 "in ways that make your model less accurate. For example, customers might generally use different "
                 "words or slang in emails, and the model based on Yelp reviews won't have seen these words.\n\n"
                 "If you wanted to see how serious this issue is, you could compare word frequencies between the two sources. "
                 "In practice, manually reading a few emails from each source may be enough to see if it's a serious issue. \n\n"
                 "If you wanted to do something fancier, you could create a dataset that contains both Yelp reviews and emails "
                 "and see whether a model can tell a reviews source from the text content. Ideally, you'd like to find "
                 "that model didn't perform well, because it would mean your data sources are similar. That approach seems "
                 "unnecessarily complex here.")

class CreateTextCatModel(CodingProblem):
    _var = 'nlp'
    _hint = ("After creating the empty model, use .create_pipe to add the TextCategorizer "
             "to the nlp model. Set the config appropriately for exclusive classes and bow "
             "architecture. Then use .add_label to add labels.")
    _solution = CS("""
# Create an empty model
nlp = spacy.blank("en")

# Add the TextCategorizer to the empty model
textcat = nlp.add_pipe("textcat")

# Add labels to text classifier
textcat.add_label("NEGATIVE")
textcat.add_label("POSITIVE")
    """)

    def check(self, nlp):
        assert nlp.has_pipe('textcat'), "Please add a TextCategorizer to the model's pipeline"

        textcat = nlp.get_pipe('textcat')
        message = f"TextCatagorizer labels should be ('NEGATIVE', 'POSITIVE'), we found {textcat.labels}"
        assert textcat.labels == ('NEGATIVE', 'POSITIVE'), message


class TrainFunction(CodingProblem):
    _var = 'train'
    _hint = ("For training the model, use `model.update`.")
    _solution = CS("""
def train(model, train_data, optimizer, batch_size=8):
    losses = {}
    random.seed(1)
    random.shuffle(train_data)
    
    for batch in minibatch(train_data, size=batch_size):
        for text, labels in batch:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, labels)
            # Update model with texts and labels
            model.update([example], sgd=optimizer, losses=losses)
        
    return losses
""")

    def check(self, train):
        
        def soln_func(model, train_data, optimizer, batch_size=8):
            losses = {}
            random.seed(1)
            random.shuffle(train_data)

            for batch in minibatch(train_data, size=batch_size):
                for text, labels in batch:
                    doc = model.make_doc(text)
                    example = Example.from_dict(doc, labels)
                    # Update model with texts and labels
                    model.update([example], sgd=optimizer, losses=losses)
                    
            return losses
        
        train_data = list(zip(train_texts, train_labels))
        
        spacy.util.fix_random_seed(1)
        random.seed(1)
        nlp = create_model()
        optimizer = nlp.begin_training()
        student_losses = train(nlp, train_data[:1000], optimizer)

        spacy.util.fix_random_seed(1)
        random.seed(1)
        nlp = create_model()
        optimizer = nlp.begin_training()
        soln_losses = soln_func(nlp, train_data[:1000], optimizer)

        assert student_losses == soln_losses, "Your loss isn't the same as our solution. Make sure to set batch size to 8."

class PredictFunction(CodingProblem):
    _var = 'predict'
    _hint = ("You can use `nlp.tokenizer()` on each text example to tokenize the input data. "
             "To make predictions, you want to get the TextCategorizer object "
             "with `nlp.get_pipe()`. The use .predict on the TextCategorizer to get the scores. "
             "With the scores array, the .argmax method will return the index of the highest "
             "value. Take note of the axis argument in .argmax so you're finding the max index "
             "for each example")
    _solution = CS("""
def predict(nlp, texts): 
    # Use the model's tokenizer to tokenize each input text
    docs = [nlp.tokenizer(text) for text in texts]
    
    # Use textcat to get the scores for each doc
    textcat = nlp.get_pipe("textcat")
    scores = textcat.predict(docs)
    
    # From the scores, find the class with the highest score/probability
    predicted_class = scores.argmax(axis=1)
    
    return predicted_class""")

    def check(self, predict):
        
        def soln_func(nlp, texts):
            # Use the model's tokenizer to tokenize each input text
            docs = [nlp.tokenizer(text) for text in texts]

            # Use textcat to get the scores for each doc
            textcat = nlp.get_pipe("textcat")
            scores = textcat.predict(docs)

            # From the scores, find the class with the highest score/probability
            predicted_class = scores.argmax(axis=1)

            return predicted_class

        spacy.util.fix_random_seed(1)
        nlp = create_model()
        optimizer = nlp.begin_training()
        train_data = list(zip(train_texts, train_labels))
        _ = train_func(nlp, train_data[:1000], optimizer)
        student_predicted = predict(nlp, val_texts[20:30])
        soln_predicted = soln_func(nlp, val_texts[20:30])

        assert np.all(student_predicted == soln_predicted)

class EvaluateFunction(CodingProblem):
    _var = 'evaluate'
    _hint = ("Use your predict function to get the predicted classes. "
             "The labels look like `{'cats': {'POSITIVE':True, 'NEGATIVE': False}}`, "
             "you'll need to convert these into 1s where POSITIVE is True, and 0 where "
             "POSITIVE is False. Once you have the predictions and true classes, calculate "
             "the accuracy")
    _solution = CS("""
    def evaluate(model, texts, labels):
        # Get predictions from textcat model
        predicted_class = predict(model, texts)
        
        # From labels, get the true class as a list of integers (POSITIVE -> 1, NEGATIVE -> 0)
        true_class = [int(each['cats']['POSITIVE']) for each in labels]
        
        # A boolean or int array indicating correct predictions
        correct_predictions = predicted_class == true_class
        
        # The accuracy, number of correct predictions divided by all predictions
        accuracy = correct_predictions.mean()
        
        return accuracy
    """)

    def check(self, evaluate):
        def soln_func(model, texts, labels):

            def predict (model, texts):
                docs = [model.tokenizer(text) for text in texts]
                textcat = model.get_pipe('textcat')
                scores = textcat.predict(docs)
                return scores.argmax(axis=1)

            # Get predictions from textcat model
            predicted_class = predict(model, texts)
            # From labels, get the true class as a list of integers (POSITIVE -> 1, NEGATIVE -> 0)
            true_class = [int(each['cats']['POSITIVE']) for each in labels]
            # A boolean or int array indicating correct predictions
            correct_predictions = predicted_class == true_class
            # The accuracy, number of correct predictions divided by all predictions
            accuracy = correct_predictions.mean()
            return accuracy

        spacy.util.fix_random_seed(1)
        nlp = create_model()
        optimizer = nlp.begin_training()
        train_data = list(zip(train_texts, train_labels))
        _ = train_func(nlp, train_data[:1000], optimizer)
        student_acc = evaluate(nlp, val_texts[:30], val_labels[:30])
        soln_acc = soln_func(nlp, val_texts[:30], val_labels[:30])

        assert np.all(student_acc == soln_acc)

class ModelOptimizationQuestion(ThoughtExperiment):
    _solution = ("Answer: There are various hyperparameters to work with here. The biggest one "
                 "is the TextCategorizer architecture. You used the simplest model which trains "
                 "faster but likely has worse performance than the CNN and ensemble models. "
                 )

qvars = bind_exercises(globals(), [
    EvaluateFeedbackFormApproach,
    CreateTextCatModel,
    TrainFunction,
    PredictFunction,
    EvaluateFunction,
    ModelOptimizationQuestion
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
