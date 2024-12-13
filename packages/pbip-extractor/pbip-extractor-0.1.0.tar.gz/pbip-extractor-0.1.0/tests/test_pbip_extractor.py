import pytest


class TestRetrieveCols:
    """
    Unit tests for the `_retrieve_cols` method in pbip_extractor.
    """

    @pytest.mark.parametrize(
        "input_string, expected_output",
        [
            # Regular Cases
            ("'Sales'[OrderID]", [["Sales", "OrderID"]]),
            ("Products[ProductName]", [["Products", "ProductName"]]),
            ("[Quantity]", [["UNKNOWN", "Quantity"]]),
            # Edge Cases
            # Edge Case 1: Empty string
            ("", []),
            # Edge Case 2: Missing closing bracket
            ("'Sales[OrderID'", []),
            # Edge Case 3: Missing opening bracket
            ("Sales]OrderID[", []),
            # Edge Case 4: Multiple references
            (
                "'Sales'[OrderID] and Products[ProductName]",
                [["Sales", "OrderID"], ["Products", "ProductName"]],
            ),
            # Edge Case 5: Nested brackets
            ("'Sales'[Order[ID]]", [["Sales", "Order[ID"]]),
            # Edge Case 6: Extra characters
            ("{ 'Sales'[OrderID] }", [["Sales", "OrderID"]]),
            # Edge Case 7: Quoted column names
            ("'Sales'['Order ID']", [["Sales", "Order ID"]]),
            # Edge Case 8: Brackets with no content
            (
                "'Customers'[CustomerID], Orders[OrderTotal], [Quantity]",
                [["Customers", "CustomerID"], ["Orders", "OrderTotal"], ["UNKNOWN", "Quantity"]],
            ),
            ("[]", []),
            # Edge Case 9: Special characters
            ("'S@les'[Order#ID]", [["S@les", "Order#ID"]]),
        ],
    )
    def test_retrieve_cols(self, extractor_instance, input_string, expected_output):
        """
        Test the `_retrieve_cols` method with various inputs, including regular and edge cases.
        """
        result = extractor_instance._retrieve_cols(input_string)
        assert result == expected_output, f"Failed for input: {input_string}"


