import pytest

from recipes import DietaryRecipe, Ingredient, Recipe, ShoppingList


def test_ingredient_create():
    i = Ingredient("Мука", 500, "г")
    assert i.name == "Мука"
    assert i.quantity == 500.0
    assert i.unit == "г"


def test_ingredient_str():
    i = Ingredient("Мука", 500, "г")
    assert str(i) == "Мука: 500.0 г"


def test_ingredient_eq():
    assert Ingredient("Мука", 500, "г") == Ingredient("Мука", 200, "г")
    assert Ingredient("Мука", 500, "г") != Ingredient("Сахар", 500, "г")
    assert Ingredient("Мука", 500, "г") != Ingredient("Мука", 500, "кг")


def test_ingredient_bad_quantity():
    with pytest.raises(ValueError):
        Ingredient("Мука", 0, "г")


def test_recipe_create():
    r = Recipe("Пицца")
    assert r.title == "Пицца"
    assert r.ingredients == []


def test_recipe_add_ingredient():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 500, "г"))
    r.add_ingredient(Ingredient("Мука", 100, "г"))
    assert len(r) == 1
    assert r.ingredients[0].quantity == 600.0


def test_recipe_scale():
    r = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    new = r.scale(2)
    assert type(new) == Recipe
    assert new is not r
    assert new.ingredients[0].quantity == 1000.0
    assert r.ingredients[0].quantity == 500.0


def test_recipe_scale_bad_ratio():
    r = Recipe("Пицца")
    with pytest.raises(ValueError):
        r.scale(0)


def test_shopping_list_add_recipe():
    r = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    s = ShoppingList()
    s.add_recipe(r, 2)
    items = s.get_list()
    assert items[0].quantity == 1000.0


def test_shopping_list_bad_portions():
    s = ShoppingList()
    with pytest.raises(ValueError):
        s.add_recipe(Recipe("Пицца"), 0)


def test_shopping_list_remove_recipe():
    s = ShoppingList()
    s.add_recipe(Recipe("Пицца", [Ingredient("Мука", 500, "г")]), 1)
    s.remove_recipe("Пицца")
    s.remove_recipe("Нет")
    assert s.get_list() == []


def test_shopping_list_get_list():
    s = ShoppingList()
    s.add_recipe(Recipe("Пицца", [Ingredient("Мука", 500, "г")]), 1)
    s.add_recipe(Recipe("Кекс", [Ingredient("Мука", 200, "г")]), 1)
    s.add_recipe(Recipe("Кекс", [Ingredient("Яйцо", 2, "шт")]), 1)
    items = s.get_list()
    assert [i.name for i in items] == ["Мука", "Яйцо"]
    assert items[0].quantity == 700.0


def test_shopping_list_add():
    a = ShoppingList()
    b = ShoppingList()
    a.add_recipe(Recipe("Пицца", [Ingredient("Мука", 500, "г")]), 1)
    b.add_recipe(Recipe("Кекс", [Ingredient("Сахар", 100, "г")]), 1)
    c = a + b
    assert len(c.get_list()) == 2
    assert len(a.get_list()) == 1
    assert len(b.get_list()) == 1


def test_dietary_recipe():
    r = DietaryRecipe("Пицца", "веган", [Ingredient("Мука", 500, "г")])
    new = r.scale(2)
    assert type(new) == DietaryRecipe
    assert new.diet_type == "веган"
    assert str(r).startswith("[веган] Пицца")