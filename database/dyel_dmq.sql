
-- Note: UPDATE AND DELETE QUERY implemented 
-- Exercises Table --
-- get all ids and names
SELECT * FROM Exercises;
SELECT exerciseId, exerciseName FROM Exercises;
-- search exercise name by user input
SELECT :exerciseNameInput FROM Exercises;
-- add exercise by user input 
INSERT INTO Exercises (exerciseName) VALUES (:exerciseNameInput);
-- update exercise by user input
UPDATE Exercises SET exerciseName = :exerciseInput WHERE exerciseId= :exercise_ID_from_exercise_form;
-- delete exercise by user input 
DELETE FROM Exercises WHERE exerciseId = :exercise_ID_selected_from_exercise_form;



-- TrainingTypes Table --
-- get all names 
SELECT * FROM TrainingTypes;
SELECT trainingType FROM TrainingTypes;
-- search training type name by user input
SELECT trainingType FROM TrainingTypes WHERE trainingType =:trainingTypeInput;
-- add training type by user input 
INSERT INTO TrainingTypes (trainingType) VALUES (:trainingTypeInput); 



-- ExerciseTrainings Table --
-- get all exercise Ids & training types
SELECT * FROM ExerciseTrainings;
-- associate exercise Id with a training type (M-to-M relationship addition) using input
INSERT INTO ExerciseTrainings (exerciseId, trainingId) 
SELECT Exercises.exerciseId, TrainingTypes.trainingId 
FROM Exercises, TrainingTypes  
WHERE Exercises.exerciseName = :exerciseNameInput
AND TrainingTypes.trainingType=:trainingTypeInput;
-- update exercise trainings data based on submission of the Update form 
UPDATE ExerciseTrainings INNER JOIN TrainingTypes 
ON TrainingTypes.trainingId = ExerciseTrainings.trainingId INNER JOIN Exercises 
ON ExerciseTrainings.exerciseId = Exercises.exerciseId 
SET ExerciseTrainings.trainingId = (SELECT trainingId FROM TrainingTypes WHERE TrainingTypes.trainingType = :trainingTypeInput) 
WHERE ExerciseTrainings.trainingId = trainingId_from_form AND ExerciseTrainings.exerciseId = exerciseId_from_form;

-- MuscleGroups Table --
-- get all names 
SELECT * FROM MuscleGroups;
SELECT muscleGroup FROM MuscleGroups;
-- search muscle group name by user input
SELECT muscleGroup FROM MuscleGroups WHERE muscleGroup = :muscleGroupInput;
-- add muscle group by user input 
INSERT INTO MuscleGroups (muscleGroup) VALUES (:muscleGroupInput);



-- ExerciseMuscles Table --
-- get all exercise Ids & muscle groups
SELECT * FROM ExerciseMuscles;
-- associate exercise Id with a muscle group (M-to-M relationship addition) using input
INSERT INTO ExerciseMuscles (exerciseId, muscleId) 
SELECT Exercises.exerciseId, MuscleGroups.muscleId 
FROM Exercises, MuscleGroups  
WHERE Exercises.exerciseName = :exerciseNameInput
AND MuscleGroups.muscleGroup= :muscleGroupInput;
-- update exercise muscles data based on submission of the Update form 
UPDATE ExerciseMuscles INNER JOIN MuscleGroups 
ON MuscleGroups.muscleId = ExerciseMuscles.muscleId INNER JOIN Exercises 
ON ExerciseMuscles.exerciseId = Exercises.exerciseId 
SET ExerciseMuscles.muscleId = (SELECT muscleId FROM MuscleGroups WHERE MuscleGroups.muscleGroup = :muscleGroupInput) 
WHERE ExerciseMuscles.muscleId = muscleId_from_form AND ExerciseMuscles.exerciseId = :exerciseId_from_form;

-- MovementTypes Table --
-- get all names 
SELECT * FROM MovementTypes;
SELECT movementType FROM MovementTypes;
-- search movement type name by user input
SELECT movementType FROM MovementTypes WHERE movementType = :movementTypeInput;
-- add movement type by user input 
INSERT INTO MovementTypes (movementType) VALUES (:movementTypeInput);



-- ExerciseMovements Table --
-- get all exercise Ids & movement types
SELECT * FROM ExerciseMovements;
-- associate exercise Id with a movement type (M-to-M relationship addition) using input
INSERT INTO ExerciseMovements (exerciseId, movementId) 
SELECT Exercises.exerciseId, MovementTypes.movementId 
FROM Exercises, MovementTypes  
WHERE Exercises.exerciseName = :exerciseNameInput
AND MovementTypes.movementType= :movementTypeInput;
-- update exercise movements data based on submission of the Update form 
UPDATE ExerciseMovements INNER JOIN MovementTypes 
ON MovementTypes.movementId = ExerciseMovements.movementId INNER JOIN Exercises 
ON ExerciseMovements.exerciseId = Exercises.exerciseId 
SET ExerciseMovements.movementId = (SELECT movementId FROM MovementTypes WHERE MovementTypes.movementType = :movementTypeInput) 
WHERE ExerciseMovements.movementId = movementId_from_form AND ExerciseMovements.exerciseId = exerciseId_from_form;

