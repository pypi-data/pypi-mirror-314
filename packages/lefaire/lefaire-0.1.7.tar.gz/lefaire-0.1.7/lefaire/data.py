from dataclasses import dataclass


@dataclass
class Project:
    ID: int
    name: str
    created: str
    started: str
    completionDate: str
    dueDate: str
    description: str
    isComplete: bool


@dataclass
class Task:
    ID: int
    projectID: int
    rank: int
    body: str
    created: str
    started: str
    completionDate: str
    isComplete: bool


# Retrieve all projects
def get_projects(cur):
    projects = []
    cur.execute(
        "SELECT ID, Name, Created, Started, CompletionDate, DueDate, Description, IsComplete from Project"
    )
    for (
        ID,
        name,
        created,
        started,
        completionDate,
        dueDate,
        description,
        isComplete,
    ) in cur:
        project = Project(
            ID, name, created, started, completionDate, dueDate, description, isComplete
        )
        projects.append(project)
    return projects


# Retrieve on particular project
def get_single_project(cur, projectID):
    if not projectIDExists(cur, projectID):
        raise Exception("Ce projet n'existe pas ! ")
    project = None
    cur.execute(
        "SELECT Name, Created, Started, CompletionDate, DueDate, Description, IsComplete from Project WHERE ID = ?",
        (projectID,),
    )
    for (
        name,
        created,
        started,
        completionDate,
        dueDate,
        description,
        isComplete,
    ) in cur:
        project = Project(
            projectID,
            name,
            created,
            started,
            completionDate,
            dueDate,
            description,
            isComplete,
        )
    return project


# Show all tasks for a project
def get_tasks(cur, projectID: int):
    if not (projectIDExists(cur, projectID)):
        raise Exception("Ce projet n'existe pas !")
    tasks = []
    cur.execute(
        "SELECT ID, Rank, Body, Created, Started, CompletionDate, IsComplete FROM Task WHERE ProjectID = ? ORDER BY Rank;",
        (projectID,),
    )

    for ID, rank, body, created, started, completionDate, isComplete in cur:
        task = Task(
            ID, projectID, rank, body, created, started, completionDate, isComplete
        )
        tasks.append(task)
    return tasks


def clean_ranks(cur, projectID: int):
    tasksList = get_tasks(cur, projectID)
    # split todo and done
    todo = []
    done = []
    for task in tasksList:
        if task.isComplete:
            done.append(task)
        else:
            todo.append(task)
    newList = done + todo
    newOrder(cur, newList)
    tasksList = get_tasks(cur, projectID)
    return tasksList


# get a specific task from a project
def get_single_task(cur, projectID, rank):
    if not taskRankExists(cur, projectID, rank):
        raise NameError("Cette tâche n'existe pas !")

    task = None
    cur.execute(
        "SELECT ID, Body, Created, Started, CompletionDate, IsComplete FROM Task WHERE ProjectID = ? AND Rank = ?;",
        (projectID, rank),
    )
    for ID, body, created, started, completionDate, isComplete in cur:
        task = Task(
            ID, projectID, rank, body, created, started, completionDate, isComplete
        )
    return task


def get_task_by_ID(cur, taskID):
    task = None
    cur.execute(
        "SELECT ProjectID, Rank, Body, Created, Started, CompletionDate, IsComplete FROM Task WHERE ID = ?;",
        (taskID,),
    )
    for projectID, rank, body, created, started, completionDate, isComplete in cur:
        task = Task(
            taskID, projectID, rank, body, created, started, completionDate, isComplete
        )
    return task


def projectNameExists(cur, projectName: str):
    cur.execute(
        "SELECT EXISTS (SELECT * FROM Project WHERE Name = ?) ;",
        (projectName,),
    )
    bool = cur.fetchone()[0]
    return bool


def projectIDExists(cur, projectID: int):
    cur.execute(
        "SELECT EXISTS (SELECT * FROM Project WHERE ID = ?) ;",
        (projectID,),
    )
    bool = cur.fetchone()[0]
    return bool


