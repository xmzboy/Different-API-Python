import requests


# Auth user
auth = ('username', 'password')

# Example params for POST and PUT requests
param_post = {"title": "Training", "description": "Morning run"}
param_put = {"title": "Training", "description": "Athletic", "done": True}

# Example GET request
resp_get = requests.get('http://127.0.0.1:5000/todo/tasks/2', auth=auth)

# Example POST request
resp_post = requests.post('http://127.0.0.1:5000/todo/tasks', json=param_post, auth=auth)

# Example PUT request
resp_put = requests.put('http://127.0.0.1:5000/todo/tasks/3', json=param_put, auth=auth)

# Example DELETE request
resp_del = requests.delete('http://127.0.0.1:5000/todo/tasks/3', auth=auth)

# Print requests results
print(resp_get.text)
print(resp_post.text)
print(resp_put.text)
print(resp_del.text)
