from functools import reduce
import numpy as np
from . import learning_utils
from decimal import Decimal
import operator

class NaiveBayes():
    def __init__(self):
        """
        Model must be trained before data can be tested against it.
        """
        self._label_priors = None
        self._feature_priors = None
        self._feature_posteriors = None

    def train(self, samples):
        """
        Trains the Naive Bayes model using a given array of Sample objects
        :param samples: An array of Sample objects.
        """
        self._label_priors = NaiveBayes.learn_label_priors(samples)
        self._feature_priors = NaiveBayes.learn_feature_priors(samples)
        self._feature_posteriors = NaiveBayes.learn_feature_posteriors(samples)

    def test(self, data):
        """
        Tests data against the learned model
        :param data: An array of binary values
        :return: label
        """
        if self._label_priors is None or \
            self._feature_priors is None or \
            self._feature_posteriors is None:
            raise Exception("Model not trained yet")

        ret = {}
        for label in self.label_priors:
            posterior_values = map(lambda x: Decimal(abs(x[0] - 1 + x[1])),
                zip(data, self.feature_posteriors[label]))
            denom_values = map(lambda x: Decimal(abs(x[0] - 1 + x[1])),
                zip(data, self.feature_priors))
            ret[label] = learning_utils.prod(posterior_values)
        return max(ret.keys(), key=lambda x: ret[x])

    @property
    def label_priors(self):
        """
        Read only
        """
        return self._label_priors

    @property
    def feature_priors(self):
        """
        Read only
        """
        return self._feature_priors

    @property
    def feature_posteriors(self):
        """
        Read only
        """
        return self._feature_posteriors

    def learn_label_priors(samples):
        """
        Values is add-one smoothed
        :param samples: An array of Sample objects
        :return: label priors
        """
        priors = {}
        for sample in samples:
            if sample.label not in priors:
                # initialize to 1 for laplace smoothing in numerator
                priors[sample.label] = 1
            priors[sample.label] += 1
        total = sum(priors.values())
        for label in priors:
            # apply laplace smoothing in denominator
            priors[label] /= total
        return priors

    def learn_feature_priors(samples):
        """
        Values are add-one smoothed
        :param samples: An array of Sample objects
        :return: feature priors
        """
        # applies laplace smoothing
        sample_length = len(samples[0].data)
        features = np.array(list(map(lambda x: x.data, samples)))
        return ((sum(features) + np.ones(sample_length)) / (len(samples) + 2)).tolist()

    def learn_feature_posteriors(samples):
        """
        Values are add-one smoothed
        :param samples: An array of Sample objects
        :return: feature posteriors indexed by label
        """
        feature_posteriors = {}
        labels = set(map(lambda x: x.label, samples))
        for label in labels:
            relevant_samples = list(filter(lambda x: x.label == label, samples))
            # laplace smoothing is applied in learn_feature_priors
            feature_posteriors[label] = NaiveBayes.learn_feature_priors(relevant_samples)
        return feature_posteriors

# if __name__ == "__main__":
#     import json
#     data = learning_utils.read_samples()
#     training_params = train(data)
#     with open("learning/nb_training_params.json", "w") as f:
#         f.write(json.dumps(training_params))
