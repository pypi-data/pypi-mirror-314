import inspect

from lesscode_flask.utils.swagger.swagger_template import get_response_template, get_header_template, get_request_body, \
    split_doc


def generate_openapi_spec(app):
    paths = {}

    for rule in app.url_map.iter_rules():
        if rule.endpoint == 'static':
            continue
        methods = rule.methods - {'HEAD', 'OPTIONS'}
        view_func = app.view_functions[rule.endpoint]
        description = view_func.__doc__
        if hasattr(view_func, '_title'):
            summary = view_func._title
        else:
            summary = ""
        operation = {}
        path = rule.rule
        for method in methods:
            method_ = method.lower()
            inter_desc, param_desc_dict, return_desc = split_doc(rule, app)
            operation_dict = {
                # "summary": inter_desc,
                "summary": summary or inter_desc,
                "tags": [rule.endpoint.split('.')[0]],
                # "description": f"Description for {method} {rule.rule}",
                "description": description,
                "responses": get_response_template()
            }

            if method_ == "post":
                path = replace_symbol(path)
                parameters = get_header_template()
                if "{" in path and "}" in path:
                    path_params = extract_path_parameters(rule, view_func, param_desc_dict)
                    parameters = parameters + path_params
                    body = extract_post_body(view_func, not_allow_list=[param["name"] for param in path_params],
                                             param_desc_dict=param_desc_dict)
                else:
                    body = extract_post_body(view_func, param_desc_dict=param_desc_dict)

                operation_dict["parameters"] = parameters
                operation_dict["requestBody"] = body

            else:
                path = replace_symbol(path)
                parameters = get_header_template() + extract_path_parameters(rule, view_func,
                                                                             param_desc_dict) + extract_get_parameters(
                    rule,
                    view_func, param_desc_dict)
                operation_dict["parameters"] = parameters

            operation[method_] = operation_dict

        paths[path] = operation
    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Auto-Generated API",
            "version": "1.0.0"
        },
        "tags": [{"name": k} for k in app.blueprints],
        "paths": paths
    }
    return openapi_spec


# 替换最后一个<和>
def replace_symbol(path):
    path = path[::-1]
    path = path.replace("<", "{", 1)
    path = path.replace(">", "}", 1)
    return path[::-1]


def get_sample_data(type):
    if type == "dict":
        return {"sample": "sample"}
    elif type == "list":
        return ["sample"]
    elif type == "int":
        return 0
    else:
        return ""


def get_params_type(param):
    type = param.annotation.__name__
    if type == "FileStorage":
        return "string"
    else:
        return type


def extract_post_body(view_func, not_allow_list=None, param_desc_dict=None):
    if param_desc_dict is None:
        param_desc_dict = {}
    body = {}
    # 提取查询参数和表单参数
    sig = inspect.signature(view_func)
    # 如果_request_type == "json 则是json结构，否则都是form-data结构
    if hasattr(view_func, "_request_type") and view_func._request_type == "urlencoded":
        request_type = "application/x-www-form-urlencoded"
    elif hasattr(view_func, "_request_type") and view_func._request_type == "form-data":
        request_type = "multipart/form-data"
    elif hasattr(view_func, "_request_type") and view_func._request_type == "json-data":
        request_type = "application/json"
    else:
        request_type = "application/json"

    required = []
    for arg, param in sig.parameters.items():
        param_info = {
            "type": get_params_type(param),
            "description": param_desc_dict[arg] if param_desc_dict.get(arg) else f"Path parameter {arg}",
        }
        # 如果默认值是空，则是必填参数
        if param.default is inspect.Parameter.empty:
            if (not_allow_list and arg not in not_allow_list) or not not_allow_list:
                required.append(arg)

            param_info["example"] = get_sample_data(param.annotation.__name__)
        else:
            param_info["default"] = param.default
            if param.default is not None:
                param_info["example"] = param.default
            else:
                param_info["example"] = get_sample_data(param.annotation.__name__)
        # 如果参数类型是FileStorage 则swagger中format为binary 显示导入文件
        if param.annotation.__name__ == "FileStorage":
            param_info["format"] = "binary"
        if (not_allow_list and arg not in not_allow_list) or not not_allow_list:
            body[arg] = param_info

    return get_request_body(body, required, request_type)


def extract_path_parameters(rule, view_func, param_desc_dict=None):
    if param_desc_dict is None:
        param_desc_dict = {}
    parameters = []
    # 提取路径参数
    for arg in rule.arguments:
        parameters.append({
            "name": arg,
            "in": "path",
            "required": True,
            "description": param_desc_dict[arg] if param_desc_dict.get(arg) else f"Path parameter {arg}",
            "schema": {
                "type": "integer" if "int" in str(view_func.__annotations__.get(arg, '')) else "string"
            }
        })
    return parameters


def extract_get_parameters(rule, view_func, param_desc_dict=None):
    if param_desc_dict is None:
        param_desc_dict = {}
    parameters = []
    # 提取查询参数和表单参数
    sig = inspect.signature(view_func)
    for arg, param in sig.parameters.items():
        if arg not in rule.arguments:
            param_info = {
                "name": arg,
                "in": "query",
                "description": param_desc_dict[arg] if param_desc_dict.get(arg) else f"Path parameter {arg}",
                "required": param.default is inspect.Parameter.empty,
                "schema": {
                    "type": "string"  # 默认设置为字符串类型，具体可根据需要调整
                }
            }
            if param.default != inspect.Parameter.empty:
                param_info["schema"]["default"] = param.default
            parameters.append(param_info)
    return parameters
