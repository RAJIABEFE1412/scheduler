from prettytable import prettytable 
from PIL import Image, ImageDraw, ImageFont
import io

import matplotlib, matplotlib.pyplot as plt
import base64

matplotlib.use('Agg') 

class DisplayMgr:

    def __init__(self,data):
        self.data = data

    def print_available_data(self):
        print("> All Availableself.data")
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()
    


    def print_dept(self):
        depts =self.data.get_depts()
        availableDeptsTable = prettytable.PrettyTable(['Dept', 'Courses'])
        for i in range(0, len(depts)):
            courses = depts.__getitem__(i).get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row(
                [depts.__getitem__(i).get_name(), tempStr])
        print(availableDeptsTable)

    def print_course(self):
        availableCoursesTable = prettytable.PrettyTable(
            ['Id', 'Course code', 'Max no. of students', 'Instructors'])
        courses =self.data.get_courses()
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = ""
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + ", "
            tempStr += instructors[len(instructors) - 1].__str__()
            availableCoursesTable.add_row(
                [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_maxNumbOfStudents()), tempStr])
        print(availableCoursesTable)

    def print_instructor(self):
        availableInstructorsTable = prettytable.PrettyTable(
            ['Id', 'Instructor'])
        instructors =self.data.get_instructors()
        for i in range(0, len(instructors)):
            availableInstructorsTable.add_row(
                [instructors[i].get_id(), instructors[i].get_name()])
        print(availableInstructorsTable)

    def print_room(self):
        availableRoomsTable = prettytable.PrettyTable(
            ['Room no.', 'Max seating capacity'])
        rooms =self.data.get_rooms()
        for i in range(0, len(rooms)):
            availableRoomsTable.add_row(
                [str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        print(availableRoomsTable)

    def print_meeting_times(self):
        availableMeetingTimeTable = prettytable.PrettyTable(
            ['Id', 'Meeting Time'])
        meetingTimes =self.data.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            availableMeetingTimeTable.add_row(
                [meetingTimes[i].get_id(), meetingTimes[i].get_time()])
        print(availableMeetingTimeTable)

    def print_generation(self, population):
        table1 = prettytable.PrettyTable(
            ['Schedule no.', 'Fitness', 'No. of conflicts', 'Classes [dept,class,room,instructor,meeting-time]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i), round(schedules[i].get_fitness(
            ), 3), schedules[i].get_numbOfConflicts(), schedules[i].__str__()])
        print(table1)
        return table1

    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(['Class no.', 'Dept', 'Course (number, max no. of students)',
                                        'Room (Capacity)', 'Instructor (Id)',  'Meeting Time (Id)'])
        for i in range(0, len(classes)):
            table.add_row([str(i), classes[i].get_dept().get_name(), classes[i].get_course().get_name() + " (" +
                           classes[i].get_course().get_number() + ", " +
                           str(classes[i].get_course(
                           ).get_maxNumbOfStudents()) + ")",
                           classes[i].get_room().get_number(
            ) + " (" + str(classes[i].get_room().get_seatingCapacity()) + ")",
                classes[i].get_instructor().get_name(
            ) + " (" + str(classes[i].get_instructor().get_id()) + ")",
                classes[i].get_meetingTime().get_time() + " (" + str(classes[i].get_meetingTime().get_id()) + ")"])
        print(table)
        return table.get_string()


