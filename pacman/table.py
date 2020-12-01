from constants import LIGHT_ORANGE


class Table:
    def __init__(self):
        self.data = []

    def draw(self, screen, top, font, count_records):
        f = open('high_scores.txt', 'r')
        data = f.read().split(sep='\n')
        data.pop()
        f.close()
        players = dict()
        records = list()
        for i in range(len(data)):
            p, s = data[i].split()
            players[int(s)] = p
            records.append(int(s))
        records.sort(reverse=True)
        if count_records > len(records):
            count_records = len(records)
        for i in range(count_records):
            self.data.append([str(i+1)+'.', str(records[i]), players[records[i]]])

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                text = font.render(self.data[i][j], 1, LIGHT_ORANGE)
                cur_x = 100 + (200 - text.get_rect().width) // 2 + 200 * j
                cur_y = top + (text.get_rect().height + 10) * i
                screen.blit(text, (cur_x, cur_y))

        self.data = []
