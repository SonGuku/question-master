from random import shuffle

from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import User, Category, Question, Answer, Score
from django.http.response import HttpResponseNotFound

# Create your views here.

max = 5


def admin(request):
    scores =Score.objects.all().order_by("-score")##按照分数从高到低排序
    return render(request, 'question/admin.html',
                  {
                      'scores':scores
                  })

def start2(request):
    return render(request, 'question/start.html')

def reg(request):
    return render(request, 'question/reg.html')

def regCommit(request):
    account = request.POST.get("account")
    password = request.POST.get("password")

    msg =""
    if account is None or account.strip()=="":
        return render(request, 'question/reg.html',
                      {
                          'msg': '账号不能为空',
                      })

    if password is None or password.strip()=="":
        return render(request, 'question/reg.html',
                      {
                          'msg': '密码不能为空',
                      })
    result = User.objects.filter(name=account)

    print(result)

    if result.exists():
        return render(request, 'question/reg.html',
                      {
                          'msg': '账号已被使用',
                      })

    user = User()
    user.name = account
    user.password = password
    user.save()

    return render(request, 'question/login.html')


def login(request):
    return render(request, 'question/login.html')


def start_answer(request):
    a = request.session.get("answerList", default=None)
    b = request.session.get("idList", default=None)
    c = request.session.get("account", default=None)
    #print(a)
    #print(b)
    #print(c)
    if a is not None:
        del request.session['answerList']  ##删除就会话
    if b is not None:
        del request.session['idList']
    if c is not None:
        del request.session['account']

    account = request.POST.get("account")
    password  = request.POST.get("password")
    print(account)
    print(password)
    if account is None or account.strip()=="":
        return render(request, 'question/login.html',
                      {
                          'msg': '账号不能为空',
                      })

    if password is None or password.strip()=="":
        return render(request, 'question/login.html',
                      {
                          'msg': '密码不能为空',
                      })

    result = User.objects.filter(name=account)

    if result.count()==0:
        return render(request, 'question/login.html',
                      {
                          'msg': '此账号不存在',
                      })

    user =result[0]
    if user.password != password:
        return render(request, 'question/login.html',
                      {
                          'msg': '密码输入错误',
                      })


    request.session["account"] = account  ##保存到会话中


    questions = Question.objects.all()
    idList = []
    for question in questions:
        idList.append(question.id)
    shuffle(idList)##打乱顺序 随机抽取10个
    id = idList[0] ##获取第一个
    request.session["idList"] = idList ##保存到会话中
    sortnum = 0 ##获取第一个

    question = get_object_or_404(Question, id=id)
    category = get_object_or_404(Category, id=question.category_id)
    print(question)
    answers = Answer.objects.filter(question=question)

    return render(request, 'question/index.html',
                  {
                      'answers': answers,
                      'question': question,
                      'category': category,
                      'id': id,
                      'sortnum':sortnum,
                      'max' :max
                  })



def show_answer(request, id):
    ##print(id)


    answer =  request.POST.get("answer")
    sortnum = request.POST.get("sortnum")
    print(sortnum)
    print(answer)

    idList = request.session.get("idList")

    answerList  = request.session.get("answerList",default=None) ##答案也存储在缓存中
    if answerList is None:
        answerList=[]

    answerList.append(answer)##保存答案到会话中

    a = request.session.get("answerList", default=None)

    if a is not None:
        del request.session['answerList'] ##删除就会话
    request.session['answerList'] = answerList ##把答案保存会话中

    id = idList[int(sortnum)+1]

    sortnum  = int(sortnum)+1


    question = get_object_or_404(Question,id=id)
    category = get_object_or_404(Category, id=question.category_id)
    print(question)
    answers = Answer.objects.filter(question=question)

    ##if not answers:
    ##    return HttpResponseNotFound()
    return  render(request, 'question/question.html',
                   {
                       'answers' : answers,
                       'question': question,
                       'category':category,
                       'id':id,
                       'sortnum': sortnum,
                       'max': max
                   })

def commit_answer(request):
    answerList = request.session.get("answerList", default=None)  ##答案也存储在缓存中
    answer = request.POST.get("answer")
    answerList.append(answer)  ##保存答案到会话中

    a = request.session.get("answerList", default=None)
    b = request.session.get("idList", default=None)
    if a is not None:
        del request.session['answerList']  ##删除就会话
    if b is not None:
        del request.session['idList']


    correct = 0
    print(answerList)
    for i in answerList:
        answer =  get_object_or_404(Answer, id=int(i))
        if answer.correct == 1:
            correct = correct + 1

    #user = User()
    #user.name = str(request.session.get("account", default=None))

    #user.score =float(correct)
    #user.save()

    account = request.session.get("account", default=None)
    user = User.objects.get(name=account)
    score1 = float(correct)
    score = Score()
    score.user = user
    score.score =  score1
    score.save()




    return render(request, 'question/result.html',
                  {

                      'correct': correct
                  })