from mlpack.linear_regression_train import linear_regression_train
from mlpack.linear_regression_predict import linear_regression_predict
class LinearRegression:
  def __init__(self,
               check_input_matrices = False,
               copy_all_inputs = False,
               lambda_ = None,
               verbose = False,
              ):

    # serializable attributes.
    self._LinearRegression = None

    # hyper-parameters.
    self.check_input_matrices = check_input_matrices
    self.copy_all_inputs = copy_all_inputs
    self.lambda_ = lambda_
    self.verbose = verbose

  def fit(self, 
          training = None,
          training_responses = None,
         ):

    out = linear_regression_train(training = training,
                                  check_input_matrices = self.check_input_matrices,
                                  copy_all_inputs = self.copy_all_inputs,
                                  lambda_ = self.lambda_,
                                  training_responses = training_responses,
                                  verbose = self.verbose,
                                 )

    self._LinearRegression = out["output_model"]

    return self

  def predict(self, 
              test = None,
             ):

    out = linear_regression_predict(input_model = self._LinearRegression,
                                    test = test,
                                    check_input_matrices = self.check_input_matrices,
                                    copy_all_inputs = self.copy_all_inputs,
                                    verbose = self.verbose,
                                   )


    return out["output_predictions"]

