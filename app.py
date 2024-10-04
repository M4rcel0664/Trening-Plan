from flask import Flask, request, render_template
#from models import db, User
from extensions import db
from models import User



#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # Miejsce Twojej bazy danych
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

#from models import User
#@app.before_first_request
#def create_tables():
    #db.create_all()

#db = SQLAlchemy()

exercises = {
    'home': [
        {'name': 'Przysiady', 'reps': '8-10'},
        {'name': 'Pompki', 'reps': '10-12'},
        {'name': 'Wykroki', 'reps': '10-15'},  # Nowe ćwiczenie
        {'name': 'Plank', 'reps': '1 minuta'}  # Nowe ćwiczenie
    ],
    'gym': [
        {'name': 'Wyciskanie sztangi', 'reps': '8-10'},
        {'name': 'Biceps', 'reps': '10-12'},
        {'name': 'Wznosy w bok', 'reps': '10-15'},
        {'name': 'Martwy ciąg', 'reps': '6-8'},  # Nowe ćwiczenie
        {'name': 'Przysiad ze sztangą', 'reps': '8-10'}  # Nowe ćwiczenie
    ]
}


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Tworzy tabele w bazie danych

    return app

app = create_app()

from models import User

@app.route('/', methods=['GET', 'POST'])
@app.route('/training', methods=['GET'])
def index():
    if request.method == 'POST':
        # Tu zbierasz dane z formularza i tworzysz plan
        user = User(
            age=request.form['age'],
            gender=request.form['gender'],
            fitness_level=request.form['fitness_level'],
            goals=request.form['goals'],
            equipment=request.form['equipment'],
            availability=request.form['availability'],
            health_limitations=request.form['health_limitations']
        )
        db.session.add(user)
        # Na podstawie zebranych danych wygeneruj plan
        training_plan = generate_training_plan(user)
        return render_template('plan.html', plan=training_plan)
    return render_template('index.html')
def home_or_training():
    if request.path == '/training':
        training_type = request.args.get('type', 'home')  # domyślnie 'home'
        selected_exercises = exercises.get(training_type, [])
        return render_template('training.html', exercises=selected_exercises, training_type=training_type)

    # Dla strony głównej
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        # Tutaj można dodać logikę przetwarzania danych z formularza
        return 'Formularz został wysłany'
