"""语言相关类型定义"""
import sys
from lbkit.errors import OdfValidateException


class IdfValidator():
    validator = {}
    name = ""

    def set_validator(self, value, name):
        self.validator = value
        self.name = name

    def odf_validate(self):
        idf_validator = idf_validator
        return []

    def odf_schema(self, allow_ref):
        allow_ref = allow_ref
        idf_validator = idf_validator
        return None


class BoolValidator(IdfValidator):
    def odf_validate(self):
        func = ["validate_odf_as_boolean(doc, node, prop, error_list)"]
        return func

    def odf_schema(self, allow_ref):
        if allow_ref:
            return {
                "anyOf": [
                    {
                        "type": "boolean"
                    },
                    {
                        "$ref": "#/$defs/ref_value"
                    }
                ]
            }
        else:
            return {
                "type": "boolean"
            }


class BoolArrayValidator(BoolValidator):
    def odf_validate(self):
        func = ["validate_odf_as_boolean_v(doc, node, prop, error_list)"]
        return func

    def odf_schema(self, allow_ref):
        parent_schema = super().odf_schema(False)
        if allow_ref:
            schema = {
                "anyOf": [
                    {
                        "type": "array",
                        "item": parent_schema
                    },
                    {
                        "$ref": "#/$defs/ref_value"
                    }
                ]
            }
        else:
            schema = {
                "type": "array",
                "item": parent_schema
            }

        return schema


class IntegerValidator(IdfValidator):
    maximum = sys.maxsize * 2
    minimum = -(sys.maxsize + 1) * 2

    def __init__(self, max, min, signed=False):
        self.maximum = max
        self.minimum = min
        self.signed = signed
        if not self.signed and self.minimum < 0:
            self.minimum = 0
        if self.maximum < self.minimum:
            raise OdfValidateException(f"The max value {self.maximum} less than or equal to {self.minimum}")
        super().__init__()

    def set_validator(self, value, name):
        super().set_validator(value, name)
        max = self.validator.get("max", self.maximum)
        if max > self.maximum:
            max = self.maximum
        min = self.validator.get("min", self.minimum)
        if min < self.minimum:
            min = self.minimum
        self.maximum = max
        self.minimum = min
        if not self.signed and self.minimum < 0:
            self.minimum = 0
        if self.maximum < self.minimum:
            raise OdfValidateException(f"The max value {self.maximum} less than or equal to {self.minimum}, property {name} validation failed")

    def odf_validate(self):
        func = []
        if self.signed:
            min_str = self.minimum
            max_str = self.maximum
            if self.minimum <= -9223372036854775808:
                min_str = "G_MININT64"
            if self.maximum >= 9223372036854775807:
                max_str = "G_MAXINT64"
            func.append(f"validate_odf_as_signed(doc, node, prop, {max_str}, {min_str}, error_list)")
        else:
            max_str = f"{self.maximum}UL"
            if self.maximum >= 18446744073709551615:
                max_str = "G_MAXUINT64"
            func.append(f"validate_odf_as_unsigned(doc, node, prop, {max_str}, {self.minimum}UL, error_list)")
        return func

    def odf_schema(self, allow_ref):
        """
            返回整数类型成员的ODF schema
            idf_validator为IDF模型中加载的数据验证器的对象
        """
        if allow_ref:
            return {
                "anyOf": [
                    {
                        "type": "integer",
                        "maximum": self.maximum,
                        "minimum": self.minimum
                    },
                    {
                        "$ref": "#/$defs/ref_value"
                    }
                ]
            }
        else:
            return {
                "type": "integer",
                "maximum": self.maximum,
                "minimum": self.minimum
            }


