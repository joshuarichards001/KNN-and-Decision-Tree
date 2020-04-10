import sys
import math


def training_parser():
    wines = []
    with open(sys.argv[-2]) as f:
        lines = [line.rstrip() for line in f]
    iter_lines = iter(lines)
    next(iter_lines)
    for line in iter_lines:
        wine_list = list(map(float, line.split()))
        wines.append([wine_list[0], wine_list[1], wine_list[2], wine_list[3], wine_list[4], wine_list[5],
                      wine_list[6], wine_list[7], wine_list[8], wine_list[9], wine_list[10], wine_list[11],
                      wine_list[12], wine_list[13]])
    return wines


def test_parser():
    wines = list()
    with open(sys.argv[-1]) as f:
        lines = [line.rstrip() for line in f]
    iter_lines = iter(lines)
    next(iter_lines)
    for line in iter_lines:
        wine_list = list(map(float, line.split()))
        wines.append([wine_list[0], wine_list[1], wine_list[2], wine_list[3], wine_list[4], wine_list[5],
                     wine_list[6], wine_list[7], wine_list[8], wine_list[9], wine_list[10], wine_list[11],
                     wine_list[12], wine_list[13]])
    return wines


def euclidean_distance(wine1, wine2):
    e_dist = 0.0
    for i in range(len(wine1) - 1):
        e_dist += (wine1[i] - wine2[i]) ** 2
    return math.sqrt(e_dist)


def get_nearest_neighbours(wine_test, train_set, k):
    e_dists = list()
    for row in train_set:
        e_dists.append((row, euclidean_distance(wine_test, row)))
    e_dists.sort(key=lambda tup: tup[1])
    nearest_neighbours = list()
    for i in range(k):
        nearest_neighbours.append(e_dists[i][0])
    return nearest_neighbours


def test_classification(wine_test, train_set, k):
    neighbours = get_nearest_neighbours(wine_test, train_set, k)
    classes = [row[-1] for row in neighbours]
    classification = max(set(classes), key=classes.count)
    return classification


# Main code
if __name__ == '__main__':
    k = int(input("Input the K value desired: "))

    training_set = training_parser()  # First file
    test_set = test_parser()  # Second file

    num_of_correct_classifications = 0
    print("For K=%d" % k)

    for item in test_set:
        predicted_class = test_classification(item, training_set, k)
        print('Actual Class: %d, Predicted Class: %d' % (item[len(item)-1], predicted_class))
        if item[len(item)-1] == predicted_class:
            num_of_correct_classifications += 1
    print("Percentage Correct = %d" % ((num_of_correct_classifications/len(test_set))*100))

