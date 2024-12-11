import typer
import os
import lefaire.view as view
import lefaire.data as data
from .connect import connect, setup
from typing_extensions import Annotated

app = typer.Typer()
move_app = typer.Typer()
app.add_typer(move_app, name="move", help="Déplacer une tâche dans la liste de tâche.")


@app.command()
def add(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    body: Annotated[str, typer.Argument(help="Corps de la tâche")] = "",
    top: Annotated[
        bool,
        typer.Option(
            "-t",
            "--top",
            help="Est-ce que la tâche est à mettre tout en haut de la pile ?",
        ),
    ] = False,
):
    """
    Ajouter une tâche.
    """
    conn = connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("À quel projet ajouter une tâche ? | (Q)uitter ")
            num = num.lower().strip()

        if num != "q":

            idByName = data.get_project_by_name(cur, num)
            if idByName:
                num = int(idByName)

            if not body:
                list(num)
                body = typer.prompt("En quoi consiste cette tâche ? | (Q)uitter ")
            low = body.lower().strip()

            if low != "q":
                task = data.add_task(cur, num, body)
                conn.commit()

                if top:
                    data.move_ext(cur, num, task.rank, "top")
                    conn.commit()
                    task = data.get_task_by_ID(cur, task.ID)

                project = data.get_single_project(cur, num)
                list(num)
                view.add(task, project)
        conn.close()

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def create(
    name: Annotated[str, typer.Argument(help="Nom du projet")] = "",
    description: Annotated[str, typer.Argument(help="Description du projet")] = "",
):
    """
    Créer un projet.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        if not name:
            name = typer.prompt("Quel est le nom de ce nouveau projet ? | (Q)uitter ")
        low = name.lower().strip()
        if low != "q":
            project = data.create_project(cur, name, description)
            conn.commit()
            list()
            view.create(project)
        conn.close()

    except NameError as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def delete(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
    all: Annotated[bool, typer.Option("-a", "--all", "-p", "--project")] = False,
):
    """
    Supprimer un projet. Pour supprimer une tâche, ajouter son rang
    """
    conn = connect()
    cur = conn.cursor()
    confirm = False
    try:
        if not num:
            if not all:
                all = typer.confirm(view.delete_all_prompt())
                confirm = True
            if all:
                num = typer.prompt("Quel projet voulez-vous supprimer ? ")
            else:
                num = typer.prompt("Dans quel projet se trouve la tâche à supprimer ? ")

        idByName = data.get_project_by_name(cur, num)
        if idByName:
            num = int(idByName)

        project = data.get_single_project(cur, num)
        if not rang:
            if not all and not confirm:
                confirm = typer.confirm(view.delete_all_prompt())
                all = confirm
            if all:
                conn.close()
                delete_project(project)
            else:
                list(project.ID)
                rang = typer.prompt("Quelle tâche doit être supprimée ? ")
        if rang:
            task = data.get_single_task(cur, project.ID, rang)

            conn.close()
            delete_task(project, task)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


def delete_project(project):
    conn = connect()
    cur = conn.cursor()

    confirm = typer.confirm(view.delete_project_warning(project))
    if confirm:
        data.delete_project(cur, project.ID)
        conn.commit()
        list()
        view.delete_project(project)
    else:
        list()
        view.delete_project_safe(project)

    conn.close()


def delete_task(project, task):
    conn = connect()
    cur = conn.cursor()

    confirm = typer.confirm(view.delete_task_warning(task, project))
    if confirm:
        data.delete_task(cur, task.ID)
        conn.commit()
        list(project.ID)
        view.delete_task(task, project)
    else:
        list(project.ID)
        view.delete_task_safe(task, project)
    conn.close()


@app.command()
def desc(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    description: Annotated[str, typer.Argument(help="Description du projet")] = "",
):
    """
    Ajouter ou modifier la description d'un projet.
    """
    conn = connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("Quel projet est à modifier ? | (Q)uitter ")
            num = num.lower().strip()
        if num != "q":
            idByName = data.get_project_by_name(cur, num)
            if idByName:
                num = idByName

            if not description:
                list(num)
                description = typer.prompt("Comment décrire le projet ? | (Q)uitter ")
            low = description.lower().strip()

            if low != "q":
                project = data.update_description(cur, num, description)
                conn.commit()
                list(num)
                view.desc(project)
        conn.close()

    except Exception as e:
        view.error(e)
        raise typer.Exit()
        conn.close()


@app.command()
def done(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
    commit: Annotated[bool, typer.Option("-g", "-c", "--git", "--commit")] = False,
):
    """
    Marquer une tâche comme terminée.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        if not num:
            list()
            num = typer.prompt(
                "À quel projet appartient la tâche à terminer ? | (Q)uitter "
            )
            num = num.lower().strip()
        if num != "q":
            idByName = data.get_project_by_name(cur, num)
            if idByName:
                num = idByName

            if not rang:
                list(num)
                rang = typer.prompt(
                    "Quel est le rang de la tâche à terminer? | (Q)uitter "
                )
                rang = rang.lower().strip()
            if rang != "q":

                project = data.get_single_project(cur, num)
                task = data.complete_task(cur, num, rang)
                conn.commit()
                view.complete(task, project)

                # add to git command to clipboard
                cmd = view.commit_cmd(task)
                if commit:
                    sure = True
                else:
                    sure = typer.confirm(view.commit_prompt(cmd))
                if sure:
                    os.system(cmd)
                    list(num)
                    view.commit_success()

        conn.close()

    except Exception as e:
        view.error(e)
        raise typer.Exit()
        conn.close()


