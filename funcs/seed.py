class Seed():
    def __init__(self, seed:str) -> None:
        self.seeder = self.xmur3(seed)

    def random(this, min:int|float = 0, max:int|float = 1) ->int|float:
        if (min > max):
            raise ValueError("The minimum value must be below the maximum value")
        if (min == max):
            return min
        return this.denormalize(this.sfc32(), min, max)

    def randomInt(this, min:int = 0, max:int = 1) ->int:
        return round(this.random(min, max))

    def denormalize(this, value:int|float, min:int|float, max:int|float) -> int|float:
        return value * (max - min) + min

    def xmur3(this, string:str) -> function:
        h = 1779033703 ^ len(string)
        for i in string:
            h = (((h ^ ord(i) & 0xFFFFFFFF) * 3432918353) & 0xFFFFFFFF)
            h = ((h << 13) | (h >> 19)) & 0xFFFFFFFF
        def randomizer() -> int:
            h = ((((h ^ h >> 16) & 0xFFFFFFFF) * 2246822507) & 0xFFFFFFFF)
            h = ((((h ^ h >> 13) & 0xFFFFFFFF) * 3266489909) & 0xFFFFFFFF)
            return (h ^ h >> 16)
        return randomizer

    def sfc32(this) -> int|float:
        a = this.seeder()
        b = this.seeder()
        c = this.seeder()
        d = this.seeder()
        t = (a + b) | 0
        a = b ^ (b >> 9)
        b = (c + (c << 3)) | 0
        c = (c << 21) | (c >> 11)
        d = (d + 1) | 0
        t = (t + d) | 0
        c = (c + t) | 0
        return t / 4294967296
