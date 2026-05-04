import pytest
from src.domain.entities.car import Car


class TestCarEntity:
    def test_create_car_success(self):
        car = Car.create(brand="BMW", model="X5", year=2024, price=50000)
        assert car.brand == "BMW"
        assert car.model == "X5"
        assert car.id is None

    def test_create_car_empty_brand_raises(self):
        with pytest.raises(ValueError, match="Brand cannot be empty"):
            Car.create(brand="", model="X5", year=2024, price=50000)

    def test_create_car_invalid_year_raises(self):
        with pytest.raises(ValueError, match="Invalid year"):
            Car.create(brand="BMW", model="X5", year=1800, price=50000)

    def test_create_car_negative_price_raises(self):
        with pytest.raises(ValueError, match="Price must be positive"):
            Car.create(brand="BMW", model="X5", year=2024, price=-100)

    def test_update_car_partial(self):
        car = Car.create(brand="BMW", model="X5", year=2024, price=50000)
        car.update(brand="Audi")
        assert car.brand == "Audi"
        assert car.model == "X5"
