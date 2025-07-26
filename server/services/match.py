import numpy as np


class groups():
    def __init__(self, threshold=0.8):
        self.threshold = threshold
        self.groups = {}
        self.users = {}
        self.next_group_id = 0

    def is_compatible(self, vec1, vec2):
        return np.dot(vec1, vec2) > self.threshold

    def addUser(self, id, vec):
        vec = np.array(vec)
        normal_factor = np.linalg.norm(vec)
        normal = vec/normal_factor if normal_factor else vec

        compatable_set = {
            id for id in self.users if self.is_compatible(self.users[id], normal)}

        self.users[id] = normal
        flag = 1

        for group_id, group in self.groups.items():
            if group == compatable_set:
                flag = 0
            if group.issubset(compatable_set):
                self.groups[group_id].add(id)

        if (flag):
            self.next_group_id += 1
            compatable_set.add(id)
            self.groups[self.next_group_id] = compatable_set

    def show_groups(self):
        for gid, members in self.groups.items():
            print(f"Group {gid}: {sorted(members)}")
        print("------------------------------------------------------------------------")
