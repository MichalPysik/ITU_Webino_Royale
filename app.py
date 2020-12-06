from flask import Flask, request, redirect, render_template, flash
import user
from aautomat import automat
from Automat import automat_class
from dice import dice
from ruleta import ruleta
from time import sleep

app = Flask(__name__, template_folder='templates')
app.secret_key = 'secret key'
Users = user.get_users()
us = Users[0]
bet = 1

@app.route('/', methods=['GET', 'POST'])
def login():
    global Users
    global us
    if request.method == 'POST':
        name = request.form['names']
        for u in Users:
            if u.get_name() == name:
                us = u
                return redirect("/casino")
    names = []
    for i in Users:
        names.append(i.get_name())
    return render_template('login.html', names=names)

@app.route('/create_user', methods=['GET', 'POST'])
def Create_user():
    global Users
    if request.method == 'POST' and 'login' in request.form:
        us = request.form['login']
        for i in Users:
            if i.get_name() == us:
                return redirect("/")
        Users.append(user.User(us))
        return redirect("/")

    return render_template('create.html')

@app.route('/casino', methods=["GET"])
def casino_menu():
    global us
    global bet
    global Users
    return render_template('cas.html', user=us.get_name(), balance=us.get_balance())

@app.route('/casino/Ruleta', methods=["GET", "POST"])
def Ruleta():
    global us
    global bet
    global Users
    global choice
    rul_red = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    rul_black = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
    choice = "red"
    bet = 1
    rul_result = 4
    rul_result_c = "red"
    if request.method == 'POST':
        if us.get_balance() <= 0:
            Users.remove(us)
            us.delete()
            return redirect('/casino/lose')
        win_check = us.get_balance()
        bet = int(request.form['bet'])
        choice = request.form['hidden_choice']
        if choice.isnumeric():
            choice = int(choice)
        rul_result = ruleta(us, bet, choice)

        if us.get_balance() > win_check:
            flash("YOU WON")
        if rul_result in rul_red:
            rul_result_c = "red"
        elif rul_result in rul_black:
            rul_result_c = "black"
        else:
            rul_result_c = "green"
    print(us.get_balance())
    return render_template('rul.html', choice=choice, bet=bet, user=us.get_name(), balance=us.get_balance(), result=rul_result, rul_result_c=rul_result_c)

@app.route('/casino/Dice', methods=["GET", "POST"])
def Dice():
    global us
    global bet
    global Users
    bet = 1
    gStatus = 30
    NoD = 1
    pSum = 0
    eSum = 0
    pThws = [1, 1, 1, 1, 1, 1]
    eThws = [2, 2, 2, 2, 2, 2]
    helpTMP = []
    if request.method == 'POST':
        if us.get_balance() <= 0:
            Users.remove(us)
            us.delete()
            return redirect('/casino/lose')
        bet = int(request.form['bet'])
        NoD = int(request.form['nOfDice'])
        if bet >= 1 and bet <= 100000 and us.get_balance() >= bet:
            gStatus, pSum, eSum, pThws, eThws = dice(us, bet, NoD)
        elif bet >= 1 and bet <= 100000:
            flash("You cannot bet more credits than you currently have")
        else:
            flash("You can only bet 1 up to 100 000 credits at once")
    for i in range (0, NoD):
        helpTMP.append(i)
    strP="/static/SKINS/DICE/" + str(pThws[NoD-1]) + "yellow.png"
    strE="/static/SKINS/DICE/" + str(eThws[NoD-1]) + "red.png"
    print(us.get_balance())
    return render_template('dice.html', bet=bet, user=us.get_name(), balance=us.get_balance(), helpTMP=helpTMP, imaP=strP, imaE=strE, gStatus=gStatus, pSum=pSum, eSum=eSum, pThws=pThws, eThws=eThws)

@app.route('/casino/Automat', methods=["GET", "POST"])
def Automat():
    global us
    global bet
    global Users
    signs=[[1, "20 x BET"],[2, "40 x BET"],[3, "80 x BET"],[4, "80 x BET"],[5, "80 x BET"],[6, "150 x BET"],[7, "300 x BET"],[8, "300 x BET"],[9, "800 x BET"],[0, "800 x BET"]]
    aut = automat_class()
    if request.method == 'POST':
        if us.get_balance() <= 0:
            Users.remove(us)
            us.delete()
            return redirect('/casino/lose')
        bet = int(request.form['bet'])
        aut.set_slots(automat(us, bet))
        if aut.get_status() == True:
            flash("YOU WON")
    str = aut.slots_for_HTML()
    return render_template('aut.html', Slots=str, bet=bet, signs=signs, balance=us.get_balance(), user=us.get_name())

@app.route('/casino/lose', methods=["GET"])
def lose():
    return render_template('lose.html')

if __name__ == '__main__':
    app.run(debug='True')
