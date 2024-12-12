#!/usr/bin/env python3
"""
DIRESA helper functions

:Author:  Geert De Paepe
:Email:   geert.de.paepe@vub.be
:License: MIT License
"""

from sys import exit
from math import prod
import tensorflow as tf
from tensorflow.keras.models import Model
from diresa.layers import OrderLayer


def covariance(x):
    """
    Computes the covariance matrix of x (normalisation is divided by N)
    :param x: 2-D array, row are variables, columns are samples
    :return: covariance matrix
    """
    mean_x = tf.expand_dims(tf.reduce_mean(x, axis=0), 0)
    mx = tf.matmul(tf.transpose(mean_x), mean_x)
    vx = tf.matmul(tf.transpose(x), x)/tf.cast(tf.shape(x)[0], tf.float32)
    cov_xx = vx - mx
    return cov_xx


def r2_score(y, y_pred):
    """
    :param y: original dataset
    :param y_pred: predicted dataset
    :return: R2 score between y and y_pred
    """
    error = tf.math.reduce_sum(tf.math.square(y - y_pred))
    var = tf.math.reduce_sum(tf.math.square(y - tf.math.reduce_mean(y, axis=0)))
    r2 = 1.0 - error / var
    return r2


def set_components_to_mean(latent, untouched=(0,)):
    """
    Sets all latent components to mean except the ones in the list (which are kept untouched)
    Limitations: assumes a flat latent space
    :param latent: latent dataset
    :param untouched: components not in this list are set to mean
    :return: latent dataset with all components set to mean except the ones in the list
    """
    for i in range(0, latent.shape[1]):
        if i not in untouched:
            latent[:, i] = tf.math.reduce_mean(latent[:, i])
    return latent


def cut_sub_model(model, sub_model_name):
    """
    Cuts a sub-model out of a keras model 
    Limitations: does not work for a sub-model of a sub-model
    :param model: keras model
    :param sub_model_name: name of the sub-model
    :return: submodel
    """
    sub_model_nbr = None
    sub_model_config = None

    for nbr, layer in enumerate(model.get_config()['layers']):
        if layer['name'] == sub_model_name:
            sub_model_config = layer['config']
            sub_model_nbr = nbr

    if sub_model_config is None:
        print(sub_model_name, " not found in model")
        exit(1)

    sub_model = Model.from_config(sub_model_config)
    weights = [layer.get_weights() for layer in model.layers[sub_model_nbr].layers[1:]]

    for layer, weight in zip(sub_model.layers[1:], weights):
        layer.set_weights(weight)

    return sub_model


def order_latent(encoder, decoder, dataset):
    latent = encoder.predict(dataset, verbose=0)
    latent_dim = latent.shape[1]

    score = []
    for component in range(latent_dim):
        latent_component = set_components_to_mean(latent, untouched=(component,))
        decoded_component = decoder.predict(latent_component, verbose=0)
        score.append(r2_score(dataset, decoded_component))

    ranking = sorted(range(len(score)), key=score.__getitem__)
    reverse_ranking = sorted(range(len(ranking)), key=ranking.__getitem__)
    ordered_score = [score[i] for i in ranking]
    return ranking, reverse_ranking, ordered_score


def encoder_decoder(model, dataset=None, encoder_name="Encoder", decoder_name="Decoder"):
    """
    Returns encoder and decoder out of DIRESA model
    If dataset is not None: adds ordering layers after encoder and before decoder
    :param model: keras model
    :param dataset: dataset
    :param encoder_name: name of the encoder
    :param decoder_name: name of the decoder
    :return: encoder and decoder model
    """
    encoder = cut_sub_model(model, encoder_name)
    decoder = cut_sub_model(model, decoder_name)

    if dataset is not None:
        order, reverse_order, _ = order_latent(encoder, decoder, dataset)
        order_layer = OrderLayer(order)
        reverse_order_layer = OrderLayer(reverse_order)
        encoder = Model(inputs=encoder.inputs, outputs=order_layer(encoder.outputs))
        decoder = Model(inputs=reverse_order_layer.inputs, outputs=decoder(reverse_order_layer.outputs))

    return encoder, decoder
