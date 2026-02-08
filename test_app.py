#!/usr/bin/env python3
"""
Простые тесты для CI/CD
"""

def test_addition():
    assert 1 + 1 == 2
    print("✅ test_addition passed")

def test_subtraction():
    assert 5 - 3 == 2
    print("✅ test_subtraction passed")

def test_calculator():
    from calculator import add, subtract
    assert add(10, 5) == 15
    assert subtract(10, 5) == 5
    print("✅ test_calculator passed")

if __name__ == "__main__":
    print("🧪 Запуск тестов...")
    test_addition()
    test_subtraction()
    test_calculator()
    print("🎉 Все тесты пройдены!")
