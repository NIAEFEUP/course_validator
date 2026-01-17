import os
import csv
from tqdm import tqdm
from dotenv import load_dotenv

from sigarra import login, get_current_enrollments_api, get_course_name_scrapping, get_current_enrollments_scrapping
from configuration import (
    ACCEPTED_COURSES, 
    EMAIL_COL_INDEX, 
    INPUT_FILE, 
    FILTERED_OUTPUT_FILE, 
    INVALID_VOTES_FILE
)

load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
cookies = login(username, password)

def process_votes():
    unique_votes_to_process = {}

    csv_file = open(INPUT_FILE, 'r', encoding='utf-8')
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for row in csv_reader:
        email = row[EMAIL_COL_INDEX]
        up_number = email.split('@')[0][2:]
        unique_votes_to_process[up_number] = row

    csv_file.close()

    valid_count = 0
    invalid_count = 0
    all_intruders_courses = set()
    intruders = {} #up_number -> [course_ids]

    with open(FILTERED_OUTPUT_FILE, 'w', newline='', encoding='utf-8') as res_file, \
         open(INVALID_VOTES_FILE, 'w', newline='', encoding='utf-8') as inv_file:
        
        results_writer = csv.writer(res_file, delimiter=',')
        invalid_writer = csv.writer(inv_file, delimiter=',')
        
        results_writer.writerow(header)
        invalid_writer.writerow(header + ['enrollments'])
        
        print(f'Processing {len(unique_votes_to_process)} unique votes...')
        for up_number, row in tqdm(unique_votes_to_process.items(), desc="Checking Enrollments"):
            student_enrollments = get_current_enrollments_scrapping(up_number, cookies)
            
            if any(course in student_enrollments for course in ACCEPTED_COURSES):
                results_writer.writerow(row)
                valid_count += 1
            else:
                row.append(student_enrollments)
                invalid_writer.writerow(row)
                invalid_count += 1
                intruders[up_number] = student_enrollments
                for course in student_enrollments:
                    all_intruders_courses.add(course)

    print("-" * 30)
    print(f"Total Unique Votes: {len(unique_votes_to_process)}")
    print(f"Valid Votes: {valid_count}")
    print(f"Invalid (Intruders): {invalid_count}")

    course_names = {}
    for course_code in all_intruders_courses:
        course_name = get_course_name_scrapping(course_code)
        course_names[course_code] = course_name
    
    print("\nIntruders courses:")
    for up_number, courses in intruders.items():
        course_list = [f"{code} - {course_names[code]}" for code in courses]
        print(f"UP{up_number}: " + ", ".join(course_list))

if __name__ == "__main__":
    process_votes()