from typing import NewType, List, Dict, Any

InputsLayout = NewType("InputsLayout", List[List[List[Dict[str,Any]]]])

def extract_not_static_inputs_from_layout(layout: InputsLayout) -> List[Dict[str, Any]]:
    """Extract from the layouts only the inputs that can be set for task initialization"""
    inputs: List[Dict[str,Dict]] = []

    for row in layout:
        for col in row:
            for input in col:
                if input['submit'] != False or not input.get('static', False):
                    inputs.append(input)

    return inputs