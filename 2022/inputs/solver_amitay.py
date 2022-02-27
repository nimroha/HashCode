from common import levelup

def reformat_people(people_input):
    return [{'name': n, 'skills': s} for n, s in people_input.items()]

def solve(people_input, projects_input):
    people = [{'name':n,'skills':s} for n,s in people_input.items()]
    free_at = {}

    projects = [{'name':n, **p} for n,p in projects_input.items()]
    sorted_projects = sorted(projects, key=lambda x: x["best_before"], reverse=False)
    assignment = {}

    ans = schedule_projects(assignment, free_at, people, people_input, sorted_projects)
    return ans


def schedule_projects(assignment, free_at, people, people_input, sorted_projects):
    for pr in sorted_projects:
        start_time = 0
        chosen_people = []
        assignment[pr["name"]] = []
        for role, (skill, level) in enumerate(pr["skills"]):
            found = False
            for pe in people:
                s = pe["skills"].get(skill, 0)
                if s >= level or \
                        (s + 1 == level and [a for a in assignment[pr["name"]] if people_input[a].get(skill, 0) >= level]):
                    if pe in chosen_people:
                        continue
                    assignment[pr["name"]].append(pe["name"])
                    start_time = max(start_time, free_at.get(pe["name"], 0))
                    chosen_people.append(pe)
                    found = True
                    break
            if not found:
                assignment[pr["name"]] = None
                break
        if assignment[pr["name"]] is None:
            continue
        for pe_name in assignment[pr["name"]]:
            free_at[pe_name] = start_time + pr["num_days"]
        levelup(pr, assignment[pr["name"]], people_input)
        people = reformat_people(people_input)
    ans = [(pr["name"], assignment[pr["name"]]) for pr in sorted_projects if assignment[pr["name"]] is not None]
    return ans

# list of tuples of project name of list of names