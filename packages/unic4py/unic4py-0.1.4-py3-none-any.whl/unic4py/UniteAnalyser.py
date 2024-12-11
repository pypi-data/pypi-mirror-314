import base64
import io
import os
import zipfile
from oslc4py_domains_auto.AutomationRequest import AutomationRequest
from oslc4py_domains_auto.AutomationResult import AutomationResult
from oslc4py_domains_auto.ParameterInstance import ParameterInstance
from oslc4py_client.Link import Link
from oslc4py_client.OSLCPythonClient import OSLCPythonClient


class UniteAnalyser:
    def __init__(self, unite_url, compilation_port, analysis_port):
        self.url = unite_url
        self.compilation_port = compilation_port
        self.analysis_port = analysis_port

        self.compilation_client = OSLCPythonClient(unite_url, compilation_port)
        self.analysis_client = OSLCPythonClient(unite_url, analysis_port)

        self.mid_result = None
        self.pass_data = {
            "stage": 0,
            "compilation_arguments": {},
            "analysis_arguments": {}
        }

    def add_compilation_argument(self, name, value):
        self.pass_data['compilation_arguments'][name] = value

    def add_analysis_argument(self, name, value):
        self.pass_data['analysis_arguments'][name] = value

    def analyse(self):
        self.register_sut()
        self.check_sut_registration()
        self.perform_analysis()
        self.get_analysis_result()
        
        return self.all_contributions(self.mid_result)

    def register_sut(self):
        compilation_request = AutomationRequest()
        compilation_request.executes_automation_plan = Link(f"{self.url}:{self.compilation_port}/compilation/services/resources/automationPlans/0")
        compilation_request.title = "Unic python automation request"
        compilation_request.description = "Requesting SUT registration"

        for arg_name, arg_value in self.pass_data['compilation_arguments'].items():
            self.parameter(compilation_request, arg_name, arg_value)

        returned_compilation_request = self.compilation_client.post(
            "compilation/services/resources/createAutomationRequest",
            compilation_request
        )
        
        self.mid_result = returned_compilation_request
        self.pass_data['compilation_request_id'] = returned_compilation_request.identifier
        self.pass_data['stage'] = 1
        return self

    def check_sut_registration(self):
        compilation_request_id = self.pass_data['compilation_request_id']
        
        compilation_result = AutomationResult()
        self.compilation_client.poll(f"compilation/services/resources/automationResults/{compilation_request_id}", compilation_result)

        sut = self.compilation_client.get_resource(f"compilation/services/resources/sUTs/{compilation_request_id}")

        self.mid_result = sut
        self.pass_data['sut_id'] = sut.identifier
        self.pass_data['stage'] = 2
        return self

    def perform_analysis(self):
        sut_id = self.pass_data['sut_id']

        analysis_request = AutomationRequest()
        analysis_request.title = "Unic python automation request"
        analysis_request.description = "Requesting analysis"
        analysis_request.executes_automation_plan = Link(f"{self.url}:{self.analysis_port}/analysis/services/resources/automationPlans/{self.pass_data['analysis_tool']}")

        for arg_name, arg_value in self.pass_data['analysis_arguments'].items():
            self.parameter(analysis_request, arg_name, arg_value)

        self.parameter(analysis_request, "SUT", f"{self.url}:{self.compilation_port}/compilation/services/resources/sUTs/{sut_id}")

        returned_analysis_request = self.analysis_client.post(
            "analysis/services/resources/createAutomationRequest",
            analysis_request
        )

        self.mid_result = returned_analysis_request
        self.pass_data['analysis_request_id'] = returned_analysis_request.identifier
        self.pass_data['stage'] = 3
        
        return self

    def get_analysis_result(self):
        analysis_request_id = self.pass_data['analysis_request_id']

        analysis_result = AutomationResult()
        self.analysis_client.poll(f"analysis/services/resources/automationResults/{analysis_request_id}", analysis_result, None, 30, 5)

        self.mid_result = analysis_result
        self.pass_data['stage'] = 4
        self.pass_data['contributions'] = self.all_contributions(analysis_result)
        
        
        return self

    def parameter(self, resource, parameter_name, parameter_value):
        instance = ParameterInstance()
        instance.name = parameter_name
        instance.value = parameter_value
        resource.add_input_parameter(instance)

    def all_contributions(self, automation_result):
        return {contribution.title: contribution.value for contribution in automation_result.contribution}

    def get_zipped_folder(self, dir, set_build_command):
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zf.write(file_path, os.path.relpath(file_path, dir))
        
        zip_data = zip_buffer.getvalue()
        base64_encoded_zip = base64.b64encode(zip_data).decode('utf-8')
        
        build_command = None
        if set_build_command:
            if any("pom.xml" in files for _, _, files in os.walk(dir)):
                build_command = "mvn install"
            elif any("Makefile" in files for _, _, files in os.walk(dir)):
                build_command = "make"
        
        return base64_encoded_zip, build_command
    
    def input_zip(self, dir_name, dir_path, set_build_command=False):
        base64input, build_command = self.get_zipped_folder(dir_path, set_build_command=set_build_command)
        
        if build_command:
            print(f"Build command set to: {build_command}")

        return f"{dir_name}.zip\n{base64input}", build_command