def get_project_by_name(cur, input: str):
    cur.execute("SELECT ID FROM Project WHERE Name = ?;", (input,))
    res = cur.fetchone()
    if res is not None:
        id = res[0]
        return id


# Add a project
def create_project(cur, projectName="Nouveau Projet", description=None):
    projectName = projectName.strip()
    if description:
        description = description.strip()
    if projectNameExists(cur, projectName):
        raise NameError("Le projet existe déjà !")

    if not description:
        description = None

    cur.execute(
        "INSERT INTO Project (Name, Created, Description) VALUES ( ?, CURRENT_TIMESTAMP, ?);",
        (projectName, description),
    )
    projectList = get_projects(cur)
    lastProject = projectList[len(projectList) - 1]
    return lastProject


def update_rank(cur, ID, newRank):
    cur.execute("UPDATE Task SET Rank = ? WHERE ID = ?;", (newRank, ID))


def newOrder(cur, list):

    for i in range(len(list)):
        task = list[i]
        update_rank(cur, task.ID, i + 1)


def taskBodyExists(cur, projectID, body):
    cur.execute(
        "SELECT EXISTS (SELECT * FROM Task WHERE ProjectID = ? AND Body = ?);",
        (projectID, body),
    )
    bool = cur.fetchone()[0]
    return bool


def taskRankExists(cur, projectID, rank):
    cur.execute(
        "SELECT EXISTS (SELECT * FROM Task WHERE ProjectID = ? AND Rank = ?);",
        (projectID, rank),
    )
    bool = cur.fetchone()[0]
    return bool


# Add a task to a project
def add_task(cur, projectID: int, body: str):
    if taskBodyExists(cur, projectID, body):
        raise Exception("la tâche existe déjà")

    clean_ranks(cur, projectID)

    body = body.strip()
    tasksList = clean_ranks(cur, projectID)
    rank = len(tasksList) + 1
    cur.execute(
        "INSERT INTO Task (ProjectID, Rank, Body) VALUES (?, ?, ?);",
        (projectID, rank, body),
    )
    uncomplete_project(cur, projectID)
    return get_single_task(cur, projectID, rank)


# Update project


def rename_project(cur, projectID, newName):
    newName = newName.strip()
    cur.execute("UPDATE Project SET Name = ? WHERE ID = ?", (newName, projectID))
    renamedProject = get_single_project(cur, projectID)
    return renamedProject


def update_description(cur, projectID, newDescription):
    newDescription = newDescription.strip()
    cur.execute(
        "UPDATE Project SET Description = ? WHERE ID = ?", (newDescription, projectID)
    )
    updatedProject = get_single_project(cur, projectID)
    return updatedProject


def update_due_date(cur, projectID, dueDate):
    cur.execute("UPDATE Project SET DueDate = ? WHERE ID = ?", (dueDate, projectID))
    updatedProject = get_single_project(cur, projectID)
    return updatedProject


def start_project(cur, projectID):
    cur.execute(
        "UPDATE Project SET Started = CURRENT_TIMESTAMP WHERE ID = ?", (projectID,)
    )
    updatedProject = get_single_project(cur, projectID)
    return updatedProject


def unstart_project(cur, projectID):
    cur.execute("UPDATE Project SET Started = NULL WHERE ID = ?", (projectID,))
    updatedProject = get_single_project(cur, projectID)
    return updatedProject


def complete_project(cur, projectID):
    cur.execute(
        "UPDATE Project SET CompletionDate = CURRENT_TIMESTAMP , isComplete = TRUE WHERE ID = ?",
        (projectID,),
    )
    updatedProject = get_single_project(cur, projectID)
    return updatedProject


def uncomplete_project(cur, projectID):
    cur.execute(
        "UPDATE Project SET CompletionDate = NULL , isComplete = FALSE WHERE ID = ?",
        (projectID,),
    )
    updatedProject = get_single_project(cur, projectID)
    return updatedProject


