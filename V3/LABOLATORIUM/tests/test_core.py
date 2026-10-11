"""Małe testy błędów istotnych naukowo. Uruchom: python -m unittest discover -s tests"""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from landsat_lab import normalized_difference,quality_mask,read_metadata,classify_land_cover,class_stats,CLASS_NODATA,ROOT
class CoreTests(unittest.TestCase):
 def test_signed_zero_and_invalid(self):
  out=normalized_difference(np.array([.6,.2,.2,0,np.nan]),np.array([.2,.6,.2,0,.1]))
  np.testing.assert_allclose(out[:3],[.5,-.5,0],atol=1e-6)
  self.assertTrue(np.isnan(out[3:]).all())
 def test_no_silent_clipping(self):
  self.assertAlmostEqual(float(normalized_difference(np.array([.3]),np.array([-.1]))[0]),2,places=5)
 def test_qa_water_is_not_nodata(self):
  qa=np.array([2,4,1,8,16,32,3<<8,1024],dtype='uint16')
  np.testing.assert_array_equal(quality_mask(qa,np.zeros_like(qa)),[1,1,0,0,0,0,0,0])
 def test_saturation_relevant_bands(self):
  sat=np.array([0,1,1<<4,1<<10],dtype='uint16')
  np.testing.assert_array_equal(quality_mask(np.full(4,2,dtype='uint16'),sat),[1,0,0,1])
 def test_metadata_scaling(self):
  m=read_metadata(ROOT/'data/scene')
  self.assertEqual(m['date'],'2013-08-07')
  self.assertEqual(m['bands']['sr_band5']['scale'],.0001)
 def test_land_cover_classes(self):
  # woda, roslinnosc, zabudowa, inne, woda ma pierwszenstwo przed roslinnoscia, brak danych
  ind={'MNDWI':np.array([.4,-.3,-.3,-.3,.2,np.nan]),'NDVI':np.array([0,.6,.1,.1,.6,.5]),'NDBI':np.array([-.2,-.2,.15,-.1,-.2,0])}
  c=classify_land_cover(ind)
  np.testing.assert_array_equal(c,[1,2,3,0,1,CLASS_NODATA])
  self.assertAlmostEqual(sum(s['percent'] for s in class_stats(c)),100,places=1)
if __name__=='__main__':unittest.main()
