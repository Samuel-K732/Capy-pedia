from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap4
import json
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap4(app)

with open("theory.json", encoding="utf-8") as file:
    theory_data = json.load(file)


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/theory')
def theory():
    return render_template("theory.html", theory=theory_data)


@app.route("/post/<int:index>")
def show_theme(index):
    requested_theme = None
    for theme in theory_data:
        if theme["id"] == index:
            requested_theme = theme
    return render_template("theme.html", theme=requested_theme)


with open("testing.json", encoding="utf-8") as file:
    test_data = json.load(file)


@app.route("/testing")
def testing():
    return render_template("testing.html", test_data=test_data)


class TestForm(FlaskForm):
    pass


@app.route("/test/<int:index>", methods=["GET", "POST"])
def show_test(index):
    requested_test = None
    for test in test_data:
        if test["id"] == index:

            correct_answers = []
            for data in test["test_content"]:
                for answer in data["answers"]:
                    if answer["type"] == "True":
                        correct_answers.append(answer["answer"])

            for question in test["test_content"]:
                setattr(TestForm, f"q{question['id']}", RadioField(
                    label=f"{question['id']}. {question['question']}",
                    choices=[question["answers"][0]["answer"], question["answers"][1]["answer"],
                             question["answers"][2]["answer"], question["answers"][3]["answer"]],
                    validators=[InputRequired(message="Вы должны выбрать один ответ.")]))
            setattr(TestForm, "submit", SubmitField('ЗАВЕРШИТЬ'))

            score = 0
            all_data = []
            form = TestForm()
            if form.validate_on_submit():
                for answer in form.data.values():
                    all_data.append(answer)
                given_answers = all_data[:10:]
                for answer in range(len(given_answers)):
                    if given_answers[answer] == correct_answers[answer]:
                        score += 1
                return render_template("results.html", score=score)
            return render_template("test.html", test=test, form=form)


if __name__ == "__main__":
    app.run(debug=True)
