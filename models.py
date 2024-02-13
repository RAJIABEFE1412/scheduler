import prettytable as prettytable
import random as rnd

NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1
POPULATION_SIZE = 9
class Data:
    # Here we declare the classroom number and the maximum student capacity of the students
    ROOMS = [["33-501", 70], ["34-203", 35]]

    # Here we declare the meeting times, in which a class can hold, here MT1, MT2 means meeting 1, meeting 2 and so on. MWF, TTH etc. means Monday, Wednesday, Friday
    MEETING_TIMES = []

    # ["MT1", "MWF 09:00 - 10:00"],
    #                  ["MT2", "MWF 10:00 - 11:00"],
    #                  ["MT3", "MWF 11:00 - 12:00"],
    #                  ["MT4", "MWF 13:00 - 14:00"],
    #                  ["MT5", "MWF 14:00 - 15:00"],
    #                  ["MT6", "MWF 15:00 - 16:00"],
    #                  ["MT7", "MWF 16:00 - 17:00"],
    #                  ["MT8", "TTH 09:00 - 10:00"],
    #                  ["MT9", "TTH 10:00 - 11:00"],
    #                  ["MT10", "TTH 11:00 - 12:00"],
    #                  ["MT11", "TTH 13:00 - 14:00"],
    #                  ["MT12", "TTH 14:00 - 15:00"],
    #                  ["MT13", "TTH 15:00 - 16:00"],
    #                  ["MT14", "TTH 16:00 - 17:00"]

    # Here we declare the professors name
    INSTRUCTORS = []
    # ["AP1", "Ms. Jasleen Kaur"],
    #                ["AP2", "Mr. Tarun"],
    #                ["AP3", "Ms. Suruchi Talwani"],
    #                ["AP4", "Mr. Arun Kochar"],
    #                ["AP5", "Ms. Priya"],
    #                ["AP6", "Dr. Priyanka Chawla"],
    #                ["AP7", "Mr. Sudha Shankar Prasad"],
    #                ["AP8", "Mr. Pankaj Kumar Keshri"]

    # Defining Constructor
    def __init__(self, json_data):
        self._rooms = []
        self._courses = []
        self._depts = []
        self._meetingTimes = []
        self._instructors = []


        for room_info in json_data.get("rooms", []):
            self._rooms.append(Room(room_info["number"], room_info["seatingCapacity"]))

        for meeting_time_info in json_data.get("meetingTimes", []):
            self._meetingTimes.append(MeetingTime(meeting_time_info["id"], meeting_time_info["time"]))

        for instructor_info in json_data.get("instructors", []):
            self._instructors.append(Instructor(instructor_info["id"], instructor_info["name"]))


# 

        # for i in range(0, 9):
        #     a = "Enter the course for index " + str(i+1)+" : "
        #     course = input(a)
        #     time = input("Enter the meeting time for course for index " + str(i+1)+" : ")

        #     self.MEETING_TIMES.append([course, time])

        # for i in range(0, 9):
        #     course = input("Enter the lecturer id for index " + str(i+1)+" : ")
        #     time = input("Enter the lecturer name for index " + str(i+1)+" : ")

        #     self.INSTRUCTORS.append([course, time])

        # for i in range(0, len(self.INSTRUCTORS)):
        #     self._instructors.append(Instructor(
        #         self.INSTRUCTORS[i][0], self.INSTRUCTORS[i][1]))
        # Inside the __init__ method of the Data class

        for i in range(0, 9):
            time = json_data.get("courses", [])[i].get("code", "")
            is_practical = json_data.get("courses", [])[i].get("isPractical", "")
            max_students = 35 if is_practical.lower() == "true" or is_practical.lower() == 't' else 70

            self._courses.append(Course("C" + str(i + 1), time, [self._instructors[i]], max_students))

        for i in range(0, 9):
            dept = json_data.get("courses", [])[i].get("department", "")
            
            for j in self._depts:
                if j.get_name().lower() == dept.lower():
                    j.set_courses(self._courses[i])
                    break
            else:
                self._depts.append(Department(dept, [self._courses[i]]))

        # for i in range(0, 9):

        #     time = input("Enter the course code " + str(i+1)+" : ")
        #     isPractical = input(
        #         "Is this course a Practical course? True/False " + str(i+1)+" : ")
        #     if(isPractical.lower() == "True" or isPractical.lower() == 't'):
        #         isPractical = 35
        #     else:
        #         isPractical = 70

        #     self._courses.append(Course("C"+str(i+1), time,
        #                   [self._instructors[i]], isPractical))

        # for i in range(0, len(self.ROOMS)):
        #     self._rooms.append(Room(self.ROOMS[i][0], self.ROOMS[i][1]))

        # for i in range(0, len(self.MEETING_TIMES)):
        #     self._meetingTimes.append(MeetingTime(
        #         self.MEETING_TIMES[i][0], self.MEETING_TIMES[i][1]))
        
        # for i in range(0, 9):
        #     dept = input("Enter dept for "+str(self._courses[0].get_name())+" : ")
            
        #     for j in self._depts:
        #         if(j.get_name().lower() == dept.lower()):
        #             j.set_courses(self._courses[i])
        #             break
        #         elif( j is self._depts[-1]):
        #             self._depts.append(dept, [self._courses[i]])
        #             break
        #         else:
        #             continue
      

        self._numberOfClasses = 0
        for i in range(0, len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_courses())

    def get_rooms(self): return self._rooms
    def get_instructors(self): return self._instructors
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_meetingTimes(self): return self._meetingTimes
    def get_numberOfClasses(self): return self._numberOfClasses