class IntegerArrayValidator(IntegerValidator):
    def odf_validate(self):
        func = []
        min_str = f"{self.minimum}UL"
        max_str = f"{self.maximum}UL"
        if self.signed:
            if self.minimum <= -9223372036854775808:
                min_str = "G_MININT64"
            if self.maximum >= 0x7fff_ffff_ffff_ffff:
                max_str = "G_MAXINT64"
        else:
            if self.maximum >= 0xffff_ffff_ffff_ffff:
                max_str = "G_MAXUINT64"

        if self.signed:
            func.append(f"validate_odf_as_signed_v(doc, node, prop, {max_str}, {min_str}, error_list)")
        else:
            func.append(f"validate_odf_as_unsigned_v(doc, node, prop, {max_str}, {min_str}, error_list)")
        return func

    def odf_schema(self, allow_ref):
        parent_schema = super().odf_schema(False)
        if allow_ref:
            schema = {
                "anyOf": [
                    {
                        "type": "array",
                        "item": parent_schema
                    },
                    {
                        "$ref": "#/$defs/ref_value"
                    }
                ]
            }
        else:
            schema = {
                "type": "array",
                "item": parent_schema
            }

        return schema


class FloatValidator(IdfValidator):
    maximum = sys.float_info.max
    minimum = -sys.float_info.max

    exclusive_max = None
    exclusive_min = None

    def __init__(self):
        self.max_key = "maximum"
        self.max_val = self.maximum
        self.min_key = "minimum"
        self.min_val = self.minimum
        super().__init__()

    def odf_validate(self):
        func = ["validate_odf_as_double(doc, node, prop, error_list)"]
        if self.exclusive_max is not None:
            func.append(f"validate_odf_as_double_exclusive_max(doc, node, prop, {self.exclusive_max}, error_list)")
        elif self.maximum != sys.float_info.max:
            func.append(f"validate_odf_as_double_max(doc, node, prop, {self.maximum}, error_list)")

        if self.exclusive_min is not None:
            func.append(f"validate_odf_as_double_exclusive_min(doc, node, prop, {self.exclusive_min}, error_list)")
        elif self.minimum != (-sys.float_info.max):
            func.append(f"validate_odf_as_double_min(doc, node, prop, {self.minimum}, error_list)")
        return func

    def set_validator(self, value, name):
        super().set_validator(value, name)
        self.maximum = self.validator.get("max", self.maximum)
        self.minimum = self.validator.get("min", self.minimum)
        self.exclusive_max = self.validator.get("exclusive_max", None)
        self.exclusive_min = self.validator.get("exclusive_min", None)
        self.max_key = "maximum"
        self.min_key = "minimum"
        self.max_val = self.maximum
        self.min_val = self.minimum
        if self.exclusive_max is not None:
            self.max_key = "exclusiveMaximum"
            self.max_val = self.exclusive_max
        if self.exclusive_min is not None:
            self.max_key = "exclusiveMinimum"
            self.min_val = self.exclusive_min

    def odf_schema(self, allow_ref):
        """
            返回整数类型成员的ODF schema
            idf_validator为IDF模型中加载的数据验证器的对象
        """
        if allow_ref:
            return {
                "anyOf": [
                    {
                        "type": "number",
                        self.max_key: self.max_val,
                        self.min_key: self.min_val
                    },
                    {
                        "$ref": "#/$defs/ref_value"
                    }
                ]
            }
        else:
            return {
                "type": "number",
                self.max_key: self.max_val,
                self.min_key: self.min_val
            }


class FloatArrayValidator(FloatValidator):
    def odf_validate(self):
        func = ["validate_odf_as_double_v(doc, node, prop, error_list)"]
        if self.exclusive_max is not None:
            func.append(f"validate_odf_as_double_exclusive_max_v(doc, node, prop, {self.exclusive_max}, error_list)")
        elif self.maximum != sys.float_info.max:
            func.append(f"validate_odf_as_double_max_v(doc, node, prop, {self.maximum}, error_list)")

        if self.exclusive_min is not None:
            func.append(f"validate_odf_as_double_exclusive_min_v(doc, node, prop, {self.exclusive_min}, error_list)")
        elif self.minimum != (-sys.float_info.max):
            func.append(f"validate_odf_as_double_min_v(doc, node, prop, {self.minimum}, error_list)")
        return func

    def odf_schema(self, allow_ref):
        parent_schema = super().odf_schema(False)
        if allow_ref:
            schema = {
                "anyOf": [
                    {
                        "type": "array",
                        "item": parent_schema
                    },
                    {
                        "$ref": "#/$defs/ref_value"
                    }
                ]
            }
        else:
            schema = {
                "type": "array",
                "item": parent_schema
            }
        return schema


