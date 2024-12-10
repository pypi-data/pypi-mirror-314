# autoencoder.py

import tensorflow as tf
from tensorflow.keras import layers, models, regularizers
import json

class Autoencoder:
    def __init__(self, encoder_config, input_dim, latent_dim, activation='relu', optimizer='adam', loss='mse', metrics=None):
        """
        Initializes the Autoencoder with the given configuration.

        :param encoder_config: List of dictionaries defining each encoder layer.
                               Each dictionary should have 'units', 'activation', 'dropout_rate', and 'regularizer'.
        :param input_dim: Integer, dimensionality of the input data.
        :param latent_dim: Integer, dimensionality of the latent space.
        :param activation: String, activation function to use (default: 'relu').
        :param optimizer: String or tf.keras optimizer instance (default: 'adam').
        :param loss: String, loss function to use (default: 'mse').
        :param metrics: List of metrics to evaluate during training (default: None).
        """
        self.encoder_config = encoder_config
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.activation = activation
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics if metrics is not None else ['mse']

        self.encoder = self.build_encoder()
        self.decoder = self.build_decoder()
        self.autoencoder = self.build_autoencoder()

    def build_encoder(self):
        """
        Builds the encoder model based on the provided configuration.
        """
        if not isinstance(self.latent_dim, int) or self.latent_dim <= 0:
            raise ValueError(f"Invalid latent_dim: {self.latent_dim}. It must be a positive integer.")

        encoder_input = layers.Input(shape=(self.input_dim,), name='Encoder_Input')
        x = encoder_input

        if not isinstance(self.encoder_config, list):
            raise ValueError("encoder_config should be a list of layer configurations (dictionaries)")

        for idx, layer_conf in enumerate(self.encoder_config):
            if not isinstance(layer_conf, dict):
                raise ValueError(f"Layer configuration at index {idx} is not a dictionary: {layer_conf}")

            units = layer_conf.get('units', 64)
            activation = layer_conf.get('activation', self.activation)
            dropout_rate = layer_conf.get('dropout_rate', 0.0)
            regularizer = layer_conf.get('regularizer', None)

            x = layers.Dense(units=units, activation=activation,
                            kernel_regularizer=self.get_regularizer(regularizer),
                            name=f'Encoder_Dense_{idx+1}')(x)
            if dropout_rate > 0.0:
                x = layers.Dropout(rate=dropout_rate, name=f'Encoder_Dropout_{idx+1}')(x)

        # Latent space
        latent = layers.Dense(self.latent_dim, activation=self.activation, name='Latent_Space')(x)

        encoder_model = models.Model(inputs=encoder_input, outputs=latent, name='Encoder')
        return encoder_model



    def build_decoder(self):
        """
        Builds the decoder model by reversing the encoder configuration.
        """
        decoder_input = layers.Input(shape=(self.latent_dim,), name='Decoder_Input')
        x = decoder_input

        reversed_config = list(reversed(self.encoder_config))
        for idx, layer_conf in enumerate(reversed_config):
            units = layer_conf.get('units', 64)
            activation = layer_conf.get('activation', self.activation)
            dropout_rate = layer_conf.get('dropout_rate', 0.0)
            regularizer = layer_conf.get('regularizer', None)

            x = layers.Dense(units=units, activation=activation,
                             kernel_regularizer=self.get_regularizer(regularizer),
                             name=f'Decoder_Dense_{idx+1}')(x)
            if dropout_rate > 0.0:
                x = layers.Dropout(rate=dropout_rate, name=f'Decoder_Dropout_{idx+1}')(x)

        # Output layer
        output_layer = layers.Dense(self.input_dim, activation='sigmoid', name='Decoder_Output')(x)

        decoder_model = models.Model(inputs=decoder_input, outputs=output_layer, name='Decoder')
        return decoder_model

    def build_autoencoder(self):
        """
        Combines the encoder and decoder into a single autoencoder model.
        """
        auto_input = self.encoder.input
        auto_output = self.decoder(self.encoder(auto_input))
        autoencoder_model = models.Model(inputs=auto_input, outputs=auto_output, name='Autoencoder')
        return autoencoder_model

    def compile(self):
        """
        Compiles the autoencoder model with the specified optimizer, loss, and metrics.
        """
        self.autoencoder.compile(optimizer=self.optimizer, loss=self.loss, metrics=self.metrics)

    def train(self, x_train, x_val=None, epochs=50, batch_size=32, callbacks=None, verbose=1):
        """
        Trains the autoencoder.

        :param x_train: Numpy array or TensorFlow tensor, training data.
        :param x_val: Numpy array or TensorFlow tensor, validation data (optional).
        :param epochs: Integer, number of epochs to train.
        :param batch_size: Integer, size of the training batches.
        :param callbacks: List of tf.keras.callbacks instances (optional).
        :param verbose: Integer, verbosity mode.
        :return: History object.
        """
        history = self.autoencoder.fit(
            x_train, x_train,
            epochs=epochs,
            batch_size=batch_size,
            shuffle=True,
            validation_data=(x_val, x_val) if x_val is not None else None,
            callbacks=callbacks,
            verbose=verbose
        )
        return history

    def evaluate(self, x_test):
        """
        Evaluates the autoencoder on test data.

        :param x_test: Numpy array or TensorFlow tensor, test data.
        :return: Evaluation metrics.
        """
        evaluation = self.autoencoder.evaluate(x_test, x_test)
        return evaluation

    def get_encoder(self):
        """
        Returns the encoder model.

        :return: tf.keras.Model, encoder.
        """
        return self.encoder

    def get_decoder(self):
        """
        Returns the decoder model.

        :return: tf.keras.Model, decoder.
        """
        return self.decoder

    def get_autoencoder(self):
        """
        Returns the autoencoder model.

        :return: tf.keras.Model, autoencoder.
        """
        return self.autoencoder

    def save_models(self, save_dir):
        """
        Saves the encoder, decoder, and autoencoder models to the specified directory.

        :param save_dir: String, directory path to save the models.
        """
        self.encoder.save(f"{save_dir}/encoder.h5")
        self.decoder.save(f"{save_dir}/decoder.h5")
        self.autoencoder.save(f"{save_dir}/autoencoder.h5")
        print(f"Models saved to {save_dir}")

    def load_models(self, save_dir):
        """
        Loads the encoder, decoder, and autoencoder models from the specified directory.

        :param save_dir: String, directory path from where to load the models.
        """
        self.encoder = models.load_model(f"{save_dir}/encoder.h5")
        self.decoder = models.load_model(f"{save_dir}/decoder.h5")
        self.autoencoder = models.load_model(f"{save_dir}/autoencoder.h5")
        print(f"Models loaded from {save_dir}")

    @staticmethod
    def get_regularizer(reg_type, **kwargs):
        """
        Returns a regularizer based on the type.

        :param reg_type: String, type of regularizer ('l1', 'l2', 'l1_l2').
        :param kwargs: Additional keyword arguments for the regularizer.
        :return: Regularizer instance or None.
        """
        if reg_type is None:
            return None
        if reg_type == 'l1':
            return regularizers.l1(**kwargs)
        elif reg_type == 'l2':
            return regularizers.l2(**kwargs)
        elif reg_type == 'l1_l2':
            return regularizers.l1_l2(**kwargs)
        else:
            raise ValueError(f"Unsupported regularizer type: {reg_type}")
        
    def extract_latent_features(self, x_train, batch_size=32, callbacks=None, verbose=1):
        """
        Extracts latent features from the encoder using the provided training data.

        :param x_train: Numpy array or TensorFlow tensor, training data.
        :param batch_size: Integer, size of the batches for prediction.
        :param callbacks: List of tf.keras.callbacks instances (optional).
        :param verbose: Integer, verbosity mode.
        :return: Numpy array of latent features.
        """
        if self.encoder is None:
            raise ValueError("Encoder model is not initialized or loaded.")

        # Use the encoder to predict the latent features
        latent_features = self.encoder.predict(x_train, batch_size=batch_size, callbacks=callbacks, verbose=verbose)

        return latent_features