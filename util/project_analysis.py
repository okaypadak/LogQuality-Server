import os

class JavaClass:
    def __init__(self, name):
        self.name = name
        self.methods = []

    def add_method(self, method_name):
        self.methods.append(method_name)

def extract_methods_in_classes(file_path):
    inside_class = False
    classes = []
    current_class = None

    with open(file_path, 'r') as java_file:
        for line in java_file:
            line = line.strip()

            if line.startswith("class "):
                if current_class:
                    classes.append(current_class)
                class_name = line.split()[1].split('{')[0]
                current_class = JavaClass(class_name)
                inside_class = True
            elif inside_class and line.startswith("}"):
                inside_class = False
            elif inside_class and ("public" in line or "private" in line) and "(" in line and ")" in line:
                method_name = line.split('(')[0].split()[-1]
                current_class.add_method(method_name)

    if current_class:
        classes.append(current_class)

    return classes

def list_methods_in_all_classes(project_directory):
    for root, dirs, files in os.walk(project_directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                classes = extract_methods_in_classes(file_path)
                for java_class in classes:
                    print(f'Class: {java_class.name}')
                    for method_name in java_class.methods:
                        print(f'\tMethod: {method_name}')

project_directory = '/path/to/your/java/project'  # Java proje dizinini buraya ekleyin

list_methods_in_all_classes(project_directory)
