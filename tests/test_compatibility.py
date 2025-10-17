"""Test compatibility across different API versions using external fixtures"""

from kenallclient.models import (
    compatible,
    v20221101,
    v20250101,
)


class TestAddressCompatibility:
    """Test Address model compatibility across versions"""

    def test_v20221101_address_loads_in_compatible(self, postalcode_v20221101):
        """Test that v2022-11-01 address data loads in compatible model"""
        address_data = postalcode_v20221101["data"][0]
        address = compatible.Address.fromdict(address_data)

        # Check common fields
        assert address.postal_code == "1008105"
        assert address.prefecture == "東京都"
        assert address.city == "千代田区"
        assert address.town == "大手町"

        # Check romanization fields are populated
        assert address.prefecture_roman == "Tokyo"
        assert address.city_roman == "Chiyoda-ku"
        assert address.town_roman == "Otemachi"
        assert address.city_ward == ""
        assert address.city_ward_roman == ""
        assert address.update_status == 0
        assert address.update_reason == 0

    def test_compatible_address_handles_unknown_fields(self, postalcode_v20221101):
        """Test that compatible Address ignores unknown fields"""
        address_data = dict(postalcode_v20221101["data"][0])
        address_data["unknown_field"] = "some value"
        address_data["future_field"] = 123

        # Should not raise an error
        address = compatible.Address.fromdict(address_data)
        assert address.postal_code == "1008105"

        # Unknown fields should not be in the object
        assert not hasattr(address, "unknown_field")
        assert not hasattr(address, "future_field")

    def test_version_specific_models_strict(self, postalcode_v20221101):
        """Test that version-specific models work with their respective data"""
        # v2022-11-01 model with v2022-11-01 data
        address_data_20221101 = postalcode_v20221101["data"][0]
        address_20221101 = v20221101.Address.fromdict(address_data_20221101)
        assert address_20221101.postal_code == "1008105"
        assert address_20221101.prefecture_roman == "Tokyo"


class TestCityCompatibility:
    """Test City model compatibility across versions"""

    def test_v20221101_city_loads_in_compatible(self, city_v20221101):
        """Test that v2022-11-01 city data loads in compatible model"""
        city_data = city_v20221101["data"][0]
        city = compatible.City.fromdict(city_data)

        assert city.jisx0402 == "13101"
        assert city.prefecture == "東京都"
        assert city.city == "千代田区"

        # Romanization fields should be populated
        assert city.prefecture_roman == "Tokyo"
        assert city.city_roman == "Chiyoda-ku"


