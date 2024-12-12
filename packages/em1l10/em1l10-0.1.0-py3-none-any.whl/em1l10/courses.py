class Course:
	
	def __init__(self, name, duration, link):
	
		self.name = name
		self.duration = duration
		self.link = link
	
	def __repr__(self):
		return f"{self.name}, {self.duration}, {self.link}"
		
courses = [
	Course("Introducción a linux", 15, "X"),
	Course("Personalización de Linux", 3, "Y"),
	Course("Introducción al Hacking", 53, "Z")
]


def list_courses():

	for course in courses:
		print(course)

def search_course_by_name(name):

	for course in courses:

		if course.name == name:
			return course
	return None
