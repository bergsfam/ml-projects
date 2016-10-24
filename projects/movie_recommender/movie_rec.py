### Stuff to do ###
### Can I get different data?
### how can I display a score with the movie?
### how can I investigate the data?
### how can I investigate the model, what is it doing? Can I show it graphically?
### how does LightFM work? - See https://arxiv.org/pdf/1507.08439v1.pdf

import numpy as np
from lightfm.datasets import fetch_movielens
from lightfm.evaluation import precision_at_k
from lightfm.evaluation import auc_score
from lightfm import LightFM
# LightFM is a library that helps to create a hybrid fetch_movielens system
# Hybrid fetch_movielens system = collaborative and content recommender

# fetch data from movie lens
data = fetch_movielens(min_rating=4.0)

# print training and test data
## let's look at these sets a little more closely
print "*" * 30
print "****** Look at the data ******"
print "*" * 30

for key, value in data.items():
    print(key, value)

print "Training data shape: ", data['train'].shape
print "Testing data shape: ", data['test'].shape

print "*" * 30
print "*" * 30
print "*" * 30

# create model
# WARP = Weighted Approximate-Rank Pairwise
# One of Four loss functions offered by LightFM
model = LightFM(loss = 'warp')

# train model
model.fit(data['train'], epochs=30, num_threads=2)

print "\n\n\n"

train_precision = precision_at_k(model, data['train'], k=10).mean()
test_precision = precision_at_k(model, data['test'], k=10).mean()

train_auc = auc_score(model, data['train']).mean()
test_auc = auc_score(model, data['test']).mean()

print('Precision: train %.2f, test %.2f.' % (train_precision, test_precision))
print('AUC: train %.2f, test %.2f.' % (train_auc, test_auc))

print "*" * 30
print "*" * 30
print "*" * 30

print "\n\n\n"

# function to take in model(above), the data (also above), and a list of users
def sample_recommendation(model, data, user_ids):

    # number of users and movies in training data
    n_users, n_items = data['train'].shape

    # for each user generate a recommendation
    for user_id in user_ids:

        # movies liked by the user
        # tocsr method -> gets into Compressed Sparse Row format
        # that's good for this sort of data with lots of movies and relatively few ratings
        known_positives = data['item_labels'][data['train'].tocsr()[user_id].indices]

        # movies predicted the user will like
        scores = model.predict(user_id, np.arange(n_items))

        # rank the scores from most liked to least liked
        # how to also display scores?
        top_items = data['item_labels'][np.argsort(-scores)]
        bottom_items = data['item_labels'][np.argsort(scores)]

        # Results
        print "User: %s" % user_id

        print "\tKnown positives:"

        for x in known_positives[:3]:
            print "\t\t%s" % x

        print "\tRecommended:"

        for x in top_items[:3]:
            print "\t\t%s" % x

        print "\tNot recommended:"

        for x in bottom_items[:3]:
            print "\t\t%s" % x


sample_recommendation(model, data, [3, 25, 450])
