from flask import Flask, render_template, request, redirect, url_for
import os
import json
import database.db_connector as db
import operator
import itertools
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

    if request.method == "POST":

        exercise_name = request.form.get('exercise_name')
        # request.form.getlist to show each instance of training,movement,muscle_groups
        training = request.form.getlist('training') 
        movement = request.form.getlist('movement')
        muscle_groups = request.form.getlist('muscle_groups')
        #print(request.form.get('exercise_name'))
        if exercise_name.IsNullOrEmpty:
            print("alerty")

        # Insert queries to insert into all M to M relationships via transitional tables
        query = "INSERT INTO Exercises (exerciseName) VALUES (%s)"
        query_args = (exercise_name) 
        query_results = db.execute_query(db_connection, query, [query_args])
        db_connection.commit()


        query = "INSERT INTO ExerciseTrainings (exerciseId, trainingId) \
        SELECT Exercises.exerciseId, TrainingTypes.trainingId \
        FROM Exercises, TrainingTypes  \
        WHERE Exercises.exerciseName = %s \
        AND TrainingTypes.trainingType= %s"
        # iterate through training list
        for i in training:
            query_args = (exercise_name, i)
            query_results = db.execute_query(db_connection, query, query_args)
            db_connection.commit()


        query = "INSERT INTO ExerciseMovements (exerciseId, movementId) \
        SELECT Exercises.exerciseId, MovementTypes.movementId \
        FROM Exercises, MovementTypes  \
        WHERE Exercises.exerciseName = %s \
        AND MovementTypes.movementType= %s"
        # iterate through movement list
        for i in movement:
            query_args = (exercise_name, i) 
            query_results = db.execute_query(db_connection, query, query_args)
            db_connection.commit()

        query = "INSERT INTO ExerciseMuscles (exerciseId, muscleId) \
        SELECT Exercises.exerciseId, MuscleGroups.muscleId \
        FROM Exercises, MuscleGroups  \
        WHERE Exercises.exerciseName = %s \
        AND MuscleGroups.muscleGroup= %s"
        # iterate through muscle group list
        for i in muscle_groups:
            query_args = (exercise_name, i) 
            query_results = db.execute_query(db_connection, query, query_args)
            db_connection.commit()
        
        # print("END OF POST")
    
    
    # values to show in form dropdowns
    get_training = "SELECT trainingType FROM TrainingTypes WHERE TrainingTypes.trainingType != 'None' "
    cursor = db.execute_query(db_connection=db_connection, query=get_training)
    training_results = cursor.fetchall() #data from database.

    get_movement = "SELECT movementType FROM MovementTypes"
    cursor = db.execute_query(db_connection=db_connection, query=get_movement)
    movement_results = cursor.fetchall() #data from database.

    get_muscle = "SELECT muscleGroup FROM MuscleGroups"
    cursor = db.execute_query(db_connection=db_connection, query=get_muscle)
    muscle_results = cursor.fetchall() #data from database.

  
    # originally had SELECT distinct (Exercises.exerciseId), .....
    # render rows for table 
    get_all = "SELECT Exercises.exerciseId, Exercises.exerciseName, TrainingTypes.trainingType, \
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
    #print(results_all) # prints how arrays look
    final_results = extract(results_all) # extract data from tuple of dictionaries

    return render_template("exercises.j2", data=final_results, training=training_results, 
    movement=movement_results, muscle=muscle_results)


# function to extract data from tuple of dictionaries for proper rendering
def extract(tupleOfDicts):
    to_keep = operator.itemgetter('exerciseId', 'exerciseName')
    to_merge = operator.itemgetter('trainingType', 'movementType', 'muscleGroup')
    listOfDicts = list(tupleOfDicts)
    listOfDicts.sort(key=to_keep)
    getting = itertools.groupby(listOfDicts, to_keep)
    final = []
    for (exerciseId, exerciseName), rest in getting:
        tra = []
        mov = []
        mus = []
        for x in rest:
            if x['trainingType'] not in tra:
                tra.append(x['trainingType'])
            if x['movementType'] not in mov:
                mov.append(x['movementType'])
            if x['muscleGroup'] not in mus:
                mus.append(x['muscleGroup'])
        final.append({'exerciseId':exerciseId, 'exerciseName':exerciseName, 'trainingType':tra, 'movementType':mov, 'muscleGroup':mus})
    #print(final)
    return final

