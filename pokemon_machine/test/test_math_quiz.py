"""Tests for game_feature.math_quiz"""

import pytest
from unittest.mock import patch
from game_feature.math_quiz import (
    _addition,
    _subtraction,
    _multiplication,
    _division,
    _percentage,
    generate_problems,
    run_quiz,
)


# =========================================================================
# Individual generators
# =========================================================================

class TestAddition:
    def test_returns_correct_question_and_answer(self):
        question, answer = _addition(3, 7)
        assert question == "3 + 7 = ?"
        assert answer == 10

    def test_zero_operands(self):
        _, answer = _addition(0, 0)
        assert answer == 0

    def test_large_numbers(self):
        _, answer = _addition(999, 1)
        assert answer == 1000


class TestSubtraction:
    def test_returns_correct_result_larger_first(self):
        question, answer = _subtraction(10, 3)
        assert question == "10 - 3 = ?"
        assert answer == 7

    def test_auto_orders_high_minus_low(self):
        """Even if a < b, the generator swaps so we never get negatives."""
        question, answer = _subtraction(3, 10)
        assert question == "10 - 3 = ?"
        assert answer == 7

    def test_equal_values(self):
        _, answer = _subtraction(5, 5)
        assert answer == 0


class TestMultiplication:
    def test_returns_correct_result(self):
        question, answer = _multiplication(4, 5)
        assert question == "4 x 5 = ?"
        assert answer == 20

    def test_multiply_by_one(self):
        _, answer = _multiplication(1, 42)
        assert answer == 42

    def test_multiply_by_zero(self):
        _, answer = _multiplication(0, 100)
        assert answer == 0


class TestDivision:
    def test_returns_rounded_result(self):
        question, answer = _division(10, 3)
        assert "10 / 3" in question
        assert answer == 3.33

    def test_clean_division(self):
        _, answer = _division(20, 5)
        assert answer == 4.0

    def test_division_by_one(self):
        _, answer = _division(7, 1)
        assert answer == 7.0


class TestPercentage:
    def test_basic_percentage(self):
        question, answer = _percentage(50, 200)
        assert "50% of 200" in question
        assert answer == 100.0

    def test_ten_percent(self):
        _, answer = _percentage(10, 90)
        assert answer == 9.0

    def test_full_percentage(self):
        _, answer = _percentage(100, 37)
        assert answer == 37.0


# =========================================================================
# generate_problems
# =========================================================================

class TestGenerateProblems:
    def test_default_returns_five(self):
        problems = generate_problems()
        assert len(problems) == 5

    def test_custom_count(self):
        problems = generate_problems(count=3)
        assert len(problems) == 3

    def test_each_problem_has_question_and_answer(self):
        for p in generate_problems():
            assert "question" in p
            assert "answer" in p
            assert isinstance(p["question"], str)
            assert isinstance(p["answer"], (int, float))

    def test_cycling_order(self):
        """With the default 5, operations appear in fixed order:
        addition, subtraction, multiplication, division, percentage."""
        problems = generate_problems(5)
        assert "+" in problems[0]["question"]
        assert "-" in problems[1]["question"]
        assert "x" in problems[2]["question"]
        assert "/" in problems[3]["question"]
        assert "%" in problems[4]["question"]


# =========================================================================
# run_quiz  (fully mocked input)
# =========================================================================

class TestRunQuiz:
    @patch("builtins.input", side_effect=["10", "5", "20", "4", "50"])
    def test_returns_positive_integer_id(self, _mock_input):
        pokemon_id = run_quiz()
        assert isinstance(pokemon_id, int)
        assert pokemon_id >= 1

    @patch("builtins.input", side_effect=["10", "5", "20", "4", "50"])
    def test_id_formula(self, _mock_input):
        """sum(10+5+20+4+50) / 5 = 17.8 → round → 18"""
        pokemon_id = run_quiz()
        assert pokemon_id == 18

    @patch("builtins.input", side_effect=["0", "0", "0", "0", "0"])
    def test_all_zeros_still_returns_min_one(self, _mock_input):
        pokemon_id = run_quiz()
        assert pokemon_id == 1  # max(1, 0)

    @patch("builtins.input", side_effect=["bad", "abc", "10", "5", "20", "4", "50"])
    def test_retries_on_invalid_input(self, _mock_input):
        """Two bad inputs should be retried; quiz still completes."""
        pokemon_id = run_quiz()
        assert isinstance(pokemon_id, int)
        assert pokemon_id >= 1
