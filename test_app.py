def add(a, b):
    return a + b

def test_add():
    assert add(2, 2) == 4
    print("✅ Test passed!")
    
if __name__ == "__main__":
    test_add()
