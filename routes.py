# routes.py
from flask import Blueprint, jsonify, request, make_response, send_file
from models import Data, Population, GeneticAlgorithm
from utils import  DisplayMgr
import base64
from PIL import Image, ImageDraw, ImageFont


generate_schedule = Blueprint('generate_schedule', __name__)

POPULATION_SIZE = 9

@generate_schedule.route('/', methods=['GET'])
def test():
    return jsonify({"message":"sample"})


@generate_schedule.route('/schedule', methods=['POST'])
def generate_schedule_route():
    # try:
        print("bcvhbjnk")
        json_data = request.get_json()
        data = Data(json_data)
        
        display_mgr = DisplayMgr(data)
        display_mgr.print_available_data()

        generation_number = 0
        print("\n> Generation # " + str(generation_number))
        
        population = Population(POPULATION_SIZE, data)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)

        display_mgr.print_generation(population)
        display_mgr.print_schedule_as_table(population.get_schedules()[0])

        genetic_algorithm = GeneticAlgorithm()
        
        while population.get_schedules()[0].get_fitness() != 1.0:
            generation_number += 1
            print("\n> Generation # " + str(generation_number))
            population = genetic_algorithm.evolve(population, data)
            population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
            display_mgr.print_generation(population)
            display_mgr.print_schedule_as_table(population.get_schedules()[0])

        # Generate a PrettyTable from the final schedule
        final_schedule = population.get_schedules()[0]
 # Assuming 'table_content' is a list of strings
        table_content = []
        for cls in final_schedule.get_classes():
            row = {
                "dept_name": cls.get_dept().get_name(),
                "course_number": cls.get_course().get_number(),
                "room_number": cls.get_room().get_number(),
                "instructor_id": cls.get_instructor().get_name(),
                "meeting_time_id": cls.get_meetingTime().get_time()
            }
            table_content.append(row)

        # Convert the list to JSON
        json_data = {"schedule": table_content}

        # Now 'json_data' contains the JSON representation of the schedule


        # Generate base64-encoded image from the PrettyTable

        return jsonify(json_data)
    
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500


