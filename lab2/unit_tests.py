import unittest
import types 
import io
from tests.testsObjects import TestClass, test_func, x, fact, d, dct
from serializers.src.serializer_creator import Creator

class TestPacker(unittest.TestCase):
    def setUp(self):
        self.f = io.StringIO()
        self.serializer = Creator.create_serializer('json')
        self.serializer = Creator.create_serializer('json', 4)
        self.deserializer = Creator.create_deserializer('json')
        self.obj = TestClass()        

    def test_dict_json(self):        
        test_dict = self.deserializer.loads(self.serializer.dumps(d))        
        self.assertEqual(d, test_dict)        
    
    def test_true_json(self):                
        test_true = self.deserializer.loads(self.serializer.dumps(self.obj.tr))        
        self.assertEqual(self.obj.tr, test_true)        
    
    def test_false_json(self):                
        test_false = self.deserializer.loads(self.serializer.dumps(self.obj.fl))        
        self.assertEqual(self.obj.fl, test_false)        
        
    def test_none_json(self):                
        test_none = self.deserializer.loads(self.serializer.dumps(self.obj.nn))        
        self.assertEqual(self.obj.nn, test_none)        
    
    def test_inf_json(self):                
        test_inf = self.deserializer.loads(self.serializer.dumps(self.obj.infin))        
        self.assertEqual(self.obj.infin, test_inf)        
    
    def test_rinf_json(self):                
        test_rinf = self.deserializer.loads(self.serializer.dumps(self.obj.rinfin))        
        self.assertEqual(self.obj.rinfin, test_rinf)        

    def test_int_json(self):                
        test_num = self.deserializer.loads(self.serializer.dumps(self.obj.num))        
        self.assertEqual(self.obj.num, test_num)        
    
    def test_float_json(self):                
        test_num = self.deserializer.loads(self.serializer.dumps(self.obj.numf))        
        self.assertEqual(self.obj.numf, test_num)        
    
    def test_list_json(self):                
        test_list = self.deserializer.loads(self.serializer.dumps(self.obj.lst))        
        self.assertEqual(self.obj.lst, test_list)
    
    def test_turple_json(self):                
        test = self.deserializer.loads(self.serializer.dumps(self.obj.turp))        
        self.assertEqual(self.obj.turp[0], test[0])

    def test_string_json(self):                
        test_string = self.deserializer.loads(self.serializer.dumps(self.obj.str))
        self.assertEqual(self.obj.str, test_string)        

    def test_function_json(self):
        data = self.serializer.dumps(test_func)
        self.assertEqual(self.deserializer.loads(data)(), 'hello world')
    
    def test_method_json(self):
        data = self.serializer.dumps(self.obj.t)
        self.assertEqual(self.deserializer.loads(data)(self.obj), {'a' : 'aaaa'}) 
    
    def test_recursion_json(self):
        data = self.serializer.dumps(fact)
        self.assertIsInstance(self.deserializer.loads(data), types.FunctionType)
    
    def test_lambda_json(self):
        data = self.serializer.dumps(x)
        self.assertIsInstance(self.deserializer.loads(data), types.FunctionType)
    
    def test_class_json(self):
        data = self.serializer.dumps(TestClass)
        self.assertEqual(self.deserializer.loads(data).kkk, TestClass.kkk)        
    
    def test_object_json(self):        
        data = self.serializer.dumps(self.obj)
        self.assertEqual(self.deserializer.loads(data).num, TestClass().num)

    def test_dict_json_file(self):        
        self.serializer = Creator.create_serializer('json')
        self.deserializer = Creator.create_deserializer('json')
        
        self.serializer.dump(dct, 'test.json')
        test_dict = self.deserializer.load('test.json')               
        self.assertEqual(dct, test_dict)        

    def test_dict_json_dump(self):                
        self.serializer.dump(d, self.f)        
                
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(d, test)        
    
    def test_true_json_dump(self):                
        self.serializer.dump(self.obj.tr, self.f)        
                
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(self.obj.tr, test)        
    
    def test_false_json_dump(self):                
        self.serializer.dump(self.obj.fl, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(self.obj.fl, test)        
        
    def test_none_json_dump(self):                
        self.serializer.dump(self.obj.nn, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(self.obj.nn, test)        
    
    def test_inf_json_dump(self):                
        self.serializer.dump(self.obj.infin, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(self.obj.infin, test)        
    
    def test_rinf_json_dump(self):                
        self.serializer.dump(self.obj.rinfin, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(self.obj.rinfin, test)        

    def test_int_json_dump(self):                
        self.serializer.dump(self.obj.num, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(self.obj.num, test)        
    
    def test_float_json_dump(self):   
        tmp = self.obj.numf             
        self.serializer.dump(tmp, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(tmp, test)        
    
    def test_list_json_dump(self):                
        tmp = self.obj.lst            
        self.serializer.dump(tmp, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(tmp, test)        
    
    def test_turple_json_dump(self):                
        tmp = self.obj.turp             
        self.serializer.dump(tmp, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(tmp[0], test[0])        

    def test_string_json_dump(self):                
        tmp = self.obj.str             
        self.serializer.dump(tmp, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(tmp, test)        

    def test_function_json_dump(self):
        tmp = test_func           
        self.serializer.dump(tmp, self.f)                        
        self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertIsInstance(tmp, types.FunctionType)        
    
    def test_method_json_dump(self):
        tmp = self.obj.t             
        self.serializer.dump(tmp, self.f)                        
        self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(tmp(), {'a': 'aaaa'})        

    def test_recursion_json_dump(self):
        tmp = fact            
        self.serializer.dump(tmp, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(tmp(3), test(3))        
    
    def test_lambda_json_dump(self):
        tmp = x             
        self.serializer.dump(tmp, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(tmp(2), test(2))        
    
    def test_class_json_dump(self):
        tmp = TestClass          
        self.serializer.dump(tmp, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(tmp().num, test().num)        
    
    def test_object_json_dump(self):        
        tmp = self.obj            
        self.serializer.dump(tmp, self.f)                        
        test = self.deserializer.load(io.StringIO(self.f.getvalue()))        
        self.assertEqual(tmp.num, test.num)         

    def test_dict_pickle(self):      
        self.serializer = Creator.create_serializer('pickle')  
        self.deserializer = Creator.create_deserializer('pickle')        
        test = self.deserializer.loads(self.serializer.dumps(d))        
        self.assertEqual(d, test)        
    
    def test_int_pickle(self):                        
        self.serializer = Creator.create_serializer('pickle')  
        self.deserializer = Creator.create_deserializer('pickle')        
        test = self.deserializer.loads(self.serializer.dumps(self.obj.num))        
        self.assertEqual(self.obj.num, test)        
    
    def test_float_pickle(self):     
        self.serializer = Creator.create_serializer('pickle')  
        self.deserializer = Creator.create_deserializer('pickle')        
        tmp = self.obj.numf
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp, test)        
    
    def test_list_pickle(self):     
        self.serializer = Creator.create_serializer('pickle')  
        self.deserializer = Creator.create_deserializer('pickle')        
        tmp = self.obj.lst
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp, test)        

    def test_string_pickle(self):                
        self.serializer = Creator.create_serializer('pickle')  
        self.deserializer = Creator.create_deserializer('pickle')        
        tmp = self.obj.str
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp, test)        

    def test_function_pickle(self):
        self.serializer = Creator.create_serializer('pickle')  
        self.deserializer = Creator.create_deserializer('pickle')        
        tmp = test_func
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp(), test())        

    def test_recursion_pickle(self):
        self.serializer = Creator.create_serializer('pickle')  
        self.deserializer = Creator.create_deserializer('pickle')        
        tmp = fact
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp(2), test(2))            
    
    def test_labmda_pickle(self):
        self.serializer = Creator.create_serializer('pickle')  
        self.deserializer = Creator.create_deserializer('pickle')        
        tmp = x
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp(2), test(2))            

    def test_class_pickle(self):        
        self.serializer = Creator.create_serializer('pickle')  
        self.deserializer = Creator.create_deserializer('pickle')        
        tmp = TestClass
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp().numf, test().numf)        

    def test_class_method_pickle(self):        
        self.serializer = Creator.create_serializer('pickle')  
        self.deserializer = Creator.create_deserializer('pickle')        
        tmp = TestClass.cl
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp(), test(TestClass))        

    def test_static_method_pickle(self):        
        self.serializer = Creator.create_serializer('pickle')  
        self.deserializer = Creator.create_deserializer('pickle')        
        tmp = TestClass.st
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp(), test())        

    def test_object_pickle(self):        
        self.serializer = Creator.create_serializer('pickle')  
        self.deserializer = Creator.create_deserializer('pickle')        
        tmp = self.obj
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp.numf, test.numf)        
    
    def test_object_pickle_file(self):        
        self.serializer = Creator.create_serializer('pickle')
        self.deserializer = Creator.create_deserializer('pickle')
        
        self.serializer.dump(dct, 'test.pickle')
        test_dict = self.deserializer.load('test.pickle')        
        self.assertEqual(dct, test_dict)        
    
    def test_dict_toml(self):        
        self.serializer = Creator.create_serializer('toml')
        self.deserializer = Creator.create_deserializer('toml')
        
        test_dict = self.deserializer.loads(self.serializer.dumps(dct))        
        self.assertEqual(dct, test_dict)        
    
    def test_dict_toml_file(self):        
        self.serializer = Creator.create_serializer('toml')
        self.deserializer = Creator.create_deserializer('toml')
        
        self.serializer.dump(dct, 'test.toml')
        test_dict = self.deserializer.load('test.toml')        
        self.assertEqual(dct, test_dict)        

    def test_dict2_toml(self):        
        self.serializer = Creator.create_serializer('toml')
        self.deserializer = Creator.create_deserializer('toml')
        
        test_dict = self.deserializer.loads(self.serializer.dumps(dct))        
        self.assertEqual(dct, test_dict)        

    def test_string_toml(self):                
        test_string = self.deserializer.loads(self.serializer.dumps(self.obj.str))
        self.assertEqual(self.obj.str, test_string)        

    def test_function_toml(self):
        data = self.serializer.dumps(test_func)
        self.assertEqual(self.deserializer.loads(data)(), 'hello world')

    def test_method_toml(self):
        data = self.serializer.dumps(self.obj.t)
        self.assertEqual(self.deserializer.loads(data)(self.obj), {'a' : 'aaaa'})
    
    def test_recursion_toml(self):
        data = self.serializer.dumps(fact)
        self.assertIsInstance(self.deserializer.loads(data), types.FunctionType)
    
    def test_lambda_toml(self):
        data = self.serializer.dumps(x)
        self.assertIsInstance(self.deserializer.loads(data), types.FunctionType)
    
    def test_class_toml(self):
        data = self.serializer.dumps(TestClass)
        self.assertEqual(self.deserializer.loads(data).kkk, TestClass.kkk)        
    
    def test_object_toml(self):
        data = self.serializer.dumps(self.obj)
        self.assertEqual(self.deserializer.loads(data).num, TestClass().num)        
    
    def test_dict_yaml(self):        
        self.serializer = Creator.create_serializer('yaml')
        self.serializer = Creator.create_serializer('yaml', 4)
        self.deserializer = Creator.create_deserializer('yaml')
        
        test_dict = self.deserializer.loads(self.serializer.dumps(d))        
        self.assertEqual(d, test_dict)        
    
    def test_dict_yaml_file(self):        
        self.serializer = Creator.create_serializer('yaml')
        self.deserializer = Creator.create_deserializer('yaml')
        
        self.serializer.dump(dct, 'test.yaml')
        test_dict = self.deserializer.load('test.yaml')        
        self.assertEqual(dct, test_dict)        

    def test_int_yaml(self):                
        self.serializer = Creator.create_serializer('yaml')        
        self.deserializer = Creator.create_deserializer('yaml')
        test_num = self.deserializer.loads(self.serializer.dumps(self.obj.num))        
        self.assertEqual(self.obj.num, test_num)        
    
    def test_inf_yaml(self):                
        self.serializer = Creator.create_serializer('yaml')        
        self.deserializer = Creator.create_deserializer('yaml')
        tmp = self.obj.infin
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp, test)        
    
    def test_rinf_yaml(self):                
        self.serializer = Creator.create_serializer('yaml')        
        self.deserializer = Creator.create_deserializer('yaml')
        tmp = self.obj.rinfin
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp, test)        
    
    def test_none_yaml(self):                
        self.serializer = Creator.create_serializer('yaml')        
        self.deserializer = Creator.create_deserializer('yaml')
        tmp = self.obj.nn
        test = self.deserializer.loads(self.serializer.dumps(tmp))        
        self.assertEqual(tmp, test)        

    def test_float_yaml(self):                
        self.serializer = Creator.create_serializer('yaml')        
        self.deserializer = Creator.create_deserializer('yaml')
        test_num = self.deserializer.loads(self.serializer.dumps(self.obj.numf))        
        self.assertEqual(self.obj.numf, test_num)        
    
    def test_list_yaml(self):                
        self.serializer = Creator.create_serializer('yaml')        
        self.deserializer = Creator.create_deserializer('yaml')
        test_list = self.deserializer.loads(self.serializer.dumps(self.obj.lst))        
        self.assertEqual(self.obj.lst, test_list)
    
    def test_string_yaml(self):                
        self.serializer = Creator.create_serializer('yaml')        
        self.deserializer = Creator.create_deserializer('yaml')
        test_string = self.deserializer.loads(self.serializer.dumps(self.obj.str))
        self.assertEqual(self.obj.str, test_string)        

    def test_function_yaml(self):
        self.serializer = Creator.create_serializer('yaml')        
        self.deserializer = Creator.create_deserializer('yaml')
        data = self.serializer.dumps(test_func)
        self.assertEqual(self.deserializer.loads(data)(), 'hello world')

    def test_recursion_yaml(self):
        self.serializer = Creator.create_serializer('yaml')        
        self.deserializer = Creator.create_deserializer('yaml')
        data = self.serializer.dumps(fact)
        self.assertIsInstance(self.deserializer.loads(data), types.FunctionType)
    
    def test_lambda_yaml(self):
        self.serializer = Creator.create_serializer('yaml')        
        self.deserializer = Creator.create_deserializer('yaml')
        data = self.serializer.dumps(x)
        self.assertIsInstance(self.deserializer.loads(data), types.FunctionType)
    
    def test_class_yaml(self):
        self.serializer = Creator.create_serializer('yaml')        
        self.deserializer = Creator.create_deserializer('yaml')
        data = self.serializer.dumps(TestClass)
        self.assertEqual(self.deserializer.loads(data).kkk, TestClass.kkk)        
        
if __name__ == "__main__":
    unittest.main()