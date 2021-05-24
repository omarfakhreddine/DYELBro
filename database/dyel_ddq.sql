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
  trainingType varchar(255) NOT NULL,
  PRIMARY KEY (trainingType)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `TrainingTypes`
INSERT INTO TrainingTypes (trainingType) VALUES ('cardio'), ('endurance'), ('anaerobic');


--
-- Table structure for table `ExerciseTrainings`
--

DROP TABLE IF EXISTS ExerciseTrainings;

CREATE TABLE ExerciseTrainings (
  exerciseId int(11) NOT NULL DEFAULT 0, -- do we  make null or autoincrement?
  trainingType varchar(255) NOT NULL DEFAULT 0,
  PRIMARY KEY (exerciseId, trainingType),
  CONSTRAINT ExerciseTrainings_fk_1 FOREIGN KEY (exerciseId) REFERENCES Exercises (exerciseId),
  CONSTRAINT ExerciseTrainings_fk_2 FOREIGN KEY (trainingType) REFERENCES TrainingTypes (trainingType)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `ExerciseTrainings`
INSERT INTO ExerciseTrainings (exerciseId, trainingType) VALUES (1, 'cardio'), (2, 'endurance'), (3, 'anaerobic');



--
-- Table structure for table `MuscleGroups`
--

DROP TABLE IF EXISTS MuscleGroups;

CREATE TABLE MuscleGroups (
  muscleGroup varchar(255) NOT NULL,
  PRIMARY KEY (muscleGroup)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `MuscleGroups`
INSERT INTO MuscleGroups (muscleGroup) VALUES ('biceps'), ('triceps'), ('quads');


--
-- Table structure for table `ExerciseMuscles`
--

DROP TABLE IF EXISTS ExerciseMuscles;

CREATE TABLE ExerciseMuscles (
  exerciseId int(11) NOT NULL DEFAULT 0, -- do we  make null or autoincrement?
  muscleGroup varchar(255) NOT NULL DEFAULT 0,
  PRIMARY KEY (exerciseId, muscleGroup),
  CONSTRAINT ExerciseMuscles_fk_1 FOREIGN KEY (exerciseId) REFERENCES Exercises (exerciseId),
  CONSTRAINT ExerciseMuscles_fk_2 FOREIGN KEY (muscleGroup) REFERENCES MuscleGroups (muscleGroup)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `ExerciseMuscles`
INSERT INTO ExerciseMuscles (exerciseId, muscleGroup) VALUES (1, 'biceps'), (2, 'triceps'), (3, 'quads');

--
-- Table structure for table `MuscleGroups`
--

DROP TABLE IF EXISTS MovementTypes;

CREATE TABLE MovementTypes (
  movementType varchar(255) NOT NULL,
  PRIMARY KEY (movementType)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `MovementTypes`
INSERT INTO MovementTypes (movementType) VALUES ('push'), ('pull'), ('hinge');


--
-- Table structure for table `ExerciseMovements`
--

DROP TABLE IF EXISTS ExerciseMovements;

CREATE TABLE ExerciseMovements (
  exerciseId int(11) NOT NULL DEFAULT 0, -- do we  make null or autoincrement?
  movementType varchar(255) NOT NULL DEFAULT 0,
  PRIMARY KEY (exerciseId, movementType),
  CONSTRAINT ExerciseMovements_fk_1 FOREIGN KEY (exerciseId) REFERENCES Exercises (exerciseId),
  CONSTRAINT ExerciseMovements_fk_2 FOREIGN KEY (movementType) REFERENCES MovementTypes (movementType)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `ExerciseMovements`
INSERT INTO ExerciseMovements (exerciseId, movementType) VALUES (1, 'push'), (2, 'pull'), (3, 'hinge');