class TestNTACorporateInfoCompatibility:
    """Test NTACorporateInfo model compatibility across versions"""

    def test_string_close_cause_loads_in_compatible(self, houjinbangou_v20240101):
        """Test that string close_cause loads in compatible model"""
        corp_data = houjinbangou_v20240101["data"]
        info = compatible.NTACorporateInfo.fromdict(corp_data)

        assert info.corporate_number == "1234567890123"
        assert info.name == "テスト株式会社"
        # In 2024-01-01, close_cause might be numeric, so when converted to compatible
        # it becomes string
        assert isinstance(info.close_cause, str)

    def test_numeric_close_cause_converts_to_string(self, houjinbangou_v20250101):
        """Test that numeric close_cause converts to string in compatible model"""
        corp_data = houjinbangou_v20250101["data"]
        info = compatible.NTACorporateInfo.fromdict(corp_data)

        assert info.corporate_number == "1234567890123"
        assert info.name == "テスト株式会社"
        assert info.close_cause == "1"  # Should convert to string
        assert isinstance(info.close_cause, str)

    def test_v20250101_model_keeps_numeric(self, houjinbangou_v20250101):
        """Test that v2025-01-01 model keeps close_cause as integer"""
        corp_data = houjinbangou_v20250101["data"]
        info = v20250101.NTACorporateInfo.fromdict(corp_data)

        assert info.corporate_number == "1234567890123"
        assert info.name == "テスト株式会社"
        assert info.close_cause == 1  # Should remain integer
        assert isinstance(info.close_cause, int)

    def test_resolver_response_compatibility(
        self, houjinbangou_v20240101, houjinbangou_v20250101
    ):
        """Test resolver response handles both string and numeric close_cause"""
        # Response with 2024-01-01 format (should convert to string in compatible mode)
        response_str = compatible.NTACorporateInfoResolverResponse.fromdict(
            houjinbangou_v20240101
        )
        assert isinstance(response_str.data.close_cause, str)

        # Response with numeric close_cause (should convert)
        response_num = compatible.NTACorporateInfoResolverResponse.fromdict(
            houjinbangou_v20250101
        )
        assert response_num.data.close_cause == "1"
        assert isinstance(response_num.data.close_cause, str)

    def test_search_response_v20230901(self, houjinbangou_search_v20230901):
        """Test v2023-09-01 search response loads correctly"""
        response = compatible.NTACorporateInfoSearcherResponse.fromdict(
            houjinbangou_search_v20230901
        )
        assert response.version == "2023-09-01"
        assert response.count == 3
        assert len(response.data) == 3

        # Check data structure (should still be strings in 2023-09-01)
        assert response.data[0].corporate_number == "1234567890123"
        assert response.data[0].sequence_number == "1"
        assert isinstance(response.data[0].sequence_number, str)

    def test_search_response_v20240101(self, houjinbangou_search_v20240101):
        """Test v2024-01-01 search response loads correctly"""
        response = compatible.NTACorporateInfoSearcherResponse.fromdict(
            houjinbangou_search_v20240101
        )
        assert response.version == "2024-01-01"
        assert response.count == 3
        assert len(response.data) == 3

        # In compatible mode, numeric types convert to strings
        assert response.data[0].corporate_number == "1234567890123"
        assert response.data[0].sequence_number == "1"
        assert isinstance(response.data[0].sequence_number, str)
        assert response.data[0].kind == "301"
        assert isinstance(response.data[0].kind, str)

        # Check address object exists
        assert (
            hasattr(response.data[0], "address")
            or response.data[0].prefecture_name is not None
        )

    def test_search_response_v20250101(self, houjinbangou_search_v20250101):
        """Test v2025-01-01 search response loads correctly"""
        response = compatible.NTACorporateInfoSearcherResponse.fromdict(
            houjinbangou_search_v20250101
        )
        assert response.version == "2025-01-01"
        assert response.count == 3
        assert len(response.data) == 3

        # In compatible mode, numeric types convert to strings
        assert response.data[0].corporate_number == "1234567890123"
        assert response.data[0].sequence_number == "1"
        assert isinstance(response.data[0].sequence_number, str)

        # close_cause should convert from number to string
        closed_corp = response.data[2]
        assert closed_corp.close_cause == "11"
        assert isinstance(closed_corp.close_cause, str)

    def test_search_response_with_explicit_version(self, houjinbangou_search_v20250101):
        """Test search response with explicit API version parameter"""
        # Using compatible model with explicit version
        response = compatible.NTACorporateInfoSearcherResponse.fromdict(
            houjinbangou_search_v20250101, api_version="2025-01-01"
        )
        assert response.version == "2025-01-01"
        assert response.count == 3

        # Even with explicit version, compatible model converts to strings
        assert isinstance(response.data[0].sequence_number, str)
        assert isinstance(response.data[0].kind, str)

    def test_search_response_api_version_propagates_to_children(
        self, houjinbangou_search_v20250101
    ):
        """Test that api_version is correctly propagated to child
        NTACorporateInfo.fromdict() calls"""
        # When we explicitly pass api_version to the searcher response,
        # it should be propagated to each NTACorporateInfo item in the data list
        response = compatible.NTACorporateInfoSearcherResponse.fromdict(
            houjinbangou_search_v20250101, api_version="2025-01-01"
        )

        # Verify that all items in data were processed with the correct api_version
        # In v2025-01-01 format, the data has 'address' object that should be flattened
        for corp_info in response.data:
            # These fields should exist because api_version was properly propagated
            # and the v2025-01-01 logic was applied
            assert hasattr(corp_info, "prefecture_name")
            assert corp_info.prefecture_name is not None

            # sequence_number and kind should be strings
            # (converted from int in v2025-01-01)
            assert isinstance(corp_info.sequence_number, str)
            assert isinstance(corp_info.kind, str)

        # Verify close_cause is converted to string in compatible model
        closed_corp = response.data[2]
        assert closed_corp.close_cause == "11"
        assert isinstance(closed_corp.close_cause, str)


