from flask import Flask, render_template, request, redirect, url_for, session
import math

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure key

def calculate_result(cumulative_inputs, total_rounds, round_number):
    rounds_left = total_rounds - round_number
    floor_avg = math.floor((9 * rounds_left) / 2)
    return floor_avg + cumulative_inputs

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        total_rounds = request.form.get('total_rounds')
        if total_rounds and total_rounds.isdigit() and int(total_rounds) > 0:
            session['total_rounds'] = int(total_rounds)
            session['current_round'] = 1
            session['inputs_so_far'] = 0
            session['results'] = []
            return redirect(url_for('input_round'))
        else:
            error = "Please enter a valid positive integer for rounds."
            return render_template('index.html', error=error)
    return render_template('index.html')

@app.route('/input', methods=['GET', 'POST'])
def input_round():
    total_rounds = session.get('total_rounds')
    current_round = session.get('current_round')
    inputs_so_far = session.get('inputs_so_far')
    results = session.get('results', [])

    round_result = None  # To store result for displaying

    if not total_rounds or not current_round:
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input and user_input.isdigit() and 0 <= int(user_input) <= 9:
            user_input = int(user_input)
            inputs_so_far += user_input
            round_result = calculate_result(inputs_so_far, total_rounds, current_round)
            results.append(round_result)

            session['inputs_so_far'] = inputs_so_far
            session['results'] = results
            session['current_round'] = current_round + 1

            # If finished all rounds, show final results
            if current_round >= total_rounds:
                return redirect(url_for('results'))

            # Otherwise, stay on input page and show the result
            return render_template('input.html', round_num=current_round, round_result=round_result)
        else:
            error = "Please enter a digit between 0 and 9."
            return render_template('input.html', round_num=current_round, error=error)

    # On GET, if it's not the first round, show previous result if available
    round_result = results[-1] if results and current_round > 1 else None
    return render_template('input.html', round_num=current_round, round_result=round_result)


@app.route('/results')
def results():
    results = session.get('results', [])
    total_rounds = session.get('total_rounds', 0)
    return render_template('res.html', results=results, total_rounds=total_rounds)

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
