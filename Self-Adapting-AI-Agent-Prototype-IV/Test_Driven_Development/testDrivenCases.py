import sys
import os
# Add parent directory to Python path for imports to work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import ast
from Unit_Test.functions import generate_python_snake_game

def test_generate_code_happy_path_contains_required_elements():
    width = 600
    height = 400
    snake_block = 20
    snake_speed = 10
    bg_color = (0, 0, 0)
    snake_color = (0, 255, 0)
    food_color = (255, 0, 0)
    code = generate_python_snake_game(width, height, snake_block, snake_speed, bg_color, snake_color, food_color)
    assert isinstance(code, str)
    assert code.strip() != ""
    # Check Pygame imports and initialization
    assert "import pygame" in code
    assert "pygame.init()" in code
    # Check window setup with correct dimensions
    assert f"pygame.display.set_mode(({width}, {height}))" in code
    # Check snake block and speed usage
    assert str(snake_block) in code
    assert f"clock.tick({snake_speed})" in code
    # Check background, snake, and food colors embedded
    assert str(bg_color) in code
    assert str(snake_color) in code
    assert str(food_color) in code
    # Check main game loop and event handling
    assert "while not game_over" in code or "while True" in code
    assert "pygame.QUIT" in code
    # Check drawing functions for snake and food
    assert "pygame.draw.rect" in code
    # Assert code is syntactically valid
    compile(code, '<string>', 'exec')

def test_generate_code_edge_small_values():
    # Smallest valid window and snake block
    width = 20
    height = 20
    snake_block = 5
    snake_speed = 1
    bg_color = (255, 255, 255)
    snake_color = (0, 0, 0)
    food_color = (128, 128, 128)
    code = generate_python_snake_game(width, height, snake_block, snake_speed, bg_color, snake_color, food_color)
    assert isinstance(code, str) and code.strip()
    # Parse AST to ensure valid Python
    ast.parse(code)
    # Verify parameters reflected correctly
    assert f"set_mode(({width}, {height}))" in code
    assert f"clock.tick({snake_speed})" in code

def test_invalid_parameters_return_falsy():
    # Negative dimensions
    assert not generate_python_snake_game(-1, 400, 20, 10, (0,0,0), (0,255,0), (255,0,0))
    assert not generate_python_snake_game(600, -100, 20, 10, (0,0,0), (0,255,0), (255,0,0))
    # Zero dimensions
    assert not generate_python_snake_game(0, 0, 20, 10, (0,0,0), (0,255,0), (255,0,0))
    # Invalid types
    assert not generate_python_snake_game("600", 400, 20, 10, (0,0,0), (0,255,0), (255,0,0))
    assert not generate_python_snake_game(600, 400, "20", 10, (0,0,0), (0,255,0), (255,0,0))
    # Invalid color tuples
    assert not generate_python_snake_game(600, 400, 20, 10, (0,0), (0,255,0), (255,0,0))
    assert not generate_python_snake_game(600, 400, 20, 10, (0,0,0,0), (0,255,0), (255,0,0))
    # Color values out of range
    assert not generate_python_snake_game(600, 400, 20, 10, (256,0,0), (0,255,0), (255,0,0))
    assert not generate_python_snake_game(600, 400, 20, 10, (0,-1,0), (0,255,0), (255,0,0))

def test_idempotent_generation():
    params = (800, 600, 20, 15, (0, 0, 0), (0, 255, 0), (255, 0, 0))
    code1 = generate_python_snake_game(*params)
    code2 = generate_python_snake_game(*params)
    assert code1 == code2

def test_generated_code_executes_minimal_ast_checks():
    # Ensure AST contains a function definition or top-level code
    code = generate_python_snake_game(300, 300, 10, 5, (10,20,30), (40,50,60), (70,80,90))
    tree = ast.parse(code)
    # Expect at least one import node and one while or for loop
    import_nodes = [node for node in tree.body if isinstance(node, ast.Import)]
    assert any(alias.name == 'pygame' for node in import_nodes for alias in node.names)
    loop_nodes = [node for node in ast.walk(tree) if isinstance(node, (ast.While, ast.For))]
    assert loop_nodes
    # Check that display set_mode call exists in AST
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    assert any(getattr(node.func, 'attr', '') == 'set_mode' for node in calls)

if __name__ == "__main__":
    pytest.main([__file__])