class StringValidator(IdfValidator):
    pattern = None
    def __init__(self, pattern):
        self.pattern = pattern
        super().__init__()

    def set_validator(self, value, name):
        super().set_validator(value, name)
        self.pattern = self.validator.get("pattern", self.pattern)

    def odf_validate(self):
        func = []
        if self.pattern is not None:
            func.append(f"validate_odf_as_string(doc, node, prop, \"{self.pattern}\", error_list)")
        else:
            pattern = "^()|(((\\\\$)|[^$]).*)$"
            func.append(f"validate_odf_as_string(doc, node, prop, \"{pattern}\", error_list)")
        return func

    def odf_schema(self, allow_ref):
        if allow_ref:
            schema = {
                "anyOf": [
                    {
                        "type": "string",
                        "pattern": "^()|(((\\\\$)|[^$]).*)$"
                    },
                    {
                        "$ref": "#/$defs/ref_value"
                    }
                ]
            }
            if self.pattern is not None:
                schema["anyOf"][0]["pattern"] = self.pattern
        else:
            schema = {
                "type": "string",
                "pattern": self.pattern
            }
        return schema


class StringArrayValidator(StringValidator):
    def odf_validate(self):
        func = []
        if self.pattern is not None:
            func.append(f"validate_odf_as_string_v(doc, node, prop, \"{self.pattern}\", error_list)")
        else:
            pattern = "^()|(((\\\\$)|[^$]).*)$"
            func.append(f"validate_odf_as_string_v(doc, node, prop, \"{pattern}\", error_list)")
        return func

    def odf_schema(self, allow_ref):
        parent_schema = super().odf_schema(False)
        if allow_ref:
            schema = {
                "anyOf": [
                    {
                        "type": "array",
                        "item": parent_schema
                    },
                    {
                        "$ref": "#/$defs/ref_value"
                    }
                ]
            }
        else:
            schema = {
                "type": "array",
                "item": parent_schema
            }
        return schema

class RefObjValidator(IdfValidator):
    def __init__(self):
        super().__init__()

    def odf_validate(self):
        func = ["validate_odf_as_ref_obj(doc, node, prop, error_list)"]
        return func

    def odf_schema(self, allow_ref):
        if allow_ref:
            schema = {
                "anyOf": [
                    {
                        "$ref": "#/$defs/ref_obj"
                    },
                    {
                        "$ref": "#/$defs/ref_value"
                    }
                ]
            }
        else:
            schema = {
                "$ref": "#/$defs/ref_obj"
            }
        return schema


class RefObjArrayValidator(RefObjValidator):
    def odf_validate(self):
        func = ["validate_odf_as_ref_obj_v(doc, node, prop, error_list)"]
        return func

    def odf_schema(self, allow_ref):
        if allow_ref:
            schema = {
                "anyOf": [
                    {
                        "$ref": "#/$defs/ref_obj_array"
                    },
                    {
                        "$ref": "#/$defs/ref_value"
                    }
                ]
            }
        else:
            schema = {
                "$ref": "#/$defs/ref_obj_array"
            }
        return schema


