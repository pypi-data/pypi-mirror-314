import unittest
import tempfile
import os
import tracemalloc

tracemalloc.start()
from lbkit.codegen.idf_interface import IdfInterface, IdfProperty
from lbkit import errors

schema_dir = os.path.realpath(os.path.join(os.getcwd(), "..", "schema"))

class TestCodeGenClass(unittest.TestCase):
    tmp_file = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp_file = tempfile.mktemp(prefix="idf_test", suffix=".yaml")
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        os.unlink(cls.tmp_file)
        return super().tearDownClass()


    def mk_interface_with_number_property(self, name, type, max, min, default_val):
        with open(self.tmp_file, mode="w+") as fp:
            fp.write(f"# yaml-language-server: $schema={schema_dir}/idf.v1.json\n")
            fp.write("version: \"0.1\"\n")
            fp.write("description: 测试接口，用于验证lb_base/lb_core，同时验证自动生成逻辑\n")
            fp.write("alias: Test\n")
            fp.write("properties:\n")
            fp.write(f"   - name: {name}\n")
            fp.write(f"     description: {name}\n")
            fp.write(f"     type: {type}\n")
            fp.write(f"     max: {max}\n")
            fp.write(f"     min: {min}\n")
            fp.write(f"     default: {default_val}\n")

    def mk_interface_with_string_property(self, name, type, pattern, default_val):
        with open(self.tmp_file, mode="w+") as fp:
            fp.write(f"# yaml-language-server: $schema={schema_dir}/idf.v1.json\n")
            fp.write("version: \"0.1\"\n")
            fp.write("description: 测试接口，用于验证lb_base/lb_core，同时验证自动生成逻辑\n")
            fp.write("alias: Test\n")
            fp.write("properties:\n")
            fp.write(f"   - name: {name}\n")
            fp.write(f"     description: {name}\n")
            fp.write(f"     type: {type}\n")
            if pattern:
                fp.write(f"     pattern: {pattern}\n")
            fp.write(f"     default: {default_val}\n")

    def mk_interface_with_double_property(self, name, type, default_val, max=None, min=None, exclusive_max=None, exclusive_min=None):
        with open(self.tmp_file, mode="w+") as fp:
            fp.write(f"# yaml-language-server: $schema={schema_dir}/idf.v1.json\n")
            fp.write("version: \"0.1\"\n")
            fp.write("description: 测试接口，用于验证lb_base/lb_core，同时验证自动生成逻辑\n")
            fp.write("alias: Test\n")
            fp.write("properties:\n")
            fp.write(f"   - name: {name}\n")
            fp.write(f"     description: {name}\n")
            fp.write(f"     type: {type}\n")
            if max is not None:
                fp.write(f"     max: {max}\n")
            if min is not None:
                fp.write(f"     min: {min}\n")
            if exclusive_max is not None:
                fp.write(f"     exclusive_max: {exclusive_max}\n")
            if exclusive_min is not None:
                fp.write(f"     exclusive_min: {exclusive_min}\n")
            fp.write(f"     default: {default_val}\n")


    def validate_boolean(self, name, type, default):
        with open(self.tmp_file, mode="w+") as fp:
            fp.write(f"# yaml-language-server: $schema={schema_dir}/idf.v1.json\n")
            fp.write("version: \"0.1\"\n")
            fp.write("description: 测试接口，用于验证lb_base/lb_core，同时验证自动生成逻辑\n")
            fp.write("alias: Test\n")
            fp.write("properties:\n")
            fp.write(f"   - name: {name}\n")
            fp.write(f"     description: {name}\n")
            fp.write(f"     type: {type}\n")
            fp.write(f"     default: {default}\n")

    def test_validate_default_bool(self):
        self.validate_boolean("b", "boolean", "true")
        IdfInterface(None, self.tmp_file)
        self.validate_boolean("b", "boolean", "false")
        IdfInterface(None, self.tmp_file)
        self.validate_boolean("b", "boolean", "False")
        IdfInterface(None, self.tmp_file)
        self.validate_boolean("b", "boolean", "True")
        IdfInterface(None, self.tmp_file)
        self.validate_boolean("b", "boolean", "ONsdf")
        with self.assertRaises(errors.PackageConfigException):
            IdfInterface(None, self.tmp_file)
        self.validate_boolean("b", "boolean", "asdaffa")
        with self.assertRaises(errors.PackageConfigException):
            IdfInterface(None, self.tmp_file)

    def test_validate_default_array_bool(self):
        self.validate_boolean("b", "array[boolean]", "[false, true]")
        IdfInterface(None, self.tmp_file)
        self.validate_boolean("b", "array[boolean]", "[on, 1]")
        # boolean值比较特殊，由json schema校验验证
        with self.assertRaises(errors.PackageConfigException):
            IdfInterface(None, self.tmp_file)

    def validate_number(self, name, type):
        self.mk_interface_with_number_property(name, type, "100", "1", "1")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_number_property(name, type, "100", "1", "100")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_number_property(name, type, "100", "1", "0")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_number_property(name, type, "100", "1", "101")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)

    def test_validate_default_byte(self):
        self.validate_number("y", "byte")

    def test_validate_default_uint16(self):
        self.validate_number("n", "uint16")

    def test_validate_default_int16(self):
        self.validate_number("q", "int16")

    def test_validate_default_int32(self):
        self.validate_number("i", "int32")

    def test_validate_default_uint32(self):
        self.validate_number("u", "uint32")

    def test_validate_default_int64(self):
        self.validate_number("x", "int64")

    def test_validate_default_uint64(self):
        self.validate_number("t", "uint64")

    def test_validate_default_size(self):
        self.validate_number("size", "size")

    def test_validate_default_uint16(self):
        self.validate_number("ssize", "ssize")

    def test_validate_default_boolean(self):
        self.validate_number("double", "double")

    def validate_array_number(self, name, type):
        self.mk_interface_with_number_property(name, f"array[{type}]", "100", "1", "[1, 1]")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_number_property(name, f"array[{type}]", "100", "1", "[100, 100]")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_number_property(name, f"array[{type}]", "100", "1", "[0, 0]")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_number_property(name, f"array[{type}]", "100", "1", "[101, 101]")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)

    def test_validate_default_array_byte(self):
        self.validate_array_number("y", "byte")

    def test_validate_default_array_uint16(self):
        self.validate_array_number("n", "uint16")

    def test_validate_default_array_int16(self):
        self.validate_array_number("q", "int16")

    def test_validate_default_array_int32(self):
        self.validate_array_number("i", "int32")

    def test_validate_default_array_uint32(self):
        self.validate_array_number("u", "uint32")

    def test_validate_default_array_int64(self):
        self.validate_array_number("x", "int64")

    def test_validate_default_array_uint64(self):
        self.validate_array_number("t", "uint64")

    def test_validate_default_array_size(self):
        self.validate_array_number("size", "size")

    def test_validate_default_array_uint16(self):
        self.validate_array_number("ssize", "ssize")

    def test_validate_default_array_double(self):
        self.validate_array_number("double", "double")

    def test_validate_array_double(self):
        self.mk_interface_with_double_property("double", f"array[double]", "[1, 1]", exclusive_max="100", exclusive_min="1")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_double_property("double", f"array[double]", "[100, 100]", exclusive_max="100", exclusive_min="1")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_double_property("double", f"array[double]", "[0.9, 0.9]", exclusive_max="100", exclusive_min="1")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_double_property("double", f"array[double]", "[100.1, 100.1]", exclusive_max="100", exclusive_min="1")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)

    def test_validate_double(self):
        self.mk_interface_with_double_property("double", "double", "1", exclusive_max="100", exclusive_min="1")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_double_property("double", "double", "100", exclusive_max="100", exclusive_min="1")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_double_property("double", "double", "0.9", exclusive_max="100", exclusive_min="1")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_double_property("double", "double", "100.1", exclusive_max="100", exclusive_min="1")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)

    def test_validate_string(self):
        self.mk_interface_with_string_property("string", "string", None, "as")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("string", "string", "^a[s]{1,2}$", "as")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("string", "string", "^a[s]{1,2}$", "ass")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("string", "string", "^a[s]{1,2}$", "asss")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("string", "string", "^a[s]{1,2}$", "a")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("string", "string", "^a[s]{1,2}$", "0.123")
        with self.assertRaises(errors.PackageConfigException):
            IdfInterface(None, self.tmp_file)

    def test_validate_array_string(self):
        self.mk_interface_with_string_property("string", "array[string]", None, "[as, as]")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("string", "array[string]", "^a[s]{1,2}$", "[as, as]")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("string", "array[string]", "^a[s]{1,2}$", "[ass, ass]")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("string", "array[string]", "^a[s]{1,2}$", "[asss, asss]")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("string", "array[string]", "^a[s]{1,2}$", "[a, a]")
        with self.assertRaises(errors.OdfValidateException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("string", "array[string]", "^a[s]{1,2}$", "[0.123, 0.123]")
        with self.assertRaises(errors.PackageConfigException):
            IdfInterface(None, self.tmp_file)

    def test_validate_object_path(self):
        self.mk_interface_with_string_property("object_path", "object_path", None, "/as")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("object_path", "object_path", None, "/a/s")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("object_path", "object_path", None, "a/s")
        with self.assertRaises(errors.PackageConfigException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("object_path", "object_path", None, "/a/s/")
        with self.assertRaises(errors.PackageConfigException):
            IdfInterface(None, self.tmp_file)

    def test_validate_array_object_path(self):
        self.mk_interface_with_string_property("object_path", "array[object_path]", None, "[/as, /as]")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("object_path", "array[object_path]", None, "[/a/s, /a]")
        IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("object_path", "array[object_path]", None, "[a/s, a/s]")
        with self.assertRaises(errors.PackageConfigException):
            IdfInterface(None, self.tmp_file)
        self.mk_interface_with_string_property("object_path", "array[object_path]", None, "[/a/s/, /a/s/]")
        with self.assertRaises(errors.PackageConfigException):
            IdfInterface(None, self.tmp_file)


if __name__ == "__main__":
    unittest.main()