@app.command()
def due(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    date: Annotated[str, typer.Argument(help="Date butoir du projet")] = "",
):
    """
    Ajouter ou modifier une date butoir (JJ/MM/AAA HH:MM:SS).
    """
    conn = connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("Quel projet est à modifier ? | (Q)uitter ")
            num = num.lower().strip()
        if num != "q":
            idByName = data.get_project_by_name(cur, num)
            if idByName:
                num = idByName

            if not date:
                list(num)
                date = typer.prompt(
                    "Quelle est la date butoir pour ce projet (JJ/MM/AAA HH:MM:SS) ? | (Q)uitter "
                )
                date = date.lower().strip()

            if date != "q":
                date = view.toUSDate(date)
                project = data.update_due_date(cur, num, date)
                conn.commit()
                list(num)
                view.due(project)
        conn.close()

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def edit(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
    body: Annotated[str, typer.Argument(help="Corps de la tâche")] = "",
):
    """
    Modifier le corps d'une tâche.
    """
    conn = connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt(
                "À quel projet appartient la tâche à modifier ? | (Q)uitter "
            )
            num = num.lower().strip()

        if num != "q":
            idByName = data.get_project_by_name(cur, num)
            if idByName:
                num = idByName

            if not rang:
                list(num)
                rang = typer.prompt(
                    "Quel est le rang de la tâche à modifier ? | (Q)uitter "
                )
                rang = rang.lower().strip()

            if rang != "q":
                if not body:
                    list(num, rang)
                    body = typer.prompt("En quoi consiste cette tâche ? | (Q)uitter ")
                lower_body = body.lower().strip()

                if lower_body != "q":
                    project = data.get_single_project(cur, num)
                    task = data.update_body(cur, num, rang, body)
                    conn.commit()
                    list(num)
                    view.edit(task, project)
        conn.close()

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


def list(num: int = 0, rang: int = 0, long: bool = False):
    """
    Lister les projets et leurs tâches.
    """
    conn = connect()
    cur = conn.cursor()
    if rang:
        task = data.get_single_task(cur, num, rang)
        view.task_info(task)
    elif num:
        idByName = data.get_project_by_name(cur, num)
        if idByName:
            num = idByName

        project = data.get_single_project(cur, num)
        taskList = data.clean_ranks(cur, num)
        view.project_info(project, taskList, long)
    else:
        projectsList = data.get_projects(cur)
        view.list(projectsList)
    conn.close()


