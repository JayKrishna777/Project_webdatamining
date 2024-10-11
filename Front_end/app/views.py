from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Register
from urllib.parse import urlparse
import pandas as  pd
import numpy as np
import pickle
import re
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE

from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier
from sklearn.svm import SVC


#importing the required libraries


Home = 'index.html'
About = 'about.html'
Login = 'login.html'
Registration = 'registration.html'
Userhome = 'userhome.html'
Load = 'load.html'
View = 'view.html'
visualization = 'preprocessing.html'
Model = 'model.html'
Prediction = 'prediction.html'



# # Home page
def index(request):

    return render(request, Home)

# # About page


def about(request):
    return render(request, About)

# # Login Page


def login(request):
    if request.method == 'POST':
        lemail = request.POST['email']
        lpassword = request.POST['password']

        d = Register.objects.filter(email=lemail, password=lpassword).exists()
        print(d)
        if d:
            return redirect(userhome)
        else:
            msg = 'Login failed'
            return render(request, Login, {'msg': msg})
    return render(request, Login)

# # registration page user can registration here


def registration(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        email = request.POST['email']
        password = request.POST['password']
        conpassword = request.POST['conpassword']
        age = request.POST['Age']
        contact = request.POST['contact']

        if password == conpassword:
            userdata = Register.objects.filter(email=email).exists()
            if userdata:
                msg = 'Account already exists'
                return render(request, Registration, {'msg': msg})
            else:
                userdata = Register(name=Name, email=email,
                                    password=password, age=age, contact=contact)
                userdata.save()
                return render(request, Login)
        else:
            msg = 'Register failed!!'
            return render(request, Registration, {'msg': msg})

    return render(request, Registration)

# # user interface


def userhome(request):

    return render(request, Userhome)

# # Load Data


def load(request):
    if request.method == "POST":
        global df
        file = request.FILES['file']
        df = pd.read_csv(r"globalterrorismdb_0718dist.csv", encoding='latin-1',low_memory=False)
        messages.info(request, "Data Uploaded Successfully")

    return render(request, Load)

# # View Data


def view(request):
    col = df.to_html
    dummy = df.head(100)

    col = dummy.columns
    rows = dummy.values.tolist()
    # return render(request, 'view.html',{'col':col,'rows':rows})
    return render(request, View, {'columns': dummy.columns.values, 'rows': dummy.values.tolist()})


# preprocessing data
def preprocessing(request):
    global x_train, x_test, y_train, y_test, xsm, ysm ,df
    
    if request.method == "POST":

        size = int(request.POST['split'])
        size = size / 100

        # Data Splitting
        x = df.drop("fraud_reported",axis=1)
        y = df["fraud_reported"]
        smote = SMOTE(random_state=2)
        xsm, ysm = smote.fit_resample(x,y)

        x_train,x_test,y_train,y_test = train_test_split(xsm, ysm, test_size=0.30, stratify=ysm, random_state=11)
       
        messages.info(request, "Data Preprocessed and It Splits Succesfully")
    return render(request, 'code1 copy.html')


def model(request):
    global x_train, x_test, y_train, y_test
    df = pd.read_csv('url_data_modified.csv')
    print(df.columns)
    print('#######################################################')
    X = df.drop(['Label','Domain','Web_Traffic'], axis =1)
    y = df.Label
    x_train,x_test,y_train,y_test =train_test_split(X,y,test_size=0.3,random_state  =20)
    print(df)

    if request.method == "POST":
        model = request.POST['algo']
        if model == "0":
            adb = AdaBoostClassifier()
            adb.fit(x_train, y_train)
            y_pred = adb.predict(x_test)
            acc_adb=accuracy_score(y_test, y_pred)
            acc_adb=acc_adb*100
            msg = 'Accuracy of Adaboost Tree : ' + str(acc_adb)
            return render(request, Model, {'msg': msg})

        elif model == "1":
            rf = RandomForestClassifier()
            rf.fit(x_train, y_train)
            y_pred = rf.predict(x_test)
            acc_rf=accuracy_score(y_test, y_pred)
            acc_rf=acc_rf*100
            msg = 'Accuracy of Random Forest Classifier : ' + str(acc_rf)
            return render(request, Model, {'msg': msg})

        elif model == "2":
            gr = GradientBoostingClassifier()
            gr.fit(x_train,y_train)
            y_pred = gr.predict(x_test)
            acc_gr=accuracy_score(y_test,y_pred)
            acc_gr=acc_gr*100
            msg = 'Accuracy of Logistic Regression : ' + str(acc_gr)
            return render(request, Model, {'msg': msg})
        
        elif model == "3":
            svm = SVC()
            svm.fit(x_train, y_train)
            y_pred = svm.predict(x_test)
            acc_svm=accuracy_score(y_test,y_pred)
            acc_svm=acc_svm*100
            msg = 'Accuracy of Support Vector Machine : ' + str(acc_svm)
            return render(request, Model, {'msg': msg})
        

    return render(request, Model)

def prediction(request):

    global x_train,x_test,y_train,y_test,x,y
    

    if request.method == 'POST':
        
        url1=(request.POST['url'])
        

        def getDomain(url):
            domain = urlparse(url).netloc
            if re.match(r"^www.", domain):
                domain = domain.replace("www.", "")
            return domain

        def havingIP(url):
            try:
                ipaddress.ip_address(url)
                ip = 1
            except:
                ip = 0
            return ip

        def haveAtSign(url):
            if "@" in url:
                at = 1
            else:
                at = 0
            return at

        def getLength(url):
            if len(url) < 54:
                length = 0
            else:
                length = 1
            return length

        def getDepth(url):
            s = urlparse(url).path.split('/')
            depth = 0
            for j in range(len(s)):
                if len(s[j]) != 0:
                    depth = depth + 1
            return depth

        def redirection(url):
            pos = url.rfind('//')
            if pos > 6:
                if pos > 7:
                    return 1
                else:
                    return 0
            else:
                return 0

        def httpDomain(url):
            domain = urlparse(url).netloc
            if 'https' in domain:
                return 1
            else:
                return 0

        shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                              r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                              r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                              r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                              r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                              r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                              r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                              r"tr\.im|link\.zip\.net"

        def tinyURL(url):
            match = re.search(shortening_services, url)
            if match:
                return 1
            else:
                return 0

        def prefixSuffix(url):
            if '-' in urlparse(url).netloc:
                return 1  # phishing
            else:
                return 0  # legitimate

        # def web_traffic(url):
        #     try:
        #         # Filling the whitespaces in the URL if any
        #         url = urllib.parse.quote(url)
        #         rank = \
        #         BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(),
        #                       "xml").find(
        #             "REACH")['RANK']
        #         rank = int(rank)
        #     except TypeError:
        #         return 1
        #     if rank < 100000:
        #         return 1
        #     else:
        #         return 0

        def domainAge(domain_name):
            creation_date = domain_name.creation_date
            expiration_date = domain_name.expiration_date
            if (isinstance(creation_date, str) or isinstance(expiration_date, str)):
                try:
                    creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
                    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
                except:
                    return 1
            if ((expiration_date is None) or (creation_date is None)):
                return 1
            elif ((type(expiration_date) is list) or (type(creation_date) is list)):
                return 1
            else:
                ageofdomain = abs((expiration_date - creation_date).days)
                if ((ageofdomain / 30) < 6):
                    age = 1
                else:
                    age = 0
            return age

        def domainEnd(domain_name):
            expiration_date = domain_name.expiration_date
            if isinstance(expiration_date, str):
                try:
                    expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
                except:
                    return 1
            if (expiration_date is None):
                return 1
            elif (type(expiration_date) is list):
                return 1
            else:
                today = datetime.now()
                end = abs((expiration_date - today).days)
                if ((end / 30) < 6):
                    end = 0
                else:
                    end = 1
            return end

        def iframe(response):
            if response == "":
                return 1
            else:
                if re.findall(r"[<iframe>|<frameBorder>]", response.text):
                    return 0
                else:
                    return 1

        def mouseOver(response):
            if response == "":
                return 1
            else:
                if re.findall("<script>.+onmouseover.+</script>", response.text):
                    return 1
                else:
                    return 0

        def rightClick(response):
            if response == "":
                return 1
            else:
                if re.findall(r"event.button ?== ?2", response.text):
                    return 0
                else:
                    return 1

        def forwarding(response):
            if response == "":
                return 1
            else:
                if len(response.history) <= 2:
                    return 0
                else:
                    return 1

        def featureExtraction(url):
            features = []
            # Address bar based features (10)
            features.append(getDomain(url))
            features.append(havingIP(url))
            features.append(haveAtSign(url))
            features.append(getLength(url))
            features.append(getDepth(url))
            features.append(redirection(url))
            features.append(httpDomain(url))
            features.append(tinyURL(url))
            features.append(prefixSuffix(url))

            # Domain based features (4)
            dns = 0
            try:
                domain_name = whois.whois(urlparse(url).netloc)
            except:
                dns = 1

            features.append(dns)
            # features.append(web_traffic(url))
            features.append(1 if dns == 1 else domainAge(domain_name))
            features.append(1 if dns == 1 else domainEnd(domain_name))

            # HTML & Javascript based features (4)
            try:
                response = requests.get(url)
            except:
                response = ""
            features.append(iframe(response))
            features.append(mouseOver(response))
            features.append(rightClick(response))
            features.append(forwarding(response))
            # features.append(label)

            return features

        data0 = pd.read_csv(r'url_data_modified.csv')
        data = data0.drop(['Domain','Web_Traffic'], axis=1).copy()
        data = data.sample(frac=1).reset_index(drop=True)
        y = data['Label']
        X = data.drop('Label', axis=1)
        from sklearn.model_selection import train_test_split

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)
        from sklearn.ensemble import RandomForestClassifier

        # instantiate the model
        forest = RandomForestClassifier(max_depth=5)
        top_doms = pd.read_csv('top-1m.csv', header=None)
        # fit the model
        forest.fit(X_train, y_train)
        print('aa')
        print(url1)
        print(type(url1))
        my_features = featureExtraction(url1)
        prob_of_doms = top_doms[1].values
        if my_features[0] in prob_of_doms:
            msg = 'Website is Safe its not Phishing website'
            return render(request,Prediction,{'msg':msg})
            # return render_template('prediction.html',msg = 'success',url=url1)
        else:
            pred1 = forest.predict([my_features[1:]])
            print(pred1)
            if pred1==0:
                msg="Website is Safe its not Phishing website"
            else:
                # email=session.get('email')
                # name=session.get('pno')
                # pno=session.get('pno')
                # ts = time.time()
                # date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                # timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                # msg = 'The website you are trying to visit not legitimate'
                # t = 'Regards,'
                # t1 = 'Phishing Website.'
                # mail_content = 'Dear ' + name +','+'\n'+msg +'\n' + '\n' + t + '\n' + t1
                # sender_address = ''
                # sender_pass = ''
                # receiver_address = email
                # message = MIMEMultipart()
                # message['From'] = sender_address
                # message['To'] = receiver_address
                # message['Subject'] = 'Phishing Website'
                # message.attach(MIMEText(mail_content, 'plain'))
                # ses = smtplib.SMTP('smtp.gmail.com', 587)
                # ses.starttls()
                # ses.login(sender_address, sender_pass)
                # text = message.as_string()
                # ses.sendmail(sender_address, receiver_address, text)
                # ses.quit()
                # url = "https://www.fast2sms.com/dev/bulkV2"
                
                # message = 'Dear ' + name +','+'\n'+msg
                # no = pno
                # data1 = {
                #     "route": "q",
                #     "message": message,
                #     "language": "english",
                #     "flash": 0,
                #     "numbers": no,
                # }
                
                # headers = {
                #     "authorization": "UwmaiQR5OoA6lSTz93nP0tDxsFEhI7VJrfKkvYjbM2C14Wde8g9lvA2Ghq5VNCjrZ4THWkF1KOwp3Bxd",
                #     "Content-Type": "application/json"
                # }
                
                # response = requests.post(url, headers=headers, json=data1)
                # print(response)
                msg="Website is not Safe it a Phishing"
            return render(request,Prediction,{'msg':msg,'url' : url1})

    return render(request,Prediction)

        
 

