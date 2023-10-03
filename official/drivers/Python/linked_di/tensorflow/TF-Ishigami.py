import dakota.interfacing as di
#import tensorflow as tf
from math import sin


#Ishigami function for global sensitivity analysis
def Ishigami(tf_params):
    #3 parameters are always expected for the Ishigami function
    x, y, z = tf_params[0], tf_params[1], tf_params[2]
    a=7.0
    b=0.1
    return sin(x) + a*sin(y)**2 + b*z**4*sin(x)


@di.python_interface
def prediction_driver(params, results):
    params_list = []
    #add current iteration dakota parameters with sample values into python list
    for i, label in enumerate(params):
        params_list.append(params[label])

    '''
    FOR TENSORFLOW (load an exported model)
    tfk_model = tf.keras.models.load_model("./exported_tfk_model.keras")
    '''

    #add function output to dakota response object 
    for i, label in enumerate(results):
        results[label].function = Ishigami(params_list)

        '''
        FOR TENSORFLOW (send parameter values to model and get a prediction)
        results[label].function = tfk_model.predict([params_list])[0][0]
        '''


    #return function output as dakota response object
    return results
