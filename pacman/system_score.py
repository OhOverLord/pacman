class SystemScore:
    combo = 0

    def get_score_for_grain(self):
        return 5
    def get_score_for_super_grain(self):
        return 100
    def get_score_for_ghost(self):
        self.combo += 1
        return self.combo * 400

    def get_pay_for_teleport(self):
        return -10

    def get_pay_for_ghost(self):
        return -50