def project_menu(num):
    choice = typer.prompt(
        "(A)jouter une tâche | (I)nfo d'une tâche | (R)enommer | Changer la (D)escription | Changer la date (B)utoir | (S)upprimer | (Q)uitter "
    )

    choice = choice.lower().strip()
    if choice == "a":
        add(num)
    elif choice == "i":
        rang = typer.prompt("Quel est le rang de la tâche à consulter ? ")
        info(num, rang)
    elif choice == "r":
        rename(num)
    elif choice == "d":
        desc(num)
    elif choice == "b":
        due(num)
    elif choice == "s":
        delete(num, "", True)
    elif choice == "q":
        print("\n")
    else:
        try:

            int(choice)
            conn = connect()
            cur = conn.cursor()
            data.get_single_task(cur, num, choice)
        except Exception as e:
            pass
            view.error(e)
        else:
            info(num, choice)


def task_menu(num, rang):
    conn = connect()
    cur = conn.cursor()
    rang = int(rang)
    task = data.get_single_task(cur, num, rang)
    menu = "(E)diter | "
    if not task.started:
        menu += "(C)ommencer | "
    if task.started and not task.isComplete:
        menu += "(A)rrêter | "
    if not task.isComplete:
        menu += "(T)erminer | "
    if task.isComplete:
        menu += "(R)etravailler | "
    menu += "(D)éplacer | (S)upprimer | (Q)uitter "

    choice = typer.prompt(menu)
    choice = choice.lower().strip()
    if choice == "e":
        edit(num, rang)
    if choice == "c":
        start(num, rang)
    if choice == "a":
        unstart(num, rang)
    if choice == "t":
        done(num, rang)
    if choice == "r":
        undo(num, rang)
    if choice == "d":
        dir = typer.prompt(
            "Déplacer vers le (H)aut | Déplacer vers le (B)as | Mettre en (P)remier | Mettre en (D)ernier "
        )
        dir = dir.lower().strip()
        if dir == "h":
            dir = "up"
        if dir == "b":
            dir = "down"
        if dir == "p":
            dir = "top"
        if dir == "d":
            dir = "bottom"
        move(dir, num, rang)
    if choice == "s":
        delete(num, rang)
    if choice == "q":
        info(num)


