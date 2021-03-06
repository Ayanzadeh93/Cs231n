
# coding: utf-8

# # k-Nearest Neighbor (kNN) exercise
# 
# *Complete and hand in this completed worksheet (including its outputs and any supporting code outside of the worksheet) with your assignment submission. For more details see the [assignments page](http://vision.stanford.edu/teaching/cs231n/assignments.html) on the course website.*
# 
# The kNN classifier consists of two stages:
# 
# - During training, the classifier takes the training data and simply remembers it
# - During testing, kNN classifies every test image by comparing to all training images and transfering the labels of the k most similar training examples
# - The value of k is cross-validated
# 
# In this exercise you will implement these steps and understand the basic Image Classification pipeline, cross-validation, and gain proficiency in writing efficient, vectorized code.

# In[1]:


import past


# In[2]:


# Run some setup code for this notebook.

import random
import numpy as np
from cs231n.data_utils import load_CIFAR10
import matplotlib.pyplot as plt

from __future__ import print_function

# This is a bit of magic to make matplotlib figures appear inline in the notebook
# rather than in a new window.
get_ipython().magic(u'matplotlib inline')
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# Some more magic so that the notebook will reload external python modules;
# see http://stackoverflow.com/questions/1907993/autoreload-of-modules-in-ipython
get_ipython().magic(u'load_ext autoreload')
get_ipython().magic(u'autoreload 2')


# In[3]:


# Load the raw CIFAR-10 data.
cifar10_dir = 'cs231n/datasets/cifar-10-batches-py'
X_train, y_train, X_test, y_test = load_CIFAR10(cifar10_dir)

# As a sanity check, we print out the size of the training and test data.
print('Training data shape: ', X_train.shape)
print('Training labels shape: ', y_train.shape)
print('Test data shape: ', X_test.shape)
print('Test labels shape: ', y_test.shape)


# In[4]:


# Visualize some examples from the dataset.
# We show a few examples of training images from each class.
classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
num_classes = len(classes)
samples_per_class = 5
for y, cls in enumerate(classes):
    idxs = np.flatnonzero(y_train == y)
    idxs = np.random.choice(idxs, samples_per_class, replace=False)
    for i, idx in enumerate(idxs):
        plt_idx = i * num_classes + y + 1
        plt.subplot(samples_per_class, num_classes, plt_idx)
        plt.imshow(X_train[idx].astype('uint8'))
        plt.axis('off')
        if i == 0:
            plt.title(cls)
plt.show()


# In[5]:


import numpy as np
import matplotlib.pyplot as plt
 
    
    
# Subsample the data for more efficient code execution in this exercise
num_training = 5000
mask =range(num_training)
X_train = X_train[mask]
y_train = y_train[mask]

num_test = 500
mask = range(num_test)
X_test = X_test[mask]
y_test = y_test[mask]    
    
# data to plot


# In[6]:


