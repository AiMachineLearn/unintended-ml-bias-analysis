from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
import tensorflow as tf
import model_bias_analysis as mba

class ModelBiasAnalysisTest(tf.test.TestCase):
    def add_examples(self, data, model_scores, label, subgroup):
        num_comments_added = len(model_scores)
        data['model_score'].extend(model_scores)
        data['label'].extend([label for a in range(num_comments_added)])
        data['subgroup'].extend([subgroup for a in range(num_comments_added)])

    def test_squared_diff_integral(self):
        x = np.linspace(0.0, 1.0, num = 100)
        y = [1]*len(x)
        result = mba.squared_diff_integral(y, x)
        self.assertAlmostEquals(result, 0.333, places = 2)    

    def test_average_squared_equality_gap_no_bias(self):
        no_bias_data = {'model_score': [], 'label': [], 
                        'subgroup': []}
        low_model_scores = [0.1, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.4]
        high_model_scores = [0.7, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 1.0]
        self.add_examples(no_bias_data, low_model_scores, 0, False)
        self.add_examples(no_bias_data, low_model_scores, 0, True)
        self.add_examples(no_bias_data, high_model_scores, 1, False)
        self.add_examples(no_bias_data, high_model_scores, 1, True)
        no_bias_df = pd.DataFrame(no_bias_data)
        
        pos_aseg, neg_aseg = mba.average_squared_equality_gap(no_bias_df,
                                                              'subgroup',
                                                              'label',
                                                              'model_score')
        self.assertAlmostEquals(pos_aseg, 0.0, places = 1)
        self.assertAlmostEquals(neg_aseg, 0.0, places = 1)

    def test_average_squared_equality_gap_small_bias(self):
        no_bias_data = {'model_score': [], 'label': [], 
                        'subgroup': []}
        low_model_scores_1 = [0.1, 0.12, 0.14, 0.15, 0.16, 0.18, 0.2]
        low_model_scores_2 = [x + 0.11 for x in low_model_scores_1]
        high_model_scores_1 = [0.7, 0.72, 0.74, 0.75, 0.76, 0.78, 0.8]
        high_model_scores_2 = [x + 0.11 for x in high_model_scores_1]
        self.add_examples(no_bias_data, low_model_scores_1, 0, False)
        self.add_examples(no_bias_data, low_model_scores_2, 0, True)
        self.add_examples(no_bias_data, high_model_scores_1, 1, False)
        self.add_examples(no_bias_data, high_model_scores_2, 1, True)
        no_bias_df = pd.DataFrame(no_bias_data)
        
        pos_aseg, neg_aseg = mba.average_squared_equality_gap(no_bias_df,
                                                              'subgroup',
                                                              'label',
                                                              'model_score')
        self.assertAlmostEquals(pos_aseg, 0.33, places = 1)
        self.assertAlmostEquals(neg_aseg, 0.33, places = 1)
        


if __name__ == "__main__":
  tf.test.main()