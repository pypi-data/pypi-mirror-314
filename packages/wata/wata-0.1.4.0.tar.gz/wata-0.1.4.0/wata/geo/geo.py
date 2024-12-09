from wata.geo.utils import utils, coord_trans

class GeoProcess:
    
    @staticmethod
    def WGS84_to_GCJ02(lat, lon):
        '''
        **功能描述**: WGS84_to_GCJ02  
        
        Args:
            lat: WGS84坐标系的纬度  
            lon: WGS84坐标系的经度  

        Returns:
            GCJ02坐标系的纬度,GCJ02坐标系的经度  
        '''
        return coord_trans.WGS84_to_GCJ02(lat, lon)
    @staticmethod
    def WGS84_to_BD09(lat, lon):
        '''
        **功能描述**: WGS84_to_BD09  
        
        Args:
            lat: WGS84坐标系的纬度  
            lon: WGS84坐标系的经度  

        Returns:
            BD09坐标系的纬度,BD09坐标系的经度  
        '''
        return coord_trans.WGS84_to_BD09(lat, lon)
    @staticmethod
    def WGS84_to_UTM(lat:float, lon:float):
        '''
        **功能描述**: WGS84_to_UTM  
        
        Args:
            lat: WGS84坐标系的纬度  
            lon: WGS84坐标系的经度  

        Returns:
            UTM坐标  
        '''
        return coord_trans.WGS84_to_UTM(lat, lon)

    @staticmethod
    def GCJ02_to_WGS84(lat, lon):
        '''
        **功能描述**: GCJ02_to_WGS84  
        
        Args:
            lat: GCJ02坐标系的纬度  
            lon: GCJ02坐标系的经度  

        Returns:  
            WGS84坐标系的纬度,WGS84坐标系的经度  
        '''
        return coord_trans.GCJ02_to_WGS84(lat, lon)
    @staticmethod
    def GCJ02_to_BD09(lat, lon):
        '''
        **功能描述**: GCJ02_to_BD09  
        
        Args:  
            lat: GCJ02坐标系的纬度  
            lon: GCJ02坐标系的经度  

        Returns:  
            BD09坐标系的纬度,BD09坐标系的经度  
        '''
        return coord_trans.GCJ02_to_BD09(lat, lon)

    @staticmethod
    def BD09_to_GCJ02(lat, lon):
        '''
        **功能描述**: BD09_to_GCJ02  
        
        Args:
            lat: BD09坐标系的纬度  
            lon: BD09坐标系的经度  

        Returns:
            GCJ02坐标系的纬度,GCJ02坐标系的经度  
        '''
        return coord_trans.BD09_to_GCJ02(lat, lon)
    @staticmethod
    def BD09_to_WGS84(lat, lon):
        '''
        **功能描述**: BD09_to_WGS84  
        
        Args:
            lat: BD09坐标系的纬度  
            lon: BD09坐标系的经度  

        Returns:
            WGS84坐标系的纬度,WGS84坐标系的经度  
        '''
        return coord_trans.BD09_to_WGS84(lat, lon)
    
    @staticmethod
    def UTM_to_WGS84(easting, northing, zone_number, zone_letter):
        '''
        **功能描述**: UTM_to_WGS84  
        
        Args:  
            easting:  
            northing:  
            zone_number: 区域ID  
            zone_letter:  

        Returns:
            WGS84坐标系的纬度,WGS84坐标系的经度  
        '''
        return coord_trans.UTM_to_WGS84(easting, northing, zone_number, zone_letter)