def generate_training_plan(user):
    # Bazowy plan, który będzie modyfikowany zależnie od danych użytkownika
    plan = {
        'Trening A': [],
        #'Wtorek': [],
        'Trening B': [],
        #'Czwartek': [],
        'Trening C': [],
       # 'Sobota': [],
        #'Niedziela': []
    }

    # Logika dla płci
    if user.gender == 'female':
        # Dla przykładu, dla kobiet możemy zaplanować mniej intensywne treningi siłowe
        strength_training = 'Trening siłowy: cięższe ciężary, mniej powtórzeń'
    else:
        # Dla mężczyzn domyślnie zakładamy trening siłowy z większymi ciężarami
        strength_training = 'Trening siłowy: cięższe ciężary, mniej powtórzeń'
        plan['Trening A'].append('Przysiad ze sztanga 3x12 powtorzen')
        plan['Trening A'].append('Wiosłowanie sztangą w opadzie tułowia podchwytem - 3x12 powtorzen')
        plan['Trening A'].append('Wyciskanie hantlami leżąc na ławce skośnej - 3x12 powtorzen '   )
        plan['Trening A'].append('Wyciskanie sztangielek siedząc nad głowę - 3x10 powtorzen')
        plan['Trening A'].append('Uginanie ramion stojąc ze sztangą łamaną- 3x12 Powtorzen')
        plan['Trening A'].append('Wyprosty ramion z linką wyciągu górnego- 3x15 powtorzen')
        plan['Trening A'].append('Spięcia brzucha leżąc na macie - Spięcia brzucha leżąc na macie 3x15 powtorzen')

    # Logika dla poziomu sprawności DO EDYCJI LUB USUNIECIA
    #Rocziaganie
    if user.fitness_level == 'beginner':
        if user.gender == 'female':
            # Plan dla kobiet
            plan['Trening A'].append('5 minut rozciągania')
            plan['Trening B'].append('5 minut rozciągania')
            plan['Trening C'].append('5 minut rozciągania')

        else:
            # Plan dla mężczyzn
            plan['Trening A'].append('5 minut rozciągania')
            plan['Trening B'].append('5 minut rozciągania')
            plan['Trening C'].append('5 minut rozciągania')

    elif user.fitness_level == 'intermediate':
        plan['Trening A'].append('5 minut rozciągania')
        plan['Trening A'].append('3 serie pompek po 10 powtorzen')
        plan['Trening B'].append('5 minut rozciągania')
        plan['Trening B'].append('3 serie pompek po 10 powtorzen')
        plan['Trening C'].append('5 minut rozciągania')
        plan['Trening C'].append('3 serie pompek po 10 powtorzen')
    elif user.fitness_level == 'advanced':
        plan['Trening A'].append('5 minut rozciągania')
        plan['Trening A'].append('3 serie pompek po 10 powtorzen')
        plan['Trening A'].append('3 serie podciaganie po 6 powtorzen')
        plan['Trening B'].append('5 minut rozciągania')
        plan['Trening B'].append('3 serie pompek po 10 powtorzen')
        plan['Trening B'].append('3 serie podciaganie po 6 powtorzen')
        plan['Trening C'].append('5 minut rozciągania')
        plan['Trening C'].append('3 serie pompek po 10 powtorzen')
        plan['Trening C'].append('3 serie podciaganie po 6 powtorzen')


    # Logika dla dostępności sprzętu

    if user.equipment == 'none':
        # Jeśli nie ma sprzętu, skupiamy się na ćwiczeniach z ciężarem własnego ciała
        for day in plan:
            #plan[day].append('Ćwiczenia z ciężarem własnego ciała')
            plan['Trening A'].append('Próby stania na rękach – 8x max hold (maksymalny możliwy czas)')
            plan['Trening A'].append('Podciągnięcia – 4x 5 powtorzen.')
            plan['Trening A'].append('Pompki pike z nogami na podwyższeniu – 4x 10 powtorzen .')
            plan['Trening A'].append('Podciąganie podchwytem – 3x 7/8 powtorzen.')
            plan['Trening A'].append('Dipy – 2x 12/13 powt.')
            plan['Trening A'].append('Plank – 3x max hold')

            plan['Trening B'].append('Próby stania na rękach – 8x max hold (maksymalny możliwy czas)')
            plan['Trening B'].append('Podciągnięcia – 4x 5 powtorzen.')
            plan['Trening B'].append('Pompki pike z nogami na podwyższeniu – 4x 10 powtorzen .')
            plan['Trening B'].append('Podciąganie podchwytem – 3x 7/8 powtorzen.')
            plan['Trening B'].append('Dipy – 2x 12/13 powt.')
            plan['Trening B'].append('Plank – 3x max hold')

            plan['Trening C'].append('Próby stania na rękach – 8x max hold (maksymalny możliwy czas)')
            plan['Trening C'].append('Podciągnięcia – 4x 5 powtorzen.')
            plan['Trening C'].append('Pompki pike z nogami na podwyższeniu – 4x 10 powtorzen .')
            plan['Trening C'].append('Podciąganie podchwytem – 3x 7/8 powtorzen.')
            plan['Trening C'].append('Dipy – 2x 12/13 powt.')
            plan['Trening C'].append('Plank – 3x max hold')


    #elif user.equipment == 'limited':
        # Dla ograniczonego sprzętu dodajemy trening z użyciem dostępnych narzędzi

        for day in plan:
            plan[day].append('Trening z użyciem dostępnego sprzętu')
    elif user.equipment == 'full':
        # Dla pełnego wyposażenia możemy zaplanować bardziej zaawansowane treningi
        plan['Trening A'].append('Wyprosty kolan na maszynie siedzac: 4x10 powtorzen')
        plan['Trening A'].append('Wyciskanie sztangi: 5x5 powtórzen')
        plan['Trening A'].append('Przyciaganie linki wyciagu dolnego: 4x12 powtorzen')
        plan['Trening A'].append('Wyciskanie hatli nad glowe siedzac: 4x8 powtorzen')
        plan['Trening A'].append("Seria laczona: Cwiczenie wykonaj jedno po drugim bez przerwy, przerwy miedzy seriami laczonymi 60-90 sekund")
        plan['Trening A'].append('a) Uginanie przeedramion z hantlami z rotacja nadgarstka: 3x12 powtórzen na strone')
        plan['Trening A'].append('b) Wyciskanie francuskie : 3x10 powtórzeń')
        plan['Trening A'].append('Hollow body: 3 serie, max sekund z zachowaniem prawidlowej techniki')
        plan['Trening B'].append('Unoszenie bioder ze sztanga: 4x12powtorzen')
        plan['Trening B'].append('Prostowanie przyciaganie drazka wyciagu gornego do bioder: 3x12 powtorzen')
        plan['Trening B'].append('Wioslowanie hantla w oparciu o laweczke; 3x10 powtorzen na strone')
        plan['Trening B'].append('Wyciskanie na maszynie hammer: 4x12 powtorzen')
        plan['Trening B'].append('Wyciskanie na maszynie hammer: 4x12 powtorzen')
        plan['Trening B'].append('Military press, wyciskanie zolnierskie: 3x10 powtorzen')
        plan['Trening B'].append("Seria laczona: Cwiczenie wykonaj jedno po drugim bez przerwy, przerwy miedzy seriami laczonymi 60-90 sekund")
        plan['Trening B'].append('a) Uginanie przedramion w waskim chwycie ze sztanga stojac: 3x12 powtorzen')
        plan['Trening B'].append('b) Prostowanie ramion z hantlami za siebie w opadzie tulowia: 3x12 powtorzen')
        plan['Trening B'].append('Swieca z prostowaniem nog lezac: 4x10 powtorzen')
        plan['Trening C'].append('Goblet box squat: 4x10 powtorzen')
        plan['Trening C'].append('Zginanie nog na maszynie siedzac: 3x10 powtorzen')
        plan['Trening C'].append('Wioslowanie sztanga nadchwytem w opadzie tulowia: 4x8 powtorzen')
        plan['Trening C'].append('Rozpietki na maszynie butterfly: 4x15 powtorzen')
        plan['Trening C'].append("Seria laczona: Cwiczenie wykonaj jedno po drugim bez przerwy, przerwy miedzy seriami laczonymi 60-90 sekund")
        plan['Trening C'].append('a) Uginanie przedramion z lina z wyciagu dolnego stojac: 3x12 powtorzen')
        plan['Trening C'].append('b) Unoszenie ramienia z wykorzystaniem linki wyciagu dolnego: 3x12 powtorzen')
        plan['Trening C'].append('Wyciskanie sztangi waskim chwytem: 4x8 powtorzen')
        plan['Trening C'].append('Russian twist: 3x12 powtorzen na strone')

        #for day in plan:
           # plan[day].append('Trening z pełnym wyposażeniem siłowni')

        # Logika na podstawie celów
    if user.goals == 'weight_loss':
        # Dodajemy więcej cardio dla utraty wagi
        for day in plan:
            plan[day].append('minimum 30 minut cardio po treningu ')
    elif user.goals == 'muscle_gain':
        # Dodajemy więcej treningu siłowego dla przyrostu mięśni
        for day in plan:
            plan[day].append(
                '20 minut cardio po treningu. I. Jeśli masz możliwość przeprowadzić cardio na zewnątrz, wykonaj interwał biegowy. Rozpocznij od 2-minutowego truchtu, następnie wykonaj: → bieg w tempie 60% maksymalnej prędkości przez 30 sekund, → marsz przez 90 sekund. Interwał wykonuj przez zalecony czas. II. Jeśli dysponujesz odpowiednim sprzętem, np. bieżnia/orbitrek, możesz przeprowadzić klasyczny trening cardio przez 20 minut. Utrzymaj tętno w przedziale 60–80% tętna maksymalnego.  ')

    # Logika dla ograniczeń zdrowotnych
#    if user.health_limitations:
        # Dostosuj trening, aby był bezpieczny dla użytkownika z ograniczeniami zdrowotnymi
       # for day in plan:
        #    plan[day].append(f'Dostosowanie ćwiczeń: {user.health_limitations}')'

    # Zwróć kompletny plan treningowy
    return plan



if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__main__":
    app.run()
