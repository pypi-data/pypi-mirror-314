"""Methods to handle labels formatting

KILI example

"categories": [
    {
        "name": "PARENT"
    }
],
"children": {
    "CLASSIFICATION_JOB": {
        "categories": [
            {
                "confidence": 100,
                "name": "ENFANT_1"
            }
        ]
    },
    "CLASSIFICATION_JOB_0": {
        "categories": [
            {
                "children": {
                    "TRANSCRIPTION_JOB_0": {
                        "text": "test 2"
                    }
                },
                "confidence": 100,
                "name": "ENFANT_2"
            },
            {
                "children": {
                    "TRANSCRIPTION_JOB": {
                        "text": "test"
                    }
                },
                "confidence": 100,
                "name": "ENFANT_1"
            }
        ]
    }
},

"""

from typing import List, Dict


def extract_main_labels(labels : Dict) -> List[Dict] :
    main_labels = []
    for list in labels:
        value = labels[list]
        for label in value['labels']:
            main_labels.append({
                "id" : label["id"],
                "name" : label["name"],
                "list" : list
            })
    
    return main_labels

def find_label_in_main_list(label_id : str, project_configuration : Dict) -> List[Dict] :
    mainLists = project_configuration["metadata"]["labelOptions"]["mainLists"]
    availableLabels = project_configuration["metadata"]["labelOptions"]["availableLabels"]
    for mlist in mainLists:
        mainListKey = mlist["name"]
        for datalistKey in mlist["keys"]:
            for label in availableLabels.get(datalistKey, []):
                if label["id"] == label_id:
                    return {
                        mainListKey : {
                            "labels" : [
                                {
                                    "id": label["id"],
                                    "name": label["name"]
                                }
                            ]
                        }
                    }
    return None