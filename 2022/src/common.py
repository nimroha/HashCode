

def naive_levelup(project, members, people):
    """only levelup on your own without mentoring"""
    for member, skill_req in zip(members, project['skills']):
        skill, needed_level = skill_req
        member_level = people[member].get(skill, 0)
        if needed_level == member_level:
            people[member][skill] += 1


def levelup(project, members, people):
    """levelup with mentor"""
    for member, skill_req in zip(members, project['skills']):
        skill, needed_level = skill_req
        member_level = people[member].get(skill, 0)
        if needed_level == member_level:
            people[member][skill] += 1
        elif needed_level == member_level + 1:
            mentors = [m for m in members if people[m].get(skill, 0) >= needed_level]
            if len(mentors) > 0:
                people[member][skill] += 1


