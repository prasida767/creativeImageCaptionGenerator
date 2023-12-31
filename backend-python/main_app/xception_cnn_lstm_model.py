from keras.src.layers import concatenate, Attention
from keras.models import Model
from keras.layers import Input, Dense, LSTM, Embedding, Dropout, Bidirectional
from keras.regularizers import l2

from tensorflow.python.keras.layers import add


def define_model(vocab_size, max_length, cnn_units=100, lstm_units=100, dropout_rate=0.5, lstm_type='Single',
                 num_layers=1, optimizer_name="adam", learning_rate=0.1, l2_reg=0.1):
    # Features from the CNN model squeezed to cnn_units nodes
    inputs1 = Input(shape=(2048,))
    fe1 = Dropout(dropout_rate)(inputs1)
    fe2 = Dense(cnn_units, activation='relu', kernel_regularizer=l2(l2_reg))(fe1)

    # LSTM sequence model
    inputs2 = Input(shape=(max_length,))
    se1 = Embedding(vocab_size, lstm_units, mask_zero=True)(inputs2)
    se2 = Dropout(dropout_rate)(se1)

    # se3 = LSTM(lstm_units)(se2)

    # Stacked LSTM layers
    lstm_layers = []
    if num_layers > 1:
        if lstm_type == "Stacked":
            for _ in range(num_layers):
                se3 = LSTM(lstm_units, return_sequences=True, dropout=dropout_rate)(se2)
            lstm_layers.append(se3)
            # Concatenate the outputs of the Stacked LSTM layers along the last axis (time steps)
            se3 = concatenate(lstm_layers, axis=-1)
        else:
            for _ in range(num_layers):
                se3 = Bidirectional(LSTM(lstm_units, return_sequences=True, dropout=dropout_rate))(se2)
    else:
        se3 = se2

    # Use only the output of the last LSTM layer for merging
    se3 = LSTM(lstm_units)(se3)

    # Attention layer to calculate attention weights
    attention = Attention()([fe2, se3])

    # Add a Dense layer to map attention output to the same dimension as LSTM output
    attention = Dense(lstm_units, activation='relu')(attention)
    # Merging both models
    decoder1 = add([fe2, se3])

    decoder2 = Dense(cnn_units, activation='relu')(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)

    # Tie it together [image, seq] [word]
    model = Model(inputs=[inputs1, inputs2], outputs=outputs)

    # Create the optimizer based on the given optimizer_name parameter
    if optimizer_name == 'SGD':
        model.compile(loss='categorical_crossentropy', optimizer='sgd')
    elif optimizer_name == 'RMSProp':
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    elif optimizer_name == 'ADAGrad':
        model.compile(loss='categorical_crossentropy', optimizer='adagrad')
    else:
        model.compile(loss='categorical_crossentropy', optimizer='adam')

    print(model.summary())

    return model
