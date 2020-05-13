import sys
import collections
import copy


# A instance within the data (represents a line in the data) has a class and a set of values
class Instance:
    def __init__(self, classification, values):
        self.classification = classification
        self.values = values


# A node with children has a attribute number and a left and right node
class Node:
    def __init__(self, att_num, left, right):
        self.att_num = att_num
        self.left = left
        self.right = right

    def report(self, indent):
        print(indent, attributes_input[self.att_num], " = True:")
        self.left.report(indent+"    ")
        print(indent, attributes_input[self.att_num], " = False:")
        self.right.report(indent+"    ")


# A node with no children has a name and a probability
class LeafNode:
    def __init__(self, name, probability):
        self.name = name
        self.probability = probability

    def report(self, indent):
        print(indent, "Class =", self.name, " , Prob =", self.probability)


# Parses a file and turns it into a list of instances
def file_parser(file_num):
    instances = list()
    with open(sys.argv[file_num]) as f:
        lines = [line.rstrip() for line in f]
    for line in lines[1:]:
        instance_value_list = line.split()
        temp = Instance(instance_value_list[0], list())
        for value in instance_value_list[1:]:
            temp.values.append(value)
        instances.append(temp)
    return instances


# Gets a list of attributes
def get_attributes():
    with open(sys.argv[-2]) as f:
        line = f.readline()
    att_list = line.split()
    del att_list[0]
    return att_list


# Classifies the instance
def build_tree(instances, attributes):
    if not instances:  # if the data_set given is empty
        return LeafNode(majority_class(training_set)[0], majority_class(training_set)[1]/len(training_set))
    if purity(instances) == 0:  # checks if there is only 1 class type
        return LeafNode(instances[0].classification, 1)
    if not attributes:  # if attributes given is empty
        return LeafNode(majority_class(instances)[0], (majority_class(instances)[1] / len(instances)))

    best_true, best_false, best_attribute_index = get_best_attribute(instances, attributes)
    attributes.remove(attributes_input[best_attribute_index])
    left = build_tree(best_true, copy.copy(attributes))
    right = build_tree(best_false, copy.copy(attributes))

    return Node(best_attribute_index, left, right)


# Gets the most pure attribute from the given instances and attributes
def get_best_attribute(instances, attributes):
    best_att_purity = 1
    best_att_index = 0
    best_true = list()
    best_false = list()

    for att_index in range(len(attributes)):
        index = attributes_input.index(attributes[att_index])
        true_list = list()
        false_list = list()

        for instance in instances:
            if instance.values[index] == "true":
                true_list.append(instance)
            else:
                false_list.append(instance)

        true_weight = len(true_list) / len(instances)
        false_weight = len(false_list) / len(instances)

        true_purity = purity(true_list) * true_weight
        false_purity = purity(false_list) * false_weight

        att_purity = true_purity + false_purity

        if att_purity < best_att_purity:
            best_att_purity = att_purity
            best_att_index = index
            best_true = copy.copy(true_list)
            best_false = copy.copy(false_list)

    return best_true, best_false, best_att_index


# Checks to see if the set is pure (c for class)
def purity(instance_set):
    if not instance_set:
        return 0.0

    classes = list()
    for instance in instance_set:
        classes.append(instance.classification)
    counter = collections.Counter(classes)

    if len(counter) == 1:
        return 0.0

    a = counter.most_common()[0][1]
    b = counter.most_common()[1][1]

    return (float(a)*float(b)) / ((len(instance_set))**2)


# Finds the class that appears the most in training set (returns a tuple of (name, frequency))
def majority_class(train_set):
    classes = list()
    for instance in train_set:
        classes.append(instance.classification)
    counter = collections.Counter(classes)
    return counter.most_common()[0]


# Determine the accuracy of
def get_algorithm_accuracy(test_data_set):
    correct_count = 0
    for instance in test_data_set:
        if instance_class(instance, tree) == instance.classification:
            correct_count += 1
    print("\n\nAlgorithm Accuracy = ", correct_count/len(test_data_set))


# Gets the predicted class of the instance from the built tree
def instance_class(instance, node):
    if isinstance(node, LeafNode):
        return node.name
    if instance.values[node.att_num] == "true":
        return instance_class(instance, node.left)
    else:
        return instance_class(instance, node.right)


# Main code
if __name__ == '__main__':
    training_set = file_parser(-2)  # First file
    test_set = file_parser(-1)  # Second file
    attributes_input = get_attributes()  # Gets Attributes from first file
    tree = build_tree(training_set, copy.copy(attributes_input))  # Builds tree
    tree.report("")  # Prints tree
    get_algorithm_accuracy(test_set)  # Checks tree against a test set
    print("Baseline Accuracy = ", majority_class(training_set)[1]/len(training_set))
