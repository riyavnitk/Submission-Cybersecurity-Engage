import random
import numpy
import pylab

class kalman_filter(object):
    '''
    This class implements a linear Kalman filter and uses the parameter names. 
    This Kalman filter implementation is adapted from code written by Greg Czerniak.

    Instances of the kalman_linear class have 7 required parameters:
    @param A : Numpy matrix representing the state transition matrix.
    @param B : Numpy matrix representing the control matrix.
    @param H : Numpy matrix representing the observation matrix.
    @param x : Numpy matrix representing the initial state estimate.
    @param P : Numpy matrix representing the initial state covariance estimate.
    @param Q : Numpy matrix representing the error in process estimate.
    @param R : Numpy matrix representing the error in measurement estimate.
    '''
    def __init__(self,A, B, H, x, P, Q, R):
        self.state_trans = A
        self.ctrl = B
        self.obs = H
        self.init_state_est = x
        self.init_cov_est = P
        self.proc_err_est = Q
        self.meas_err_est = R


    def get_state(self):
        '''
        Method to return the inital state estimate.
        @return: Returns a numpy matrix containing the initial state estimate value.'''
        return self.init_state_est


    def step(self, ctrl_vec, meas_vec):
        '''
        Method to perform the Kalman filtering prediction, observation and update steps.
        '''
        # Prediction step
        pred_state_est = (self.state_trans * self.init_state_est) + (self.ctrl * ctrl_vec)
        pred_prob_est = ((self.state_trans * self.init_cov_est) * numpy.transpose(self.state_trans)) + self.proc_err_est
        # Observation step
        # residual - the discrepancy between the predicted and actual measurement
        residual = meas_vec - (self.obs * pred_state_est)
        residual_cov = (self.obs * pred_prob_est * numpy.transpose(self.obs)) + self.meas_err_est
        # Update step
        kalman_gain = pred_prob_est * numpy.transpose(self.obs) * numpy.linalg.inv(residual_cov)
        self.init_state_est = pred_state_est + (kalman_gain * residual)
        # Determine the size of and create the identity matrix
        size = self.init_cov_est.shape[0] 
        id_matrix = numpy.eye(size)
        # Update the covariance based on the results of the previous steps
        self.init_cov_est = (id_matrix - (kalman_gain * self.obs)) * pred_prob_est





class noise_generator:
    '''
    This class implements a random noise generator for generating a noisy data series used to test a kalman_linear class instance.

    Instances of the noise_generator class require 2 parameters:
    @param mean: Float value of the mean for creating the Gaussian distribution. 
    @param std_dev: Float value of the standard deviation used to create the Gaussian distribution.
    '''
    def __init__(self, mean, std_dev): 
        self.mean = mean
        self.std_dev = std_dev
    

    def get_noise(self):
        '''
        Method to generate a random float value from a Gaussian distrubution.
        @return: Returns a random Float value from the generated Gaussian distribution.
        '''
        return random.gauss(self.mean, self.std_dev)
    

    def get_mean(self):
        '''
        Method to return the mean of the Gaussian distribution. 
        This value represents the "actual" value that is being obscured by the noisy data.
        @return: Returns the float value passed in as the Gaussian distribution mean.
        '''
        return self.mean
    

def test_kalman(A, B, H, x, P, Q, R, noise_mean, noise_std_dev, data_size): 
    '''
    Test function for testing a kalman_linear class instance on a randomly generated noisy data series.
    The function generates a plot of the noisy data series, 
    the estimated value returned by the linear Kalman filtering function and the actual value that the noisy data would be otherwise obscuring.
    The function takes 10 required parameters:
    @param A: Numpy matrix reperesenting the state transition matrix.
    @param B: Numpy matrix reperesenting the control matrix.
    @param H: Numpy matrix reperesenting the observation matrix.
    @param x: Numpy matrix representing the initial state estimate.
    @param P: Numpy matrix representing the initial covariance estimate.
    @param Q: Numpy matrix representing the error in process estimate.
    @param R: Numpy matrix representing the error in measurement estimate. 
    @param mean: Float value of the mean for creating the Gaussian distribution. 
    @param std_dev: Float value of the standard deviation used to create the Gaussian distribution.
    @param data_size: Integer value indicating the desired size of the test data series.
    '''
    # Create class instances
    filter = kalman_linear(A,B,H,xhat,P,Q,R)
    generator = noise_generator(noise_mean, noise_std_dev)
    # Create storage for generated data
    noisy_data = []
    actual_val = []
    kalman = []
    # Create the noisy and filtered linear data series
    for i in range(data_size):
        noisy_val = generator.get_noise() 
        noisy_data.append(noisy_val) 
        actual_val.append(generator.get_mean()) 
        kalman.append(filter.get_state()[0,0]) 
        filter.step(numpy.matrix([0]), numpy.matrix([noisy_val]))

    # Create plot of the noisy and filtered data
    pylab.plot(range(data_size), noisy_data, 'r', range(data_size), kalman, 'g', range(data_size), actual_val, 'b')
    pylab.xlabel('Time')
    pylab.ylabel('Noisy Data')
    pylab.title('Estimation of Noisy Data Series with Kalman Filter') 
    pylab.legend(('Noisy Values','Kalman Filtered Values', 'Actual Value')) 
    pylab.show()