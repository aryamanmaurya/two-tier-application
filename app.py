from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session management (for flash messages)

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Retrieve and clean user input
            name = request.form['name'].strip()
            age = request.form['age']

            # Validate age is a number and within range
            if not age.isdigit() or not (0 <= int(age) <= 100):
                flash("Please enter a valid age between 0 and 100.")
                return redirect(url_for('index'))
            age = int(age)

            # Capitalize first letter of name
            name = name.capitalize()

            # Connect to the database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert data into the database
            cursor.execute("INSERT INTO userdata (name, age) VALUES (%s, %s)", (name, age))
            conn.commit()

            # Close the connection
            cursor.close()
            conn.close()

            flash("User data saved successfully!")
            return redirect(url_for('index'))

        except mysql.connector.Error as err:
            flash(f"Database error: {err}")
            return redirect(url_for('index'))

        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('index'))

    return render_template('index.html')

# Route to display all users
@app.route('/users')
def users():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch all records from userdata table
        cursor.execute("SELECT * FROM userdata")
        users_data = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        return render_template('users.html', users=users_data)

    except mysql.connector.Error as err:
        flash(f"Database error: {err}")
        return redirect(url_for('index'))

    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

