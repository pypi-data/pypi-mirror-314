import requests, sys, json, base64
from urllib.parse import quote

base_parameters={
    "api-version":"7.1-preview.1"
}

def encode_token(TOKEN=str) -> str:
    credenciales = f"Basic:{TOKEN}"
    credenciales_base64 = base64.b64encode(credenciales.encode()).decode('utf-8')
    return credenciales_base64

def actualizar_json(base, actualizacion):
    for k, v in actualizacion.items():
        base[k] = actualizar_json(base.get(k, {}), v) if isinstance(v, dict) else v
    return base

def create_pr(API_URL=str, PROJECT=str, TOKEN=str, REPO_ID=str, sourceRefName=str, targetRefName=str, pr_title=str, headers=object|None, data=object|None, params=object|None) -> object:
    """
    Creates a Pull Request (PR) in a specified repository.

    Args:
        API_URL (str): Base URL of the API for creating PRs.
        PROJECT (str): Name of the project where the PR will be created.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR will be created.
        data (dict): Additional data for creating the PR.
        headers (dict): Additional headers for creating the PR.
        params (dict): Additional parameters for creating the PR.
        sourceRefName (str): Name of the source branch for the PR.
        targetRefName (str): Name of the target branch for the PR.
        pr_title (str): Title of the Pull Request.

    Returns:
        object: Dictionary with information about the success or failure of the PR creation, including function code and PR details.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "lastMergeSourceCommit": <último_commit_de_la_fusión>,
                "pullRequestId": <ID_del_PR>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_error>
            }
    """

    body={
        "sourceRefName": f"refs/heads/{sourceRefName}",
        "targetRefName": f"refs/heads/{targetRefName}",
        "title": f"{pr_title} {sourceRefName} to {targetRefName}",
        "description": "[skip ci] Pr creada en pipeline"
    }
    base_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "Authorization": f"Basic {encode_token(TOKEN)}"
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    if data is not None and isinstance(data, dict):
        actualizar_json(body, data)
    try:
        json_response = requests.post(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{REPO_ID}/pullrequests",  data=json.dumps(body), headers=base_headers, params=base_parameters)
        response = json.loads(json_response.text)
        if json_response.status_code == 201 and response['status'] == "active":
            def_response={
                "function_code":200,
                "message": "PR Creada correctamente",
                "lastMergeSourceCommit": {
                    "commitId": f"{response['lastMergeSourceCommit']['commitId']}",
                    "url": f"{response['lastMergeSourceCommit']['url']}"
                },
                "pullRequestId": f"{response['pullRequestId']}"
            }
        else:
            def_response={
                "function_code":f"{json_response.status_code}",
                "message":f"{response['message']}"
            }            
        return def_response
    except requests.RequestException as e: 
        print(f"Error al crear la pr \n {e.strerror}")
        sys.exit(1)

def get_pr_data(API_URL=str, TOKEN=str, REPO_ID=str, sourceRefName=str, targetRefName=str, headers=object|None, params=object|None) -> object:
    """
    Retrieves data about a specific Pull Request (PR) based on branch information.

    Args:
        API_URL (str): Base URL of the API for retrieving PR data.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository to search for the PR.
        params (dict): Additional parameters for retrieving PR data.
        sourceBranch (str): Name of the source branch for the PR.
        targetBranch (str): Name of the target branch for the PR.

    Returns:
        object: Dictionary with information about the PR, including function code and response data.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_error>
            }
    """

    parameters_get_prs={
    "searchCriteria.repositoryId":f"{REPO_ID}",
    "searchCriteria.status":"active",
    "searchCriteria.targetRefName":f"{targetRefName}",
    "searchCriteria.sourceRefName":f"{sourceRefName}"
    }
    base_headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {encode_token(TOKEN)}"
    }

    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, parameters_get_prs)
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        response=json.loads(requests.get(url=f"{API_URL}/pullrequests", params=base_parameters, headers=base_parameters).text)
        if response['status_code'] == 200:
            def_response={
                    "function_code":200,
                    "response_json": f"{response[0]}"
                }
        else:
            def_response={
                "function_code":f"{response['status_code']}",
                "message":f"{response['message']}"
            } 
        return def_response
    except requests.RequestException as e:
        print(f"Error al obtener datos de la PR: \n {e.strerror}")
        sys.exit(1)

