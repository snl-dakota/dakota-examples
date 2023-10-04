import dakota.interfacing as di
import tensorflow as tf

tfk_model = tf.keras.models.load_model("./exported_tfk_model.keras")

@di.python_interface
def prediction_driver(params, results):
    params_list = []
    #add current iteration dakota parameters with sample values into python list
    for i, label in enumerate(params):
        params_list.append(params[label])
   
    #add function output to dakota response object 
    for i, label in enumerate(results):
        results[label].function = tfk_model.predict([params_list])[0][0]
        
    #return function output as dakota response object
    return results
