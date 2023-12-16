import os
import re

class JavaCodeAnalyzer:
    def __init__(self, project_path):
        self.project_path = project_path

    def analyze_project(self):

        java_files = [f for f in self.list_files(self.project_path, '.java')]

        result_list = []

        for java_file in java_files:
            with open(java_file, 'r', encoding='utf-8') as file:
                java_code = file.read()
                class_data = self.analyze_java_code(java_code)
                result_list.append(class_data)

        return result_list

    def list_files(self, directory, extension):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(extension):
                    yield os.path.join(root, file)

    def analyze_java_code(self, java_code):

        class_pattern = re.compile(r'class\s+([\w_$]+)\s*\{')
        method_pattern = re.compile(r'(\w+)\s+(\w+)\s*\([^)]*\)\s*\{')

        class_count = len(re.findall(class_pattern, java_code))
        if class_count > 1:
            return None
        else:

            class_data = {}
            current_class = None

            for match in re.finditer(class_pattern, java_code):
                class_name = match.group(1)
                current_class = {'methods': []}
                class_data[class_name] = current_class

                for method_match in re.finditer(method_pattern, java_code):
                    method_name = method_match.group(2)
                    current_class['methods'].append(method_name)

        return class_data

