import unittest
import wkbheader

'''
Testwkbs extracted from Postgis 2.0.3
'''

class WKBHeaderTest(unittest.TestCase):
    def setUp(self):
        self.point_wgs84 = "0101000020E610000000000000000008400000000000001040".decode('hex')#point(3, 4), 4326 Little endian
        self.point_google = "010100002031BF0D0000000000000008400000000000001040".decode('hex')#point(3, 4), 900913 Little endian
        self.point_nosrid = "010100000000000000000008400000000000001040".decode('hex')#point(3, 4), Little endian no srid

        self.geocol_line_poly_wgs84 = \
            "01030000A0E6100000010000000400000000000000000024400000000000000840000000000000004000000000000010400000000000001C400000000000002040000000000000084000000000000022400000000000002840000000000000244000000000000008400000000000000040".decode('hex')
        self.geocol_line_poly_nosrid = \
            "0103000080010000000400000000000000000024400000000000000840000000000000004000000000000010400000000000001C400000000000002040000000000000084000000000000022400000000000002840000000000000244000000000000008400000000000000040".decode('hex')

        self.point_nosrid_bigendian = "000000000140000000000000004010000000000000".decode('hex')

    def tearDown(self):
        pass

    def test_get_endian(self):
        assert wkbheader.has_little_endian(self.point_nosrid)
        assert wkbheader.has_little_endian(self.point_google)
        assert not wkbheader.has_little_endian(self.point_nosrid_bigendian)

    def test_has_srid(self):
        assert wkbheader._has_srid(wkbheader._get_type(self.point_google, wkbheader._LITTLE_ENDIAN))
        assert not wkbheader._has_srid(wkbheader._get_type(self.point_nosrid, wkbheader._LITTLE_ENDIAN))

    def test_get_srid(self):
        assert wkbheader.get_srid(self.point_nosrid) is None
        assert wkbheader.get_srid(self.point_google) == 900913
        assert wkbheader.get_srid(self.point_wgs84) == 4326

    def test_endian_types(self):
        assert wkbheader.get_type_int(self.point_nosrid) == wkbheader.get_type_int(self.point_nosrid_bigendian)

    def test_drop_srid_from_type(self):
        point_with_srid_type = 536870913
        point_without_srid = 1
        assert wkbheader._drop_type_srid(point_with_srid_type) == point_without_srid

    def test_drop_srid(self):
        assert wkbheader.drop_srid(self.point_nosrid) == self.point_nosrid
        assert wkbheader.drop_srid(self.point_google) == self.point_nosrid
        assert wkbheader.drop_srid(self.point_wgs84) == self.point_nosrid

    def test_create_srid(self):
        assert wkbheader.set_srid(self.point_nosrid, 4326) == self.point_wgs84
        assert wkbheader.set_srid(self.point_nosrid, 900913) == self.point_google

    def test_replace_srid(self):
        assert wkbheader.set_srid(self.point_google, 4326) == self.point_wgs84
        assert wkbheader.set_srid(self.point_wgs84, 900913) == self.point_google

    def test_geocollection_change_srid(self):
        assert wkbheader.drop_srid(self.geocol_line_poly_wgs84) == self.geocol_line_poly_nosrid
        assert wkbheader.set_srid(self.geocol_line_poly_nosrid, 4326) == self.geocol_line_poly_wgs84


if __name__ == '__main__':
    unittest.main()