class CTypeBase(object):
    """C语言相关的操作函数＆类型定义"""
    def __init__(self, declare, out_declare, free_func, encode_func, decode_func,
                 validator: IdfValidator = None,
                 const_declare = None,
                 const_free_func = None,
                 const_decode_func = None):
        self.declare = declare
        # 作为函数出参时的变量申明
        self.out_declare = out_declare
        self.free_func = free_func
        self.encode_func = encode_func
        self.decode_func = decode_func
        self.validator = validator
        # Req消息顶层数据结构的释放和解码函数，注意顶层的(string/signature/object_path)数据可以是const的
        self.const_declare = const_declare
        self.const_free_func = const_free_func
        self.const_decode_func = const_decode_func
        if const_declare is None:
            self.const_declare = self.declare
        if const_free_func is None:
            self.const_free_func = self.free_func
        if const_decode_func is None:
            self.const_decode_func = self.decode_func


"""定义支持的C语言类型"""
CTYPE_OBJS = {
    "boolean": CTypeBase(
        ["gboolean <arg_name>"],
        ["gboolean *<arg_name>"],
        [],
        ["<arg_out> = g_variant_new_boolean(<arg_name>)"],
        ["<arg_in> = g_variant_get_boolean(<arg_name>)"],
        BoolValidator()
    ),
    "byte": CTypeBase(
        ["guint8 <arg_name>"],
        ["guint8 *<arg_name>"],
        [],
        ["<arg_out> = g_variant_new_byte(<arg_name>)"],
        ["<arg_in> = g_variant_get_byte(<arg_name>)"],
        IntegerValidator(0xff, 0)
    ),
    "int16": CTypeBase(
        ["gint16 <arg_name>"],
        ["gint16 *<arg_name>"],
        [],
        ["<arg_out> = g_variant_new_int16(<arg_name>)"],
        ["<arg_in> = g_variant_get_int16(<arg_name>)"],
        IntegerValidator(0x7fff, -(0x8000), True)
    ),
    "uint16": CTypeBase(
        ["guint16 <arg_name>"],
        ["guint16 *<arg_name>"],
        [],
        ["<arg_out> = g_variant_new_uint16(<arg_name>)"],
        ["<arg_in> = g_variant_get_uint16(<arg_name>)"],
        IntegerValidator(0xffff, 0)
    ),
    "int32": CTypeBase(
        ["gint32 <arg_name>"],
        ["gint32 *<arg_name>"],
        [],
        ["<arg_out> = g_variant_new_int32(<arg_name>)"],
        ["<arg_in> = g_variant_get_int32(<arg_name>)"],
        IntegerValidator(0x7fff_ffff, -(0x8000_0000), True)
    ),
    "uint32": CTypeBase(
        ["guint32 <arg_name>"],
        ["guint32 *<arg_name>"],
        [],
        ["<arg_out> = g_variant_new_uint32(<arg_name>)"],
        ["<arg_in> = g_variant_get_uint32(<arg_name>)"],
        IntegerValidator(0xffff_ffff, 0)
    ),
    "int64": CTypeBase(
        ["gint64 <arg_name>"],
        ["gint64 *<arg_name>"],
        [],
        ["<arg_out> = g_variant_new_int64(<arg_name>)"],
        ["<arg_in> = g_variant_get_int64(<arg_name>)"],
        IntegerValidator(0x7fff_ffff_ffff_ffff, -(0x8000_0000_0000_0000), True)
    ),
    "uint64": CTypeBase(
        ["guint64 <arg_name>"],
        ["guint64 *<arg_name>"],
        [],
        ["<arg_out> = g_variant_new_uint64(<arg_name>)"],
        ["<arg_in> = g_variant_get_uint64(<arg_name>)"],
        IntegerValidator(0xffff_ffff_ffff_ffff, 0)
    ),
    "size": CTypeBase(
        ["gsize <arg_name>"],
        ["gsize *<arg_name>"],
        [],
        ["<arg_out> = g_variant_new_uint64(<arg_name>)"],
        ["<arg_in> = g_variant_get_uint64(<arg_name>)"],
        IntegerValidator(0xffff_ffff_ffff_ffff, 0)
    ),
    "ssize": CTypeBase(
        ["gssize <arg_name>"],
        ["gssize *<arg_name>"],
        [],
        ["<arg_out> = g_variant_new_int64(<arg_name>)"],
        ["<arg_in> = g_variant_get_int64(<arg_name>)"],
        IntegerValidator(0x7fff_ffff_ffff_ffff, -(0x8000_0000_0000_0000), True)
    ),
    "double": CTypeBase(
        ["gdouble <arg_name>"],
        ["gdouble *<arg_name>"],
        [],
        ["<arg_out> = g_variant_new_double(<arg_name>)"],
        ["<arg_in> = g_variant_get_double(<arg_name>)"],
        FloatValidator()
    ),
    "unixfd": CTypeBase(
        ["gint32 <arg_name>"],
        ["gint32 *<arg_name>"],
        [],
        ["<arg_out> = g_variant_new_handle(<arg_name>)"],
        ["<arg_in> = g_variant_get_handle(<arg_name>)"],
        IntegerValidator(0x7fff_ffff_ffff_ffff, 0, True)
    ),
    "string": CTypeBase(
        ["<const>gchar *<arg_name>"],
        ["gchar **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_string_encode(<arg_name>)"],
        ["<arg_in> = g_strdup(g_variant_get_string(<arg_name>, NULL))"],
        StringValidator("^.*$"),
        ["const gchar *<arg_name>"],
        [],
        ["<arg_in> = g_variant_get_string(<arg_name>, NULL)"],
    ),
    "object_path": CTypeBase(
        ["<const>gchar *<arg_name>"],
        ["gchar **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_object_path_encode(<arg_name>)"],
        ["<arg_in> = g_strdup(g_variant_get_string(<arg_name>, NULL))"],
        StringValidator("^(/[A-Z0-9a-z_]+)*$"),
        ["const gchar *<arg_name>"],
        [],
        ["<arg_in> = g_variant_get_string(<arg_name>, NULL)"],
    ),
    "signature": CTypeBase(
        ["<const>gchar *<arg_name>"],
        ["gchar **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_signature_encode(<arg_name>)"],
        ["<arg_in> = g_strdup(g_variant_get_string(<arg_name>, NULL))"],
        StringValidator("^([abynqiuxtdsogv\\\\{\\\\}\\\\(\\\\)])+$"),
        ["const gchar *<arg_name>"],
        [],
        ["<arg_in> = g_variant_get_string(<arg_name>, NULL)"],
    ),
    "variant": CTypeBase(
        ["GVariant *<arg_name>"],
        ["GVariant **<arg_name>"],
        ["lb_unref_p((GVariant **)&<arg_name>)"],
        ["g_variant_take_ref(<arg_name>)", "<arg_out> = g_variant_new_variant(<arg_name>)"],
        ["<arg_in> = g_variant_get_variant(<arg_name>)"],
        IdfValidator()
    ),
    "array[boolean]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gboolean *<arg_name>"],
        ["gsize *n_<arg_name>" ,"gboolean **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_array_boolean_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = lb_array_boolean_decode(<arg_name>, &n_<arg_in>)"],
        BoolArrayValidator()
    ),
    "array[byte]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>guint8 *<arg_name>"],
        ["gsize *n_<arg_name>" ,"guint8 **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_array_byte_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = lb_array_byte_decode(<arg_name>, &n_<arg_in>)"],
        IntegerArrayValidator(0xff, 0)
    ),
    "array[int16]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gint16 *<arg_name>"],
        ["gsize *n_<arg_name>" ,"gint16 **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_array_int16_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = lb_array_int16_decode(<arg_name>, &n_<arg_in>)"],
        IntegerArrayValidator(0x7fff, -(0x8000), True)
    ),
    "array[uint16]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>guint16 *<arg_name>"],
        ["gsize *n_<arg_name>" ,"guint16 **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_array_uint16_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = lb_array_uint16_decode(<arg_name>, &n_<arg_in>)"],
        IntegerArrayValidator(0xffff, 0)
    ),
    "array[int32]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gint32 *<arg_name>"],
        ["gsize *n_<arg_name>" ,"gint32 **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_array_int32_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = lb_array_int32_decode(<arg_name>, &n_<arg_in>)"],
        IntegerArrayValidator(0x7fff_ffff, -(0x80000000), True)
    ),
    "array[uint32]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>guint32 *<arg_name>"],
        ["gsize *n_<arg_name>" ,"guint32 **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_array_uint32_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = lb_array_uint32_decode(<arg_name>, &n_<arg_in>)"],
        IntegerArrayValidator(0xffff_ffff, 0)
    ),
    "array[int64]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gint64 *<arg_name>"],
        ["gsize *n_<arg_name>" ,"gint64 **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_array_int64_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = lb_array_int64_decode(<arg_name>, &n_<arg_in>)"],
        IntegerArrayValidator(0x7fff_ffff_ffff_ffff, -(0x8000_0000_0000_0000), True)
    ),
    "array[uint64]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>guint64 *<arg_name>"],
        ["gsize *n_<arg_name>" ,"guint64 **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_array_uint64_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = lb_array_uint64_decode(<arg_name>, &n_<arg_in>)"],
        IntegerArrayValidator(0xffff_ffff_ffff_ffff, 0)
    ),
    "array[ssize]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gssize *<arg_name>"],
        ["gsize *n_<arg_name>" ,"gssize **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_array_int64_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = lb_array_int64_decode(<arg_name>, &n_<arg_in>)"],
        IntegerArrayValidator(0x7fff_ffff_ffff_ffff, -(0x8000_0000_0000_0000), True)
    ),
    "array[size]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gsize *<arg_name>"],
        ["gsize *n_<arg_name>" ,"gsize **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_array_uint64_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = lb_array_uint64_decode(<arg_name>, &n_<arg_in>)"],
        IntegerArrayValidator(0xffff_ffff_ffff_ffff, 0)
    ),
    "array[double]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gdouble *<arg_name>"],
        ["gsize *n_<arg_name>" ,"gdouble **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_array_double_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = lb_array_double_decode(<arg_name>, &n_<arg_in>)"],
        FloatArrayValidator()
    ),
    "array[unixfd]": CTypeBase(
        ["gsize n_<arg_name>" ,"<const>gint32 *<arg_name>"],
        ["gsize *n_<arg_name>" ,"gint32 **<arg_name>"],
        ["lb_free_p((void **)&<arg_name>)"],
        ["<arg_out> = lb_array_handle_encode(<arg_name>, n_<arg_name>)"],
        ["<arg_in> = lb_array_handle_decode(<arg_name>, &n_<arg_in>)"],
        IntegerArrayValidator(0x7fff_ffff_ffff_ffff, 0, True)
    ),
    "array[string]": CTypeBase(
        ["gchar *<const>*<arg_name>"],
        ["gchar ***<arg_name>"],
        ["lb_strfreev_p(&<arg_name>)"],
        ["<arg_out> = lb_array_string_encode(<arg_name>)"],
        ["<arg_in> = lb_array_string_decode(<arg_name>)"],
        StringArrayValidator("^.*$")
    ),
    "array[object_path]": CTypeBase(
        ["gchar *<const>*<arg_name>"],
        ["gchar ***<arg_name>"],
        ["lb_strfreev_p(&<arg_name>)"],
        ["<arg_out> = lb_array_object_path_encode(<arg_name>)"],
        ["<arg_in> = lb_array_object_path_decode(<arg_name>)"],
        StringArrayValidator("^(/[A-Z0-9a-z_]+)*$")
    ),
    "array[signature]": CTypeBase(
        ["gchar *<const>*<arg_name>"],
        ["gchar ***<arg_name>"],
        ["lb_strfreev_p(&<arg_name>)"],
        ["<arg_out> = lb_array_signature_encode(<arg_name>)"],
        ["<arg_in> = lb_array_signature_decode(<arg_name>)"],
        StringArrayValidator("^([abynqiuxtdsogv\\\\{\\\\}\\\\(\\\\)])+$")
    )
}