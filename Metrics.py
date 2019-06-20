import pandas as pd

DNNOutput = pd.read_csv("outputs/OptimumDNNOutput.csv")
forestOutput = pd.read_csv("outputs/UseCase19ForestOutput.csv")
testingData = pd.read_csv("inputs/UseCase1TestShuffled.csv", keep_default_na=False, header=0, delimiter='\t', quoting=3)

# result 1 means fake news and 0 means real news
f = open("outputs/OptimumMetrics.txt",'w')

def forestMetrics():
    truePositives = 0
    trueNegatives = 0
    falsePositives = 0
    falseNegatives = 0
    numArticles = testingData["text"].size

    for i in range(0, numArticles):
        forestResult = forestOutput["label"][i]
        testLabel = testingData["label"][i]
        if forestResult == 1 and forestResult == testLabel:
            truePositives = truePositives + 1
        if forestResult == 0 and forestResult == testLabel:
            trueNegatives =trueNegatives + 1
        if forestResult == 1 and forestResult != testLabel:
            falsePositives = falsePositives + 1
        if forestResult == 0 and forestResult != testLabel:
            falseNegatives = falseNegatives + 1

    accuracy = (truePositives + trueNegatives)/numArticles
    # How many correct
    if truePositives + falsePositives != 0:
        precision = truePositives/(truePositives + falsePositives)
    else:
        precision = truePositives/1
    # Percentage of predicted fake articles that are actually fake
    recall = truePositives/(truePositives + falseNegatives)
    # Probability of a fake article being labelled as fake
    if (falsePositives + trueNegatives == 0):
        FPR = 0
    else:
        FPR = falsePositives/(falsePositives + trueNegatives)
    # Probability of a real article being labelled as fake
    prevalence = (truePositives + falseNegatives)/numArticles
    # How many of the set are fake
    if truePositives + falsePositives !=0:
        FDR = falsePositives/(truePositives + falsePositives)
    else:
        FDR = 0
    # How many of the articles predicted as fake are actually real
    FOR = falseNegatives/(falseNegatives + trueNegatives)
    # How many of the articles predicted as real are actually fake
    NPV = trueNegatives/(falseNegatives + trueNegatives)
    # How many of the articles predicted as real are actually real
    FNR = falseNegatives/(truePositives + falseNegatives)
    # How many of the fake articles are predicted as real
    if (falsePositives + trueNegatives == 0):
        TNR = 0
    else:
        TNR = trueNegatives/(falsePositives + trueNegatives)
    # How many of the predicted real articles are actually real
    if recall == 0 and precision == 0:
        F1Score = 0
    if recall == 0 and precision != 0:
        F1Score = (1 / (((0)+(1/precision))/2))
    if precision == 0 and recall != 0:
        F1Score = (1 / (((1 / recall) + (0)) / 2))
    if recall != 0 and precision != 0:
        F1Score = (1 / (((1 / recall) + (1 / precision)) / 2))
    # Measure's accuracy considering precision and recall
    youdenJ = (recall + TNR) - 1
    # Probability of an informed decision

    print("Random Forest Metrics:", file = f)
    print("\t Number of true positives = ", truePositives, file = f)
    print("\t Number of true negatives = ", trueNegatives, file = f)
    print("\t Number of false positives = ", falsePositives, file = f)
    print("\t Number of false negatives = ", falseNegatives, file = f)
    print("\t Accuracy = ", round(accuracy*100, 2), "%", file = f)
    print("\t Prevalence = ", round(prevalence*100, 2), "%", file = f)
    print("\t Positive Predictive Value/Precision = ", round(precision*100, 2), "%", file = f)
    print("\t True Positive Rate/Recall = ", round(recall*100, 2), "%", file = f)
    print("\t Negative Predictive Value = ", round(NPV*100, 2), "%", file = f)
    print("\t False Positive Rate/Fall-Out = ", round(FPR*100, 2), "%", file = f)
    print("\t False Discovery Rate = ", round(FDR*100, 2), "%", file = f)
    print("\t False Omission Rate = ", round(FOR*100, 2), "%", file = f)
    print("\t False Negative Rate = ", round(FNR*100, 2), "%", file = f)
    print("\t True Negative Rate = ", round(TNR*100, 2), "%", file = f)
    print("\t F1 Score = ", round(F1Score, 2), file = f)
    print("\t Youden's J score = ", round(youdenJ, 2), file = f)


