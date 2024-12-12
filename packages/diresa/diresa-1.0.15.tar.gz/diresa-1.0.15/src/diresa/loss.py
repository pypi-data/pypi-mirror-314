#!/usr/bin/env python3
"""
DIRESA loss classes/functions

:Author:  Geert De Paepe
:Email:   geert.de.paepe@vub.be
:License: MIT License
"""

import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.losses import Loss
from diresa.toolbox import covariance


@tf.keras.utils.register_keras_serializable()
class LatentCovLoss(Loss):
    """
    Latent covariance loss class
    Latent covariance weight is annealed by AnnealingCallback
    """
    def __init__(self, cov_weight=K.variable(1.), **kwargs):
        """
        :param cov_weight: tensorflow variable with initial covariance loss weight
        """
        super().__init__(**kwargs)
        self.cov_weight = cov_weight

    def call(self, _, latent):
        """
        :param _: not used (loss functions need 2 params: the true and predicted values)
        :param latent: batch of latent vectors
        :return: weighted covariance loss
        """
        cov = tf.math.abs(covariance(latent))
        cov_square = tf.math.multiply(cov, cov)
        nbr_of_cov = tf.shape(latent)[-1] * (tf.shape(latent)[-1] - 1)
        cov_loss = (tf.math.reduce_sum(cov_square) - tf.linalg.trace(cov_square)) / tf.cast(nbr_of_cov, "float32")
        return self.cov_weight * cov_loss

    def get_config(self):
        config = super().get_config()
        config.update({'cov_weight': self.cov_weight.numpy()})
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)


@tf.keras.utils.register_keras_serializable()
def mae_dist_loss(_, distances):
    """
    Absolute Error between original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of absolute errors
    """
    ae = tf.math.abs(distances[:, 0] - distances[:, 1])
    return ae


@tf.keras.utils.register_keras_serializable()
def male_dist_loss(_, distances):
    """
    Absolute Error between logarithm of original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of absolute logarithmic errors
    """
    ale = tf.math.abs(tf.math.log1p(distances[:, 0]) - tf.math.log1p(distances[:, 1]))
    return ale


@tf.keras.utils.register_keras_serializable()
def mape_dist_loss(_, distances):
    """
    Absolute Percentage Error between original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of absolute percentage errors
    """
    epsilon = 1e-8
    ape = tf.math.abs((distances[:, 0] - distances[:, 1]) / (distances[:, 0] + epsilon))
    return ape


@tf.keras.utils.register_keras_serializable()
def mse_dist_loss(_, distances):
    """
    Squared Error between original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of squared errors
    """
    se = tf.math.square(distances[:, 0] - distances[:, 1])
    return se


@tf.keras.utils.register_keras_serializable()
def msle_dist_loss(_, distances):
    """
    Squared Error between logarithm of original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of squared logarithmic errors
    """
    sle = tf.math.square(tf.math.log1p(distances[:, 0]) - tf.math.log1p(distances[:, 1]))
    return sle


@tf.keras.utils.register_keras_serializable()
def corr_dist_loss(_, distances):
    """
    Correlation loss between original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: 1 - correlation coefficient
    """
    cov = covariance(distances)
    cov_sqrt = tf.math.sqrt(tf.math.abs(cov))
    return 1 - cov[0, 1] / (cov_sqrt[0, 0] * cov_sqrt[1, 1])


@tf.keras.utils.register_keras_serializable()
def corr_log_dist_loss(_, distances):
    """
    Correlation loss between logarithm of original and latent distances
    
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: 1 - correlation coefficient (of logarithmic distances)
    """
    cov = covariance(tf.math.log1p(distances))
    cov_sqrt = tf.math.sqrt(tf.math.abs(cov))
    return 1 - cov[0, 1] / (cov_sqrt[0, 0] * cov_sqrt[1, 1])
