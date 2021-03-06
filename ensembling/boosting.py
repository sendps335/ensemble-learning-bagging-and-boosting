import util
import numpy as np
import sys
import random

PRINT = True


random.seed(42)
np.random.seed(42)

def small_classify(y):
    classifier, data = y
    return classifier.classify(data)

class AdaBoostClassifier:
    """
    AdaBoost classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    
    """

    def __init__( self, legalLabels, max_iterations, weak_classifier, boosting_iterations):
        self.legalLabels = legalLabels
        self.boosting_iterations = boosting_iterations
        self.classifiers = [weak_classifier(legalLabels, max_iterations) for _ in range(self.boosting_iterations)]
        self.alphas = [0]*self.boosting_iterations

    def train( self, trainingData, trainingLabels):
        """
        The training loop trains weak learners with weights sequentially. 
        The self.classifiers are updated in each iteration and also the self.alphas 
        """
        
        self.features = trainingData[0].keys()
        
        size_sampled_data = int(len(trainingData))
        sampled_weights = [(1.0/size_sampled_data)] * size_sampled_data
        

        for i in range(self.boosting_iterations):
            self.classifiers[i].train(trainingData, trainingLabels, sampled_weights)
            error = 0
            for j in range(len(trainingData)):
                if self.classifiers[i].classify([trainingData[j]])[0] != trainingLabels[j]:
                    error = error + sampled_weights[j]

            for j in range(len(trainingData)):
                if self.classifiers[i].classify([trainingData[j]])[0] == trainingLabels[j]:
                    sampled_weights[j]  = sampled_weights[j] * (error/ (1 - error))

            # Normalize the sampled_weight list
            sum_of_weights = sum(sampled_weights)
            for p in range(len(sampled_weights)):
                sampled_weights[p]  = sampled_weights[p] / sum_of_weights

            self.alphas[i] = np.log((1 - error) / error)
            #print "training loop: ", i





    def classify( self, data):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label. This is done by taking a polling over the weak classifiers already trained.
        See the assignment description for details.

        Recall that a datum is a util.counter.

        The function should return a list of labels where each label should be one of legaLabels.
        """

        
        prediction = []
        for i in range(len(data)):
            guesses = []
            for j in range(self.boosting_iterations):
                guesses.append(self.classifiers[j].classify([data[i]])[0] * self.alphas[j])

            prediction.append(int(np.sign(sum(guesses))))

        return prediction