@app.command()
def info(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
    long: Annotated[
        bool,
        typer.Option(
            "-l", "-v", "--long", "--verbose", help="Affiche toutes les tâches ?"
        ),
    ] = False,
):
    """
    Détailler les infos sur un projet.
    """
    try:
        if rang:
            list(num, rang)
            task_menu(num, rang)
        else:
            if not num:
                list()
                num = typer.prompt(
                    "Entrer le numéro du projet à consulter | (C)réer un projet | (Q)uitter"
                )
                num = num.lower().strip()
            if num == "c":
                create()

            elif not num == "q":
                list(num, 0, long)
                project_menu(num)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def init():
    """
    Créé un mot de passe et un utilisateur pour se connecter à MariaDB
    """
    try:
        setup()

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def relocate(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    new: Annotated[int, typer.Argument(help="Nouveau numéro du projet")] = 0,
):
    """
    Changer le numéro d'identifiant d'un projet
    """
    conn = connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("Quel projet est à deplacer ? | (Q)uitter")
            num = num.lower().strip()
        if num != "q":
            idByName = data.get_project_by_name(cur, num)
            if idByName:
                num = idByName

            project = data.get_single_project(cur, num)

            if not new:
                new = typer.prompt(
                    f"Quel est le nouvel identifiant du projet {project.name}? | (Q)uitter"
                )
                new = new.lower().strip()

            if new != "q":

                project = data.relocate_project(cur, num, new)
                conn.commit()
                list()
                view.relocate(project)
        conn.close()
    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def rename(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    name: Annotated[str, typer.Argument(help="Nouveau nom du projet")] = "",
):
    """
    Renommer un projet.
    """
    conn = connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("Quel projet est à renommer ? | (Q)uitter")
            num = num.lower().strip()

        if num != "q":
            idByName = data.get_project_by_name(cur, num)
            if idByName:
                num = idByName

            if not name:
                name = typer.prompt(
                    "Quel est le nouveau nom de ce projet ? | (Q)uitter"
                )
            low = name.lower().strip()

            if low != "q":
                data.rename_project(cur, num, name)
                conn.commit()
                list()
                view.rename(num, name)

        conn.close()

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def start(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Marquer une tâche comme commencée.
    """
    conn = connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt(
                "À quel projet appartient la tâche à commencer ? | (Q)uitter"
            )
            num = num.lower().strip()

        if num != "q":
            idByName = data.get_project_by_name(cur, num)
            if idByName:
                num = idByName
            if not rang:
                list(num)
                rang = typer.prompt(
                    "Quel est le rang de la tâche à commencer ? | (Q)uitter"
                )
                rang = rang.lower().strip()

            if rang != "q":
                project = data.get_single_project(cur, num)
                task = data.start_task(cur, num, rang)
                conn.commit()
                list(num)
                view.start(task, project)
        conn.close()

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def undo(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Marquer une tâche comme non terminée.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        if not num:
            list()
            num = typer.prompt(
                "À quel projet appartient la tâche à retravailler ? | (Q)uitter"
            )
            num = num.lower().strip()

        if num != "q":
            idByName = data.get_project_by_name(cur, num)
            if idByName:
                num = idByName
            if not rang:
                list(num)
                rang = typer.prompt(
                    "Quel est le rang de la tâche à retravailler ? | (Q)uitter"
                )
                rang = rang.lower().strip()

            if rang != "q":
                project = data.get_single_project(cur, num)
                task = data.uncomplete_task(cur, num, rang)
                conn.commit()
                list(num)
                view.uncomplete(task, project)
        conn.close()

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def unstart(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Marquer une tâche comme non commencée.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        if not num:
            list()
            num = typer.prompt(
                "À quel projet appartient la tâche à arrêter ? | (Q)uitter"
            )
            num = num.lower().strip()

        if num != "q":
            idByName = data.get_project_by_name(cur, num)
            if idByName:
                num = idByName

            if not rang:
                list(num)
                rang = typer.prompt(
                    "Quel est le rang de la tâche à arrêter ? | (Q)uitter"
                )
                rang = rang.lower().strip()

            if rang != "q":

                project = data.get_single_project(cur, num)
                task = data.unstart_task(cur, num, rang)
                conn.commit()
                list(num)
                view.unstart(task, project)
        conn.close()

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


def move(
    dir: Annotated[str, typer.Argument(help="Direction")],
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche dans la liste de tâche.
    """
    conn = connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt(
                "À quel projet appartient la tâche à déplacer ?| (Q)uitter"
            )
            num = num.lower().strip()

        if num != "q":
            idByName = data.get_project_by_name(cur, num)
            if idByName:
                num = idByName

            if not rang:
                list(num)
                rang = typer.prompt(
                    "Quel est le rang de la tâche à déplacer ? | (Q)uitter"
                )
                rang = rang.lower().strip()

            if rang != "q":

                rang = int(rang)
                task = data.get_single_task(cur, num, rang)
                project = data.move(cur, num, rang, dir)
                conn.commit()
                list(num)
                view.move(task, project, dir)
        conn.close()

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@move_app.command("up")
def move_up(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche vers le haut dans la liste de tâche.
    """
    move("up", num, rang)


@move_app.command("down")
def move_down(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche vers le bas dans la liste de tâche
    """
    move("down", num, rang)


@move_app.command("top")
def move_top(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche tout en haut de la liste de tâche.
    """
    move("top", num, rang)


@move_app.command("bottom")
def move_bottom(
    num: Annotated[str, typer.Argument(help="Numéro du projet")] = "",
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche tout en vas de la liste de tâche.
    """
    move("bottom", num, rang)


if __name__ == "__main__":
    app()
