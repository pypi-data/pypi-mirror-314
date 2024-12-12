from nbautoeval import Args, ExerciseClass, ClassScenario, ClassExpression

class Comma:

    def __init__(self, *, a=None, b=None):
        if a is None and b is None:
            raise ValueError(f"a or b must be specified")
        if a is not None:
            self.a = a 
        else:
            self.a = 2 * b
    def __repr__(self):
        return f"{self.a}"

scenario1 = ClassScenario(
    # arguments to the constructor
    Args(a=10),
    # a list of expressions, with 
    # INSTANCE and CLASS replaced as appropriate
    ClassExpression("repr(INSTANCE)"),
)

exo_comma = ExerciseClass (
    Comma, [scenario1],
    layout='pprint')

if __name__ == '__main__':
    exo_comma.correction(Comma)

