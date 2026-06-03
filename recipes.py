class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit
    

class Recipe:
    def __init__(self, title: str, ingredients=None):
        self.title = title
        self.ingredients = ingredients if ingredients is not None else []

    def add_ingredient(self, ingredient: Ingredient):
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0

    def scale(self, ratio: float):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Некорректный коэффициент")

        new_ingredients = []
        for ing in self.ingredients:
            new_ingredient = Ingredient(
            ing.name,
            ing.quantity * ratio,
            ing.unit
            )
            new_ingredients.append(new_ingredient)
            
        

        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        ingredients_text = "\n".join(
            str(ingredient) for ingredient in self.ingredients
        )
        return f"{self.title}\nИнгредиенты:\n{ingredients_text}"
    
class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")

        scaled_recipe = recipe.scale(portions)

        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [
            item for item in self._items
            if item[1] != title
        ]

    def get_list(self):
        result = {}

        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)

            if key in result:
                result[key] += ingredient.quantity
            else:
                result[key] = ingredient.quantity

        shopping_list = []
        for (name, unit), quantity in result.items():
            shopping_list.append(Ingredient(name, quantity, unit))

        shopping_list.sort(key=lambda ingredient: ingredient.name)
        
        return shopping_list

    def __add__(self, other):
        new_list = ShoppingList()

        new_list._items = self._items.copy() + other._items.copy()

        return new_list
    
class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        scaled_recipe = super().scale(ratio)

        return DietaryRecipe(
            self.title,
            self.diet_type,
            scaled_recipe.ingredients
        )

    def __str__(self):
        return f"[{self.diet_type}] " + super().__str__()