class TestBankModelsCompatibility:
    """Test bank models (v2023-09-01+)"""

    def test_bank_model(self, bank_v20230901):
        """Test Bank model"""
        bank_data = bank_v20230901["data"]
        bank = compatible.Bank.fromdict(bank_data)
        assert bank.code == "0001"
        assert bank.name == "みずほ銀行"
        assert bank.romaji == "mizuho"

    def test_banks_response(self, banks_v20230901):
        """Test BanksResponse model"""
        response = compatible.BanksResponse.fromdict(banks_v20230901)
        assert response.version == "2023-09-01"
        assert len(response.data) == 3
        assert response.data[0].code == "0001"
        assert response.data[0].name == "みずほ銀行"
        assert response.data[1].code == "0005"
        assert response.data[1].name == "三菱UFJ銀行"

    def test_bank_branch_model(self, bank_branch_v20230901):
        """Test BankBranch model"""
        branch_data = bank_branch_v20230901["data"]["branch"]
        branch = compatible.BankBranch.fromdict(branch_data)
        assert branch.code == "001"
        assert branch.name == "東京営業部"
        assert branch.romaji == "tokyo"

    def test_bank_branches_response(self, bank_branches_v20230901):
        """Test BankBranchesResponse model"""
        response = compatible.BankBranchesResponse.fromdict(bank_branches_v20230901)
        assert response.version == "2023-09-01"
        assert len(response.data) == 3
        assert response.data["001"][0].code == "001"
        assert response.data["001"][0].name == "東京営業部"


class TestInvoiceModelsCompatibility:
    """Test invoice issuer models (v2024-01-01+)"""

    def test_invoice_issuer_model(self, invoice_issuer_v20240101):
        """Test NTAQualifiedInvoiceIssuerInfo model"""
        issuer_data = invoice_issuer_v20240101["data"]
        issuer = compatible.NTAQualifiedInvoiceIssuerInfo.fromdict(issuer_data)
        assert issuer.qualified_invoice_issuer_number == "T1234567890123"
        assert issuer.name == "テスト株式会社"
        assert issuer.address.prefecture == "東京都"
        assert issuer.address.city == "千代田区"
        assert issuer.address.street_number == "大手町１丁目１番１号"

    def test_invoice_issuer_response(self, invoice_issuer_v20240101):
        """Test NTAQualifiedInvoiceIssuerInfoResolverResponse model"""
        response = compatible.NTAQualifiedInvoiceIssuerInfoResolverResponse.fromdict(
            invoice_issuer_v20240101
        )
        assert response.version == "2024-01-01"
        assert response.data.qualified_invoice_issuer_number == "T1234567890123"
        assert response.data.trade_name == "Test Corporation"


class TestHolidayModelsCompatibility:
    """Test holiday models (same across all versions)"""

    def test_holiday_model(self):
        """Test Holiday model with inline data"""
        holiday = compatible.Holiday.fromdict(
            {
                "title": "元日",
                "date": "2024-01-01",
                "day_of_week": 1,
                "day_of_week_text": "monday",
            }
        )
        assert holiday.title == "元日"
        assert holiday.date == "2024-01-01"
        assert holiday.day_of_week == 1
        assert holiday.day_of_week_text == "monday"

    def test_holiday_search_result(self, dummy_holiday_search_json):
        """Test HolidaySearchResult model using existing fixture"""
        result = compatible.HolidaySearchResult.fromdict(dummy_holiday_search_json)
        assert len(result.data) > 0
        assert result.data[0].title == "元日"
        assert result.data[0].date == "2022-01-01"


class TestFactoryCompatibility:
    """Test factory functions with version-specific fixtures"""

    def test_address_factory_with_different_versions(self, postalcode_v20221101):
        """Test address factory handles different version data"""
        from kenallclient.models.factories import create_address_resolver_response

        # Test with v2022-11-01 data
        response_20221101 = create_address_resolver_response(postalcode_v20221101)
        assert isinstance(response_20221101, compatible.AddressResolverResponse)
        assert response_20221101.data[0].prefecture_roman == "Tokyo"

    def test_corporate_info_factory_handles_type_conversion(
        self, houjinbangou_v20240101, houjinbangou_v20250101
    ):
        """Test corporate info factory handles close_cause type conversion"""
        from kenallclient.models.factories import (
            create_corporate_info_resolver_response,
        )

        # 2024-01-01 should convert to string in compatible mode
        response_str = create_corporate_info_resolver_response(houjinbangou_v20240101)
        assert isinstance(response_str.data.close_cause, str)

        # Numeric close_cause should convert to string in compatible mode
        response_num = create_corporate_info_resolver_response(houjinbangou_v20250101)
        assert response_num.data.close_cause == "1"
        assert isinstance(response_num.data.close_cause, str)

        # But stay numeric when using v2025-01-01 specific version
        response_v2025 = create_corporate_info_resolver_response(
            houjinbangou_v20250101, api_version="2025-01-01"
        )
        assert response_v2025.data.close_cause == 1
        assert isinstance(response_v2025.data.close_cause, int)