def DNNMetrics():
    truePositives = 0
    trueNegatives = 0
    falsePositives = 0
    falseNegatives = 0
    numArticles = testingData["text"].size

    for i in range(0, numArticles):
        DNNResult = DNNOutput["label"][i]
        testLabel = testingData["label"][i]
        if DNNResult == 1 and DNNResult == testLabel:
            truePositives = truePositives + 1
        if DNNResult == 0 and DNNResult == testLabel:
            trueNegatives = trueNegatives + 1
        if DNNResult == 1 and DNNResult != testLabel:
            falsePositives = falsePositives + 1
        if DNNResult == 0 and DNNResult != testLabel:
            falseNegatives = falseNegatives + 1

    accuracy = (truePositives + trueNegatives) / numArticles
    # How many correct
    precision = truePositives / (truePositives + falsePositives)
    # Percentage of predicted fake articles that are actually fake
    recall = truePositives / (truePositives + falseNegatives)
    # Probability of a fake article being labelled as fake
    if (falsePositives + trueNegatives == 0):
        FPR = 0
    else:
        FPR = falsePositives/(falsePositives + trueNegatives)
        # Probability of a real article being labelled as fake
    prevalence = (truePositives + falseNegatives) / numArticles
    # How many of the set are fake
    FDR = falsePositives / (truePositives + falsePositives)
    # How many of the articles predicted as fake are actually real
    FOR = falseNegatives / (falseNegatives + trueNegatives)
    # How many of the articles predicted as real are actually fake
    NPV = trueNegatives / (falseNegatives + trueNegatives)
    # How many of the articles predicted as real are actually real
    FNR = falseNegatives / (truePositives + falseNegatives)
    # How many of the fake articles are predicted as real
    if (falsePositives + trueNegatives == 0):
        TNR = 0
    else:
        TNR = trueNegatives/(falsePositives + trueNegatives)
        # How many of the predicted real articles are actually real
    F1Score = (1 / (((1 / recall) + (1 / precision)) / 2))
    # Measure's accuracy considering precision and recall
    if (falsePositives + trueNegatives == 0):
        youdenJ = 0
    else:
        youdenJ = (recall + TNR) - 1
    # Probability of an informed decision
    #((truePositives / (truePositives + falseNegatives)) +
                   #(trueNegatives / (trueNegatives + falsePositives))) - 1


    print("DNN Metrics:", file = f)
    print("\t Number of true positives = ", truePositives, file = f)
    print("\t Number of true negatives = ", trueNegatives, file = f)
    print("\t Number of false positives = ", falsePositives, file = f)
    print("\t Number of false negatives = ", falseNegatives, file = f)
    print("\t Accuracy = ", round(accuracy * 100, 2), "%", file = f)
    print("\t Prevalence = ", round(prevalence * 100, 2), "%", file = f)
    print("\t Positive Predictive Value/Precision = ", round(precision * 100, 2), "%", file = f)
    print("\t True Positive Rate/Recall = ", round(recall * 100, 2), "%", file = f)
    print("\t Negative Predictive Value = ", round(NPV * 100, 2), "%", file = f)
    print("\t False Positive Rate/Fall-Out = ", round(FPR * 100, 2), "%", file = f)
    print("\t False Discovery Rate = ", round(FDR * 100, 2), "%", file = f)
    print("\t False Omission Rate = ", round(FOR * 100, 2), "%", file = f)
    print("\t False Negative Rate = ", round(FNR * 100, 2), "%", file = f)
    print("\t True Negative Rate = ", round(TNR * 100, 2), "%", file = f)
    print("\t F1 Score = ", round(F1Score, 2), file = f)
    print("\t Youden's J score = ", round(youdenJ, 2), file = f)


#forestMetrics()
DNNMetrics()

