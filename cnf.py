class CNF:
    def __init__(self, body, difference = []):
        self.body = body
        self.difference = difference
    def standardlize_variable(self):
        bind_dict = {}
        for statement in self.body.list_of_statements:
            bind_dict = statement.standardlize_variable(bind_dict=bind_dict)
        for difference in self.difference:
            difference[0].term = bind_dict[difference[0].term]
            difference[1].term = bind_dict[difference[1].term]
    def check_difference(self, binding):
        differ = True
        for difference in self.difference:
            if binding.bind(difference[0]) == binding.bind(difference[1]):
                differ = False
                break
        return differ