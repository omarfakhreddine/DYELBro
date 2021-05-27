from flask import Flask, render_template
from flask import request, redirect
import os
import json
import database.db_connector as db

"""
MYSQL on hand Syntax.

SELECT:
SELECT [columns] FROM [table] (WHERE [condition]) (ORDER BY [column] ASC/DESC) (LIMIT [num])
"""

"""
TODO: write queries for each table/form
TODO: create for loops in templates to handle query results
TODO: make database entities have unique requirement
TODO: make search functional by making search input into forms
"""

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes


@app.route('/')
def root():
    return render_template("home.j2")


@app.route('/exercises', methods=['POST', 'GET'])
def exercises():
    
    headings = ("Exercise ID", "Exercise Name", "Training Type", "Movement Type", "Muscle Groups")
    placeholder = (
    ("1", "Bench Press", "Strength", "Push", "Chest, Arms"),
    ("2", "Deadlift", "Strength", "Pull", "Back"),
    ("3", "Romanian Squat", "Strength", "Squat", "Legs"),
    ("4", "Bicep Curl", "Strength", "Pull", "Arms")
    )

    if request.method == "POST":
        exercise_name = request.form.get('exercise_name')
        training = request.form.get('training')
        movement = request.form.get('movement')
        muscle_groups = request.form.get('muscle_groups')
        
        query = "INSERT INTO Exercises (exerciseName) VALUES (%s)"
        query_args = (exercise_name) 
        query_results = db.execute_query(db_connection, query, [query_args])
        db_connection.commit()

        #query = "INSERT INTO ExerciseTrainings (trainingType) VALUES (%s)"
        #query_args = (training) 
        #query_results = db.execute_query(db_connection, query, [query_args])
        #db_connection.commit()

        #query = "INSERT INTO ExerciseMovements (movementType) VALUES (%s)"
        #query_args = (movement) 
        #query_results = db.execute_query(db_connection, query, [query_args])
        #db_connection.commit()
        
        #query = "INSERT INTO ExerciseMuscles (muscleGroup) VALUES (%s)"
        #query_args = (muscle_groups) 
        #query_results = db.execute_query(db_connection, query, [query_args])
        #db_connection.commit()

        query = "INSERT INTO TrainingTypes (trainingType) VALUES (%s)"
        query_args = (training) 
        query_results = db.execute_query(db_connection, query, [query_args])
        db_connection.commit()

        query = "INSERT INTO MovementTypes (movementType) VALUES (%s)"
        query_args = (movement) 
        query_results = db.execute_query(db_connection, query, [query_args])
        db_connection.commit()
        
        query = "INSERT INTO MuscleGroups (muscleGroup) VALUES (%s)"
        query_args = (muscle_groups) 
        query_results = db.execute_query(db_connection, query, [query_args])
        db_connection.commit()


    #get_id = "SELECT exerciseId FROM Exercises WHERE exerciseName = 'bench press' "
    #cursor = db.execute_query(db_connection=db_connection, query=get_id)
    #results_id = cursor.fetchall() #data from database.

    #get_ex = "SELECT exerciseName FROM Exercises WHERE exerciseId = 1"
    #cursor = db.execute_query(db_connection=db_connection, query=get_ex)
    #results_ex = cursor.fetchall() #data from database.
     
    #get_train = "SELECT trainingType FROM TrainingTypes WHERE trainingType = 'cardio' "
    #cursor = db.execute_query(db_connection=db_connection, query=get_train)
    #results_tr= cursor.fetchall() #data from database.

    #get_move = "SELECT movementType FROM MovementTypes WHERE movementType = 'hinge' "
    #cursor = db.execute_query(db_connection=db_connection, query=get_move)
    #results_mov= cursor.fetchall() #data from database.

    #get_musc = "SELECT muscleGroup FROM MuscleGroups WHERE muscleGroup = 'biceps' "
    #cursor = db.execute_query(db_connection=db_connection, query=get_musc)
    #results_musc= cursor.fetchall() #data from database.

    get_all = "SELECT Exercises.exerciseId, Exercises.exerciseName, TrainingTypes.trainingType, \
    MovementTypes.movementType, MuscleGroups.muscleGroup FROM Exercises \
    INNER JOIN ExerciseTrainings \
    ON Exercises.exerciseID = ExerciseTrainings.exerciseId \
    INNER JOIN TrainingTypes \
    ON ExerciseTrainings.trainingType = TrainingTypes.trainingType \
    INNER JOIN ExerciseMovements \
    ON Exercises.exerciseId = ExerciseMovements.exerciseId \
    INNER JOIN MovementTypes \
    ON ExerciseMovements.movementType = MovementTypes.movementType \
    INNER JOIN ExerciseMuscles \
    ON Exercises.exerciseID = ExerciseMuscles.exerciseId  \
    INNER JOIN MuscleGroups  \
    ON ExerciseMuscles.muscleGroup = MuscleGroups.muscleGroup"

    cursor = db.execute_query(db_connection=db_connection, query=get_all)
    results_all= cursor.fetchall() #data from database.

    return render_template("exercises.j2", data=results_all)
   # return render_template("exercises.j2", headings=headings, data=placeholder)
   # return render_template("exercises.j2", id_num=results_id, ex_num=results_ex, tr_num=results_tr)
   

    
@app.route('/muscle_groups', methods=['GET', 'POST'])
def muscle_groups():
    placeholder = (
    ("Chest, Arms"), ("Back"), ("Legs"), ("Arms")
    )

    if request.method == 'POST':

        muscle_groups = request.form.get('muscle_groups')
        print("The muscle group is", muscle_groups)
        query = "INSERT INTO MuscleGroups (muscleGroup) VALUES (%s)"
        query_args = (muscle_groups) 
        query_results = db.execute_query(db_connection, query, [query_args])
        db_connection.commit()

    
    get_data = "SELECT muscleGroup FROM MuscleGroups"
    cursor = db.execute_query(db_connection=db_connection, query=get_data)
    results = cursor.fetchall() #data from database.
        

    return render_template("muscle_groups.j2", data=results)
    
@app.route('/movement_types', methods=['GET', 'POST'])
def movement_types():
    
    placeholder = (
    ("hinge"), ("push"), ("pull"), ("flex")
    )

    if request.method == 'POST':

        movement_type = request.form.get('movement')
        print("The movement type is", movement_type)

        query = "INSERT INTO MovementTypes (movementType) VALUES (%s)"
        query_args = (movement_type) 
        query_results = db.execute_query(db_connection, query, [query_args])
        db_connection.commit()

    get_data = "SELECT movementType FROM MovementTypes"
    cursor = db.execute_query(db_connection=db_connection, query=get_data)
    results = cursor.fetchall() #data from database.

    return render_template("movement_types.j2", data=results)

    
@app.route('/training_types', methods=['GET','POST'])
def training_types():
    
    if request.method == 'POST':

        training = request.form.get('training')
        print("The training type is", training)

        query = "INSERT INTO TrainingTypes (trainingType) VALUES (%s)"
        query_args = (training) 
        query_results = db.execute_query(db_connection, query, [query_args])
        db_connection.commit()

    get_data = "SELECT trainingType FROM TrainingTypes"
    cursor = db.execute_query(db_connection=db_connection, query=get_data)
    results = cursor.fetchall() #data from database.

    return render_template("training_types.j2", data=results)

    # Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9191))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