def relocate_project(cur, projectID, newID):
    if projectIDExists(cur, newID):
        raise Exception(f"Le projet n°{newID} existe déjà !")

    cur.execute(
        "UPDATE Project SET ID = ? WHERE ID = ?",
        (
            newID,
            projectID,
        ),
    )
    # changer le project ID de ces taches
    cur.execute(
        "UPDATE Task SET ProjectID = ? WHERE ProjectID = ?",
        (
            newID,
            projectID,
        ),
    )
    change_auto_increment(cur)
    updatedProject = get_single_project(cur, newID)
    return updatedProject


def change_auto_increment(cur):
    try:
        # find the bigger ID
        cur.execute("SELECT MAX(ID) FROM Project")
        maxID = cur.fetchone()[0]
        # Make the auto-increment the next number
        if maxID:
            auto_increment = f"{maxID + 1}"
            cur.execute(f"ALTER TABLE Project AUTO_INCREMENT={auto_increment};")
            cur.execute("COMMIT")
    except Exception:
        raise Exception("Erreur de manipulation des auto-increments ")


# Update a task
def update_body(cur, projectID, rank, newBody):
    newBody = newBody.strip()
    cur.execute(
        "UPDATE Task SET Body = ? WHERE ProjectID = ? AND Rank = ?",
        (newBody, projectID, rank),
    )
    updatedTask = get_single_task(cur, projectID, rank)
    return updatedTask


def swap_rank(cur, projectID, currentRank, newRank):
    firstTask = get_single_task(cur, projectID, currentRank)
    secondTask = get_single_task(cur, projectID, newRank)
    cur.execute("UPDATE Task SET Rank = ? WHERE ID=?", (newRank, firstTask.ID))
    cur.execute("UPDATE Task SET Rank = ? WHERE ID=?", (currentRank, secondTask.ID))
    updatedProject = get_single_project(cur, projectID)
    return updatedProject


def move_up(cur, projectID, rank):
    task = get_single_task(cur, projectID, rank)
    if rank == 1:
        raise Exception(
            f"'{task.body}' est la première tâche, elle ne peut donc pas monter plus haut."
        )
    return swap_rank(cur, projectID, rank, rank - 1)


def move_down(cur, projectID, rank):
    task = get_single_task(cur, projectID, rank)
    try:
        get_single_task(cur, projectID, rank + 1)
    except Exception:
        raise Exception(
            f"'{task.body}' est la dernière tâche, elle ne peut donc pas descendre plus bas."
        )
    return swap_rank(cur, projectID, rank, rank + 1)


def move_ext(cur, projectID, rank, ext):
    task = get_single_task(cur, projectID, rank)
    ext = ext.lower()
    tasksList = clean_ranks(cur, projectID)
    # split todo and done
    todo = []
    done = []
    if rank == 1 and ext == "top":
        raise Exception(
            f"'{task.body}' est déjà la première tâche, elle ne peut donc pas monter plus haut."
        )
    if rank == len(tasksList) and ext == "bottom":
        raise Exception(
            f"'{task.body}' est déjà la dernière tâche, elle ne peut donc pas descendre plus bas."
        )
    for current in tasksList:
        if current != task:
            if current.isComplete:
                done.append(current)
            else:
                todo.append(current)
    if ext == "top":
        if task.isComplete:
            done.insert(0, task)
        else:
            todo.insert(0, task)
    else:
        if task.isComplete:
            done.append(task)
        else:
            todo.append(task)

    newList = done + todo
    newOrder(cur, newList)
    return get_single_project(cur, projectID)


def move(cur, projectID, rank, dir):
    clean_ranks(cur, projectID)
    dir = dir.lower()
    if dir == "up":
        return move_up(cur, projectID, rank)
    elif dir == "down":
        return move_down(cur, projectID, rank)
    elif dir == "top" or dir == "bottom":
        return move_ext(cur, projectID, rank, dir)
    else:
        raise Exception("La direction ne peut être que 'top', 'bottom', 'up' ou 'down'")


