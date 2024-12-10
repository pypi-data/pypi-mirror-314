""" unit tests """
from collections import namedtuple
from copy import deepcopy

import pytest

from ae.base import UNSET

from ae.deep import (
    DEFAULT_LEAF_TYPES, deepest_key_filter, deepest_value_filter, flattest_key_filter, flattest_value_filter,
    key_list_object, key_value, next_key_of_path, object_items, replace_object, key_path_string, key_path_object,
    pop_object, deep_replace, deep_search, deep_update)


class TestHelpers:
    def test_deepest_key_filter_arg_types(self):
        assert not deepest_key_filter(1)            # int arg (e.g. for tuple/list/dict index/key)
        assert not deepest_key_filter((1, 'b', ))   # tuple arg
        assert not deepest_key_filter('abc')        # str arg
        # noinspection PyTypeChecker
        assert not deepest_key_filter(None)         # even None

    def test_deepest_key_filter_excluded(self):
        assert deepest_key_filter('canvas')         # kivy canvas
        assert deepest_key_filter('self')
        assert deepest_key_filter('window')

    def test_deepest_value_filter_callable(self):
        def _test_func():
            pass

        class _TestClass:
            def _test_method(self):
                pass

            @classmethod
            def _test_class_method(cls):
                pass

            @staticmethod
            def _test_static_method():
                pass

        assert deepest_value_filter(_test_func, [])
        assert deepest_value_filter(_TestClass()._test_method, [])
        assert deepest_value_filter(_TestClass._test_class_method, [])
        assert deepest_value_filter(_TestClass()._test_static_method, [])

    def test_deepest_value_filter_real_types(self):
        assert deepest_value_filter(None, [])
        assert deepest_value_filter(1.23, [])
        assert deepest_value_filter(123, [])
        assert deepest_value_filter(pytest, [])

    def test_deepest_value_filter_recursion(self):
        str_obj = "abc"
        class _TestClass:
            pass
        tst_cls = _TestClass()

        assert deepest_value_filter(str_obj, [(str_obj, 0)])
        assert deepest_value_filter(tst_cls, [(tst_cls, 'attr')])
        assert deepest_value_filter(tst_cls, [(tst_cls, 'attr'), (str_obj, 1)])

    def test_flattest_key_filter(self):
        assert not flattest_key_filter(1)            # int arg (e.g. for tuple/list/dict index/key)
        assert not flattest_key_filter((1, 'b', ))   # tuple arg
        assert not flattest_key_filter('abc')        # str arg
        # noinspection PyTypeChecker
        assert not flattest_key_filter(None)         # even None

    def test_flattest_key_filter_excluded(self):
        assert flattest_key_filter('canvas')         # kivy canvas
        assert flattest_key_filter('self')
        assert flattest_key_filter('window')

    def test_flattest_value_filter_real_types(self):
        assert flattest_value_filter(None, [])
        assert flattest_value_filter(1.23, [])
        assert flattest_value_filter(123, [])
        assert flattest_value_filter(pytest, [])

    def test_flattest_value_filter_recursion(self):
        str_obj = "abc"
        class _TestClass:
            pass
        tst_cls = _TestClass()

        assert flattest_value_filter(str_obj, [(str_obj, 0)])
        assert flattest_value_filter(tst_cls, [(tst_cls, 'attr')])
        assert flattest_value_filter(tst_cls, [(tst_cls, 'attr'), (str_obj, 1)])

    def test_key_list_object_data(self):
        assert key_list_object([]) is UNSET
        assert key_list_object([({}, 'any not existing key')]) is UNSET

        dic = {'69': "str_key_val", 69: "int_key_val", 't': (1, "234", 6.9)}
        assert key_list_object([(dic, '69')]) == "str_key_val"
        assert key_list_object([(dic, 69)]) == "int_key_val"

        assert key_list_object([(dic, 't'), (dic['t'], 0)]) == 1
        assert key_list_object([(dic, 't'), (dic['t'], 1)]) == "234"
        assert key_list_object([(dic, 't'), (dic['t'], 2)]) == 6.9

        assert key_list_object([(dic, 't'), (dic['t'], 1), (dic['t'][1], 1)]) == "3"

    def test_key_list_object_exception(self):
        with pytest.raises(TypeError):
            key_list_object([([], 'any invalid key')])
        with pytest.raises(ValueError):
            key_list_object([([], )])   # type: ignore

    def test_key_path_object_dict_keys(self):
        dic = {}

        assert 123 not in dic
        assert key_path_object(dic, '[123]', new_value="int_key_val") is UNSET
        assert key_path_object(dic, '[123]') == "int_key_val"
        assert key_path_object(dic, '123') == "int_key_val"
        assert 123 in dic

        assert "123" not in dic
        assert key_path_object(dic, '["123"]', new_value="str_key_val") is UNSET
        assert key_path_object(dic, '["123"]') == "str_key_val"
        assert key_path_object(dic, '123') == "int_key_val"   # !!!!
        assert "123" in dic

        assert (1, "2") not in dic
        assert key_path_object(dic, '[(1, "2")]', new_value="tuple_key_val") is UNSET
        assert key_path_object(dic, '[(1, "2")]') == "tuple_key_val"
        assert (1, "2") in dic

        deeper_dic = {'deeper_key': "deep_val"}
        dic = {'key.with.sep': deeper_dic, 'key.with[sep]': deeper_dic}
        assert key_path_object(dic, "key.with.sep") == deeper_dic
        assert key_path_object(dic, "key.with.sep.deeper_key") == "deep_val"
        assert key_path_object(dic, "key.with.sep[deeper_key]") == "deep_val"
        assert key_path_object(dic, "key.with[sep]") == deeper_dic
        assert key_path_object(dic, "key.with[sep].deeper_key") == "deep_val"
        assert key_path_object(dic, "key.with[sep][deeper_key]") == "deep_val"

    def test_key_path_object_docstring_example(self):
        class AClass:
            """ child test class """
            str_attr_name_a = "a_attr_val"
            dict_attr = {'a_str_key': 3, 999: "value_with_int_key", '999': "..str_key"}

        class BClass:
            """ root test class """
            str_attr_name_b = "b_b_b_b_b"
            b_obj = AClass()

        obj = BClass()
        assert key_path_object(obj, 'str_attr_name_b') == "b_b_b_b_b"
        assert key_path_object(obj, 'b_obj.str_attr_name_a') == "a_attr_val"
        assert key_path_object(obj, 'b_obj.str_attr_name_a.5') == "r"  # 6th char of "a_attr_val"
        assert key_path_object(obj, 'b_obj.dict_attr.a_str_key') == 3

        assert key_path_object(obj, 'b_obj.dict_attr[999]') == "value_with_int_key"
        assert key_path_object(obj, 'b_obj.dict_attr["999"]') == "..str_key"
        assert key_path_object(obj, 'b_obj.dict_attr["a_str_key"]') == 3
        assert key_path_object(obj, 'b_obj.dict_attr[\'a_str_key\']') == 3

        assert key_path_object(obj, 'b_obj.dict_attr[a_str_key]') == 3

    def test_key_path_object_distinguish_int_str_key(self):
        dic = {'69': "str_key_val", 69: "int_key_val"}
        assert key_path_object(dic, "'69'") == "str_key_val"
        assert key_path_object(dic, "69") == "int_key_val"

    def test_key_path_object_item_value(self):
        class TstA:
            """ test class """
            att = "a_att_value"
            dic = dict(a_key="a_dict_val", a_dict={'a_key': "a_a_dict_val", 33: "a_a_num_key_val"})
            lis = ["a_list_val"]

        class TstB:
            """ test class """
            att = "b_att_value"
            a_att = TstA()

        a = TstA()
        b = TstB()
        c = list((TstA(), b))
        d = {'a': TstA(), 'b': b, 'c': c, (9,): 'num_tuple_key_val', ('t',): 'str_tuple_key_val'}

        assert key_path_object(a, 'att') == "a_att_value"
        assert key_path_object(a, 'att[1]') == "_"
        assert key_path_object(a, 'att.1') == "_"
        assert key_path_object(a, 'att[-1]') == "e"
        assert key_path_object(a, 'att.-1') == "e"
        assert key_path_object(a, 'dic["a_key"]') == "a_dict_val"
        assert key_path_object(a, 'dic.a_key') == "a_dict_val"

        assert key_path_object(a, 'dic["a_key"]') == "a_dict_val"
        assert key_path_object(a, 'dic[a_key]') == "a_dict_val"
        assert key_path_object(a, 'dic.a_key') == "a_dict_val"
        assert key_path_object(a, 'dic[\'a_dict\']') == {33: "a_a_num_key_val", 'a_key': "a_a_dict_val"}
        assert key_path_object(a, 'dic["a_dict"]') == {33: "a_a_num_key_val", 'a_key': "a_a_dict_val"}
        assert key_path_object(a, 'dic["a_dict"]["a_key"]') == "a_a_dict_val"
        assert key_path_object(a, 'dic.a_dict.a_key') == "a_a_dict_val"
        assert key_path_object(a, 'dic["a_dict"][33]') == "a_a_num_key_val"
        assert key_path_object(a, 'dic.a_dict.33') == "a_a_num_key_val"
        assert key_path_object(a, 'lis[0]') == "a_list_val"
        assert key_path_object(a, 'lis.0') == "a_list_val"

        assert key_path_object(b, 'att') == "b_att_value"
        assert isinstance(key_path_object(b, 'a_att'), TstA)
        assert key_path_object(b, 'a_att.att') == "a_att_value"
        assert key_path_object(b, 'a_att.att[-1]') == "e"
        assert key_path_object(b, 'a_att.att.-1') == "e"
        assert key_path_object(b, 'a_att.dic["a_key"]') == "a_dict_val"
        assert key_path_object(b, 'a_att.dic.a_key') == "a_dict_val"
        assert key_path_object(b, 'a_att.dic["a_dict"]') == {33: "a_a_num_key_val", 'a_key': "a_a_dict_val"}
        assert key_path_object(b, 'a_att.dic.a_dict') == {33: "a_a_num_key_val", 'a_key': "a_a_dict_val"}
        assert key_path_object(b, 'a_att.dic["a_dict"]["a_key"]') == "a_a_dict_val"
        assert key_path_object(b, 'a_att.dic.a_dict.a_key') == "a_a_dict_val"
        assert key_path_object(b, 'a_att.dic["a_dict"][33]') == "a_a_num_key_val"
        assert key_path_object(b, 'a_att.dic.a_dict.33') == "a_a_num_key_val"
        assert key_path_object(b, 'a_att.lis[0]') == "a_list_val"
        assert key_path_object(b, 'a_att.lis.0') == "a_list_val"

        assert key_path_object(c, '[0].att') == "a_att_value"
        assert key_path_object(c, '0].att') == "a_att_value"
        assert key_path_object(c, '0.att') == "a_att_value"
        assert isinstance(key_path_object(c, '0]'), TstA)
        assert key_path_object(c, '0].att[-1]') == "e"
        assert key_path_object(c, '0].dic["a_key"]') == "a_dict_val"
        assert key_path_object(c, '0].dic["a_dict"]') == {33: "a_a_num_key_val", 'a_key': "a_a_dict_val"}
        assert key_path_object(c, '0].dic["a_dict"]["a_key"]') == "a_a_dict_val"
        assert key_path_object(c, '0.dic.a_dict.a_key') == "a_a_dict_val"
        assert key_path_object(c, '0].dic["a_dict"][33]') == "a_a_num_key_val"
        assert key_path_object(c, '0.dic.a_dict.33') == "a_a_num_key_val"
        assert key_path_object(c, '0].lis[0]') == "a_list_val"
        assert key_path_object(c, '0.lis.0') == "a_list_val"

        assert key_path_object(c, '1].a_att.att') == "a_att_value"
        assert key_path_object(c, '1.a_att.att') == "a_att_value"
        assert isinstance(key_path_object(c, '1].a_att'), TstA)
        assert isinstance(key_path_object(c, '1.a_att'), TstA)
        assert key_path_object(c, '1].a_att.att[-1]') == "e"
        assert key_path_object(c, '1].a_att.dic["a_key"]') == "a_dict_val"
        assert key_path_object(c, '1].a_att.dic["a_dict"]') == {33: "a_a_num_key_val", 'a_key': "a_a_dict_val"}
        assert key_path_object(c, '1].a_att.dic["a_dict"]["a_key"]') == "a_a_dict_val"
        assert key_path_object(c, '1].a_att.dic[a_dict][a_key]') == "a_a_dict_val"
        assert key_path_object(c, '1.a_att.dic.a_dict.a_key') == "a_a_dict_val"
        assert key_path_object(c, '1].a_att.dic[a_dict][33]') == "a_a_num_key_val"
        assert key_path_object(c, '1.a_att.dic.a_dict.33') == "a_a_num_key_val"
        assert key_path_object(c, '1].a_att.lis[0]') == "a_list_val"
        assert key_path_object(c, '1.a_att.lis.0') == "a_list_val"
        assert key_path_object(c, '1.a_att.lis.0]') == "a_list_val"

        assert key_path_object(d, 'a.att') == "a_att_value"
        assert isinstance(key_path_object(d, 'a'), TstA)
        assert key_path_object(d, 'a.att[-1]') == "e"
        assert key_path_object(d, 'a.dic.a_key') == "a_dict_val"
        assert key_path_object(d, "a.dic[a_dict]") == {33: "a_a_num_key_val", 'a_key': "a_a_dict_val"}
        assert key_path_object(d, 'a.dic[a_dict][a_key]') == "a_a_dict_val"
        assert key_path_object(d, 'a.dic.a_dict.a_key') == "a_a_dict_val"
        assert key_path_object(d, 'a.dic[a_dict][33]') == "a_a_num_key_val"
        assert key_path_object(d, 'a.dic.a_dict.33') == "a_a_num_key_val"
        assert key_path_object(d, '\'a\'].lis[0]') == "a_list_val"
        assert key_path_object(d, 'a.lis.0') == "a_list_val"

        assert key_path_object(d, 'a].att') == "a_att_value"
        assert isinstance(key_path_object(d, 'a]'), TstA)
        assert key_path_object(d, 'a].att[-1]') == "e"
        assert key_path_object(d, 'a].dic[a_key]') == "a_dict_val"
        assert key_path_object(d, 'a].dic[a_dict]') == {33: "a_a_num_key_val", 'a_key': "a_a_dict_val"}
        assert key_path_object(d, 'a].dic[a_dict].a_key') == "a_a_dict_val"
        assert key_path_object(d, 'a].dic[a_dict].33') == "a_a_num_key_val"
        assert key_path_object(d, 'a].lis[0]') == "a_list_val"

        assert key_path_object(d, 'b].att') == "b_att_value"
        assert key_path_object(d, 'b].a_att.att') == "a_att_value"
        assert key_path_object(d, 'b].a_att.att[-1]') == "e"
        assert key_path_object(d, 'b].a_att.dic[a_key]') == "a_dict_val"
        assert key_path_object(d, 'b].a_att.dic[a_dict]') == {33: "a_a_num_key_val", 'a_key': "a_a_dict_val"}
        assert key_path_object(d, 'b].a_att.dic[a_dict][a_key]') == "a_a_dict_val"
        assert key_path_object(d, 'b].a_att.dic[a_dict][33]') == "a_a_num_key_val"
        assert key_path_object(d, 'b].a_att.lis[0]') == "a_list_val"

        assert key_path_object(d, 'c][0].att') == "a_att_value"
        assert key_path_object(d, 'c][0].att') == "a_att_value"
        assert key_path_object(d, 'c][0].att[-1]') == "e"
        assert key_path_object(d, 'c][0].dic[a_key]') == "a_dict_val"
        assert key_path_object(d, 'c][0].dic[a_dict]') == {33: "a_a_num_key_val", 'a_key': "a_a_dict_val"}
        assert key_path_object(d, 'c][0].dic[a_dict][a_key]') == "a_a_dict_val"
        assert key_path_object(d, 'c][0].dic[a_dict][33]') == "a_a_num_key_val"
        assert key_path_object(d, 'c][0].lis[0]') == "a_list_val"

        assert key_path_object(d, '(9,)') == "num_tuple_key_val"
        assert key_path_object(d, '("t",)') == "str_tuple_key_val"

        assert key_path_object(a, 'invalid_attr') is UNSET
        assert key_path_object(a, '[invalid_key]') is UNSET
        with pytest.raises(TypeError):
            key_path_object(c, '[invalid_idx]')
        assert key_path_object(d, '[invalid_key]') is UNSET

    def test_key_path_object_set(self):
        class TstA:
            """ test class """
            att = "a_att_value"
            dic = dict(a_key="a_dict_val", a_dict={'a_key': "a_a_dict_val", 33: "a_a_num_key_val"})
            lis = ["a_list_val"]
            tup = (0, "1", 2.3)

        class TstB:
            """ test class """
            att = "b_att_value"
            a_att = TstA()

        a = TstA()
        b = TstB()

        assert key_path_object(a, 'att', new_value="a_att_new_value") == "a_att_value"
        assert key_path_object(a, 'att') == "a_att_new_value"

        assert key_path_object(a, 'dic[\'a_key\']', new_value="a_dict_new_val") == "a_dict_val"
        assert key_path_object(a, 'dic["a_key"]') == "a_dict_new_val"
        assert key_path_object(a, 'dic.a_key') == "a_dict_new_val"

        assert 99 not in a.dic
        assert key_path_object(a, 'dic[99]', new_value="new_dict_item_with_int_key") is UNSET
        assert key_path_object(a, 'dic.99') == "new_dict_item_with_int_key"

        assert key_path_object(a, 'dic["a_dict"]', {'a_key': "a_a_dict_new_val", 33: "a_a_num_key_val"}
                           ) == {33: "a_a_num_key_val", 'a_key': "a_a_dict_val"}
        assert key_path_object(a, 'dic["a_dict"]["a_key"]', new_value="a_a_dict_newer_val") == "a_a_dict_new_val"
        assert key_path_object(a, 'dic["a_dict"]["a_key"]') == "a_a_dict_newer_val"
        assert key_path_object(b, 'a_att.dic["a_dict"]["a_key"]') == "a_a_dict_newer_val"

        assert key_path_object(a, 'dic["a_dict"][33]', new_value="new_dict_with_int_key") == "a_a_num_key_val"
        assert key_path_object(a, 'dic["a_dict"][33]') == "new_dict_with_int_key"

        assert key_path_object(a, 'lis[0]', new_value="a_list_new_val") == "a_list_val"
        assert key_path_object(a, 'lis[0]') == "a_list_new_val"
        assert key_path_object(b, 'a_att.lis[0]') == "a_list_new_val"

        assert key_path_object(b, 'att', new_value="b_att_new_value") == "b_att_value"
        assert key_path_object(b, 'att') == "b_att_new_value"

        assert key_path_object(b, 'a_att.att', new_value="xyz") == "a_att_value"
        assert key_path_object(b, 'a_att.att') == "xyz"
        assert key_path_object(b, 'a_att.att[-1]') == "z"

    def test_key_path_object_set_immutable(self):
        str_val = "bCd"
        deeper_tup = ("a", "b", "c")
        tup_val = (0, "1", 2.3, deeper_tup)
        dic = dict(str_item=str_val, tup_item=tup_val)

        class Tst:
            """ test class """
            dic_att = dic
        obj = Tst()

        assert key_path_object(obj, 'dic_att[str_item][2]') == "d"
        assert key_path_object(obj, 'dic_att["str_item"][2]', new_value="D") == str_val[2] == "d"
        assert obj.dic_att['str_item'][2] == "d"            # unchanged because single char in str cannot be changed

        assert key_path_object(obj, 'dic_att[tup_item][3][0]', new_value=0) == "a"
        assert obj.dic_att['tup_item'][3][0] == 0
        assert key_path_object(obj, 'dic_att.tup_item][3][0]') == 0

        assert key_path_object(dic, 'str_item[0]', new_value="B") == "b"
        assert key_path_object(dic, 'str_item[0]') == "b"   # unchanged because single char in str cannot be changed
        assert key_path_object(dic, 'str_item', new_value="changed_string") == str_val
        assert dic['str_item'] == "changed_string"

        assert key_path_object(dic, 'tup_item[1]', new_value=1) == "1"
        assert dic['tup_item'][1] == 1
        assert key_path_object(dic, 'tup_item][1]') == 1

        assert key_path_object(dic, 'tup_item[3][1]', new_value=1) == "b"
        assert dic['tup_item'][3][1] == 1
        assert key_path_object(dic, 'tup_item][3][1]') == 1

    def test_key_path_string(self):
        assert key_path_string([("aBc", 1)]) == "1"
        assert key_path_string([(["aBc"], 0), ("aBc", 1)]) == "0.1"

        class Tst:
            """ test object """
        obj = Tst()
        assert key_path_string([(obj, 'att_name'), ("aBc", 1)]) == "att_name.1"
        assert key_path_string([(obj, 'att_name'), ("aBc", 1), (obj, "any")]) == "att_name.1.any"
        assert key_path_string([(obj, 'att_name'), ("aBc", (3, )), (obj, "any")]) == "att_name.(3,).any"

    def test_key_value(self):
        assert key_value('') == ''
        assert key_value('str') == 'str'
        assert key_value('33') == 33
        assert key_value('()') == ()
        assert key_value('(6,)') == (6, )
        assert key_value('(6, )') == (6, )

    def test_next_key_of_path_exception(self):
        with pytest.raises(IndexError):
            assert next_key_of_path('')

    def test_next_key_of_path_number(self):
        assert next_key_of_path('99') == (99, '', '')
        assert next_key_of_path('99]') == (99, ']', '')
        assert next_key_of_path('6.9') == (6, '.', '9')
        assert next_key_of_path('6.9]') == (6, '.', '9]')
        assert next_key_of_path('[6.9]') == ('', '[', '6.9]')

        assert next_key_of_path('"99"') == ('99', '', '')
        assert next_key_of_path('\'99\'') == ('99', '', '')
        assert next_key_of_path('"99"]') == ('99', ']', '')
        assert next_key_of_path('\'99\']') == ('99', ']', '')
        assert next_key_of_path('[99]') == ('', '[', '99]')

    def test_next_key_of_path_str(self):
        assert next_key_of_path('a') == ('a', '', '')
        assert next_key_of_path('a[b]') == ('a', '[', 'b]')
        assert next_key_of_path('a[1]') == ('a', '[', '1]')

        assert next_key_of_path('a.b[c]') == ('a', '.', 'b[c]')
        assert next_key_of_path('a_b[c]') == ('a_b', '[', 'c]')
        assert next_key_of_path('a_b_c]') == ('a_b_c', ']', '')

        assert next_key_of_path('"a".b[c]') == ('a', '.', 'b[c]')
        assert next_key_of_path('"a".b["c"]') == ('a', '.', 'b["c"]')
        assert next_key_of_path('"a".b[\'c\']') == ('a', '.', 'b[\'c\']')

        assert next_key_of_path('b["c"]') == ('b', '[', '"c"]')
        assert next_key_of_path('b[\'c\']') == ('b', '[', '\'c\']')

        assert next_key_of_path('"c"]') == ('c', ']', '')
        assert next_key_of_path('\"\\c\"]') == ('\\c', ']', '')
        assert next_key_of_path('\\"\\c\\"]') == ('\\"\\c\\"', ']', '')
        assert next_key_of_path('\'c\']') == ('c', ']', '')
        assert next_key_of_path('\'\c\']') == ('\\c', ']', '')

    def test_next_key_of_path_tuple(self):
        assert next_key_of_path('(33,)') == ((33, ), '', '')
        assert next_key_of_path('(33, )') == ((33, ), '', '')
        assert next_key_of_path('(33,)[0]') == ((33, ), '[', '0]')

    def test_object_items_dict(self):
        dic = {'s': "str_val", 'i': 69}
        assert object_items(dic) == [('s', "str_val"), ('i', 69)]
        assert not object_items(dic, leaf_types=DEFAULT_LEAF_TYPES + (dict, ))
        assert object_items(dic, key_filter=lambda key: key == 's') == [('i', 69)]

    def test_object_items_list(self):
        lis = ["a", 6.9, (96, )]
        assert object_items(lis) == [(0, "a"), (1, 6.9), (2, (96, ))]
        assert object_items(lis, leaf_types=()) == [(0, "a"), (1, 6.9), (2, (96, ))]
        assert not object_items(lis, leaf_types=DEFAULT_LEAF_TYPES + (list, ))

    def test_object_items_namedtuple(self):
        NamTup = namedtuple("TestInt", ['att1', 'att2'])
        # noinspection PyArgumentList
        nam_tup = NamTup(1, att2=2)
        assert object_items(nam_tup) == [(0, 1), (1, 2)]
        assert not object_items(nam_tup, leaf_types=DEFAULT_LEAF_TYPES + (NamTup, ))

        NamTup = namedtuple("TestChar", "att1 att2")
        # noinspection PyArgumentList
        nam_tup = NamTup("a", "b")
        assert object_items(nam_tup) == [(0, "a"), (1, "b")]
        assert not object_items(nam_tup, leaf_types=DEFAULT_LEAF_TYPES + (NamTup, ))

    def test_object_items_object(self):
        class TstA:
            """ test data class """
            str_attr = "a"
            num_attr = 6.9
            tup_attr = (96, )

        assert not object_items(TstA)
        assert not object_items(TstA, leaf_types=(type, ))
        assert set(object_items(TstA, leaf_types=())) == {('num_attr', 6.9), ('str_attr', 'a'), ('tup_attr', (96,))}

        obj = TstA()
        assert set(object_items(obj)) == {('str_attr', 'a'), ('tup_attr', (96,)), ('num_attr', 6.9)}
        assert set(object_items(obj, leaf_types=(TstA, ))) == set()
        assert set(object_items(obj, leaf_types=())) == {('str_attr', "a"), ('num_attr', 6.9), ('tup_attr', (96,))}

    def test_object_items_set(self):
        tst_set = {1, 2}
        assert not object_items(tst_set)
        assert object_items(tst_set, leaf_types=()) == [(0, 1), (1, 2)]

    def test_object_items_string(self):
        assert object_items("aBc", leaf_types=()) == [(0, "a"), (1, "B"), (2, "c")]
        assert not object_items("aBc")

    def test_object_items_tuple(self):
        tup = ("a", 6.9, (96, ))
        assert object_items(tup) == [(0, "a"), (1, 6.9), (2, (96, ))]
        assert object_items(tup, leaf_types=()) == [(0, "a"), (1, 6.9), (2, (96, ))]
        assert not object_items(tup, leaf_types=DEFAULT_LEAF_TYPES + (tuple, ))

    def test_pop_object_dict(self):
        sub_dict = {'str_key': "str_val", 69: 96, 6.9: 9.6, (33, ): (99, )}
        dic = {'sub_dict': sub_dict}

        assert pop_object([(dic, 'sub_dict'), (sub_dict, 69)]) == 96
        assert 69 not in sub_dict

        assert pop_object([(dic, 'sub_dict'), (sub_dict, 'str_key'), (sub_dict['str_key'], 0)]) == "s"
        assert 'str_key' in sub_dict
        assert sub_dict['str_key'] == "tr_val"
        assert 'sub_dict' in dic

        assert pop_object([(dic, 'sub_dict'), (dic['sub_dict'], (33, )), (dic['sub_dict'][(33, )], 0)]) == 99
        assert 99 not in dic['sub_dict'][(33, )]
        assert dic['sub_dict'][(33, )] == ()

    def test_pop_object_exception(self):
        sub_tup = ("str_val", 96, 9.6, (33, 99,))
        tup = (sub_tup, )
        dic = {'tup_key': tup}

        with pytest.raises(ValueError):
            # pop cannot be done without a mutable parent data structure (like dict or list)
            pop_object([(tup, 0), (tup[0], 3), (tup[0][3], 0)])
        assert len(dic['tup_key'][0][3]) == 2
        assert len(dic['tup_key'][0]) == 4

        with pytest.raises(ValueError):
            pop_object([])

        with pytest.raises(IndexError):
            pop_object([(dic, 'tup_key'), (tup, 0), (tup[0], 3), (sub_tup[3], 33)])

    def test_pop_object_list(self):
        sub_tup = ("str_val", 96, 9.6, (33, 99, ))
        tup = (sub_tup, )
        lst = [tup]

        assert pop_object([(lst, 0), (tup, 0), (sub_tup, 0), (sub_tup[0], 6)]) == "l"
        assert lst[0][0][0] == "str_va"

        assert pop_object([(lst, 0), (tup, 0), (sub_tup, 3), (tup[0][3], 1)]) == 99
        assert len(lst[0][0][3]) == 1
        assert lst[0][0][3] == (33, )

    def test_pop_object_obj(self):
        str_val = "bCd"
        deeper_tup = ("a", "b", 3)
        tup_val = (0, "1", 2.3, deeper_tup)

        class Tst:
            """ test object """
            str_att = str_val
            tup_att = tup_val
        obj = Tst()

        assert pop_object([(obj, 'tup_att'), (tup_val, 1), ("1", 0)]) == "1"
        assert obj.tup_att[1] == ""

        assert pop_object([(obj, 'tup_att'), (tup_val, 3), (deeper_tup, 2)]) == 3
        assert 3 not in obj.tup_att[3]
        assert len(obj.tup_att[3]) == 2

        assert pop_object([(obj, 'tup_att'), (tup_val, 3), (deeper_tup, 0)]) == "a"
        assert "a" not in obj.tup_att[3]
        assert obj.tup_att[3][0] == "b"

        assert pop_object([(obj, 'str_att')]) == str_val
        assert not hasattr(obj, 'str_attr')

    def test_pop_object_str(self):
        str_val = "test"
        lst = [str_val]

        assert pop_object([(lst, 0), (lst[0], 1)]) == "e"
        assert lst == ["tst"]

    def test_replace_object_dict(self):
        str_val = "bCd"
        deeper_tup = ('a', 'b', 3)
        tup_val = (0, "1", 2.3, deeper_tup)
        dic = dict(str_item=str_val, tup_item=tup_val)

        assert dic['str_item'] == str_val
        replace_object([(dic, 'str_item')], str_val)
        assert dic['str_item'] == str_val

        replace_object([(dic, 'str_item'), (str_val, 0)], "_")
        assert dic['str_item'] == str_val       # unchanged because char in str cannot be changed

        assert dic['tup_item'][1] == "1"
        assert dic['tup_item'][3][2] == 3
        replace_object([(dic, 'tup_item'), (tup_val, 3), (deeper_tup, 2)], 6)
        assert dic['tup_item'][3][2] == 6

        lst_copy = lst = [dic]
        replace_object([(lst, 0), (dic, 'tup_item'), (tup_val, 3), (deeper_tup, 2)], "99")
        assert lst[0]['tup_item'][3][2] == "99"
        assert lst is lst_copy

        replace_object([(dic, 'tup_item'), (tup_val, 1)], 11)
        assert dic['tup_item'][1] == 11
        assert key_path_object(dic, "['tup_item'][1]") == 11

        replace_object([(dic, 'tup_item')], "new_string")
        assert dic['tup_item'] == "new_string"
        assert key_path_object(dic, "['tup_item']") == "new_string"

    def test_replace_object_exception(self):
        sub_tup = ("str_val", 96, 9.6, (33, 99,))
        tup = (sub_tup, )
        dic = {'tup_key': tup}

        with pytest.raises(ValueError):
            # pop cannot be done without a mutable parent data structure (like dict or list)
            replace_object([(tup, 0), (tup[0], 3), (tup[0][3], 0)], "new_val")
        assert len(dic['tup_key'][0][3]) == 2
        assert len(dic['tup_key'][0]) == 4

        with pytest.raises(ValueError):
            replace_object([], "new_val")

        with pytest.raises(ValueError):     # because no immutable parent object found
            replace_object([(tup, 0)], "_")

        # on wrong tuple index no IndexError will be raised
        replace_object([(dic, 'tup_key'), (tup, 0), (tup[0], 3), (sub_tup[3], 999)], "new_val")
        assert dic['tup_key'][0][3] == (33, 99, "new_val")
        replace_object([(dic, 'tup_key'), (tup, 0), (tup[0], 3), (sub_tup[3], -1)], "new_val")
        assert dic['tup_key'][0][3] == (33, "new_val", 33, 99)

    def test_replace_object_list(self):
        str_val = "bCd"
        deeper_tup = ('a', 'b', 3)
        tup_val = (0, "1", 2.3, deeper_tup)
        lst = ["a", str_val, tup_val]

        replace_object([(lst, 0)], "b")
        assert lst[0] == "b"

        replace_object([(lst, 2), (tup_val, 3), (deeper_tup, 2)], 6)
        assert lst[2][3][2] == 6

        replace_object([(lst, 2)], "new_string")
        assert lst[2] == "new_string"

        replace_object([(lst, 1), (str_val, 0)], "_")
        assert lst[1][0] == "b"     # unchanged because char in str cannot be replaced

    def test_replace_object_obj(self):
        str_val = "bCd"
        deeper_tup = ('a', 'b', 3)
        tup_val = (0, "1", 2.3, deeper_tup)

        class Tst:
            """ test object """
            str_att = str_val
            tup_att = tup_val
        obj = Tst()

        assert obj.tup_att[1] == "1"
        replace_object([(obj, 'tup_att'), (tup_val, 1)], 1)
        assert obj.tup_att[1] == 1

        replace_object([(obj, 'tup_att'), (tup_val, 3), (deeper_tup, 2)], "99")
        assert obj.tup_att[3][2] == "99"

        replace_object([(obj, 'tup_att')], "new_string")
        assert obj.tup_att == "new_string"

        replace_object([(obj, 'str_att'), (str_val, 2)], "_")
        assert obj.str_att[2] == "d"        # unchanged because character in str type cannot be replaced