# function to extract data from only one row
def extractRow(row):
    to_keep = operator.itemgetter('exerciseId', 'exerciseName')
    to_merge = operator.itemgetter('trainingType', 'movementType', 'muscleGroup')
    li = []
    li.append(row)
    li.sort(key=to_keep)
    getting = itertools.groupby(li, to_keep)
    final = []
    for (exerciseId, exerciseName), rest in getting:
        tra = []
        mov = []
        mus = []
        for x in rest:
            if x['trainingType'] not in tra:
                tra.append(x['trainingType'])
            if x['movementType'] not in mov:
                mov.append(x['movementType'])
            if x['muscleGroup'] not in mus:
                mus.append(x['muscleGroup'])
        final.append({'exerciseId':exerciseId, 'exerciseName':exerciseName, 'trainingType':tra, 'movementType':mov, 'muscleGroup':mus})
    return final


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
         
        # get data from search
        search_bar = request.form.get('search-bar')
        #print(search_bar)
        
        
        # render for dropdowns   
        get_training = "SELECT trainingType FROM TrainingTypes WHERE TrainingTypes.trainingType != 'None' "
        cursor = db.execute_query(db_connection=db_connection, query=get_training)
        training_results = cursor.fetchall() #data from database.
        get_movement = "SELECT movementType FROM MovementTypes"
        cursor = db.execute_query(db_connection=db_connection, query=get_movement)
        movement_results = cursor.fetchall() #data from database.
        get_muscle = "SELECT muscleGroup FROM MuscleGroups"
        cursor = db.execute_query(db_connection=db_connection, query=get_muscle)
        muscle_results = cursor.fetchall() #data from database.
        
        # render rows for table 
        get_all = "SELECT Exercises.exerciseId, Exercises.exerciseName, TrainingTypes.trainingType, \
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
        ON ExerciseMuscles.muscleId = MuscleGroups.muscleId WHERE Exercises.exerciseName = '%s' " % (search_bar)
        cursor = db.execute_query(db_connection=db_connection, query=get_all)
        results_all = cursor.fetchall() #data from database.
        #print(results_all) # prints how arrays look
        final_results = extract(results_all) # extract data for proper rendering
        return render_template("exercises.j2", data=final_results, training=training_results, movement=movement_results, muscle=muscle_results)
            
  
    
@app.route('/muscle_groups', methods=['GET', 'POST'])
def muscle_groups():

    if request.method == 'POST':
     
        muscle_groups = request.form.get('muscle_groups')
        print("The muscle group is", muscle_groups)
        if any(x.isalpha() or x.isdigit() for x in muscle_groups):
            query = "INSERT INTO MuscleGroups (muscleGroup) VALUES (%s)"
            query_args = (muscle_groups) 
            query_results = db.execute_query(db_connection, query, [query_args])
            db_connection.commit()

    
    get_data = "SELECT distinct muscleGroup FROM MuscleGroups"
    cursor = db.execute_query(db_connection=db_connection, query=get_data)
    results = cursor.fetchall() #data from database.
        

    return render_template("muscle_groups.j2", data=results)

@app.route('/search_muscle', methods=['GET','POST'])
def search_muscle():
    if request.method == 'POST':

        search_bar = request.form.get('search-bar')

        if search_bar.isalpha() or search_bar.isdigit():
            get_data = "SELECT muscleGroup FROM MuscleGroups WHERE MuscleGroups.muscleGroup= '%s' "  % (search_bar)
            cursor = db.execute_query(db_connection=db_connection, query=get_data)
            results = cursor.fetchall() #data from database.

            return render_template("muscle_groups.j2", data=results)
        else:
            return redirect(url_for('muscle_groups'))

    


@app.route('/movement_types', methods=['GET', 'POST'])
def movement_types():
    
    if request.method == 'POST':

        movement_type = request.form.get('movement')
        print("The movement type is", movement_type)
        if any(x.isalpha() or x.isdigit() for x in movement_type):
            query = "INSERT INTO MovementTypes (movementType) VALUES (%s)"
            query_args = (movement_type) 
            query_results = db.execute_query(db_connection, query, [query_args])
            db_connection.commit()

    get_data = "SELECT distinct movementType FROM MovementTypes"
    cursor = db.execute_query(db_connection=db_connection, query=get_data)
    results = cursor.fetchall() #data from database.

    return render_template("movement_types.j2", data=results)



@app.route('/search_movement', methods=['GET','POST'])
def search_movement():
    if request.method == 'POST':

        search_bar = request.form.get('search-bar')

        
        get_data = "SELECT movementType FROM MovementTypes WHERE MovementTypes.movementType = '%s' "  % (search_bar)
        cursor = db.execute_query(db_connection=db_connection, query=get_data)
        results = cursor.fetchall() #data from database.

        return render_template("movement_types.j2", data=results)

    
