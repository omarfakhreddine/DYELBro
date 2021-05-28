--
-- Table structure for table `Exercises`
--

DROP TABLE IF EXISTS Exercises;

CREATE TABLE Exercises (
  exerciseId int(11) NOT NULL AUTO_INCREMENT,
  exerciseName varchar(255) NOT NULL,
  PRIMARY KEY (exerciseId)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `Exercises`
INSERT INTO Exercises (exerciseName) VALUES ('bench press'), ('deadlift'), ('squat');



--
-- Table structure for table `TrainingTypes`
--

DROP TABLE IF EXISTS TrainingTypes;

CREATE TABLE TrainingTypes (
  trainingId  int(11) NOT NULL AUTO_INCREMENT,
  trainingType varchar(255) NOT NULL,
  PRIMARY KEY (trainingId)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `TrainingTypes`
INSERT INTO TrainingTypes (trainingType) VALUES ('cardio'), ('endurance'), ('anaerobic');


--
-- Table structure for table `ExerciseTrainings`
--

DROP TABLE IF EXISTS ExerciseTrainings;

CREATE TABLE ExerciseTrainings (
  exerciseId int(11) NOT NULL, -- do we  make null or autoincrement?
  trainingId  int(11) NOT NULL,
  PRIMARY KEY (exerciseId, trainingId),
  CONSTRAINT ExerciseTrainings_fk_1 FOREIGN KEY (exerciseId) REFERENCES Exercises (exerciseId) ON DELETE CASCADE,
  CONSTRAINT ExerciseTrainings_fk_2 FOREIGN KEY (trainingId) REFERENCES TrainingTypes (trainingId) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `ExerciseTrainings`
INSERT INTO ExerciseTrainings (exerciseId, trainingId) VALUES (1, 1), (2, 2), (3, 3);



--
-- Table structure for table `MuscleGroups`
--

DROP TABLE IF EXISTS MuscleGroups;

CREATE TABLE MuscleGroups (
  muscleId int(11) NOT NULL AUTO_INCREMENT,
  muscleGroup varchar(255) NOT NULL,
  PRIMARY KEY (muscleId)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `MuscleGroups`
INSERT INTO MuscleGroups (muscleGroup) VALUES ('biceps'), ('triceps'), ('quads');


--
-- Table structure for table `ExerciseMuscles`
--

DROP TABLE IF EXISTS ExerciseMuscles;

CREATE TABLE ExerciseMuscles (
  exerciseId int(11) NOT NULL, -- do we  make null or autoincrement?
  muscleId int(11) NOT NULL,
  PRIMARY KEY (exerciseId, muscleId),
  CONSTRAINT ExerciseMuscles_fk_1 FOREIGN KEY (exerciseId) REFERENCES Exercises (exerciseId) ON DELETE CASCADE,
  CONSTRAINT ExerciseMuscles_fk_2 FOREIGN KEY (muscleId) REFERENCES MuscleGroups (muscleId) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `ExerciseMuscles`
INSERT INTO ExerciseMuscles (exerciseId, muscleId) VALUES (1, 1), (2, 2), (3, 3);

--
-- Table structure for table `MuscleGroups`
--

DROP TABLE IF EXISTS MovementTypes;

CREATE TABLE MovementTypes (
  movementId  int(11) NOT NULL AUTO_INCREMENT,
  movementType varchar(255) NOT NULL,
  PRIMARY KEY (movementId)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `MovementTypes`
INSERT INTO MovementTypes (movementType) VALUES ('push'), ('pull'), ('hinge');


--
-- Table structure for table `ExerciseMovements`
--

DROP TABLE IF EXISTS ExerciseMovements;

CREATE TABLE ExerciseMovements (
  exerciseId int(11) NOT NULL, -- do we  make null or autoincrement?
  movementId  int(11) NOT NULL,
  PRIMARY KEY (exerciseId, movementId),
  CONSTRAINT ExerciseMovements_fk_1 FOREIGN KEY (exerciseId) REFERENCES Exercises (exerciseId) ON DELETE CASCADE,
  CONSTRAINT ExerciseMovements_fk_2 FOREIGN KEY (movementId) REFERENCES MovementTypes (movementId) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `ExerciseMovements`
INSERT INTO ExerciseMovements (exerciseId, movementId) VALUES (1, 1), (2, 2), (3, 3);