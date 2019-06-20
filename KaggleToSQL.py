import pandas as pd
import pymysql

train = pd.read_csv("inputs/kaggleFakeandReal.csv", keep_default_na=False)

db = pymysql.connect(host="localhost", user='ylb14192', password='201445765', database='ylb14192')
cursor = db.cursor()

db2 = pymysql.connect(host="localhost", user='ylb14192', password='201445765', database='ylb14192')
cursor2 = db2.cursor()


# 1 = fake
# 0 = real

i = 0
fakeCount = 0
realCount = 0
index = 0
limit = 250
while i < limit:
    while realCount < 125:
        if train["text"][index] != "":
            text = train["text"][index]
            if train["label"][index] == 0:
                label = float(train["label"][index])
                print("Article %d of %d" % (i + 1, limit))
                insertCommand = "INSERT INTO `kaggleTrain`(`id`, `text`, `label`) VALUES (%s, %s, %s)"
                cursor.execute(insertCommand, (None, text, label))
                db.commit()
                realCount = realCount + 1
                i = i + 1
                index = index + 1
            else:
                index = index + 1
        else:
            print("invalid")
            index = index + 1
    while fakeCount < 125:
        if train["text"][index] != "":
            text = train["text"][index]
            if train["label"][index] == 1:
                label = float(train["label"][index])
                print("Article %d of %d" % (i + 1, limit))
                insertCommand = "INSERT INTO `kaggleTrain`(`id`, `text`, `label`) VALUES (%s, %s, %s)"
                cursor.execute(insertCommand, (None, text, label))
                db.commit()
                fakeCount = fakeCount + 1
                index = index + 1
                i = i + 1
            else:
                index = index + 1
        else:
            print("invalid")
            index = index + 1
db.close()

i = 0
fakeCount = 0
realCount = 0
index = 2000
limit = 500
while i < limit:
    while realCount < 250:
        if train["text"][index] != "":
            text = train["text"][index]
            if train["label"][index] == 0:
                label = float(train["label"][index])
                print("Article %d of %d" % (i + 1, limit))
                insertCommand2 = "INSERT INTO `kaggleTest`(`id`, `text`, `label`) VALUES (%s, %s, %s)"
                cursor2.execute(insertCommand2, (None, text, label))
                db2.commit()
                realCount = realCount + 1
                i = i + 1
                index = index + 1
            else:
                index = index + 1
        else:
            index = index + 1
    while fakeCount < 250:
        if train["text"][index] != "":
            text = train["text"][index]
            if train["label"][index] == 1:
                label = float(train["label"][index])
                print("Article %d of %d" % (i + 1, limit))
                insertCommand2 = "INSERT INTO `kaggleTest`(`id`, `text`, `label`) VALUES (%s, %s, %s)"
                cursor2.execute(insertCommand2, (None, text, label))
                db2.commit()
                fakeCount = fakeCount + 1
                index = index + 1
                i = i + 1
            else:
                index = index + 1
        else:
            index = index + 1
db2.close()
