## Animal is-a object (yes, sort of confusing) look at the extra credit
class Animal(object):
    pass

## Dog is-a Animal
class Dog(Animal):

    def __init__(self, name):
        ## Dog has-a name
        self.name = name

## Cat is-a Animal
class Cat(Animal):

    def __init__(self, name):
        ## Cat has-a name
        self.name = name

## Person is-a object
class Person(object):

    def __init__(self, name):
        ## Person has-a name
        self.name = name

        ## Person has-a pet of some kind
        self.pet = None

## Employee is-a Person
class Employee(Person):

    def __init__(self, name, salary):
        ## Employee can give a person a name 
        super(Employee, self).__init__(name)
        ## Employee has-a salary
        self.salary = salary

## Fish is-a object
class Fish(object):
    pass

## Salmon is-a Fish
class Salmon(Fish):
    pass

## Halibut is-a Fish
class Halibut(Fish):
    pass


## rover is-a Dog
rover = Dog("Rover")

## stan is-a Cat
stan = Cat("Stan")

## mary is-a Person
mary = Person("Mary")

## mary has-a pet stan, stan is-a Cat
mary.pet = stan

## frank is-a Employee which is-a Person, has-a salary of 120,000
frank = Employee("Frank", 120000)

## frank has-a pet rover, rover is-a Dog
frank.pet = rover

## flipper is-a Fish
flipper = Fish()

## crouse is-a Salmon
crouse = Salmon()

## harry is-a Halibut
harry = Halibut()
