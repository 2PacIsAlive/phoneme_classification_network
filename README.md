# Phoneme Classification Neural Network
#### Running the Program:
To run the program, simply type:
```
python net_six.py
```
into your terminal or command prompt. Currently, the network only supports 6 inputs. These inputs are the /a/, /chi/, and /e/ japanese phonemes, each annunciated by a male and a female voice. 

Upon startup, the program will ask you if you want to load weights.
* Loading Weights (y):
  * While the network usually converges on a solution, this process can take quite a long time. The amount of time required seems to depend entirely on the random weights generated, as the time taken to reach 0% error can take anywhere from 400 to 3000 epochs. As such, you can load (and save) pre-trained weights. Currently, the only weights file that the network structure supports is `six_phonemes.data`. Type this in when prompted to load the weights or open it in a text editor to see the values. 
* Using Random Weights (n):
  * If weights are not loaded, the network will initialize random weights for all connections, and will attempt to train itself.
  * Choosing this option will activate a pre-test, in which the program will attempt to classify the input phonemes using the random weights. 

##### Training
* Minus Phase
  * During each epoch of training, each input is presented once to the network. 
  * After computing the activations of the hidden and output units, the network takes the maximally activated output unit as a "guess" about which phoneme was presented. 
  * Training stops when the network correctly identifies all phonemes in a 100 epoch cycle, or when the recursion depth is exceeded. 
  * After each 100 epoch cycle, the network will print the number of incorrect trials. If this number (the error) is greater than 0, the network will continue training. If the error is 0, the network will proceed to the testing phase.
* Plus Phase
  * During the plus phase, the network computes an error value by subtracting the activation of the chosen unit from the expected value. 
  * For each unit in the layer below, the unit's activation is multiplied by this error and the learning rate (currently 0.05), and this value is added to the previous weight value for the connection to compute the new weight. As such, correct associations are always enforced and incorrect associations are always punished. 

##### Testing
* Testing occurs after the network finishes training, or directly following the loading of pre-trained weights. The program will print out the expected output and network output for each trial, and the phonemes themselves will be voiced through the speakers. 

#### Network Structure:
The network consists of three layers:

* Input
  * The input layer represents the phonemes that the network attempts to classify. 
  * The phonemes, accessible in the japanese_mp3s folder, are converted into visual input using a tool developed by Christoph Lauer called [Sonogram](http://www.christoph-lauer.de/sonogram), an audio spectrum analyzer which displays the frequency domain of the phonemes across time. 
  * The images generated for each phoneme are scaled down to 100x100 pixels. At the beginning of each minus phase (the part of training in which activation flows up the network), the network receives a matrix containing the color values of each pixel, which are then converted to activations. 
* Hidden
  * During the minus phase, each neuron in the hidden layer is activated via a sigmoid function, which takes as input the sum of the hidden unit's weights for each input unit multiplied by the activation of that input unit. 
  * The size of the hidden layer can be changed in the NeuralNetwork.makeNetwork() function.
* Output
  * The output units are activated in the same fashion as the hidden units. 
  * Each output unit corresponds to one phoneme.