class Schedule:
    def __init__(self,data):
        self._data = data
        self._classes = []
        self._numbOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self): return self._numbOfConflicts

    def get_fitness(self):
        if (self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        depts = self._data.get_depts()
        for i in range(0, len(depts)):
            courses = depts[i].get_courses()
            for j in range(0, len(courses)):
                newClass = Class(self._classNumb, depts[i], courses[j])
                self._classNumb += 1
                newClass.set_meetingTime(self._data .get_meetingTimes(
                )[rnd.randrange(0, len(self._data.get_meetingTimes()))])
                newClass.set_room(
                    self._data.get_rooms()[rnd.randrange(0, len(self._data.get_rooms()))])
                newClass.set_instructor(courses[j].get_instructors(
                )[rnd.randrange(0, len(courses[j].get_instructors()))])
                self._classes.append(newClass)
        return self

    def calculate_fitness(self):
        self._numbOfConflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            if (classes[i].get_room().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._numbOfConflicts += 1
            for j in range(0, len(classes)):
                if (j >= i):
                    if (classes[i].get_meetingTime() == classes[j].get_meetingTime() and
                            classes[i].get_id() != classes[j].get_id()):
                        if (classes[i].get_room() == classes[j].get_room()):
                            self._numbOfConflicts += 1
                        if (classes[i].get_instructor() == classes[j].get_instructor()):
                            self._numbOfConflicts += 1
        return 1 / ((1.0*self._numbOfConflicts + 1))

    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes)-1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes)-1])
        return returnValue


class Population:
    def __init__(self, size, data):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(0, size):
            self._schedules.append(Schedule(data).initialize())

    def get_schedules(self): return self._schedules


class GeneticAlgorithm:
    def evolve(self, population, data): return self._mutate_population(
        self._crossover_population(population, data))
        

    def _crossover_population(self, pop, data):
        self.data = data
        crossover_pop = Population(0, self.data)
        
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[
                0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[
                0]
            crossover_pop.get_schedules().append(
                self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule(self.data).initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if (rnd.random() > 0.5):
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule(self.data).initialize()
        for i in range(0, len(mutateSchedule.get_classes())):
            if(MUTATION_RATE > rnd.random()):
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0,self.data)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(
                pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Course:
    def __init__(self, number, name, instructors, maxNumbOfStudents):
        self._number = number
        self._name = name
        self._maxNumbOfStudents = maxNumbOfStudents
        self._instructors = instructors

    def get_number(self): return self._number

    def get_name(self): return self._name

    def get_instructors(self): return self._instructors

    def get_maxNumbOfStudents(self): return self._maxNumbOfStudents

    def __str__(self): return self._name


class Instructor:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def get_id(self): return self._id

    def get_name(self): return self._name

    def __str__(self): return self._name


class Room:
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity

    def get_number(self): return self._number

    def get_seatingCapacity(self): return self._seatingCapacity


class MeetingTime:
    def __init__(self, id, time):
        self._id = id
        self._time = time

    def get_id(self): return self._id

    def get_time(self): return self._time


class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses

    def get_name(self): return self._name

    def set_courses(self, c): self._courses.append(c)

    def get_courses(self): return self._courses


class Class:
    def __init__(self, id, dept, course):
        self._id = id
        self._dept = dept
        self._course = course
        self._instructor = None
        self._meetingTime = None
        self._room = None

    def get_id(self): return self._id

    def get_dept(self): return self._dept

    def get_course(self): return self._course

    def get_instructor(self): return self._instructor

    def get_meetingTime(self): return self._meetingTime

    def get_room(self): return self._room

    def set_instructor(self, instructor): self._instructor = instructor

    def set_meetingTime(self, meetingTime): self._meetingTime = meetingTime

    def set_room(self, room): self._room = room

    def __str__(self):
        return str(self._dept.get_name()) + "," + str(self._course.get_number()) + "," + \
            str(self._room.get_number()) + "," + str(self._instructor.get_id()
                                                     ) + "," + str(self._meetingTime.get_id())
