import unittest
from proj1 import *
#proj1.py should contain your data class and function definitions
#these do not contribute positivly to your grade. 
#but your grade will be lowered if they are missing




class TestRegionFunctions(unittest.TestCase):

    def test_emissions_per_capita_normal(self):
        rc = RegionCondition(
            region=Region(
                rect=GlobeRect(0.0, 1.0, 0.0, 1.0),
                name="Test City",
                terrain="other"
            ),
            year=2020,
            pop=100,
            ghg_rate=250.0
        )
        self.assertAlmostEqual(emissions_per_capita(rc), 2.5, places=4)

    def test_emissions_per_capita_zero_pop(self):
        rc = RegionCondition(
            region=Region(
                rect=GlobeRect(0.0, 1.0, 0.0, 1.0),
                name="Empty Region",
                terrain="ocean"
            ),
            year=2020,
            pop=0,
            ghg_rate=100.0
        )
        self.assertAlmostEqual(emissions_per_capita(rc), 0.0, places=4)

    def test_area_positive(self):
        gr = GlobeRect(0.0, 1.0, 0.0, 1.0)
        self.assertTrue(area(gr) > 0)

    def test_area_wraparound_positive(self):
        gr = GlobeRect(-10.0, 10.0, 170.0, -170.0)
        self.assertTrue(area(gr) > 0)

    def test_area_zero_exact(self):
        gr = GlobeRect(5.0, 5.0, 10.0, 10.0)
        self.assertAlmostEqual(area(gr), 0.0, places=4)

    def test_emissions_per_square_km_normal(self):
        rc = region_conditions[0]
        expected = rc.ghg_rate / area(rc.region.rect)
        self.assertAlmostEqual(emissions_per_square_km(rc), expected, places=4)

    def test_get_density_normal(self):
        rc = region_conditions[1]
        expected = rc.pop / area(rc.region.rect)
        self.assertAlmostEqual(get_density(rc), expected, places=4)

    def test_get_density_zero_area_case_safe(self):
        rc = RegionCondition(
            region=Region(
                rect=GlobeRect(5.0, 5.0, 10.0, 10.0),
                name="Zero Area Region",
                terrain="other"
            ),
            year=2020,
            pop=1000,
            ghg_rate=500.0
        )
        self.assertAlmostEqual(get_density(rc), 0.0, places=4)

    def test_densest_returns_string(self):
        result = densest(region_conditions)
        self.assertTrue(isinstance(result, str))

    def test_densest_custom(self):
        big_area = RegionCondition(
            region=Region(
                rect=GlobeRect(0.0, 10.0, 0.0, 10.0),
                name="Big Sparse",
                terrain="other"
            ),
            year=2020,
            pop=1000,
            ghg_rate=100.0
        )
        small_area = RegionCondition(
            region=Region(
                rect=GlobeRect(0.0, 1.0, 0.0, 1.0),
                name="Small Dense",
                terrain="other"
            ),
            year=2020,
            pop=1000,
            ghg_rate=100.0
        )
        self.assertEqual(densest([big_area, small_area]), "Small Dense")

    def test_densest_single_region(self):
        only = RegionCondition(
            region=Region(
                rect=GlobeRect(0.0, 2.0, 0.0, 2.0),
                name="Only Region",
                terrain="forest"
            ),
            year=2020,
            pop=500,
            ghg_rate=50.0
        )
        self.assertEqual(densest([only]), "Only Region")

    def test_growth_rate_ocean(self):
        self.assertAlmostEqual(growth_rate("ocean"), 0.0001, places=8)

    def test_growth_rate_mountains(self):
        self.assertAlmostEqual(growth_rate("mountains"), 0.0005, places=8)

    def test_growth_rate_forest(self):
        self.assertAlmostEqual(growth_rate("forest"), -0.00001, places=8)

    def test_growth_rate_other(self):
        self.assertAlmostEqual(growth_rate("other"), 0.0003, places=8)

    def test_project_condition_year(self):
        rc = region_conditions[0]
        projected = project_condition(rc, 5)
        self.assertEqual(projected.year, rc.year + 5)

    def test_project_condition_region_unchanged(self):
        rc = region_conditions[0]
        projected = project_condition(rc, 5)
        self.assertEqual(projected.region, rc.region)

    def test_project_condition_changes_population(self):
        rc = region_conditions[1]
        projected = project_condition(rc, 10)
        self.assertNotEqual(projected.pop, rc.pop)

    def test_project_condition_zero_population(self):
        rc = RegionCondition(
            region=Region(
                rect=GlobeRect(0.0, 1.0, 0.0, 1.0),
                name="Zero Pop",
                terrain="ocean"
            ),
            year=2020,
            pop=0,
            ghg_rate=500.0
        )
        projected = project_condition(rc, 10)
        self.assertEqual(projected.pop, 0)
        self.assertAlmostEqual(projected.ghg_rate, 0.0, places=4)

    def test_project_condition_zero_years(self):
        rc = region_conditions[0]
        projected = project_condition(rc, 0)
        self.assertEqual(projected.year, rc.year)
        self.assertEqual(projected.region, rc.region)
        self.assertEqual(projected.pop, rc.pop)
        self.assertAlmostEqual(projected.ghg_rate, rc.ghg_rate, places=4)


if __name__ == "__main__":
    unittest.main()