def add_reviwer(API_URL=str, PROJECT=str, TOKEN=str, REPO_ID=str, pullRequestId=str, reviewerId=str, headers=object|None, data=object|None, params=object|None) -> object:
    """
    Adds a required reviewer to a Pull Request.

    Args:
        API_URL (str): Base URL of the API for adding a reviewer.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR is located.
        params (dict): Additional parameters for adding the reviewer.
        pullRequestId (str): ID of the Pull Request.
        reviewerId (str): ID of the reviewer to be added.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and a message.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_error>
            }
    """

    body = {
        "vote": 0,
        "isRequired": True
    }
    base_headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {encode_token(TOKEN)}"
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    if data is not None and isinstance(data, dict):
        actualizar_json(body, data)
    try:
        response = requests.put(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{REPO_ID}/pullrequests/{pullRequestId}/reviewers/{reviewerId}", headers=base_headers, params=base_parameters, data=json.dumps(body))
        if response.status_code == 200:
            response = json.loads(response.text)
            json_response={
                "function_code":200,
                "message":f"Revisor {response['displayName']} agregado correctamente a la PR {pullRequestId}."
            }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al añadir un reviwer: \n {e.strerror}")
        sys.exit(1)

def approve_pr(API_URL=str, PROJECT=str, TOKEN=str, REPO_ID=str, pullRequestId=str, reviewerId=str, headers=object|None, data=object|None, params=object|None) -> object:
    """
    Approves a Pull Request as a reviewer.

    Args:
        API_URL (str): Base URL of the API for approving a PR.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR is located.
        params (dict): Additional parameters for approving the PR.
        pullRequestId (str): ID of the Pull Request to be approved.
        reviewerId (str): ID of the reviewer approving the PR.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and a message.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_error>
            }
    """

    body = {
        "vote": 10  # 10 significa que el revisor aprueba la PR
    }
    base_headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {encode_token(TOKEN)}"
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    if data is not None and isinstance(data, dict):
        actualizar_json(body, data)
    try:
        response = requests.put(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{REPO_ID}/pullrequests/{pullRequestId}/reviewers/{reviewerId}", headers=base_headers, data=json.dumps(body), params=base_parameters)
        if response.status_code == 200:
            json_response={
                "function_code":200,
                "message":f"Revisor {json.loads(response.text)['displayName']} ha aprobado la PR {pullRequestId}."
            }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al aprobar la pr: \n {e.strerror}")
        sys.exit(1)

def complete_pr(API_URL=str, PROJECT=str, TOKEN=str, REPO_ID=str, pullRequestId=str, commitData=str, headers=object|None, data=object|None, params=object|None) -> object:
    """
    Completes (merges) a Pull Request.

    Args:
        API_URL (str): Base URL of the API for completing a PR.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR is located.
        params (dict): Additional parameters for completing the PR.
        pullRequestId (str): ID of the Pull Request to be completed.
        commitData (dict): Data about the commit to be merged, including 'commitId' and 'url'.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and a message.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_error>
            }
    """

    body = {
        "status": "completed",
        "lastMergeSourceCommit": {
            "commitId": f"{commitData['commitId']}",
            "url": f"{commitData['url']}"
        },
        "completionOptions": {
            "deleteSourceBranch": False,
            "mergeCommitMessage": "PR completada automáticamente",
            "squashMerge": False
        }
    }
    base_headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {encode_token(TOKEN)}"
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    if data is not None and isinstance(data, dict):
        actualizar_json(body, data)
    try:
        response = requests.patch(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{REPO_ID}/pullrequests/{pullRequestId}", headers=base_headers, data=json.dumps(body), params=base_parameters)
        if response.status_code == 200:

            json_response={
                "function_code":200,
                "message":f"PR {pullRequestId} completada y mergeada correctamente."
            }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al completar la pr: \n {e.strerror}")
        sys.exit(1)

def get_project(API_URL=str, TOKEN=str, name=str, headers=object|None, params=object|None) -> object:
    """
    Retrieves information about a project by its name.

    Args:
        API_URL (str): Base URL of the API for retrieving project information.
        TOKEN (str): Authorization token for API access.
        name (str): Name of the project to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and project ID.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "projectId": <Id del proyecto>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "projectId": <Id del proyecto>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/_apis/projects", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            for project in json.loads(response.text)['value']:
                if name in project['name']:
                    json_response={
                        "function_code":200,
                        "projectId": f"{project['id']}",
                        "message":f"Obtencion de projectos correcto"
                    }
                    break

        else:
            json_response={
                "function_code":f"{response.status_code}",
                "projectId": "0",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los proyectos: \n {e.strerror}")
        sys.exit(1)

def get_teams_by_projectId(API_URL=str, TOKEN=str, REPO_ID=str, project_id=str, team_name=str, headers=object|None, params=object|None) -> object:
    """
    Retrieves information about a specific team in a project by its name.

    Args:
        API_URL (str): Base URL of the API for retrieving team information.
        TOKEN (str): Authorization token for API access.
        project_id (str): ID of the project.
        team_name (str): Name of the team to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and team ID.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "teamId": <Id del team>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "teamId": <Id del team>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/_apis/projects/{project_id}/teams", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            for team in json.loads(response.text)['value']:
                if team_name in team['name']:
                    json_response={
                        "function_code":200,
                        "teamId": f"{team['id']}",
                        "message":f"Obtencion de equipos correcto"
                    }
                    break
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "teamId": "0",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los equipos: \n {e.strerror}")
        sys.exit(1)

def get_reviewer_id_by_team_id(API_URL=str, TOKEN=str, REPO_ID=str, project_id=str, team_id=str, user_email=str, headers=object|None, params=object|None) -> object:
    """
    Retrieves the reviewer ID by team ID and user email.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        TOKEN (str): Authorization token for API access.
        project_id (str): ID of the project.
        team_id (str): ID of the team.
        user_email (str): Email of the user whose reviewer ID is needed.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and reviewer ID.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "reviwerId": <Id del reviwer>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "reviwerId": <Id del reviwer>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/_apis/projects/{project_id}/teams/{team_id}/members", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            for user in json.loads(response.text)['value']:
                if user['uniqueName'] == user_email:
                    json_response={
                        "function_code":200,
                        "reviwerId": f"{user['id']}",
                        "message":f"Obtencion de Id de usuario correcto"
                    }
                    break
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "reviwerId": "0",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los miembros del equipo: \n {e.strerror}")
        sys.exit(1)

def get_repo_id(API_URL=str, PROJECT=str, TOKEN=str, repo_name=str, headers=object|None, params=object|None) -> object:
    """
    Retrieves the reviewer ID by team ID and user email.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        TOKEN (str): Authorization token for API access.
        repo_name (str): Repo name to obtain.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and repo ID.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "repoId": <Id del reviwer>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "repoId": <Id del reviwer>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            for repos in json.loads(response.text)['value']:
                if repos['name'] == repo_name:
                    json_response={
                        "function_code":200,
                        "repoId": f"{repos['id']}",
                        "message":f"Obtencion de Id de repositorio correcto"
                    }
                    break
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "repoId": "0",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los miembros del equipo: \n {e.strerror}")
        sys.exit(1)
