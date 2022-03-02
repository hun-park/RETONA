import tensorflow as tf
from tensorflow.keras.layers import Input, MaxPooling2D, Conv2D, Flatten, Dropout, Dense, Softmax

def cnn(input_shape=(35,35,1),classes=10,kernel_size=4,pool_size=2,filters=64,dropout=0.2):
    
    input_layer = Input(shape=input_shape)
    net = Conv2D(filters=filters,kernel_size=kernel_size, activation='relu')(input_layer)
    net = MaxPooling2D(pool_size)(net)
    net = Conv2D(filters=filters,kernel_size=kernel_size, activation='relu')(net)
    net = MaxPooling2D(pool_size)(net)
    net = Conv2D(filters=filters,kernel_size=kernel_size, activation='relu')(net)
    net = Flatten()(net)
    net = Dropout(dropout)(net)
    net = Dense(classes)(net)   
    output_layer = Softmax()(net)
    print(output_layer.name)

    return tf.keras.models.Model(inputs=input_layer, outputs=output_layer)

if __name__ == '__main__':
    cnn()
