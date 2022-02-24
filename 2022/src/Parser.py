import numpy as np
import pandas as pd

def parseIn(path):
    with open(path, 'r') as fp:
        num_contributors, num_projects = fp.readline().strip().split()
        people = {}
        all_skills = []
        for i in range(int(num_contributors)):
            person_name, num_skills = fp.readline().strip().split()
            skills = [fp.readline().strip().split() for _ in range(int(num_skills))] # (skill_name, skill_level)
            people[person_name] = {skill[0]: int(skill[1]) for skill in skills}
            all_skills.extend(list(people[person_name].keys()))

        projects = {}
        for j in range(int(num_projects)):
            project_name, num_days, score, best_before, num_roles = fp.readline().strip().split()
            needed_skills = [fp.readline().strip().split() for _ in range(int(num_roles))]  # (skill_name, min_skill_level)

            projects[project_name] = {'num_days':    int(num_days),
                                      'best_before': int(best_before),
                                      'score':       int(score),
                                      'skills':      [(s[0], int(s[1])) for s in needed_skills]}


        return people, projects, list(set(all_skills))


def parseOut(path, plan):
    with open(path, 'w') as fp:
        fp.write(f'{len(plan)}\n')
        for project_name, members in plan:
            fp.write(f'{project_name}\n')
            fp.write(f'{" ".join(members)}\n')

if __name__ == '__main__':
    test_plan = [('alpha', ['tom', 'brady']), ('beta', ['putin', 'biden'])]
    parseOut('../inputs/test_result.txt', test_plan)
    optimal_example = [('WebServer', ['Bob', 'Anna']), ('Logging', ['Anna']), ('WebChat', ['Maria', 'Bob'])]
    parseOut('../inputs/a_an_example_result.txt', optimal_example)

