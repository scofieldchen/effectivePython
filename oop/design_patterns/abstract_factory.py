"""
抽象工厂模式(Abstract Factory Pattern)

提供一个共同的接口来创建多个相互关联的多个对象
"""

class PetShop(object):
    """抽象工厂"""

    def __init__(self, animal_factory=None):
        self.pet_factory = animal_factory

    def show_pet(self):
        """用抽象工厂创建一个具体工厂"""
        pet = self.pet_factory()
        print("create %s instance" % str(pet))
        print("It says %s" % pet.speak())


class Cat(object):
    """具体工厂"""

    def __str__(self):
        return "Cat"

    def speak(self):
        return "I am cat"


class Dog(object):
    """具体工厂"""

    def __str__(self):
        return "Dog"

    def speak(self):
        return "I am dog"


if __name__ == "__main__":
    cat_shop = PetShop(Cat)
    cat_shop.show_pet()

    dog_shop = PetShop(Dog)
    dog_shop.show_pet()
