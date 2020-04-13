import sys
import collections


# a instance within the data (represents a line in the data)
class Instance:
    def __init__(self, values):
        self.values = values


# A node with children
class Node:
    def __init__(self, att, att_num, left, right):
        self.att = att
        self.att_num = att_num
        self.left = left
        self.right = right

    def report(self, indent):
        print(indent, self.att, " = True:")
        self.left.report(indent+"    ")

        print(indent, self.att, " = False:")
        self.right.report(indent+"    ")


# A node with no children
class LeafNode:
    def __init__(self, name, probability):
        self.name = name
        self.probability = probability

    def report(self, indent):
        print(indent, "Class = ", self.name, " , Prob = ", self.probability)


# Classifies the instance
def build_tree(data_set, attributes):
    if not data_set:  # if the data_set given is empty
        return LeafNode(majority_class(training_set)[0], majority_class(training_set)[1]/len(training_set))  # fix
    if purity(data_set) == 1:  # checks if there is only 1 class type
        return LeafNode(data_set[0].values[0], 1)
    if not attributes:  # if attributes given is empty
        return LeafNode(majority_class(data_set)[0], (majority_class(data_set)[1] / len(data_set)))

    best_att_purity = 0
    best_att = 0
    best_true = list()
    best_false = list()
    removed_attributes = list()
    for att_index in range(1, len(attributes)):
        if removed_attributes.__contains__(att_index):
            continue
        true_list = list()
        false_list = list()
        for instance in data_set:
            if instance.values[att_index] == "true":
                true_list.append(instance)
            else:
                false_list.append(instance)
        att_purity = (purity(true_list)+purity(false_list))/2
        if att_purity > best_att_purity:
            best_att_purity = att_purity
            best_att = att_index
            best_true = true_list
            best_false = false_list
    removed_attributes.append(best_att)
    left = build_tree(best_true, attributes)
    right = build_tree(best_false, attributes)
    return Node(get_attributes()[best_att], best_att, left, right)


# determine the accuracy of
def get_algorithm_accuracy(test_data_set):
    correct_count = 0
    for instance in test_data_set:
        if instance_class(instance, tree) == instance.values[0]:
            correct_count += 1
    print("\n\nAlgorithm Accuracy = ", correct_count/len(test_data_set))


# gets the predicted class of the instance from the built tree
def instance_class(instance, node):
    if isinstance(node, LeafNode):
        return node.name
    if instance.values[node.att_num] == "true":
        return instance_class(instance, node.left)
    else:
        return instance_class(instance, node.right)


# Parses a file and turns it into a list of instances
def file_parser(file_num):
    instances = list()
    with open(sys.argv[file_num]) as f:
        lines = [line.rstrip() for line in f]
    for line in lines[1:]:
        instance_value_list = line.split()
        temp = Instance(list())
        for value in instance_value_list:
            temp.values.append(value)
        instances.append(temp)
    return instances


# Gets a list of attribute labels
def get_attributes():
    with open(sys.argv[-2]) as f:
        line = f.readline()
    att_list = line.split()
    return att_list


# Checks to see if the set is pure (c for class)
def purity(train_set):
    if not train_set:
        return 0
    classes = list()
    for instance in train_set:
        classes.append(instance.values[0])
    counter = collections.Counter(classes)
    if len(counter) == 1:
        return 1
    a = counter.most_common()[0][1]
    b = counter.most_common()[1][1]
    return (a*b)/((a+b)**2)


# Finds the class that appears the most in training set
def majority_class(train_set):
    classes = list()
    for instance in train_set:
        classes.append(instance.values[0])
    counter = collections.Counter(classes)
    return counter.most_common()[0]


# Main code
if __name__ == '__main__':
    training_set = file_parser(-2)  # First file
    test_set = file_parser(-1)  # Second file
    attributes_input = get_attributes()  # Gets Attributes from first file
    tree = build_tree(training_set, attributes_input)  # Builds tree
    tree.report("")  # Prints tree
    get_algorithm_accuracy(test_set)  # Checks tree against a test set
    print("Baseline Accuracy = ", majority_class(training_set)[1]/len(training_set))
