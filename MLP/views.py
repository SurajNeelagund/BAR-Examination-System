from django.shortcuts import render

def Exam(request):
    if (request.method=="POST"):
        data=request.POST
        decile1 = data.get('textdecile1')
        decile1b = data.get('textdecile1b')
        decile3 = data.get('textdecile3')
        gender = data.get('textgender')
        lsat = data.get('textlsat')
        ugpa = data.get('textugpa')
        fulltime = data.get('textfulltime')
        tier = data.get('texttier')
        fincome = data.get('textfincome')

        if('buttonsubmit' in request.POST):
            import pandas as pd
            path = "C:\\Users\\DELL\\OneDrive\\Desktop\\Internship\\Data\\train_dataset.csv"
            data = pd.read_csv(path)
            inputs = data.drop(['parttime','male','pass_bar','grad','race1'],'columns')
            output = data.drop(['parttime','male','decile3','decile1','sex','lsat','ugpa','grad','fulltime','fam_inc','race1','tier','decile1b'],'columns')
            import sklearn
            import numpy as np
            from sklearn.model_selection import train_test_split
            x_train,x_test,y_train,y_test=train_test_split(inputs,output,train_size=0.8)
            from sklearn.preprocessing import StandardScaler
            sc=StandardScaler()
            x_train=sc.fit_transform(x_train)
            x_test=sc.fit_transform(x_test)
            from sklearn.svm import SVC
            model = SVC()
            model.fit(x_train,y_train)
            y_pred=model.predict(x_test)
            from sklearn.metrics import accuracy_score
            acc=accuracy_score(y_test,y_pred)*100
            accc='The accuracy is '+str(acc)
            new_data = np.array([[float(decile3),float(decile1),float(gender),float(lsat),float(ugpa),float(fulltime),float(fincome),float(tier),float(decile1b)]])
            newdata = sc.transform(new_data)
            pred = model.predict(newdata)
            if pred == 1:
                result = "Student will Pass"
            if float(decile1) == 1:
                result = "Student will Fail"
            else:
                result = "Student will Pass"
            return render(request,'Exam.html',context={'result':result,'accuracy':accc})
    return render(request,'Exam.html')
