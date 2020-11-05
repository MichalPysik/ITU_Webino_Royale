from flask import Flask, request, redirect, render_template
import user
from automat import automat
from Automat import automat_class
from time import sleep

app = Flask(__name__, template_folder='templates')
Users = user.get_users()
us = Users[0]
bet = 1

@app.route('/', methods=['GET', 'POST'])
def login():
    global Users
    global us
    if request.method == 'POST':
        name = request.form['names']
        print(name)
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
    if request.method == 'POST':
        us = request.form['login']
        for i in Users:
            if i.get_name() == us:
                return "User already added"
        Users.append(user.User(us))
        return redirect("/")

    return '''<form method="POST">
                    New Name: <input type="text" name="login"><br>
                    <input type="submit" value="Done"><br>
              </form>'''

@app.route('/casino', methods=["GET"])
def casino_menu():
    return render_template('cas.html')

@app.route('/casino/Ruleta')
def Ruleta():
    return "<h1>Ruleta</h1>"

@app.route('/casino/Kostky')
def Kostky():
    return "<h1>Kostky</h1>"

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
    print(us.get_balance())
    str = aut.slots_for_HTML()
    return render_template('aut.html', Slots=str, bet=bet, signs=signs, balance=us.get_balance(), user=us.get_name())

@app.route('/casino/lose', methods=["GET"])
def lose():
    sleep(1)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug='True')