@app.route('/training_types', methods=['GET','POST'])
def training_types():
    
    if request.method == 'POST':

        training = request.form.get('training')
        search_bar = request.form.get('search-bar')

        print("The training type is", training)
        query = "SELECT trainingType from TrainingTypes WHERE trainingType = (%s)"
        query_args = (search_bar, ) 
        query_results = db.execute_query(db_connection, query, [query_args])
        db_connection.commit()

        query = "INSERT INTO TrainingTypes (trainingType) VALUES (%s)"
        query_args = (training) 
        query_results = db.execute_query(db_connection, query, [query_args])
        db_connection.commit()

    get_data = "SELECT distinct trainingType FROM TrainingTypes WHERE TrainingTypes.trainingType != 'None' "
    cursor = db.execute_query(db_connection=db_connection, query=get_data)
    results = cursor.fetchall() #data from database.

    return render_template("training_types.j2", data=results)

@app.route('/search_training', methods=['GET','POST'])
def search_training():
    if request.method == 'POST':

        search_bar = request.form.get('search-bar')

   
        get_data = "SELECT trainingType FROM TrainingTypes WHERE TrainingTypes.trainingType = '%s' "  % (search_bar)
        cursor = db.execute_query(db_connection=db_connection, query=get_data)
        results = cursor.fetchall() #data from database.

        return render_template("training_types.j2", data=results)



