class Number:
    def __init__(self, number):
        self.number = number

    # kiểm tra chẵn lẽ
    def is_even(self):
        return self.number % 2 == 0


_number = Number(10)
print(_number.is_even())
