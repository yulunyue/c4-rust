# Translated Rust code to Python
# This code is related to entity and vector data structures

class Closest:
    def __init__(self, entity_list, distance):
        self.entity_list = entity_list
        self.distance = distance

    def get(self):
        return self.entity_list[0] if self.entity_list else None

    def has_one(self):
        return len(self.entity_list) == 1

    def get_pos(self):
        return self.entity_list[0].get_pos() if self.entity_list else None

    def get_mean_pos(self):
        if self.has_one():
            return self.get_pos()

        sum_x, sum_y = 0.0, 0.0
        for entity in self.entity_list:
            pos = entity.get_pos()
            sum_x += pos.x
            sum_y += pos.y

        mean_x = sum_x / len(self.entity_list)
        mean_y = sum_y / len(self.entity_list)

        return Vector(mean_x, mean_y)


def get_closest_to(from_vector, targets):
    closest_entities = []
    min_distance = float('inf')

    for target in targets:
        distance = target.get_pos().sqr_euclidean_to(from_vector)
        if not closest_entities or distance < min_distance:
            closest_entities.clear()
            closest_entities.append(target)
            min_distance = distance
        elif distance == min_distance:
            closest_entities.append(target)

    return Closest(closest_entities, min_distance ** 0.5)