@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    print(id)
   
    if request.method == 'POST':

        update_name = request.form.get('update_name')
        # request.form.getlist to get each instance of training,movement,muscle_groups
        update_train = request.form.getlist('update_train') 
        trainId = request.form.getlist('trainId') 
        update_move = request.form.getlist('update_move')
        moveId = request.form.getlist('moveId') 
        update_musc = request.form.getlist('update_musc')
        muscId = request.form.getlist('muscId') 
        
    
        for u, h in zip(update_musc, muscId):
             print(u, h)
        
        # check if there was any input to update exercise name
        if any(x.isalpha() or x.isdigit() for x in update_name):
            query = "UPDATE Exercises SET exerciseName = %s WHERE exerciseID = %s" 
            query_args = (update_name, id ) 
            query_results = db.execute_query(db_connection, query, query_args)
            db_connection.commit()

        # for each element in training type in cell run queries to update values using name and id
        for u, h in zip(update_train, trainId):
            # null update training type to fulfill project requirements
            if not u.isalpha() or u.isdigit():
                queryNull = "UPDATE ExerciseTrainings INNER JOIN TrainingTypes \
                ON TrainingTypes.trainingId = ExerciseTrainings.trainingId INNER JOIN Exercises \
                ON ExerciseTrainings.exerciseId = Exercises.exerciseId SET ExerciseTrainings.trainingId = 1 \
                WHERE ExerciseTrainings.trainingId = %s AND ExerciseTrainings.exerciseId = %s " 
                query_args = (h, id) # leave comma if only 1 argument
                query_results = db.execute_query(db_connection, queryNull, query_args)
                db_connection.commit()
            else:
                # if value to update is not in table, insert
                query1 = "INSERT INTO TrainingTypes (trainingType)\
                SELECT %s FROM TrainingTypes AS new WHERE NOT EXISTS \
                (SELECT trainingType FROM TrainingTypes WHERE trainingType = %s) LIMIT 1"  # cambia esta vaina
                query_args = (u, u) # leave comma if only 1 argument
                query_results = db.execute_query(db_connection, query1, query_args)
                db_connection.commit()

                # update corresponding id in transitional table
                query2 = "UPDATE ExerciseTrainings INNER JOIN TrainingTypes \
                ON TrainingTypes.trainingId = ExerciseTrainings.trainingId INNER JOIN Exercises \
                ON ExerciseTrainings.exerciseId = Exercises.exerciseId \
                SET ExerciseTrainings.trainingId = (SELECT trainingId FROM TrainingTypes WHERE TrainingTypes.trainingType = %s) \
                WHERE ExerciseTrainings.trainingId = %s AND ExerciseTrainings.exerciseId = %s " 
                query_args = (u, h, id) # leave comma if only 1 argument
                query_results = db.execute_query(db_connection, query2, query_args)
                db_connection.commit()
    
        # for each element in movement type in cell run queries to update values using name and id
        for u, h in zip(update_move, moveId):
            # if value to update is not in table, insert
                query1 = "INSERT INTO MovementTypes (movementType)\
                SELECT %s FROM MovementTypes AS new WHERE NOT EXISTS \
                (SELECT movementType FROM MovementTypes WHERE movementType = %s) LIMIT 1"
                query_args = (u, u) # leave comma if only 1 argument
                query_results = db.execute_query(db_connection, query1, query_args)
                db_connection.commit()
                
                # update corresponding id in transitional table
                query2 = "UPDATE ExerciseMovements INNER JOIN MovementTypes \
                ON MovementTypes.movementId = ExerciseMovements.movementId INNER JOIN Exercises \
                ON ExerciseMovements.exerciseId = Exercises.exerciseId \
                SET ExerciseMovements.movementId = (SELECT movementId FROM MovementTypes WHERE MovementTypes.movementType = %s) \
                WHERE ExerciseMovements.movementId = %s AND ExerciseMovements.exerciseId = %s " 
                query_args = (u, h, id) # leave comma if only 1 argument
                query_results = db.execute_query(db_connection, query2, query_args)
                db_connection.commit()

        # for each element in movement type in cell run queries to update values using name and id
        for u, h in zip(update_musc, muscId):
            # if value to update is not in table, insert
                query1 = "INSERT INTO MuscleGroups (muscleGroup)\
                SELECT %s FROM MuscleGroups AS new WHERE NOT EXISTS \
                (SELECT muscleGroup FROM MuscleGroups WHERE muscleGroup = %s) LIMIT 1"
                query_args = (u, u) # leave comma if only 1 argument
                query_results = db.execute_query(db_connection, query1, query_args)
                db_connection.commit()
                
                # update corresponding id in transitional table
                query2 = "UPDATE ExerciseMuscles INNER JOIN MuscleGroups \
                ON MuscleGroups.muscleId = ExerciseMuscles.muscleId INNER JOIN Exercises \
                ON ExerciseMuscles.exerciseId = Exercises.exerciseId \
                SET ExerciseMuscles.muscleId = (SELECT muscleId FROM MuscleGroups WHERE MuscleGroups.muscleGroup = %s) \
                WHERE ExerciseMuscles.muscleId = %s AND ExerciseMuscles.exerciseId = %s " 
                query_args = (u, h, id) # leave comma if only 1 argument
                query_results = db.execute_query(db_connection, query2, query_args)
                db_connection.commit()
        
        return redirect(url_for('exercises'))
     
            
    
    # values to render what to change for each table
    get_training = "SELECT TrainingTypes.trainingType, TrainingTypes.trainingId FROM TrainingTypes INNER JOIN ExerciseTrainings \
    ON ExerciseTrainings.trainingId = TrainingTypes.trainingId \
    INNER JOIN Exercises \
    ON Exercises.exerciseId = ExerciseTrainings.exerciseId \
    WHERE Exercises.exerciseId = %s" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=get_training)
    training_results = cursor.fetchall() #data from database.

    get_movement = "SELECT MovementTypes.movementType, MovementTypes.movementId FROM MovementTypes INNER JOIN ExerciseMovements \
    ON ExerciseMovements.movementId = MovementTypes.movementId \
    INNER JOIN Exercises \
    ON Exercises.exerciseId = ExerciseMovements.exerciseId \
    WHERE Exercises.exerciseId = %s" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=get_movement)
    movement_results = cursor.fetchall() #data from database.

    get_muscle = "SELECT MuscleGroups.muscleGroup, MuscleGroups.muscleId FROM MuscleGroups INNER JOIN ExerciseMuscles \
    ON ExerciseMuscles.muscleId = MuscleGroups.muscleId \
    INNER JOIN Exercises \
    ON Exercises.exerciseId = ExerciseMuscles.exerciseId \
    WHERE Exercises.exerciseId = %s" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=get_muscle)
    muscle_results = cursor.fetchall() #data from database.


    # a row from table 
    get_row = "SELECT Exercises.exerciseId, Exercises.exerciseName, TrainingTypes.trainingType, \
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
    ON ExerciseMuscles.muscleId = MuscleGroups.muscleId WHERE Exercises.exerciseId = %s" % (id)
    cursor = db.execute_query(db_connection=db_connection, query=get_row)
    results_row = cursor.fetchone() #fetchone just gets row
    #print(results_row) # prints how arrays look
    
    if results_row == None:
        return "NOT FOUND"

    final_results = extractRow(results_row)

    #a_query = "SELECT exerciseId, exerciseName FROM Exercises"
    #cursor = db.execute_query(db_connection=db_connection, query=a_query)
    #a_query = cursor.fetchall() 
    #print(a_query)
    #final_results = extract(a_query) ???
    
    #return render_template("update.j2",data=final_results)

    return render_template("update.j2", data=final_results, training=training_results, movement=movement_results, muscle=muscle_results)
 
@app.route('/delete/<int:id>')
def delete(id):
    #delete_exercise = request.form.get('trainId') 

   # if POST and make sure the POST GET STUFF IS in the app route and un-comment get stuff below
   
    #print(id)
    # Delete query for Exercise table that satisfies project requirements
    query = "DELETE FROM Exercises WHERE exerciseID = %s" 
    query_args = (id, ) 
    query_results = db.execute_query(db_connection, query, query_args)
    db_connection.commit()

    return redirect(url_for('exercises'))

                
    # Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9191))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