class TestDeepFunctions:
    def test_deep_replace_data(self):
        sub_lst = ["b_list_0", "search_index_value", "search_key_value3"]
        data = dict(
            a_str="a_str",
            a_list=["a_list_0", "search_index_value", 2, dict(a_list_a="a_list_a_str", search_key="search_key_value1")],
            a_dict=dict(
                b_str="b_str",
                b_dict=dict(
                    c_tuple=("1st_tuple_value", "search_value", "3rd_tuple_value", 3,),
                    c_str="c str",
                    search_key="search_key_value2",
                ),
                b_list=sub_lst,
            )
        )

        deep_replace(data, lambda _p, _k, v: "replaced_value" if v == "search_value" else UNSET)
        assert data['a_dict']['b_dict']['c_tuple'][1] == "replaced_value"

        deep_replace(data, lambda _p, k, _v: "replaced_index_value" if k == 2 else UNSET)     # search_index_value
        assert data['a_list'][2] == "replaced_index_value"
        assert data['a_dict']['b_list'][2] == sub_lst[2] == "replaced_index_value"

        obj_path = [(data, 'a_dict'), (data['a_dict'], 'b_list'), (data['a_dict']['b_list'], 2)]
        deep_replace(data, lambda p, k, _v: "replaced_key_value" if k == 'search_key' or p == obj_path else UNSET)
        assert data['a_list'][3]['search_key'] == "replaced_key_value"
        assert data['a_dict']['b_dict']['search_key'] == "replaced_key_value"
        assert data['a_dict']['b_list'][2] == sub_lst[2] == "replaced_key_value"

        lst = [69]
        deep_replace(lst, lambda _p, _k, _v: "replacing all", leaf_types=())
        assert lst == ["replacing all"]

        # test recursion prevention
        deep_replace(data, lambda _p, _k, _v: UNSET, leaf_types=())
        deep_replace(lst, lambda _p, _k, _v: UNSET, leaf_types=())
        deep_replace([69], lambda _p, _k, _v: UNSET, leaf_types=())
        deep_replace(["t"], lambda _p, _k, _v: UNSET, leaf_types=())

        deep_replace(data, lambda _p, _k, _v: UNSET, key_filter=lambda key: True)
        deep_replace(data, lambda _p, _k, _v: UNSET, key_filter=lambda key: False)
        deep_replace([69], lambda _p, _k, _v: UNSET, key_filter=lambda key: False)

        deep_replace(data, lambda _p, _k, _v: UNSET, value_filter=lambda val, obj_keys: True)
        deep_replace(data, lambda _p, _k, _v: UNSET, value_filter=lambda val, obj_keys: False)
        deep_replace([69], lambda _p, _k, _v: UNSET, value_filter=lambda val, obj_keys: False)

        # test total overwrite
        deep_replace(data, lambda _p, _k, _v: "WIPED")
        for _k, _v in data.items():
            assert _v == "WIPED"

    def test_deep_replace_exception(self):
        with pytest.raises(ValueError):
            deep_replace(('tuple', 'are', 'only', 'replaced', 'in', 'deeper', 'data'),
                         lambda _p, _k, _v: "replacing all")

        with pytest.raises(AttributeError):     # because int attributes cannot be replaced
            deep_replace(99, lambda _p, _k, _v: "replacing all", leaf_types=())

    def test_deep_replace_immutable(self):
        str_val = "AbCbE"
        deeper_tup = ("a", "b")
        tup_val = (3, "0120", 1, deeper_tup)
        tst_list = [str_val, tup_val]
        tst_dict = dict(l=tst_list)

        # data keeps unchanged because str type not gets searched deeper onto char level
        deep_replace(tst_dict, lambda _p, k, v: "d" if v == "b" and k == 3 else UNSET)
        assert tst_dict['l'][0][3] == str_val[3] == "b"
        assert tst_dict['l'][1][3][1] == "b"        # unchanged because k == 3 (not 1)

        deep_replace(tst_dict, lambda _p, _k, v: "d" if v == "b" else UNSET)
        assert tst_list[0][3] == "b"
        assert tst_dict['l'][1][3][1] == "d"        # changed because "b" was a string leaf value

        deep_replace(tst_dict, lambda _p, _k, v: "d" if v == "b" else UNSET)
        assert tst_list[0][1] == tst_list[0][3] == str_val[1] == str_val[3] == "b"

        deep_replace(tst_dict, lambda _p, _k, v: "!" if v == "0" else UNSET, leaf_types=())
        assert tst_dict['l'][1][1][0] == tst_list[1][1][3] == "0"

        deep_replace(tst_dict, lambda _p, _k, v: "changed_string" if v == str_val else UNSET, leaf_types=(list, ))
        assert tst_dict['l'][0] == tst_list[0] == str_val

        # check changes
        deep_replace(tst_dict, lambda _p, _k, v: "changed_string" if v == str_val else UNSET)
        assert tst_dict['l'][0] == tst_list[0] == "changed_string"  # whole string got replaced
        
        deep_replace(tst_dict, lambda _p, _k, v: int(v) if v == "0120" else UNSET)
        assert tst_dict['l'][1][1] == tst_list[1][1] == 120         # leaf object type got changed from str to int
        
        deep_replace(tst_dict, lambda _p, _k, v: "Replaced" if v == "a" else UNSET)
        assert tst_dict['l'][1][3][0] == tst_list[1][3][0] == "Replaced"    # deeper leaf object got changed
        
    def test_deep_search_dict(self):
        str_val = "bCd"
        tup_val = (0, str_val, 2.3)
        dic = dict(str_item=str_val, tup_item=tup_val)

        obj_key = [(dic, 'str_item')]
        assert deep_search(dic, lambda p, k, v: p == obj_key) == \
               [(obj_key, 'str_item', str_val)]
        assert deep_search(dic, lambda p, k, v: p == obj_key, leaf_types=()) == \
               [(obj_key, 'str_item', str_val)]
        assert deep_search(dic, lambda p, k, v: p == obj_key, leaf_types=(str, )) == \
               [(obj_key, 'str_item', str_val)]
        assert deep_search(dic, lambda p, k, v: p == obj_key, key_filter=lambda key: False) == \
               [(obj_key, 'str_item', str_val)]
        assert deep_search(dic, lambda p, k, v: p == obj_key, key_filter=lambda key: True) == \
               []
        assert deep_search(dic, lambda p, k, v: p == obj_key, value_filter=lambda val, obj_keys: False) == \
               [(obj_key, 'str_item', str_val)]
        assert deep_search(dic, lambda p, k, v: p == obj_key, value_filter=lambda val, obj_keys: True) == \
               [(obj_key, 'str_item', str_val)]

        assert deep_search(dic, lambda p, k, v: k == 2) == \
               [([(dic, 'tup_item'), (dic['tup_item'], 2)], 2, 2.3)]

        assert deep_search(dic, lambda p, k, v: v == str_val) == \
               [([(dic, 'str_item')], 'str_item', str_val),
                ([(dic, 'tup_item'), (dic['tup_item'], 1)], 1, str_val),
                ]

        obj_key = [(dic, 'str_item'), (dic['str_item'], 1)]
        assert deep_search(dic, lambda p, k, v: p == obj_key) == []  # single chars/bytes cannot be searched
        assert deep_search(dic, lambda p, k, v: p == obj_key, leaf_types=()) == []
        assert deep_search(dic, lambda p, k, v: p == obj_key, key_filter=lambda key: False) == []
        assert deep_search(dic, lambda p, k, v: p == obj_key, value_filter=lambda val, obj_keys: False) == []

    def test_deep_search_obj(self):
        str_val = "bCd"
        tup_val = (0, str_val, 2.3)

        class Tst:
            """ test class """
            dic_att = dict(str_item=str_val, tup_item=tup_val)

        obj = Tst()

        assert deep_search(obj, lambda p, k, v: p == [(obj, 'dic_att'), (obj.dic_att, 'str_item')]) == \
               [([(obj, 'dic_att'), (obj.dic_att, 'str_item')], 'str_item', str_val)]

        assert deep_search(obj, lambda p, k, v: k == 2) == \
               [([(obj, 'dic_att'), (obj.dic_att, 'tup_item'), (obj.dic_att['tup_item'], 2)], 2, 2.3)]

        assert deep_search(obj, lambda p, k, v: v == str_val) == \
               [([(obj, 'dic_att'), (obj.dic_att, 'str_item')], 'str_item', str_val),
                ([(obj, 'dic_att'), (obj.dic_att, 'tup_item'), (obj.dic_att['tup_item'], 1)], 1, str_val),
                ]

    def test_deep_search_str(self):
        str_val = "bCd"

        assert deep_search(str_val, lambda p, k, v: True) == []

        assert deep_search(str_val, lambda p, k, v: True, leaf_types=(bytes, int, float, type)) == \
               [([('bCd', 0)], 0, 'b'), ([('bCd', 1)], 1, 'C'), ([('bCd', 2)], 2, 'd')]

        dic = dict(str_item=str_val, str_item2=str_val)
        assert deep_search(dic, lambda p, k, v: True, leaf_types=(bytes, int, float, type)) == \
               [([({'str_item': 'bCd', 'str_item2': 'bCd'}, 'str_item')], 'str_item', 'bCd'),
                ([({'str_item': 'bCd', 'str_item2': 'bCd'}, 'str_item2')], 'str_item2', 'bCd'),
                ]
        obj_key = [(dic, 'str_item'), (dic['str_item'], 1)]
        assert deep_search(dic, lambda p, k, v: p == obj_key, leaf_types=(bytes, int, float, type)) == []

    def test_deep_update_dict(self):
        obj = {'key1': "key1_val", (2, ): "key2_val", 3: "key3_val", 'key_old': "key_old_val",
               'key4': {'key4-k1': "key4_k1_val",
                        'key4-k2': {'key4-k2-k21': "key4_k2_k21_val",
                                    'key4-k2-k22': "key4_k2_k22_old"},
                        'key4-k3': "key4_k3_old"}}
        upd = {'key1': "key1_chg", (2, ): "key2_chg", 3: "key3_chg", 'key_add': "key_add_val",
               'key4': {'key4-k1': "key4_k1_chg",
                        'key4-k2': {'key4-k2-k21': "key4_k2_k21_chg",
                                    'key4-k2-k23': "key4_k2_k23_add"},
                        }}
        upd_copy = deepcopy(upd)
        deep_update(obj, upd)

        assert obj['key1'] == "key1_chg"
        assert obj[(2, )] == "key2_chg"
        assert obj[3] == "key3_chg"
        assert obj['key_old'] == "key_old_val"
        assert 'key_add' in obj
        assert obj['key_add'] == "key_add_val"

        assert obj['key4']['key4-k1'] == "key4_k1_chg"
        assert obj['key4']['key4-k2'] == {'key4-k2-k21': "key4_k2_k21_chg",
                                          'key4-k2-k22': "key4_k2_k22_old",
                                          'key4-k2-k23': "key4_k2_k23_add"}
        assert obj['key4']['key4-k3'] == "key4_k3_old"

        assert upd == upd_copy

    def test_deep_update_dict_with_separator_in_keys(self):
        obj = {'key1': "key1_val", (2, ): "key2_val", 3: "key3_val", 'key_old': "key_old_val",
               'key4': {'key4.k1': "key4_k1_val",
                        'key4[k2': {'key4.k[2]21': "key4_k2_k21_val",
                                    'key4.k2.k22': "key4_k2_k22_old"},
                        'key4.k3': "key4_k3_old"}}
        upd = {'key1': "key1_chg", (2, ): "key2_chg", 3: "key3_chg", 'key_add': "key_add_val",
               'key4': {'key4.k1': "key4_k1_chg",
                        'key4[k2': {'key4.k[2]21': "key4_k2_k21_chg",
                                    'key4.k2.k[3': "key4_k2_k23_add"},
                        }}
        upd_copy = deepcopy(upd)
        deep_update(obj, upd)

        assert obj['key1'] == "key1_chg"
        assert obj[(2, )] == "key2_chg"
        assert obj[3] == "key3_chg"
        assert obj['key_old'] == "key_old_val"
        assert 'key_add' in obj
        assert obj['key_add'] == "key_add_val"

        assert obj['key4']['key4.k1'] == "key4_k1_chg"
        assert obj['key4']['key4[k2'] == {'key4.k[2]21': "key4_k2_k21_chg",
                                          'key4.k2.k22': "key4_k2_k22_old",
                                          'key4.k2.k[3': "key4_k2_k23_add"}
        assert obj['key4']['key4.k3'] == "key4_k3_old"

        assert upd == upd_copy

    def test_deep_update_pop(self):
        lst = [1, 2, 3]
        with pytest.raises(IndexError):
            deep_update(lst, [UNSET, "2", UNSET, "3"])

        lst = [1, 2, 3]
        deep_update(lst, [UNSET, "2", UNSET])
        assert lst == ["2"]

        dic = {'a': 1, 'b': 2, 'c': 3}
        deep_update(dic, {'a': UNSET, 'b': "2", 'c': UNSET})
        assert dic == {'b': "2"}

        dic = {'a': 1, 'b': 2}
        deep_update(dic, {'a': UNSET, 'b': "2", 'c': "3"})
        assert dic == {'b': "2", 'c': "3"}
