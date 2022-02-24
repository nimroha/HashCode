

def naive_levelup(project, members, people):
    """only levelup on your own without mentoring"""
    for member, skill_req in zip(members, project['skills']):
        skill, needed_level = skill_req
        member_level = people[member][skill]
        if needed_level == member_level:
            people[member][skill] += 1

