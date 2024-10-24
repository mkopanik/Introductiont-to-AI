from functools import total_ordering

@total_ordering
class Edge:
    def __init__(self, path_length, vertex_nr):
        self.path_length = path_length
        self.vertex_nr = vertex_nr
    
    def __repr__(self):
        return f"{self.path_length}, {self.vertex_nr}"

    def __eq__(self, o):
        # if not self._is_valid_operand(o):
        #     return NotImplemented
        return self.path_length == o.path_length

    def __lt__(self, o):
        # if not self._is_valid_operand(o):
        #     return NotImplemented
        return self.path_length < o.path_length