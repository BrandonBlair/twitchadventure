class AdventureGame(object):
    name = "Generic Game"

    def __init__(self):
        self.header = f"*** {self.name} ***"
        self.step_index = 0
        self.steps = []

    def describe_current_step(self):
        return self.current_step.desc

    def attempt(self, txt):
        current_step = self.current_step
        remaining_words = current_step.solution_words_remaining
        if remaining_words == 0:
            self.proceed_to_next_step()
            return current_step.success_msg
        else:
            return remaining_words

    def proceed_to_next_step(self):
        self.current_step.solved = True
        self.step_index += 1

    @property
    def current_step(self):
        return self.steps[self.step_index]

    def cout(self, text):
        opt = f"{self.header}: {text}"
        return opt


class Step(object):
    solution_set = {}
    success_msg = "You solved the step!"
    desc = "A generic step"

    def __init__(self):
        self.solved = False

    def solution_words_remaining(self, txt):
        words = self.ipt_words(txt)
        return self.solution_set - words

    def ipt_words(self, ipt):
        words = ipt.split(' ')
        return set(words)
