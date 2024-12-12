.. _conv2D:

Convolutional example
=====================

**8. A convolutional example**

If your dataset consists of a number of variables (e.g. temperature and pressure, so 2 variables) over a 2 dimensional grid, 
convolutional layers can be used in the encoder/decoder. Here is an example for a grid (y, x) = (32, 64). 
The dataset would then have a size of (nbr_of_samples, 32, 64, 2). We will use a stack of 4 convolutional/maxpooling blocks 
in the encoder (the decoder mirrors the encoder). The first block uses 3 Conv2D layers, the second bock 2 and the third block 1, 
followed by a MaxPooling2D layer (*stack=(3, 2, 1)*). The number of filters in the first block is 32, in the second 16 and 
in the third 8 (*stack_filters=(32, 16, 8)*). The number of filters in Latent space, before flattening, is 1 (*latent_filters=1*). 
This will result in a latent size (before flattening) of (8, 16, 1).

.. code-block:: ipython
  
  diresa = build_diresa(input_shape=(32, 64, 2), stack=(3, 2, 1), stack_filters=(32, 16, 8), latent_filters=1)
  diresa.summary(expand_nested=True)


	
	