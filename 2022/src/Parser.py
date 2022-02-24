import numpy as np
import pandas as pd
from dataclasses import dataclass

@dataclass
class Street:
    start: int
    end: int
    name: str
    duration: int


@dataclass
class Data:
    streets: dict
    paths: list
    num_steps: int
    num_intersections: int
    num_streets: int
    num_cars: int
    bonus: int


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

            projects[project_name] = {'num_days':    num_days,
                                      'best_before': best_before,
                                      'score':       score,
                                      'skills':      [(s[0], int(s[1])) for s in needed_skills]}


        return people, projects, list(set(all_skills))


def parseOut(path, schedules):
    with open(path, 'w') as fp:
        schedules = {k: v for k, v in schedules.items() if len(v) > 0}
        fp.write(f'{len(schedules)}\n')
        for intersection, schedule in schedules.items():
            fp.write(f'{intersection}\n')
            fp.write(f'{len(schedule)}\n')
            for name, duration in schedule:
                fp.write(f'{name} {duration}\n')

if __name__ == '__main__':
    example_schedule = {1: [('a', 3), ('b', 2)],
                        3: [('z', 1), ('e', 3)]}
    parseIn('inputs/example.txt')
    parseOut('inputs/example_result.txt', example_schedule)
