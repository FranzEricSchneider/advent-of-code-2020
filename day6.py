class Questionaire:
    def __init__(self):
        self.answers = set()

    def add_line(self, line):
        for char in line.strip():
            self.answers.add(char)

    @property    
    def yes_counts(self):
        return len(self.answers)

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
