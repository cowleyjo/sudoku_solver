import requests

def api_call(difficulty: str = "easy", solution: bool = True, array: bool = True):
    body = {
        "difficulty": difficulty, # "easy", "medium", or "hard" (defaults to "easy")
        "solution": solution, # True or False (defaults to True)
        "array": array # True or False (defaults to False)
    }

    headers =  {"Content-Type":"application/json"}

    response = requests.post("https://youdosudoku.com/api/", json=body, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    data = response.json()

    puzzle = data["puzzle"]
    
    return puzzle