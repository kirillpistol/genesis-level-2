import unittest
from level2_algorithms.numeric import Numeric,Evaluator

class NumericTests(unittest.TestCase):
    def test_stats_restore(self):
        algorithm=Numeric()
        for x in (10,20,30):result=algorithm.process(x)
        self.assertEqual(result['mean'],20)
        self.assertEqual(result['sample_variance'],100)
        restored=Numeric(algorithm.state())
        self.assertEqual(restored.process(40)['mean'],25)
    def test_evaluation(self):
        evaluator=Evaluator()
        evaluator.process(dict(prediction=2,target=1))
        result=evaluator.process(dict(prediction=2,target=3))
        self.assertEqual(result['mae'],1)
        self.assertEqual(result['rmse'],1)
    def test_reject_data_and_invalid_state(self):
        for value in (True,'secret',float('nan'),1e200):
            with self.assertRaises(ValueError):Numeric().process(value)
        with self.assertRaises(ValueError):Numeric(dict(n=True,mean=0,m2=0))
    def test_no_training_exchange(self):
        self.assertFalse(hasattr(Numeric(),'train'))
        self.assertFalse(hasattr(Numeric(),'merge'))
