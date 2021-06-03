# from collections import defaultdict
import operator
import itertools



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
    #print(tuple(final))
    print(final)


def getRow(row):
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
    #print(tuple(final))
    print(final)






#    dd = defaultdict(list)
#
#    for dicts in tupleOfDicts:
#        for key, value in dicts:
#            if key == 'exerciseId':
#                #print(dict[key])
#                for key, value in dicts.items():
#                    #print(dicts[key])
#                    dd[key].append(value)
#
#
#
#    print(dd)
#    print("check")
#








results_all = (
{'exerciseId': 1, 'exerciseName': 'bench press', 'trainingType': 'cardio', 'movementType': 'push', 'muscleGroup': 'biceps'}, 
{'exerciseId': 4, 'exerciseName': 'cry', 'trainingType': 'cardio', 'movementType': 'push', 'muscleGroup': 'biceps'}, 
{'exerciseId': 4, 'exerciseName': 'cry', 'trainingType': 'cardio', 'movementType': 'push', 'muscleGroup': 'triceps'}, 
{'exerciseId': 4, 'exerciseName': 'cry', 'trainingType': 'endurance', 'movementType': 'push', 'muscleGroup': 'biceps'}, 
{'exerciseId': 4, 'exerciseName': 'cry', 'trainingType': 'endurance', 'movementType': 'push', 'muscleGroup': 'triceps'}, 
{'exerciseId': 4, 'exerciseName': 'cry', 'trainingType': 'cardio', 'movementType': 'pull', 'muscleGroup': 'biceps'}, 
{'exerciseId': 4, 'exerciseName': 'cry', 'trainingType': 'cardio', 'movementType': 'pull', 'muscleGroup': 'triceps'}, 
{'exerciseId': 2, 'exerciseName': 'deadlift', 'trainingType': 'endurance', 'movementType': 'pull', 'muscleGroup': 'triceps'}, 
{'exerciseId': 4, 'exerciseName': 'cry', 'trainingType': 'endurance', 'movementType': 'pull', 'muscleGroup': 'biceps'}, 
{'exerciseId': 4, 'exerciseName': 'cry', 'trainingType': 'endurance', 'movementType': 'pull', 'muscleGroup': 'triceps'}, 
{'exerciseId': 3, 'exerciseName': 'squat', 'trainingType': 'anaerobic', 'movementType': 'hinge', 'muscleGroup': 'quads'}
)

row = {'exerciseId': 1, 'exerciseName': 'cry', 'trainingType': 'cardio', 'movementType': 'push', 'muscleGroup': 'biceps'}

x = extract(results_all)
print(x)

y = getRow(row)
print(y)