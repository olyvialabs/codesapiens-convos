import os

import escodegen
import esprima


def find_files(directory):
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.js'):
                files_list.append(os.path.join(root, file))
    return files_list


def extract_functions(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()
        functions = {}
        tree = esprima.parseScript(source_code)
        for node in tree.body:
            if node.type == 'FunctionDeclaration':
                func_name = node.id.name if node.id else '<anonymous>'
                functions[func_name] = escodegen.generate(node)
            elif node.type == 'VariableDeclaration':
                for declaration in node.declarations:
                    if declaration.init and declaration.init.type == 'FunctionExpression':
                        func_name = declaration.id.name if declaration.id else '<anonymous>'
                        functions[func_name] = escodegen.generate(
                            declaration.init)
                    # this was manually added, not sure if it's correct
                    elif declaration.init:
                        var_name = declaration.id.name
                        var_value = escodegen.generate(declaration.init)
                        functions[var_name] = var_value
            elif node.type == 'ClassDeclaration':
                for subnode in node.body.body:
                    if subnode.type == 'MethodDefinition':
                        func_name = subnode.key.name
                        functions[func_name] = escodegen.generate(
                            subnode.value)
                    elif subnode.type == 'VariableDeclaration':
                        for declaration in subnode.declarations:
                            if declaration.init and declaration.init.type == 'FunctionExpression':
                                func_name = declaration.id.name if declaration.id else '<anonymous>'
                                functions[func_name] = escodegen.generate(
                                    declaration.init)
        return functions


def extract_modules(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()
        modules = []
        tree = esprima.parseScript(source_code, {'sourceType': 'module'})
        for node in tree.body:
            # For ES6 modules
            if node.type == 'ImportDeclaration':
                modules.append(node.source.value)
            # For CommonJS modules
            elif node.type == 'CallExpression' and node.callee.name == 'require':
                modules.append(node.arguments[0].value)
        return modules


def extract_classes(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()
        classes = {}
        tree = esprima.parseScript(source_code)
        for node in tree.body:
            if node.type == 'ClassDeclaration':
                class_name = node.id.name
                function_names = []
                for subnode in node.body.body:
                    if subnode.type == 'MethodDefinition':
                        function_names.append(subnode.key.name)
                classes[class_name] = ", ".join(function_names)
    return classes


def extract_functions_and_classes(directory):
    files = find_files(directory)
    functions_dict = {}
    classes_dict = {}
    modules_dict = {}
    for file in files:
        functions = extract_functions(file)
        if functions:
            functions_dict[file] = functions
        classes = extract_classes(file)
        if classes:
            classes_dict[file] = classes
        modules = extract_modules(file)
        if modules:
            modules_dict[file] = modules

    return functions_dict, classes_dict  # , modules_dict
