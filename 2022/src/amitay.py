from common import levelup

def reformat_people(people_input):
    return [{'name': n, 'skills': s} for n, s in people_input.items()]

def solve(people_input, projects_input):
    people = [{'name':n,'skills':s} for n,s in people_input.items()]
    free_at = {}

    projects = [{'name':n, **p} for n,p in projects_input.items()]
    sorted_projects = sorted(projects, key=lambda x: x["score"], reverse=False)
    # sorted_projects = sorted(projects, key=lambda x: x["num_days"], reverse=False)

    # sorted_projects = sorted(projects, key=lambda x: x["best_before"], reverse=False)
    assignment = []
    not_assigned = sorted_projects[:]
    while True:
        initial_len = len(not_assigned)
        people, not_assigned = iterate_proj(assignment, free_at, people, people_input, not_assigned)
        if len(not_assigned) == initial_len:
            break

    return assignment


def iterate_proj(assignment, free_at, people, people_input, yet_not_2):
    yet_not_3 = []
    for pr in yet_not_2:
        proj_assign, people = assign_project(free_at, people, people_input, pr)
        if proj_assign:
            assignment.append((pr["name"], proj_assign))
        else:
            yet_not_3.append(pr)
    return people, yet_not_3


def assign_project(free_at, people, people_input, pr):
    start_time = 0
    chosen_people = []
    pr_assignment = []
    for role, (skill, level) in enumerate(pr["skills"]):
        found = False
        for pe in people:
            s = pe["skills"].get(skill, 0)
            if s >= level or \
                    (s + 1 == level and [a for a in pr_assignment if people_input[a].get(skill, 0) >= level]):
                if pe in chosen_people:
                    continue
                pr_assignment.append(pe["name"])
                start_time = max(start_time, free_at.get(pe["name"], 0))
                chosen_people.append(pe)
                found = True
                break
        if not found:
            pr_assignment = None
            break
    if pr_assignment is None:
        return None, people
    for pe_name in pr_assignment:
        free_at[pe_name] = start_time + pr["num_days"]
    levelup(pr, pr_assignment, people_input)
    people = reformat_people(people_input)
    return pr_assignment, people

# list of tuples of project name of list of names