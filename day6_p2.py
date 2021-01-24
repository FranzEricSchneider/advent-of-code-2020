class Questionaire:
    def __init__(self):
        self.answers = []

    def add_line(self, line):
        self.answers.append(line.strip())

    @property    
    def yes_counts(self):
        if len(self.answers) == 1:
            return len(self.answers[0])
        else:
            candidates = [
                char
                for char in self.answers[0]
                if all([char in other_answer
                        for other_answer in self.answers[1:]])
            ]
            return len(candidates)

def main():
    with open("day6.txt", "r") as fin:
        entries = []
        questionaire = Questionaire()
        for line in fin.readlines():
            if line == "\n":
                entries.append(questionaire)
                questionaire = Questionaire()
            else:
                questionaire.add_line(line)
        entries.append(questionaire)

    print(f"{sum([e.yes_counts for e in entries])} summed yes counts")


if __name__ == '__main__':
    main()
