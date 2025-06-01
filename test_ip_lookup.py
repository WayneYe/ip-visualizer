import pytest
import geoip2.database
import geoip2.errors
from unittest.mock import patch, MagicMock
from ip_lookup import lookup_ip


class MockGeoIP2City:
    """Mock class for geoip2.database.Reader"""
    def __init__(self, *args, **kwargs):
        pass
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        
    def city(self, ip):
        if ip == "8.8.8.8":  # Google's public DNS
            return self._create_mock_response(
                city_name="Mountain View",
                country_name="United States",
                latitude=37.40599,
                longitude=-122.078514,
                time_zone="America/Los_Angeles",
                postal_code="94043",
                continent_name="North America"
            )
        elif ip == "1.1.1.1":  # Cloudflare's DNS
            return self._create_mock_response(
                city_name="Los Angeles",
                country_name="United States",
                latitude=34.0522,
                longitude=-118.2437,
                time_zone="America/Los_Angeles",
                postal_code="90001",
                continent_name="North America"
            )
        else:
            raise geoip2.errors.AddressNotFoundError("The address 192.0.2.0 is not in the database.")
    
    @staticmethod
    def _create_mock_response(city_name, country_name, latitude, longitude, 
                            time_zone, postal_code, continent_name):
        response = MagicMock()
        
        # Create mock objects for nested attributes
        response.city = MagicMock()
        response.city.name = city_name
        
        response.country = MagicMock()
        response.country.name = country_name
        
        response.location = MagicMock()
        response.location.latitude = latitude
        response.location.longitude = longitude
        response.location.time_zone = time_zone
        
        response.postal = MagicMock()
        response.postal.code = postal_code
        
        response.continent = MagicMock()
        response.continent.name = continent_name
        
        return response


def test_lookup_ip_success():
    """Test successful IP lookup with known IP address."""
    with patch('geoip2.database.Reader', new=MockGeoIP2City):
        result = lookup_ip("8.8.8.8")
        
        assert result is not None
        assert result["ip"] == "8.8.8.8"
        assert result["city"] == "Mountain View"
        assert result["country"] == "United States"
        assert result["latitude"] == 37.40599
        assert result["longitude"] == -122.078514
        assert result["timezone"] == "America/Los_Angeles"
        assert result["postal_code"] == "94043"
        assert result["continent"] == "North America"


def test_lookup_ip_not_found():
    """Test IP lookup with an IP not in the database."""
    with patch('geoip2.database.Reader', new=MockGeoIP2City):
        result = lookup_ip("192.0.2.0")  # Test-Net IP address
        assert result is None


def test_lookup_ip_different_location():
    """Test IP lookup with a different known IP address."""
    with patch('geoip2.database.Reader', new=MockGeoIP2City):
        result = lookup_ip("1.1.1.1")
        
        assert result is not None
        assert result["ip"] == "1.1.1.1"
        assert result["city"] == "Los Angeles"
        assert result["country"] == "United States"
        assert result["postal_code"] == "90001"


@patch('geoip2.database.Reader')
def test_lookup_ip_database_error(mock_reader):
    """Test handling of database errors during IP lookup."""
    # Simulate a database read error
    mock_reader.return_value.__enter__.return_value.city.side_effect = Exception("Database read error")
    
    result = lookup_ip("8.8.8.8")
    assert result is None


if __name__ == "__main__":
    pytest.main(["-v"])
