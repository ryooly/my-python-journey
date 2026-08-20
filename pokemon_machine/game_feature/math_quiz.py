import random


def _addition(a: int, b: int) -> tuple[str, float]:
    return f"{a} + {b} = ?", a + b


def _subtraction(a: int, b: int) -> tuple[str, float]:
    hi, lo = max(a, b), min(a, b)
    return f"{hi} - {lo} = ?", hi - lo


def _multiplication(a: int, b: int) -> tuple[str, float]:
    return f"{a} x {b} = ?", a * b


def _division(a: int, b: int) -> tuple[str, float]:
    return f"{a} / {b} = ? (round to 2 decimals)", round(a / b, 2)


def _percentage(a: int, b: int) -> tuple[str, float]:
    return f"{a}% of {b} = ?", round((a / 100) * b, 2)


_GENERATORS = [
    _addition,
    _subtraction,
    _multiplication,
    _division,
    _percentage,
]


def generate_problems(count: int = 5) -> list[dict]:
    """Return *count* math problems (one per operation type, then cycling)."""
    problems: list[dict] = []

    for i in range(count):
        gen = _GENERATORS[i % len(_GENERATORS)]
        a = random.randint(1, 50)
        b = random.randint(1, 50)

        # avoid trivial / zero-edge cases for division
        if gen is _division:
            b = random.randint(2, 20)
            a = b * random.randint(2, 10)  # guarantees clean division

        question, answer = gen(a, b)
        problems.append({"question": question, "answer": answer})

    return problems


def run_quiz() -> int:
    """Present 5 problems, collect answers, return the averaged result as a pokemon ID."""
    problems = generate_problems(5)
    results: list[float] = []

    print("\n===========================================")
    print("        MATH QUIZ - CATCH A POKEMON        ")
    print("===========================================")

    for i, p in enumerate(problems, 1):
        print(f"\n  Question {i}: {p['question']}")
        while True:
            try:
                user_input = float(input("  Your answer: "))
                results.append(user_input)
                break
            except ValueError:
                print("  Invalid input. Please enter a number.")

    # Sum all results then divide by the number of questions to get the ID
    total = sum(results)
    pokemon_id = max(1, abs(round(total / len(results))))

    print(f"\n-------------------------------------------")
    print(f"  Your answers : {results}")
    print(f"  Total        : {total}")
    print(f"  Final ID     : {pokemon_id}  (total / {len(results)}, rounded)")
    print(f"-------------------------------------------")

    return pokemon_id
