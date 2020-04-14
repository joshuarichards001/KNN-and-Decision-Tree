import sys
import math
from statistics import mode


# A class defining a certain wine
class Wine:
    def __init__(self, classification, values):
        self.classification = int(classification)
        self.values = values


# parsers the wines from a file into a list
def parser(file_num):
    wines = list()
    with open(sys.argv[file_num]) as f:
        lines = [line.rstrip() for line in f]
    iter_lines = iter(lines)
    next(iter_lines)
    for line in iter_lines:
        wine_list = list(map(float, line.split()))
        wines.append(Wine(wine_list[13], [wine_list[0], wine_list[1], wine_list[2], wine_list[3], wine_list[4],
                                          wine_list[5], wine_list[6], wine_list[7], wine_list[8], wine_list[9],
                                          wine_list[10], wine_list[11], wine_list[12]]))
    return wines


# Gets the range of all of the features
def calculate_ranges():
    num_of_values = len(train_set[0].values)
    value_ranges = list()
    w, h = len(train_set), num_of_values
    all_values = [[0 for x in range(w)] for y in range(h)]  # Creates 2D array of size w by h

    for idx in range(num_of_values):
        for jdx in range(len(train_set)):
            all_values[idx][jdx] = train_set[jdx].values[idx]

    for idx in range(num_of_values):
        max_value = max(all_values[idx])
        min_value = min(all_values[idx])
        value_ranges.append(max_value - min_value)

    return value_ranges


# Classifies the test values
def test_classification(wine1):
    neighbours_classes = get_nearest_neighbours_classes(wine1)
    return mode(neighbours_classes)  # Gets the most common occurring class


# Gets the nearest neighbours
def get_nearest_neighbours_classes(wine1):
    e_dists = list()
    for wine2 in train_set:
        e_dists.append((wine2.classification, euclidean_distance(wine1.values, wine2.values)))
    e_dists.sort(key=lambda tup: tup[1])
    nearest_neighbours = list()
    for idx in range(k):
        nearest_neighbours.append(e_dists[idx][0])
    return nearest_neighbours


# Calculates the euclidean distance between wine1 and wine2
def euclidean_distance(item_1, item_2):
    e_dist = 0.0
    for idx in range(len(item_1)):
        e_dist += ((item_1[idx] - item_2[idx])**2) / (ranges[idx]**2)
    return math.sqrt(e_dist)


# Main code
if __name__ == '__main__':

    k = int(input("Input the K value desired: "))
    train_set = parser(-2)  # First file
    test_set = parser(-1)  # Second file
    ranges = calculate_ranges()

    print("For K=%d" % k)

    num_correct_classifications = 0
    for i, item in enumerate(test_set):
        item_predicted_class = test_classification(item)
        print('Wine: %d, Actual Class: %d, Predicted Class: %d' % (i, item.classification, item_predicted_class))
        if item.classification == item_predicted_class:  # if prediction is correct increase num_correct_classifications
            num_correct_classifications += 1

    print("Accuracy = ", (num_correct_classifications/len(test_set)))
