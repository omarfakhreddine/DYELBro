from flask import Flask, render_template, request, redirect
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

    # values for insert form dropdowns
    get_training = "SELECT trainingType FROM TrainingTypes"
    cursor = db.execute_query(db_connection=db_connection, query=get_training)
    training_results = cursor.fetchall() #data from database.

    get_movement = "SELECT movementType FROM MovementTypes"
    cursor = db.execute_query(db_connection=db_connection, query=get_movement)
    movement_results = cursor.fetchall() #data from database.

    get_muscle = "SELECT muscleGroup FROM MuscleGroups"
    cursor = db.execute_query(db_connection=db_connection, query=get_muscle)
    muscle_results = cursor.fetchall() #data from database.
    
    # rows for table 
    get_all = " SELECT distinct (Exercises.exerciseId), Exercises.exerciseName, TrainingTypes.trainingType, \
    MovementTypes.movementType, MuscleGroups.muscleGroup FROM Exercises \
    INNER JOIN ExerciseTrainings \
    ON Exercises.exerciseId = ExerciseTrainings.exerciseId \
    INNER JOIN TrainingTypes \
    ON ExerciseTrainings.trainingId = TrainingTypes.trainingId \
    INNER JOIN ExerciseMovements \
    ON Exercises.exerciseId = ExerciseMovements.exerciseId \
    INNER JOIN MovementTypes \
    ON ExerciseMovements.movementId = MovementTypes.movementId \
    INNER JOIN ExerciseMuscles \
    ON Exercises.exerciseId = ExerciseMuscles.exerciseId  \
    INNER JOIN MuscleGroups  \
    ON ExerciseMuscles.muscleId = MuscleGroups.muscleId"
    cursor = db.execute_query(db_connection=db_connection, query=get_all)
    results_all = cursor.fetchall() #data from database.

    return render_template("exercises.j2", data=results_all, training=training_results, 
    movement=movement_results, muscle=muscle_results)
   

    if request.method == "POST":

        exercise_name = request.form.get('exercise_name')
        training = request.form.get('training')
        movement = request.form.get('movement')
        muscle_groups = request.form.get('muscle_groups')
        
        query = "INSERT INTO Exercises (exerciseName) VALUES (%s)"
        query_args = (exercise_name) 
        query_results = db.execute_query(db_connection, query, [query_args])
        db_connection.commit()

        query = "INSERT INTO ExerciseTrainings (exerciseId, trainingId) \
        SELECT Exercises.exerciseId, TrainingTypes.trainingId \
        FROM Exercises, TrainingTypes  \
        WHERE Exercises.exerciseName = %s \
        AND TrainingTypes.trainingType= %s"
        query_args = (exercise_name, training) 
        query_results = db.execute_query(db_connection, query, query_args)
        db_connection.commit()

        query = "INSERT INTO ExerciseMovements (exerciseId, movementId) \
        SELECT Exercises.exerciseId, MovementTypes.movementId \
        FROM Exercises, MovementTypes  \
        WHERE Exercises.exerciseName = %s \
        AND MovementTypes.movementType= %s"
        query_args = (exercise_name, movement) 
        query_results = db.execute_query(db_connection, query, query_args)
        db_connection.commit()

        query = "INSERT INTO ExerciseMuscles (exerciseId, muscleId) \
        SELECT Exercises.exerciseId, MuscleGroups.muscleId \
        FROM Exercises, MuscleGroups  \
        WHERE Exercises.exerciseName = %s \
        AND MuscleGroups.muscleGroup= %s"
        query_args = (exercise_name, muscle_groups) 
        query_results = db.execute_query(db_connection, query, query_args)
        db_connection.commit()
        

        #query = "INSERT INTO ExerciseTrainings (exerciseId, trainingId) VALUES (%s)"
        #query_args = (exerciseId, trainingId) 
        #query_results = db.execute_query(db_connection, query, [query_args])
        #db_connection.commit()


        #query = "INSERT INTO ExerciseMovements (exerciseId, movementId) VALUES (%s)"
        #query_args = (exerciseId, movementId) 
        #query_results = db.execute_query(db_connection, query, [query_args])
        #db_connection.commit()

        #query = "INSERT INTO ExerciseMuscles (exerciseId, muscleId) VALUES (%s)"
        #query_args = (exerciseId, muscleId) 
        #query_results = db.execute_query(db_connection, query, [query_args])
        #db_connection.commit()



        print("CHECK")

    
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

    
    get_data = "SELECT distinct muscleGroup FROM MuscleGroups"
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

    get_data = "SELECT distinct movementType FROM MovementTypes"
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

    get_data = "SELECT distinct trainingType FROM TrainingTypes"
    cursor = db.execute_query(db_connection=db_connection, query=get_data)
    results = cursor.fetchall() #data from database.

    return render_template("training_types.j2", data=results)



#@app.route('/update/<int:id>', methods = ['POST', 'GET'])
#exercise_update = "SELECT distinct trainingType FROM TrainingTypes"

#def update_exercise(id):
    #if request.method == "POST":
        #exercise_update = request.form.get('update_ex')
        #db_connection.commit()
        #redirect('/exercises')

    #return render_template("update.j2", exercise_update = exercise_update)

     #<form action="/update/{{row.id}}" method="POST">
      #    <button type="submit"> Update </button> <button>Delete</button>
       # </form> put in exercise.j2
  
    #if request.method == 'GET':

        #query = " SELECT distinct (Exercises.exerciseId), Exercises.exerciseName, TrainingTypes.trainingType, \
        #MovementTypes.movementType, MuscleGroups.muscleGroup FROM Exercises \
        #INNER JOIN ExerciseTrainings \
        #ON Exercises.exerciseId = ExerciseTrainings.exerciseId \
        #INNER JOIN TrainingTypes \
        #ON ExerciseTrainings.trainingId = TrainingTypes.trainingId \
        #INNER JOIN ExerciseMovements \
        #ON Exercises.exerciseId = ExerciseMovements.exerciseId \
        #INNER JOIN MovementTypes \
        #ON ExerciseMovements.movementId = MovementTypes.movementId \
        #INNER JOIN ExerciseMuscles \
        #ON Exercises.exerciseId = ExerciseMuscles.exerciseId  \
        #INNER JOIN MuscleGroups  \
        #ON ExerciseMuscles.muscleId = MuscleGroups.muscleId \
        #WHERE Exercise.exerciseId = %s" 
        #query_args = (id) 
        #cursor = db.execute_query(db_connection=db_connection, query=get_it)
        #results_it = cursor.fetchone() #data from database.

       # if results_it == None:
        #    return "Not found"

        #get_data = "SELECT distinct trainingType FROM TrainingTypes"
        #cursor = db.execute_query(db_connection=db_connection, query=get_data)
        #results = cursor.fetchall() #data from database.

        #return render_template("training_types.j2", data=results)

        









    # Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9191))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