class TestAddToTmdlDict:
    """
    Unit tests for the `_add_to_tmdl_dict` method in pbip_extractor.
    """

    @pytest.mark.parametrize(
        "tablename, colname, new_key, new_value, initial_tmdl_dict, expected_tmdl_dict",
        [
            # Regular Cases
            # Regular Case 1: Adding a new key-value pair to a new table and new column
            ("Orders", "OrderTotal", "is_related", True, {}, {"Orders": {"OrderTotal": {"is_related": True}}}),
            # Regular Case 2: Adding a new key-value pair to an existing table but a new column
            (
                "Customers",
                "CustomerName",
                "dataType",
                "String",
                {"Customers": {"CustomerID": {"is_primary_key": True}}},
                {"Customers": {"CustomerID": {"is_primary_key": True}, "CustomerName": {"dataType": "String"}}},
            ),
            # Regular Case 3: Adding a new key-value pair to a new table and new column
            ("Products", "Price", "dataType", "Decimal", {}, {"Products": {"Price": {"dataType": "Decimal"}}}),
            # Edge Cases
            # Edge Case 1: Adding with special characters in table and column names
            (
                "S@les",
                "Order#ID",
                "metadata",
                {"description": "Special chars"},
                {},
                {"S@les": {"Order#ID": {"metadata": {"description": "Special chars"}}}},
            ),
            # Edge Case 2: Adding multiple key-value pairs to the same table and column
            (
                "Customers",
                "CustomerID",
                "Datatype",
                "String",
                {"Customers": {"CustomerID": {"is_primary_key": True}}},
                {
                    "Customers": {
                        "CustomerID": {
                            "is_primary_key": True,
                            "Datatype": "String",
                        }
                    }
                },
            ),
            # Edge Case 3: Overwriting an existing key-value pair
            (
                "Customers",
                "CustomerID",
                "is_primary_key",
                False,
                {"Customers": {"CustomerID": {"is_primary_key": True}}},
                {"Customers": {"CustomerID": {"is_primary_key": False}}},
            ),
            # Edge Case 4: Adding to an existing table with multiple columns
            (
                "Orders",
                "OrderDate",
                "dataType",
                "Date",
                {
                    "Orders": {
                        "OrderTotal": {"is_related": True},
                    }
                },
                {"Orders": {"OrderTotal": {"is_related": True}, "OrderDate": {"dataType": "Date"}}},
            ),
            # Edge Case 5: Adding a key-value pair where new_value is None
            ("Inventory", "StockLevel", "nullable", None, {}, {"Inventory": {"StockLevel": {"nullable": None}}}),
        ],
    )
    def test_add_to_tmdl_dict(
        self, extractor_instance, tablename, colname, new_key, new_value, initial_tmdl_dict, expected_tmdl_dict
    ):
        """
        Test the `_add_to_tmdl_dict` method with various inputs, including regular and edge cases.
        """
        extractor_instance.tmdl_dict = initial_tmdl_dict

        extractor_instance._add_to_tmdl_dict(tablename, colname, new_key, new_value)

        assert extractor_instance.tmdl_dict == expected_tmdl_dict, (
            f"For input (tablename='{tablename}', colname='{colname}', "
            f"new_key='{new_key}', new_value='{new_value}'), "
            f"expected tmdl_dict to be {expected_tmdl_dict} but got {extractor_instance.tmdl_dict}"
        )

    def test_add_to_tmdl_dict_raises_value_error_empty_tablename(self, extractor_instance):
        """Test that parsing an empty string raises a ValueError."""
        input_data = ""

        # Configure the mock to raise ValueError when parsing an empty string
        extractor_instance.parse_json_string.side_effect = ValueError("Empty string is not valid JSON")

        with pytest.raises(ValueError) as exc_info:
            extractor_instance._parse_json_strings(input_data)

        assert str(exc_info.value) == "Empty string is not valid JSON"

        extractor_instance.parse_json_string.assert_called_once_with(input_data)

    def test_add_with_empty_tablename(self, extractor_instance):
        """Test that adding with an empty tablename raises a ValueError."""
        with pytest.raises(ValueError) as exc_info:
            extractor_instance._add_to_tmdl_dict(
                tablename="", colname="CustomerID", new_key="is_primary_key", new_value=True
            )
        assert str(exc_info.value) == "tablename must be a non-empty string."

    def test_add_with_non_string_tablename(self, extractor_instance):
        """Test that adding with a non-string tablename raises a ValueError."""
        with pytest.raises(ValueError) as exc_info:
            extractor_instance._add_to_tmdl_dict(
                tablename=123, colname="CustomerID", new_key="is_primary_key", new_value=True
            )
        assert str(exc_info.value) == "tablename must be a non-empty string."

    def test_add_with_empty_colname(self, extractor_instance):
        """Test that adding with an empty colname raises a ValueError."""
        with pytest.raises(ValueError) as exc_info:
            extractor_instance._add_to_tmdl_dict(
                tablename="Customers", colname="", new_key="is_primary_key", new_value=True
            )
        assert str(exc_info.value) == "colname must be a non-empty string."

    def test_add_with_non_string_colname(self, extractor_instance):
        """Test that adding with a non-string colname raises a ValueError."""
        with pytest.raises(ValueError) as exc_info:
            extractor_instance._add_to_tmdl_dict(
                tablename="Customers", colname=456, new_key="is_primary_key", new_value=True
            )
        assert str(exc_info.value) == "colname must be a non-empty string."

    def test_add_with_empty_new_key(self, extractor_instance):
        """Test that adding with an empty new_key raises a ValueError."""
        with pytest.raises(ValueError) as exc_info:
            extractor_instance._add_to_tmdl_dict(
                tablename="Customers", colname="CustomerID", new_key="", new_value=True
            )
        assert str(exc_info.value) == "new_key must be a non-empty string."

    def test_add_with_non_string_new_key(self, extractor_instance):
        """Test that adding with a non-string new_key raises a ValueError."""
        with pytest.raises(ValueError) as exc_info:
            extractor_instance._add_to_tmdl_dict(
                tablename="Customers", colname="CustomerID", new_key=789, new_value=True
            )
        assert str(exc_info.value) == "new_key must be a non-empty string."
