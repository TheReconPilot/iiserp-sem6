from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas as pd
import numpy as np
import os

# Filenames
courseTemplateFilename = "templates/course_template.html"
deptTemplateFilename = "templates/dept_template.html"
dataFilename = "data/mth_courses.csv"
instructorDataFilename = "data/mth_instructors.csv"
# addResourcesFilename = "addresources.csv"
deptFilename = "html/mth.html"

# Import data

def preprocessing(csv_file):
    df = pd.read_csv(csv_file, delimiter=",", header=0)  #reads the .csv file and uses 1st row as header
    df.replace(np.nan, "", regex=True, inplace=True) # replace all null values with blank
    df = df.to_dict('records')  #creates a dictionary
    return df

courses = preprocessing(dataFilename)
instData = preprocessing(instructorDataFilename)

# Merge the datasets
for course in courses:
    instructors = []
    for prof in instData:
        if prof["courseid"] == course["id"]:
            instructors.append(prof)
    course["instructors"] = instructors

# Jinja Setup
env = Environment(loader=FileSystemLoader(os.path.abspath(".")), autoescape=select_autoescape(["html"]))
courseTemplate = env.get_template(courseTemplateFilename)
deptTemplate = env.get_template(deptTemplateFilename)

# Start working
for course in courses:
    # print("course:", course)
    # print()
    course["coursehtml"] = courseTemplate.render(course=course)
    # print("courseinfo:", course["courseinfo"])

output = deptTemplate.render(courses=courses)

with open(deptFilename, "w") as outfile:
    outfile.write(output)

print("Tasked Completed Successfully!")
