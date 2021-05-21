-- Please Hold NO Criticism Back, I am sure I did not do this correctly!!!! --


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
SELECT :trainingTypeInput FROM TrainingTypes;
-- add training type by user input 
INSERT INTO TrainingTypes (trainingType) VALUES (:trainingTypeInput);
-- update training type by user input
UPDATE TrainingTypes SET trainingType = :trainingTypeInput WHERE trainingType = :trainingType_from_training_type_form;
-- delete training type by user input 
DELETE FROM TrainingTypes WHERE trainingType = :trainingType_selected_from_training_type_form;


-- ExerciseTrainings Table --
-- get all exercise Ids & training types
SELECT * FROM ExerciseTrainings;
-- associate exercise Id with a training type (M-to-M relationship addition)
INSERT INTO ExerciseTrainings (exerciseId, trainingType) VALUES (:exercise_id_from_exerciseIdInput, :trainingType_from_trainingTypeInput);
-- update exercises data based on submission of the Update exercise form 
UPDATE ExerciseTrainings SET exerciseId = :exercise_ID_from_exercise_form;
-- update training type data based on submission of the Update training type form 
UPDATE ExerciseTrainings SET trainingType = :trainingType_from_training_type_form;
-- dis-associate exercise id from a training type (M-to-M relationship deletion)
DELETE FROM ExerciseTrainings WHERE exerciseId = :exercise_ID_selected_from_exercises_and_training_types_list AND trainingType = :training_type_selected_from_exercises_and_training_types_list;



-- MuscleGroups Table --
-- get all names 
SELECT * FROM MuscleGroups;
SELECT muscleGroup FROM MuscleGroups;
-- search muscle group name by user input
SELECT :muscleGroupInput FROM MuscleGroups;
-- add muscle group by user input 
INSERT INTO MuscleGroups (muscleGroup) VALUES (:muscleGroupInput);
-- update muscle group by user input
UPDATE MuscleGroups SET muscleGroup = :muscleGroupInput WHERE muscleGroup = :muscleGroup_from_muscle_group_form;
-- delete muscle group by user input 
DELETE FROM MuscleGroups WHERE muscleGroup = :muscleGroup_selected_from_muscle_group_form;


-- ExerciseMuscles Table --
-- get all exercise Ids & muscle groups
SELECT * FROM ExerciseMuscles;
-- associate exercise Id with a muscle group (M-to-M relationship addition)
INSERT INTO ExerciseMuscles (exerciseId, muscleGroup) VALUES (:exercise_id_from_exerciseIdInput, :muscleGroup_from_muscleGroupInput);
-- update exercises data based on submission of the Update exercise form 
UPDATE ExerciseMuscles SET exerciseId = :exercise_ID_from_exercise_form;
-- update muscle group data based on submission of the Update muscle group form 
UPDATE ExerciseMuscles SET muscleGroup = :muscleGroup_from_muscle_group_form;
-- dis-associate exercise id from a muscle group (M-to-M relationship deletion)
DELETE FROM ExerciseMuscles WHERE exerciseId = :exercise_ID_selected_from_exercises_and_muscle_groups_list AND muscleGroup = :muscle_group_selected_from_exercises_and_muscle_groups_list;


-- MovementTypes Table --
-- get all names 
SELECT * FROM MovementTypes;
SELECT movementType FROM MovementTypes;
-- search movement type name by user input
SELECT :movementTypeInput FROM MovementTypes;
-- add movement type by user input 
INSERT INTO MovementTypes (movementType) VALUES (:movementTypeInput);
-- update movement type by user input
UPDATE MovementTypes SET movementType = :movementTypeInput WHERE movementType = :movementType_from_movement_type_form;
-- delete movement type by user input 
DELETE FROM MovementTypes WHERE movementType = :movementType_selected_from_movement_type_form;


-- ExerciseMovments Table --
-- get all exercise Ids & movement types
SELECT * FROM ExerciseMovements;
-- associate exercise Id with a movement type (M-to-M relationship addition)
INSERT INTO ExerciseMovements (exerciseId, movementType) VALUES (:exercise_id_from_exerciseIdInput, :muscleGroup_from_movementTypeInput);
-- update exercises data based on submission of the Update exercise form 
UPDATE ExerciseMovements SET exerciseId = :exercise_ID_from_exercise_form;
-- update movement type data based on submission of the Update movement type form 
UPDATE ExerciseMovements SET movementType = :movementType_from_movement_type_form;
-- dis-associate exercise id from a movement type (M-to-M relationship deletion)
DELETE FROM ExerciseMovements WHERE exerciseId = :exercise_ID_selected_from_exercises_and_movement_types_list AND movementType = :movement_type_selected_from_exercises_and_movement_types_list;