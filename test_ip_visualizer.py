import pytest
from unittest.mock import patch, MagicMock, mock_open
from ip_visualizer import load_ip_data, get_ip_locations, create_heatmap


# Test data
TEST_CSV_DATA = """_source.cg.detail.remote_addr,other_field
8.8.8.8,test1
1.1.1.1,test2
8.8.8.8,test3
192.168.1.1,test4
"""

# Mock GeoIP2 response
def create_mock_geoip_response(ip):
    mock_response = MagicMock()
    mock_response.location = MagicMock()
    
    if ip == "8.8.8.8":
        mock_response.location.latitude = 37.40599
        mock_response.location.longitude = -122.078514
    elif ip == "1.1.1.1":
        mock_response.location.latitude = 34.0522
        mock_response.location.longitude = -118.2437
    else:
        mock_response.location.latitude = None
        mock_response.location.longitude = None
    
    return mock_response


def test_load_ip_data():
    """Test loading IP addresses from a CSV file."""
    # Create a mock file object with our test data
    with patch('pandas.read_csv') as mock_read_csv:
        # Setup mock return value
        mock_df = MagicMock()
        mock_df.__getitem__.return_value.dropna.return_value.unique.return_value = ["8.8.8.8", "1.1.1.1"]
        mock_read_csv.return_value = mock_df
        
        # Call the function with a dummy filename
        result = load_ip_data("dummy.csv")
        
        # Verify the result
        assert len(result) == 2
        assert "8.8.8.8" in result
        assert "1.1.1.1" in result


@patch('ip_visualizer.geoip2.database.Reader')
def test_get_ip_locations_success(mock_reader):
    """Test successful IP to location conversion."""
    # Setup mock reader
    mock_reader_instance = MagicMock()
    mock_reader.return_value.__enter__.return_value = mock_reader_instance
    
    # Configure the mock to return different responses based on IP
    def mock_city(ip):
        return create_mock_geoip_response(ip)
    
    mock_reader_instance.city.side_effect = mock_city
    
    # Test data
    test_ips = ["8.8.8.8", "1.1.1.1"]
    
    # Call the function
    locations, ip_counts = get_ip_locations(test_ips)
    
    # Verify results
    assert len(locations) == 2
    assert len(ip_counts) == 2
    assert (37.40599, -122.078514) in ip_counts
    assert (34.0522, -118.2437) in ip_counts
    assert ip_counts[(37.40599, -122.078514)] == 1


@patch('ip_visualizer.geoip2.database.Reader')
def test_get_ip_locations_invalid_ip(mock_reader):
    """Test handling of invalid IP addresses."""
    # Setup mock reader to raise an exception for invalid IPs
    mock_reader_instance = MagicMock()
    mock_reader.return_value.__enter__.return_value = mock_reader_instance
    mock_reader_instance.city.side_effect = Exception("Invalid IP")
    
    # Test with an invalid IP
    locations, ip_counts = get_ip_locations(["invalid.ip"])
    
    # Verify no locations were returned
    assert len(locations) == 0
    assert len(ip_counts) == 0


def test_create_heatmap():
    """Test creation of heatmap (basic verification)."""
    # Setup test data
    locations = [(37.7749, -122.4194), (34.0522, -118.2437)]
    ip_counts = {
        (37.7749, -122.4194): 5,
        (34.0522, -118.2437): 3
    }
    
    # Create a mock for the HeatMap class
    mock_heatmap_instance = MagicMock()
    
    # Mock folium.Map and HeatMap
    with patch('folium.Map') as mock_map, \
         patch('ip_visualizer.HeatMap', return_value=mock_heatmap_instance) as mock_heatmap:
        # Setup mock map
        mock_map_instance = MagicMock()
        mock_map.return_value = mock_map_instance
        
        # Call the function
        create_heatmap(locations, ip_counts)
        
        # Verify the map was created with correct parameters
        mock_map.assert_called_once()
        
        # Verify heatmap was created with correct data
        expected_heat_data = [
            [37.7749, -122.4194, 5],
            [34.0522, -118.2437, 3]
        ]
        mock_heatmap.assert_called_once_with(expected_heat_data)
        
        # Verify heatmap was added to the map
        mock_heatmap_instance.add_to.assert_called_once_with(mock_map_instance)
        
        # Verify the map was saved
        mock_map_instance.save.assert_called_once_with("ip_heatmap.html")


@patch('builtins.open', new_callable=mock_open)
@patch('pandas.read_csv')
def test_main_with_mock_data(mock_read_csv, mock_file):
    """Test the main function with mocked data."""
    # Setup mock data
    mock_df = MagicMock()
    mock_df.__getitem__.return_value.dropna.return_value.unique.return_value = ["8.8.8.8", "1.1.1.1"]
    mock_read_csv.return_value = mock_df
    
    # Mock the rest of the dependencies
    with patch('ip_visualizer.generate_ip_list') as mock_gen_ips, \
         patch('ip_visualizer.get_ip_locations') as mock_get_locations, \
         patch('ip_visualizer.create_heatmap') as mock_create_heatmap, \
         patch('sys.argv', ['ip_visualizer.py', 'test.csv']):
        
        # Setup mock return values
        mock_gen_ips.return_value = ["8.8.8.8", "1.1.1.1"]
        mock_get_locations.return_value = ([(37.7749, -122.4194)], {(37.7749, -122.4194): 1})
        
        # Import and run main
        from ip_visualizer import main
        main()
        
        # Verify the heatmap creation was attempted
        mock_create_heatmap.assert_called_once()


if __name__ == "__main__":
    pytest.main(["-v"])
