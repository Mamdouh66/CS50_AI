from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# Puzzle 0
knowledge0 = And(
    # A is either a knight or a knave but not both
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),
    # A is a knight if and only if they are both not
    Biconditional(AKnight, And(AKnave, AKnight))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A, B is either a knight or a knave but not both
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),
    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),
    # A is A knave if and only if  they are both not, because they can't be both the same thing, and a knight won't lie
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
knowledge2 = And(
    # A, B is either a knight or a knave but not both
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),
    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),
    # They can't be both the same thing so A is lying and he is knave, and B is a knight
    # A is a knave if and only if A and B are knaves, B is a knight if and only if they are not knight in the same time
    Biconditional(AKnight, And(AKnave, BKnave)),
    Biconditional(BKnight, Not(And(AKnight, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A, B, C is either a knight or a knave but not both
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),
    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),
    Or(CKnave, CKnight),
    Not(And(CKnave, CKnight)),
    # A is either a knight or knave, we don't know so he is in the Or above for Reduncdancy
    # B says that A said i'm a knave, but A didn't  so B is a knight if and only if A is a knight
    # and he told the truth that he is a knave, which is a contradaction that doesn't make sense
    # and if he was a knave he wouldn't tell the truth, so B must B a knave, if B is a knave and he said
    # that C is a knave so he lied and C is a knight, and C told the truth that A is a knight
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    Biconditional(BKnight, CKnave),
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
