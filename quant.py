hour = 1    # time is dimensionless
minute = hour / 60

class Resource: 
    roster = []

    def __init_subclass__(cls) -> None:
        __class__.roster.append(cls)

class RoomHour(Resource): pass
class Sanity(Resource): pass
class LMD(Resource): pass
class ExpBlue(Resource): pass
class DrawChance(Resource): pass

class Basket(dict):
    def __add__(self, other):
        if other == 0:
            return self
        assert isinstance(other, __class__)
        result = __class__()
        for t in Resource.roster:
            result[t] = self.get(t, 0) + other.get(t, 0)

        return result
    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, scaler):
        result = __class__()
        for t in Resource.roster:
            result[t] = self.get(t, 0) * scaler
        return result
    def __rmul__(self, scaler):
        return self.__mul__(scaler)
    
    def __truediv__(self, divider):
        return (1 / divider) * self

    def __repr__(self) -> str:
        buffer = []
        for k, v in self.items():
            if v == 0:
                continue
            k: type
            buffer.append(f'{v:.4f} {k.__name__}')
        return '[' + ', '.join(buffer) + ']'

exp_gold = Basket({ExpBlue: 1000 / 400})
cert_green = (Basket({LMD: 2000}) + 2 * exp_gold) / 10

# find fixpoint
duplicate_op = Basket()
for _ in range(30):
    # print(_, duplicate_op)
    orundum = Basket({DrawChance: 1 / 600}) + duplicate_op / 600
    cert_yellow = 10 * 600 * orundum / 70
    duplicate_op = sum((
        .00 * cert_green * 2, 
        .00 * cert_green * 2, 
        .40 * cert_green * 10, 
        .50 * (cert_green * 30 + cert_yellow), 
        .08 * cert_yellow * 8, 
        .02 * cert_yellow * 15, 
    ))

device = Basket({Sanity: 9 / .5114})
shard = Basket({RoomHour: 1, LMD: 1000}) + device

def orundumTrade(scaler=1):
    cost = Basket({RoomHour: 2}) + 2 * shard
    gain = 20 * orundum

    cost *= scaler
    gain *= scaler

    print(f'{cost = }')
    print(f'{gain = }')
    print()

orundumTrade()
print('One draw')
orundumTrade(1 / 0.042)
print('full base, one day, assuming 2-5-2')
orundumTrade(24 * 7 / 4)
print('150 sanity')
orundumTrade(150 / 35.1975)