#for visualization i got help from these websites.
# https://www.w3resource.com/graphics/matplotlib/barchart/matplotlib-barchart-exercise-14.php
#https://pythonspot.com/matplotlib-bar-chart/
fig, ax = plt.subplots()
fig_ticks=('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
bar_width = 0.45
opacity = 0.8
ind=np.arange(len(fig_ticks))
rects1 = plt.bar(ind,np.histogram(y_train)[0], bar_width,
                 alpha=opacity,
                 color='b',
                 label='Trainset')
 
rects2 = plt.bar(ind,np.histogram(y_test)[0], bar_width,
                 alpha=opacity,
                 color='g',
                 label='Testset')
 
plt.xlabel('Classes')
plt.ylabel('Sample Frequency')
plt.title('Frequency of trainigset')
plt.xticks(ind, (fig_ticks))
plt.legend()
 
plt.tight_layout()
plt.show()


# In[7]:


# Reshape the image data into rows
X_train = np.reshape(X_train, (X_train.shape[0], -1))
X_test = np.reshape(X_test, (X_test.shape[0], -1))
print(X_train.shape, X_test.shape)


# In[8]:


print ('Checking the shape of sampled data.')
print ('Subsample Training data shape: ', X_train.shape)
print ('Subsample Training labels shape: ', y_train.shape)
print ('Subsample Test data shape: ', X_test.shape)
print ('Subsample Test labels shape: ', y_test.shape)


# In[9]:


from cs231n.classifiers import KNearestNeighbor
# we should install follow dependencies 
#pip install pillow
#pip install future
# Create a kNN classifier instance. 
# Remember that training a kNN classifier is a noop: 
# the Classifier simply remembers the data and does no further processing 
classifier = KNearestNeighbor()
classifier.train(X_train, y_train)


# We would now like to classify the test data with the kNN classifier. Recall that we can break down this process into two steps: 
# 
# 1. First we must compute the distances between all test examples and all train examples. 
# 2. Given these distances, for each test example we find the k nearest examples and have them vote for the label
# 
# Lets begin with computing the distance matrix between all training and test examples. For example, if there are **Ntr** training examples and **Nte** test examples, this stage should result in a **Nte x Ntr** matrix where each element (i,j) is the distance between the i-th test and j-th train example.
# 
# First, open `cs231n/classifiers/k_nearest_neighbor.py` and implement the function `compute_distances_two_loops` that uses a (very inefficient) double loop over all pairs of (test, train) examples and computes the distance matrix one element at a time.

# In[10]:


# Open cs231n/classifiers/k_nearest_neighbor.py and implement
# compute_distances_two_loops.
import time
# Test your implementation:
tic1 = time.time()
dists = classifier.compute_distances_two_loops(X_test)
tic2 = time.time()
print(tic2-tic1)
print (dists.shape)


# In[11]:


# We can visualize the distance matrix: each row is a single test example and
# its distances to training examples
plt.imshow(dists, interpolation='none')
plt.xlabel('Eculidian distance of training and testset image.')
plt.ylabel('trainset image')
plt.title('testset')
plt.show()


# **Inline Question #1:** Notice the structured patterns in the distance matrix, where some rows or columns are visible brighter. (Note that with the default color scheme black indicates low distances while white indicates high distances.)
# 
# - What in the data is the cause behind the distinctly bright rows?
# - What causes the columns?

# **Your Answer**: *fill this in.*
# 
# 

# In[12]:


# Now implement the function predict_labels and run the code below:
# We use k = 1 (which is Nearest Neighbor).
y_test_pred = classifier.predict_labels(dists, k=1)

# Compute and print the fraction of correctly predicted examples
num_correct = np.sum(y_test_pred == y_test)
accuracy = float(num_correct) / num_test
print('Got %d / %d correct => accuracy: %f' % (num_correct, num_test, accuracy))


# You should expect to see approximately `27%` accuracy. Now lets try out a larger `k`, say `k = 5`:

# In[13]:


y_test_pred = classifier.predict_labels(dists, k=5)
num_correct = np.sum(y_test_pred == y_test)
accuracy = float(num_correct) / num_test
print('Got %d / %d correct => accuracy: %f' % (num_correct, num_test, accuracy))


# You should expect to see a slightly better performance than with `k = 1`.

# In[14]:


# Now lets speed up distance matrix computation by using partial vectorization
# with one loop. Implement the function compute_distances_one_loop and run the
# code below:
dists_one = classifier.compute_distances_one_loop(X_test)

# To ensure that our vectorized implementation is correct, we make sure that it
# agrees with the naive implementation. There are many ways to decide whether
# two matrices are similar; one of the simplest is the Frobenius norm. In case
# you haven't seen it before, the Frobenius norm of two matrices is the square
# root of the squared sum of differences of all elements; in other words, reshape
# the matrices into vectors and compute the Euclidean distance between them.
difference = np.linalg.norm(dists - dists_one, ord='fro')
print('Difference was: %f' % (difference, ))
if difference < 0.001:
    print('Good! The distance matrices are the same')
else:
    print('Uh-oh! The distance matrices are different')


# In[15]:


# Now implement the fully vectorized version inside compute_distances_no_loops
# and run the code
dists_two = classifier.compute_distances_no_loops(X_test)

# check that the distance matrix agrees with the one we computed before:
difference = np.linalg.norm(dists - dists_two, ord='fro')
print('Difference was: %f' % (difference, ))
if difference < 0.001:
    print('Good! The distance matrices are the same')
else:
    print('Uh-oh! The distance matrices are different')


# In[16]:


# Let's compare how fast the implementations are
def time_function(f, *args):
    """
    Call a function f with args and return the time (in seconds) that it took to execute.
    """
    import time
    tic = time.time()
    f(*args)
    toc = time.time()
    return toc - tic

two_loop_time = time_function(classifier.compute_distances_two_loops, X_test)
print('Two loop version took %f seconds' % two_loop_time)

one_loop_time = time_function(classifier.compute_distances_one_loop, X_test)
print('One loop version took %f seconds' % one_loop_time)

no_loop_time = time_function(classifier.compute_distances_no_loops, X_test)
print('No loop version took %f seconds' % no_loop_time)

# you should see significantly faster performance with the fully vectorized implementation


# ### Cross-validation
# 
# We have implemented the k-Nearest Neighbor classifier but we set the value k = 5 arbitrarily. We will now determine the best value of this hyperparameter with cross-validation.

# In[17]:


num_folds = 5
k_choices = [1, 3, 5, 8, 10, 12, 15, 20, 50, 100]

X_train_folds = []
y_train_folds = []
################################################################################
# TODO:                                                                        #
# Split up the training data into folds. After splitting, X_train_folds and    #
# y_train_folds should each be lists of length num_folds, where                #
# y_train_folds[i] is the label vector for the points in X_train_folds[i].     #
# Hint: Look up the numpy array_split function.                                #
################################################################################
# pass
#split training set and label into 5 part.
X_train_folds,y_train_folds=np.array_split(X_train, 5), np.array_split(y_train, 5)
################################################################################
#                                 END OF YOUR CODE                             #
################################################################################

# A dictionary holding the accuracies for different values of k that we find
# when running cross-validation. After running cross-validation,
# k_to_accuracies[k] should be a list of length num_folds giving the different
# accuracy values that we found when using that value of k.
k_to_accuracies = {}


################################################################################
# TODO:                                                                        #
# Perform k-fold cross validation to find the best value of k. For each        #
# possible value of k, run the k-nearest-neighbor algorithm num_folds times,   #
# where in each case you use all but one of the folds as training data and the #
# last fold as a validation set. Store the accuracies for all fold and all     #
# values of k in the k_to_accuracies dictionary.                               #
################################################################################
# pass

for k in k_choices:
     
    
    for fold in range(num_folds): 
        
        #creat validation and temp data 
        
        X_validation = X_train_folds[fold]
        Y_validation = y_train_folds[fold]
        #store the remaining folds and their label and concatinating them 
        temp_X_train = np.concatenate(X_train_folds[:fold] + X_train_folds[fold + 1:])
        temp_y_train = np.concatenate(y_train_folds[:fold] + y_train_folds[fold + 1:])

        #Initialize the classifier
        classifier = KNearestNeighbor()
        #start to train
        classifier.train( temp_X_train, temp_y_train )
        
        #Compute the dist matrix
        distance_t = classifier.compute_distances_no_loops(X_validation)
        
        distance_of_predict = classifier.predict_labels(distance_t, k=k)
        
     
        #analyze the accuracy of prediction.
        total_exp =  X_validation.shape[0]
        
        accuracy = float( np.sum(distance_of_predict == Y_validation)) / total_exp
        #append accuracy to the dictionary.
        k_to_accuracies.setdefault(k, []).append(accuracy)

    
    
################################################################################
#                                 END OF YOUR CODE                             #
################################################################################

# Print out the computed accuracies

for k in sorted(k_to_accuracies):
    for accuracy in k_to_accuracies[k]:
        
        print ('k = %d, accuracy = %f' % (k, accuracy))


# In[22]:


import operator

k_to_mean_accuracy = {}
max_K=[]
for k in k_to_accuracies:
    k_to_mean_accuracy[k] = np.mean(k_to_accuracies[k])
    #a[k]=k_to_mean_accuracy[k]
    

my_mat_k=[1,3,5,8,10,12,15,20,50,100]
#for extracting the max item from dictionary i use this website 
#https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary/23428922
best_k=int(max(k_to_mean_accuracy.iteritems(), key=operator.itemgetter(1))[0])

print (best_k)
print('best k average accuaracy:')
print(max(k_to_mean_accuracy.values()))


# In[24]:


#k_to_mean_accuracy
avg_plt_k=k_to_mean_accuracy.values()
import matplotlib.pyplot as plt
plt.plot(my_mat_k,avg_plt_k,'ro',color='g')
plt.ylabel('Accuracy')
plt.xlabel('value of K')
plt.xlim(-5,105)
plt.title('Average Accuracy of 5-fold for different k')
plt.grid()
plt.show()


# In[20]:


# plot the raw observations
for k in k_choices:
    accuracies = k_to_accuracies[k]
    plt.scatter([k] * len(accuracies), accuracies)

# plot the trend line with error bars that correspond to standard deviation
accuracies_mean = np.array([np.mean(v) for k,v in sorted(k_to_accuracies.items())])
accuracies_std = np.array([np.std(v) for k,v in sorted(k_to_accuracies.items())])
plt.errorbar(k_choices, accuracies_mean, yerr=accuracies_std)
plt.title('Cross-validation on k')
plt.xlabel('k')
plt.ylabel('Cross-validation accuracy')
plt.show()


# In[21]:


# Based on the cross-validation results above, choose the best value for k,   
# retrain the classifier using all the training data, and test it on the test
# data. You should be able to get above 28% accuracy on the test data.
best_k = k_choices[np.argmax(accuracies_mean)]
classifier = KNearestNeighbor()
classifier.train(X_train, y_train)
y_test_pred = classifier.predict(X_test, k=best_k)

# Compute and display the accuracy
num_correct = np.sum(y_test_pred == y_test)
accuracy = float(num_correct) / X_test.shape[0]
print ('Got %d / %d correct => accuracy: %f' % (num_correct, num_test, accuracy))

