import os
import re

import plyj
from plyj.model import MethodDeclaration
from plyj.parser import Parser
class JavaCodeAnalyzer:
    def __init__(self, project_path):
        self.project_path = project_path

    def get_classes_info(self, java_code):
        # Java kodunu analiz etmek için Parser oluştur
        parser = Parser()

        # Java kodunu parse et
        tree = parser.parse_string(java_code)

        class_info_list = []

        # Her bir sınıf için bilgileri topla
        for type_declaration in tree.type_declarations:
            # Sınıf adını al
            class_name = type_declaration.name

            # Sınıf gövdesini al
            class_body = type_declaration.body

            # Sınıfın metod isimlerini topla
            method_names = [method_declaration.name for method_declaration in class_body if isinstance(method_declaration, MethodDeclaration)]

            class_info = {
                'class_name': class_name,
                'method_names': method_names
            }

            class_info_list.append(class_info)

        return class_info_list

    def analyze_project(self):

        java_files = [f for f in self.list_files(self.project_path, '.java')]

        result_list = []

        for java_file in java_files:
            with open(java_file, 'r', encoding='utf-8') as file:
                java_code = file.read()
                class_data = self.get_classes_info(java_code)
                result_list.append(class_data)

        return result_list

    def list_files(self, directory, extension):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(extension):
                    yield os.path.join(root, file)

