from sklearn.tree import DecisionTreeClassifier
import pandas as pd

def tree_to_code(tree, feature_names):
    from sklearn.tree import _tree
    tree_ = tree.tree_
    feature_name = [
    feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    # print ("def tree({}):".format(", ".join(feature_names)))

    def recurse(node, depth):
        indent = "    " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print ("{}if [{}] <= {}:".format(indent, name, threshold))
            recurse(tree_.children_left[node], depth + 1)
            print ("{}else:  # if [{}] > {}".format(indent, name, threshold))
            recurse(tree_.children_right[node], depth + 1)
        else:
            try:
                print ("{}return {}".format(indent, tree_.value[node][0][0] < tree_.value[node][0][1]))
                # print ("{}return {}".format(indent, tree_.value[node]))
            except:
                print("{}???".format(indent))

    recurse(0, 1)

with open('run/out.txt', 'r') as f:
    featureNames = f.readline()[:-1].split(',')
    flagNames = f.readline()[:-1].split(',')
    features = []
    flags = []

    while True:
        featureStr = f.readline()
        if featureStr == '':
            break
        flagStr = f.readline()

        features.append([int(n) for n in featureStr.split(',')])
        flags.append([int(n) for n in flagStr.split(',')])

    # print(features)
    # print(flags)

    # make a dictionary to map from column names to data
    d = {}
    for i in range(len(featureNames)):
        d[featureNames[i]] = [l[i] for l in features]
    for i in range(len(flagNames)):
        d[flagNames[i]] = [l[i] for l in flags]

    trainingData = pd.DataFrame(data=d)

featureMatrix = trainingData[featureNames].values
for flag in flagNames:
    labels = trainingData[flag].values

    print("\nLearning for flag "+flag)
    # print("Feature Matrix:")
    # print(featureMatrix)
    # print("Labels:")
    # print(labels)
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(featureMatrix,labels)

    tree_to_code(clf,featureNames)

def main():
    features = ['V1==0','V1-ve' ,'V2==0','V2-ve','I3==ADD','I3==MUL','I3==XOR','I3==SUB']
    training_data = pd.read_csv('learn/example_training_data.csv')
    feature_matrix = training_data[features].values
    labels = training_data['cp_covered'].values
    print("Feature Matrix:")
    print(feature_matrix)
    print("\nCover Points:")
    print(labels)

    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(feature_matrix,labels)

    print("\nTree:")
    tree_to_code(clf,features)