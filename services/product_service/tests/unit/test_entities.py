from catalog.domain.entities import Category, Product


def test_product_in_stock_flag_reflects_quantity() -> None:
    product = Product.create(
        name="Wireless Headphones",
        slug="wireless-headphones",
        description="Bluetooth",
        price=79.99,
        category_id="cat-1",
        stock_quantity=10,
    )
    assert product.is_in_stock is True


def test_product_out_of_stock_flag_reflects_quantity() -> None:
    product = Product.create(
        name="Wireless Headphones",
        slug="wireless-headphones",
        description="Bluetooth",
        price=79.99,
        category_id="cat-1",
        stock_quantity=0,
    )
    assert product.is_in_stock is False


def test_category_child_relationship() -> None:
    parent = Category.create(name="Electronics", slug="electronics")
    child = Category.create(name="Audio", slug="audio", parent_id=parent.id)
    assert child.parent_id == parent.id