def start_task(cur, projectID, rank):
    task = get_single_task(cur, projectID, rank)
    if task.started:
        raise Exception(f"La tâche '{task.body}' est déjà commencée.")
    if task.isComplete:
        raise Exception(f"La tâche '{task.body}' est déjà terminée.")
    cur.execute(
        "UPDATE Task SET started = CURRENT_TIMESTAMP WHERE ProjectID = ? AND Rank = ?",
        (projectID, rank),
    )
    project = get_single_project(cur, projectID)
    if not project.started:
        start_project(cur, projectID)
    if task.isComplete:
        uncomplete_task(cur, projectID, rank)
    updatedTask = get_single_task(cur, projectID, rank)
    return updatedTask


def noTasksStarted(tasksList):
    for task in tasksList:
        if task.started or task.isComplete:
            return False
    return True


def checkifStarted(cur, projectID):
    tasksList = clean_ranks(cur, projectID)
    if noTasksStarted(tasksList):
        unstart_project(cur, projectID)


def unstart_task(cur, projectID, rank):
    task = get_single_task(cur, projectID, rank)
    if not task.started:
        raise Exception(f"La tâche '{task.body}' n'est pas encore commencée.")
    if task.isComplete:
        raise Exception(f"La tâche '{task.body}' est déjà terminée.")
    cur.execute(
        "UPDATE Task SET started = NULL WHERE ProjectID = ? AND Rank = ?",
        (projectID, rank),
    )
    project = get_single_project(cur, projectID)
    if project.started:
        checkifStarted(cur, projectID)
    updatedTask = get_single_task(cur, projectID, rank)
    if updatedTask.isComplete:
        uncomplete_task(cur, projectID, rank)
    return updatedTask


def allTasksComplete(tasksList):
    for task in tasksList:
        if not task.isComplete:
            return False
    return True


def checkCompleteness(cur, projectID):
    tasksList = clean_ranks(cur, projectID)
    if not tasksList:
        uncomplete_project(cur, projectID)
        unstart_project(cur, projectID)
    elif allTasksComplete(tasksList):
        complete_project(cur, projectID)
    else:
        uncomplete_project(cur, projectID)


def complete_task(cur, projectID, rank):
    task = get_single_task(cur, projectID, rank)
    if task.isComplete:
        raise Exception(f"La tâche '{task.body}' est déjà terminée")

    if int(rank) > 1:
        move_ext(cur, projectID, rank, "top")
    newTask = get_task_by_ID(cur, task.ID)
    rank = newTask.rank
    if not task.started:
        start_task(cur, projectID, rank)
    cur.execute(
        "UPDATE Task SET CompletionDate = CURRENT_TIMESTAMP, IsComplete = True WHERE ID = ? ",
        (task.ID,),
    )
    checkCompleteness(cur, projectID)
    clean_ranks(cur, projectID)
    updatedTask = get_task_by_ID(cur, task.ID)
    return updatedTask


def uncomplete_task(cur, projectID, rank):
    task = get_single_task(cur, projectID, rank)
    if not task.isComplete:
        raise Exception(f"La tâche '{task.body}' n'est pas terminée")
    cur.execute(
        "UPDATE Task SET CompletionDate = NULL, IsComplete = False WHERE ProjectID = ? AND Rank = ?",
        (projectID, rank),
    )
    checkCompleteness(cur, projectID)
    updatedTask = get_single_task(cur, projectID, rank)
    return updatedTask


def delete_project(cur, projectID):
    if not projectIDExists(cur, projectID):
        raise Exception("Le project n'existe pas ")
    cur.execute("DELETE FROM Project WHERE ID = ?", (projectID,))
    cur.execute("DELETE FROM Task WHERE ProjectID = ?;", (projectID,))
    change_auto_increment(cur)
    updatedList = get_projects(cur)
    return updatedList


def delete_task(cur, taskID):
    task = get_task_by_ID(cur, taskID)
    if not taskRankExists(cur, task.projectID, task.rank):
        raise Exception("La tâche n'existe pas")
    projectID = task.projectID
    cur.execute("DELETE FROM Task WHERE ID = ?;", (taskID,))
    checkifStarted(cur, projectID)
    checkCompleteness(cur, projectID)
    return clean_ranks(cur, projectID)
