#include "lb_base.h"
#include "${intf.name}.h"

<% class_name = intf.alias %>\
## 定义结构体ODF加载函数
% for name, stru in intf.structures.items():
/* ${name} structure object */
/* START: 结构体${name}及其数组类型的ODF校验函数 */
static gboolean __attribute__((unused)) _validate_odf_as_struct_${name}(yaml_document_t *doc, yaml_node_t *node, GString *prop, GSList **error_list);
static gboolean __attribute__((unused)) _validate_odf_as_struct_${name}_v(yaml_document_t *doc, yaml_node_t *node, GString *prop, GSList **error_list);

% endfor
## 定义枚举ODF加载函数
% for name, enum in intf.enumerations.items():
/* START: 枚举${name}及其数组类型的ODF校验函数 */
static gboolean __attribute__((unused)) _validate_odf_as_enum_${name}(yaml_document_t *doc, yaml_node_t *node, GString *prop, GSList **error_list);
static gboolean __attribute__((unused)) _validate_odf_as_enum_${name}_v(yaml_document_t *doc, yaml_node_t *node, GString *prop, GSList **error_list);

% endfor
## 定义字典ODF加载函数
% for name, dictionary in intf.dictionaries.items():
static gboolean __attribute__((unused)) _validate_odf_as_dict_${name}(yaml_document_t *doc, yaml_node_t *node, GString *prop, GSList **error_list);
static gboolean __attribute__((unused)) _validate_odf_as_dict_${name}_v(yaml_document_t *doc, yaml_node_t *node, GString *prop, GSList **error_list);

% endfor
% for name, stru in intf.structures.items():
/* ${name}结构体类型序列化（struct转GVariant）函数 */
GVariant *${name}_encode(const ${name} *value)
{
    % if stru.values.has_variant_value:
    g_assert(value);

    % else:
    static ${name} default_val;
    if (value == NULL) {
        value = &default_val;
    }
    % endif
    __attribute__((unused)) GVariant *tmp = NULL;
    GVariantBuilder builder;
    const gchar *sig = "${stru.signature}";
    g_variant_builder_init(&builder, G_VARIANT_TYPE(sig));
    % for prop in stru.values.parameters:
        % for line in prop.encode_func():
    ${line.replace("<arg_out>", "tmp").replace("n_<arg_name>", "value->n_" + prop.name).replace("<arg_name>", "value->" + prop.name)};
        % endfor
    g_variant_builder_add_value(&builder, tmp);
    % endfor
    return g_variant_builder_end(&builder);
}

/**
 * ${name}结构体类型反序列化（GVariant转struct）函数，返回以NULL结束的指针数组
 * Note: return an EMPTY ${name} object when `in` is NULL
 */
${name} *${name}_decode(GVariant *in)
{
    GVariantIter iter;
    __attribute__((unused)) GVariant *tmp = NULL;
    ${name} *output = g_new0(${name}, 1);
    if (!in) {
        return output;
    }

    (void)g_variant_iter_init(&iter, in);
    % for prop in stru.values.parameters:
    /* process ${prop.name} */
    tmp = g_variant_iter_next_value(&iter);
        % for line in prop.decode_func():
    ${line.replace("<arg_name>", "tmp").replace("n_<arg_in>", "output->n_" + prop.name).replace("<arg_in>", "output->" + prop.name)};
        % endfor
    g_variant_unref(tmp);
    % endfor
    return output;
}

/* ${name}结构体指针释放 */
void ${name}_free(${name} **value)
{
    if (!value || !(*value)) {
        return;
    }

    ${name}_clean(*value);
    g_free(*value);
    *value = NULL;
}

/* ${name}结构体指针释放 */
void ${name}_clean(${name} *value)
{
    if (!value) {
        return;
    }

    % for prop in stru.values.parameters:
        % for line in prop.free_func():
    ${line.replace("<arg_name>", "value->" + prop.name)};
        % endfor
    % endfor
}

/* ${name}结构体组件类型序列化（struct转GVariant）函数，values以NULL结束的数组 */
GVariant *${name}_encode_v(${name} * const *values)
{
    GVariantBuilder builder;
    GVariant *tmp = NULL;
    const gchar *sig = "a${stru.signature}";
    g_variant_builder_init(&builder, G_VARIANT_TYPE(sig));
    for (int i = 0; values && values[i]; i++) {
        tmp = ${name}_encode(values[i]);
        g_variant_builder_add_value(&builder, tmp);
    }
    return g_variant_builder_end(&builder);
}

/* ${name}结构体数组类型反序列化（GVariant转struct）函数，返回以NULL结束的指针数组 */
${name} **${name}_decode_v(GVariant *in)
{
    if (!in) {
        return NULL;
    }

    GVariantIter iter;
    GVariant *tmp = NULL;

    (void)g_variant_iter_init(&iter, in);
    gsize n = g_variant_iter_n_children(&iter);
    if (n == 0) {
        return NULL;
    }
    ${name} **output = g_new0(${name} *, n + 1);
    for (gsize i = 0; i < n; i++) {
        tmp = g_variant_iter_next_value(&iter);
        output[i] = ${name}_decode(tmp);
        g_variant_unref(tmp);
    }
    return output;
}

/* ${name}结构体指针数组释放 */
void ${name}_free_v(${name} ***value)
{
    if(!value || !(*value)) {
        return;
    }

    for (int i = 0; (*value)[i]; i++) {
        ${name}_free((*value) + i);
    }
    g_free(*value);
    *value = NULL;
}

gboolean _validate_odf_as_struct_${name}(yaml_document_t *doc, yaml_node_t *node,
    GString *prop, GSList **error_list)
{
    g_assert(doc && node && prop && error_list);
    if (node->type != YAML_MAPPING_NODE) {
        *error_list = g_slist_append(*error_list, g_error_new(ODF_ERROR, ODF_ERROR_PROP_VALIDATE_TYPE_ERROR,
            "the node type of property %s is not a mapping, get %s", prop->str, lb_yaml_node_type_str(node->type)));
        return FALSE;
    }
    __attribute__((unused)) gsize len = prop->len;
    gboolean valid = TRUE;
    __attribute__((unused)) yaml_node_t *val;
    GHashTable *prop_table = load_yaml_mapping_to_hash_table(doc, node);
    % for prop in stru.values.parameters:
    val = g_hash_table_lookup(prop_table, "${prop.name}");
    if (val) {
        g_string_append(prop, ".${prop.name}");
        % for func in prop.odf_validate(False):
        if (!${func.replace("node,", "val,")})
            valid = FALSE;
        % endfor
        g_string_truncate(prop, len);
    }
    % endfor
    g_hash_table_destroy(prop_table);
    return valid;
}

gboolean _validate_odf_as_struct_${name}_v(yaml_document_t *doc, yaml_node_t *node,
    GString *prop, GSList **error_list)
{
    g_assert(doc && node && prop && error_list);
    if (node->type != YAML_SEQUENCE_NODE) {
        *error_list = g_slist_append(*error_list, g_error_new(ODF_ERROR, ODF_ERROR_PROP_VALIDATE_TYPE_ERROR,
            "the node type of property %s is not a sequence, get %s", prop->str, lb_yaml_node_type_str(node->type)));
        return FALSE;
    }
    gsize len = prop->len;
    gint i = 0;
    yaml_node_t *val = NULL;
    gboolean valid = TRUE;
    for (yaml_node_item_t *item = node->data.sequence.items.start; item < node->data.sequence.items.top; item++) {
        g_string_append_printf(prop, ".%d", i);
        val = yaml_document_get_node(doc, *item);
        if (!_validate_odf_as_struct_${name}(doc, val, prop, error_list)) {
            valid = FALSE;
        }
        g_string_truncate(prop, len);
        i++;
    }
    return valid;
}

%endfor
% for name, enum in intf.enumerations.items():
## 枚举序列化和反序列化函数
static const gchar *_${name}StrMap[] = {
% for value in enum.values.parameters:
    "${intf.name}.${name}.${value.name}",
% endfor
};

const gchar *${name}_as_string(${name} value)
{
    if (value >= _${name}Invalid) {
        return "com.litebmc.Errors.Enum.Invalid";
    }
    return _${name}StrMap[value];
}

/* ${name}枚举类型序列化（enum转string）函数 */
GVariant *${name}_encode(${name} value)
{
    ## 非法值返回com.litebmc.Errors.Enum.Invalid
    if (value > ${name}_${enum.values.parameters[len(enum.values.parameters) - 1].name}) {
        return g_variant_new_string("com.litebmc.Errors.Enum.Invalid");
    }
    return g_variant_new_string(_${name}StrMap[value]);
}

/* ${name}枚举类型反序列化（string转enum）函数 */
${name} ${name}_decode(GVariant *in)
{
    if (!in) {
        return _${name}Invalid;
    }

    const gchar *in_val = g_variant_get_string(in, NULL);
    for (int i = 0; i <= ${len(enum.values.parameters)}; i++) {
        if (g_strcmp0(in_val, _${name}StrMap[i]) == 0) {
            return (${name})i;
        }
    }
    return _${name}Invalid;
}

/* ${name}枚举类型序列化（enum转string）函数 */
GVariant *${name}_encode_v(const ${name} *values, gsize n)
{
    g_assert(n == 0 || values);

    GVariantBuilder builder;
    g_variant_builder_init(&builder, G_VARIANT_TYPE("as"));
    GVariant *tmp = NULL;
    for (gsize i = 0; i < n; i++) {
        tmp = ${name}_encode(values[i]);
        g_variant_builder_add_value(&builder, tmp);
    }
    return g_variant_builder_end(&builder);
}

/* ${name}枚举类型反序列化（string转enum）函数 */
${name} *${name}_decode_v(GVariant *in, gsize *n)
{
    g_assert(n);
    if (!in) {
        *n = 0;
        return NULL;
    }
    GVariantIter iter;
    int id = 0;
    gchar *str_val = NULL;

    (void)g_variant_iter_init(&iter, in);
    *n = g_variant_iter_n_children(&iter);
    if (*n == 0) {
        return NULL;
    }
    ${name} *output = g_new0(${name}, *n);
    while (g_variant_iter_loop(&iter, "s", &str_val)) {
        for (int i = 0; i < ${len(enum.values.parameters)}; i++) {
            if (g_strcmp0(str_val, _${name}StrMap[i]) == 0) {
                output[id++] = (${name})i;
            }
        }
    }
    return output;
}

gboolean _validate_odf_as_enum_${name}(yaml_document_t *doc, yaml_node_t *node,
    GString *prop, GSList **error_list)
{
    gboolean valid = validate_odf_as_string(doc, node, prop, "^.*$", error_list);
    if (!valid) {
        return FALSE;
    }
    const gchar *value = node->data.scalar.value;
    for (int i = 0; i <= ${len(enum.values.parameters)}; i++) {
        if (g_strcmp0(value, ${name}_as_string(i)) == 0) {
            return TRUE;
        }
    }
    *error_list = g_slist_append(*error_list, g_error_new(ODF_ERROR, ODF_ERROR_PROP_VALIDATE_TYPE_ERROR,
        "the value of property %s is is unsupportted, get %s", prop->str, value));
    return FALSE;
    return FALSE;
}

gboolean _validate_odf_as_enum_${name}_v(yaml_document_t *doc, yaml_node_t *node,
    GString *prop, GSList **error_list)
{
    g_assert(doc && node && prop && error_list);
    if (node->type != YAML_SEQUENCE_NODE) {
        *error_list = g_slist_append(*error_list, g_error_new(ODF_ERROR, ODF_ERROR_PROP_VALIDATE_TYPE_ERROR,
            "the node type of property %s is not a sequence, get %s", prop->str, lb_yaml_node_type_str(node->type)));
        return FALSE;
    }
    gsize len = prop->len;
    gint i = 0;
    yaml_node_t *val = NULL;
    gboolean valid = TRUE;
    for (yaml_node_item_t *item = node->data.sequence.items.start; item < node->data.sequence.items.top; item++) {
        g_string_append_printf(prop, ".%d", i);
        val = yaml_document_get_node(doc, *item);
        if (!_validate_odf_as_enum_${name}(doc, val, prop, error_list)) {
            valid = FALSE;
        }
        g_string_truncate(prop, len);
        i++;
    }
    return valid;
}

% endfor
## 生成字典处理函数
% for name, dictionary in intf.dictionaries.items():
typedef struct {
    GHashTable *_hash;
    ${name} dict;
} ${name}Real;
<% key_declare = ", ".join(dictionary.key_obj.declare()).replace("<arg_name>", "key").replace("<const>", "const ") %>\

/**
 * Drop the ${name}${dictionary.key} contained within it
 */
static void ${name}${dictionary.key}_free_data(${name}${dictionary.key} *value)
{
    if (!value) {
        return;
    }

    % for value in dictionary.values.parameters:
        % for line in value.free_func():
    ${line.replace("<arg_name>", "value->" + value.name)};
        % endfor
    % endfor
    g_free(value);
}

/**
 * Drop ${name}${dictionary.key} and the memory contained within it
 * then *value will set NULL
 */
void ${name}${dictionary.key}_free(${name}${dictionary.key} **value)
{
    g_assert(value);
    if (*value == NULL) {
        return;
    }
    ${name}${dictionary.key}_free_data(*value);
    *value = NULL;
}

/**
 * Note: the ownership NOT transferred
 */
static ${name}${dictionary.key} *${name}_lookup(const ${name} *dict, ${key_declare})
{
    % if dictionary.key_is_string:
    if (!dict || !key) {
    % else:
    if (!dict) {
    % endif
        return NULL;
    }

    const ${name}Real *dict_real = CONTAINER_OF(dict, ${name}Real, dict);
    return (${name}${dictionary.key} *)g_hash_table_lookup(dict_real->_hash, GUINT_TO_POINTER((guint64)key));
}

/**
 * ${name}_insert
 * if return TRUE, ownership of `value` is transferred to the dict
 */
static gboolean ${name}_insert(const ${name} *dict, ${key_declare}, ${name}${dictionary.key} **value)
{
    % if dictionary.key_is_string:
    if (!dict || !key || !value || !(*value)) {
    % else:
    if (!dict || !value || !(*value)) {
    % endif
        return FALSE;
    }

    const ${name}Real *dict_real = CONTAINER_OF(dict, ${name}Real, dict);
    % if dictionary.key_type in ["string", "object_path", "signature"]:
    gboolean ret = g_hash_table_insert(dict_real->_hash, g_strdup(key), *value);
    % else:
    gboolean ret = g_hash_table_insert(dict_real->_hash, GUINT_TO_POINTER((guint64)key), *value);
    % endif
    if (ret) {
        *value = NULL;
    }
    return ret;
}

/**
 * ${name}_remove
 * Remove a `key` member from then `dict`
 * the key (not the input argument key) and value stored in the dict will be release after removed
 */
static gboolean ${name}_remove(const ${name} *dict, ${key_declare})
{
    % if dictionary.key_is_string:
    if (!dict || !key) {
    % else:
    if (!dict) {
    % endif
        return FALSE;
    }

    const ${name}Real *dict_real = CONTAINER_OF(dict, ${name}Real, dict);
    return g_hash_table_remove(dict_real->_hash, GUINT_TO_POINTER((guint64)key));
}

/**
 * ${name}_contains
 * Check whether the `key` member exists in the `dict`
 */
static gboolean ${name}_contains(const ${name} *dict, ${key_declare})
{
    const ${name}${dictionary.key} *data = ${name}_lookup(dict, key);
    return data ? TRUE : FALSE;
}

/**
 * ${name}_clear
 * Clear `dict`
 */
static void ${name}_clear(const ${name} *dict)
{
    if (!dict) {
        return;
    }

    const ${name}Real *dict_real = CONTAINER_OF(dict, ${name}Real, dict);
    g_hash_table_remove_all(dict_real->_hash);
}

static void ${name}_foreach(const ${name} *dict, ${name}_func func, gpointer user_data)
{
    if (!dict || !func) {
        return;
    }

    const ${name}Real *dict_real = CONTAINER_OF(dict, ${name}Real, dict);
    g_hash_table_foreach(dict_real->_hash, (GHFunc)func, user_data);
}

static void ${name}_init(${name} *dict)
{
    dict->lookup = ${name}_lookup;
    dict->insert = ${name}_insert;
    dict->remove = ${name}_remove;
    dict->contains = ${name}_contains;
    dict->clear = ${name}_clear;
    dict->foreach = ${name}_foreach;
}

${name} *${name}_new(void)
{
    ${name}Real *output = g_new0(${name}Real, 1);
    output->_hash = g_hash_table_new_full(${dictionary.hash_func}, ${dictionary.equal_func}, ${dictionary.key_free},
        (GDestroyNotify)${name}${dictionary.key}_free_data);
    ${name}_init(&output->dict);
    return &output->dict;
}

/**
 * convert ${name}${dictionary.key} to GVariant object and add to dict_builder
 */
static void ${name}_foreach_encode(${key_declare}, ${name}${dictionary.key} *value, GVariantBuilder *dict_builder)
{
    % if dictionary.key_is_string:
    g_assert(key && value && dict_builder);
    % else:
    g_assert(value && dict_builder);
    % endif

    __attribute__((unused)) GVariant *tmp = NULL;
    GVariantBuilder builder;
    % if len(dictionary.values.parameters) == 1:
    ## 当只有一个成员时直接添加值
    const gchar *sig = "{${dictionary.key_obj.signature}${dictionary.values.signature}}";
    % else:
    ## 当有多个成员时第二个值为结构体
    const gchar *sig = "{${dictionary.key_obj.signature}(${dictionary.values.signature})}";
    % endif
    g_variant_builder_init(&builder, G_VARIANT_TYPE(sig));
    % for line in dictionary.key_obj.encode_func():
    ${line.replace("<arg_out>", "tmp").replace("<arg_name>", "key")};
    % endfor
    g_variant_builder_add_value(&builder, tmp);
    % if len(dictionary.values.parameters) == 1:
        % for value in dictionary.values.parameters:
    /* ${value.description} */
            % for line in value.encode_func():
    ${line.replace("<arg_out>", "tmp").replace("n_<arg_name>", "value->n_" + value.name).replace("<arg_name>", "value->" + value.name)};
            % endfor
    g_variant_builder_add_value(&builder, tmp);
        % endfor
    % else:
    GVariantBuilder value_builder;
    const gchar *val_sig = "(${dictionary.values.signature})";
    g_variant_builder_init(&value_builder, G_VARIANT_TYPE(val_sig));

        % for value in dictionary.values.parameters:
    /* ${value.description} */
            % for line in value.encode_func():
    ${line.replace("<arg_out>", "tmp").replace("n_<arg_name>", "value->n_" + value.name).replace("<arg_name>", "value->" + value.name)};
            % endfor
    g_variant_builder_add_value(&value_builder, tmp);
        % endfor
    g_variant_builder_add_value(&builder, g_variant_builder_end(&value_builder));

    % endif
    g_variant_builder_add_value(dict_builder, g_variant_builder_end(&builder));
}

/**
 * Encode ${name} to GVariant object
 */
GVariant *${name}_encode(const ${name} *dict)
{
    GVariantBuilder builder;

    const gchar *sig = "${dictionary.signature}";
    g_variant_builder_init(&builder, G_VARIANT_TYPE(sig));
    if (dict) {
        dict->foreach(dict, (${name}_func)${name}_foreach_encode, (gpointer)&builder);
    }
    return g_variant_builder_end(&builder);
}

${name} *${name}_decode(GVariant *in)
{
    GVariantIter iter;
    GVariantIter kv_iter;
    % if len(dictionary.values.parameters) > 1:
    GVariantIter item_iter;
    % endif
    GVariant *next_mem = NULL;

    ${name} *dict = ${name}_new();
    if (!in) {
        return dict;
    }

    g_variant_iter_init(&iter, in);
    while (TRUE) {
        cleanup_unref GVariant *next_item = g_variant_iter_next_value(&iter);
        if (!next_item) {
            return dict;
        }
        g_variant_iter_init(&kv_iter, next_item);
        cleanup_unref GVariant *key = g_variant_iter_next_value(&kv_iter);

        ${", ".join(dictionary.key_obj.declare()).replace("<arg_name>", "key_val").replace("<const>", "")};
        % for line in dictionary.key_obj.decode_func():
        ${line.replace("<arg_name>", "key").replace("<arg_in>", "key_val")};
        % endfor
        ## 创建一个新的字典成员
        ${name}${dictionary.key} *item = g_new0(${name}${dictionary.key}, 1);
        ## 只有一个成员场景
        % if len(dictionary.values.parameters) == 1:
            % for prop in dictionary.values.parameters:
        /* decode ${prop.name} */
        next_mem = g_variant_iter_next_value(&kv_iter);
                % for line in prop.decode_func():
        ${line.replace("<arg_name>", "next_mem").replace("n_<arg_in>", "item->n_" + prop.name).replace("<arg_in>", "item->" + prop.name)};
                % endfor
        g_variant_unref(next_mem);
            % endfor
        % else:
        ## 有多个成员时需要创建新的迭代器
        cleanup_unref GVariant *value = g_variant_iter_next_value(&kv_iter);
        g_variant_iter_init(&item_iter, value);
            % for prop in dictionary.values.parameters:
        /* decode ${prop.name} */
        next_mem = g_variant_iter_next_value(&item_iter);
                % for line in prop.decode_func():
        ${line.replace("<arg_name>", "next_mem").replace("n_<arg_in>", "item->n_" + prop.name).replace("<arg_in>", "item->" + prop.name)};
                % endfor
        g_variant_unref(next_mem);
            % endfor
        % endif
        dict->insert(dict, key_val, &item);
        % for line in dictionary.key_obj.free_func():
        ${line.replace("<arg_name>", "key_val")};
        % endfor
    }
}

void ${name}_free(${name} **dict)
{
    if (!dict || !(*dict)) {
        return;
    }

    ${name}Real *dict_real = CONTAINER_OF(*dict, ${name}Real, dict);
    g_hash_table_destroy(dict_real->_hash);
    g_free(dict_real);
    *dict = NULL;
}

GVariant *${name}_encode_v(${name} * const *dicts)
{
    GVariantBuilder builder;
    const gchar *sig = "a${dictionary.signature}";
    g_variant_builder_init(&builder, G_VARIANT_TYPE(sig));
    for (int i = 0; dicts && dicts[i]; i++) {
        GVariant *tmp = ${name}_encode(dicts[i]);
        g_variant_builder_add_value(&builder, tmp);
    }
    return g_variant_builder_end(&builder);
}

${name} **${name}_decode_v(GVariant *in)
{
    if (!in) {
        return NULL;
    }

    GVariantIter iter;
    g_variant_iter_init(&iter, in);
    gsize n = g_variant_iter_n_children(&iter);
    if (n == 0) {
        return NULL;
    }
    ${name} **output = g_new0(${name} *, n + 1);
    for (gsize i = 0; i < n; i++) {
        GVariant *tmp = g_variant_iter_next_value(&iter);
        output[i] = ${name}_decode(tmp);
        g_variant_unref(tmp);
    }
    return output;
}

void ${name}_free_v(${name} ***value)
{
    if (!value || !(*value)) {
        return;
    }
    for (int i = 0; (*value)[i]; i++) {
        ${name}_free((*value) + i);
    }
    g_free(*value);
    *value = NULL;
}

gboolean _validate_odf_as_dict_${name}(yaml_document_t *doc, yaml_node_t *node,
    GString *prop, GSList **error_list)
{
    g_assert(doc && node && prop && error_list);
    if (node->type != YAML_SEQUENCE_NODE) {
        *error_list = g_slist_append(*error_list, g_error_new(ODF_ERROR, ODF_ERROR_PROP_VALIDATE_TYPE_ERROR,
            "the node type of property %s is not a sequence, get %s", prop->str, lb_yaml_node_type_str(node->type)));
        return FALSE;
    }

    gboolean valid = TRUE;
    GHashTable *prop_table = NULL;
    yaml_node_t *val = NULL;
    gsize len = prop->len;
    yaml_node_item_t *top = node->data.sequence.items.top;
    yaml_node_item_t *start = node->data.sequence.items.start;
    for (yaml_node_item_t *item = start; item < top; item++) {
        val = yaml_document_get_node(doc, *item);
        ## 转换成hash表以获取key和properties
        prop_table = load_yaml_mapping_to_hash_table(doc, val);
        yaml_node_t *key = g_hash_table_lookup(prop_table, "key");
        yaml_node_t *properties = g_hash_table_lookup(prop_table, "properties");
        g_hash_table_destroy(prop_table);
        g_string_append_printf(prop, ".key");
        % for func in dictionary.key_obj.odf_validate(False):
        if (!${func.replace("node,", "key,")})
            valid = FALSE;
        % endfor
        g_string_truncate(prop, len);

        ## 转换成hash表
        prop_table = load_yaml_mapping_to_hash_table(doc, properties);
        ## 迭代所有成员并从odf中还原数据
        % for prop in dictionary.values.parameters:
        val = g_hash_table_lookup(prop_table, "${prop.name}");
        if (val) {
            g_string_append(prop, ".properties.${prop.name}");
            % for func in prop.odf_validate(False):
            if (!${func.replace("node,", "val,")})
                valid = FALSE;
            % endfor
            g_string_truncate(prop, len);
        }
        % endfor
        g_hash_table_destroy(prop_table);
    }
    return valid;
}

gboolean _validate_odf_as_dict_${name}_v(yaml_document_t *doc, yaml_node_t *node,
    GString *prop, GSList **error_list)
{
    g_assert(doc && node && prop && error_list);
    if (node->type != YAML_SEQUENCE_NODE) {
        *error_list = g_slist_append(*error_list, g_error_new(ODF_ERROR, ODF_ERROR_PROP_VALIDATE_TYPE_ERROR,
            "the node type of property %s is not a sequence, get %s", prop->str, lb_yaml_node_type_str(node->type)));
        return FALSE;
    }
    gsize len = prop->len;
    gint i = 0;
    yaml_node_t *val = NULL;
    gboolean valid = TRUE;
    for (yaml_node_item_t *item = node->data.sequence.items.start; item < node->data.sequence.items.top; item++) {
        g_string_append_printf(prop, ".%d", i);
        val = yaml_document_get_node(doc, *item);
        if (!_validate_odf_as_dict_${name}(doc, val, prop, error_list)) {
            valid = FALSE;
        }
        g_string_truncate(prop, len);
        i++;
    }
    return valid;
}

% endfor
## 生成每个属性的GDBus属性GDBusPropertyInfo对象name}
% for prop in intf.properties:
    % if prop.private:
        % if len(prop.annotations) > 0:
/* annotation for the property ${prop.name} */
static GDBusAnnotationInfo ${class_name}_prop_${prop.name}_annotations_i[] = {
            % for anno in prop.annotations:
    {
        .ref_count = -1,
        .key = "${anno.name}",
        .value = "${anno.value}",
    },
            % endfor
};\
<% id = 0 %>
static GDBusAnnotationInfo *${class_name}_prop_${prop.name}_annotations[] =
{
            % for anno in prop.annotations:
    &${class_name}_prop_${prop.name}_annotations_i[${id}],\
<% id = id + 1 %>
            % endfor
    NULL,
};

        % endif
static GDBusPropertyInfo ${class_name}_property_${prop.name} =
{
    .ref_count = -1,
    .name = "${prop.name}",
    .signature = "${prop.signature}",
    .flags = ${prop.access_flag},
        % if len(prop.annotations) > 0:
    .annotations = ${class_name}_prop_${prop.name}_annotations,
        % endif
};

    % endif
% endfor
% if len(intf.properties):
LBBase *_get_real_object(const ${class_name} *object)
{
    LBBase *real = (LBBase *)strstr((const char *)object, LB_MAGIC);
    if ((gconstpointer)real != (gconstpointer)object) {
        log_error("Get real object fail, Perhaps the memory has been freed, call abort() now");
        abort();
    }
    return real;
}
% endif
## 只有自动生成工具版本号大于等于3的才会生成get和set方法
% if codegen_version >= 3:
% for prop in intf.properties:
static void ${class_name}_set_${prop.name}_variant(LBO *object, GVariant *value)
{
    g_assert(value && object);
    ${class_name} *real_obj = (${class_name} *)_get_real_object(object);
    % for line in prop.free_func():
    ${line.replace("<arg_name>", "real_obj->" + prop.name)};
    % endfor
    % for line in prop.decode_func():
    ${line.replace("n_<arg_in>", "real_obj->n_" + prop.name).replace("<arg_in>", "real_obj->" + prop.name).replace("<arg_name>", "value")};
    % endfor
}

static GVariant *${class_name}_get_${prop.name}_variant(LBO *object)
{
    g_assert(object);
    GVariant *out = NULL;
    ${class_name} *real_obj = (${class_name} *)_get_real_object(object);
    % for line in prop.encode_func():
    ${line.replace("<arg_out>", "out").replace("n_<arg_name>", "real_obj->n_" + prop.name).replace("<arg_name>", "real_obj->" + prop.name)};
    % endfor
    return out;
}

%endfor
%endif
static ${class_name}_Properties _${class_name}_properties =
{
<% id = 0 %>\
    % for prop in intf.properties:
    .${prop.name} = {
        .id = ${id},
        .name = "${prop.name}",
        % if prop.private:
        .info = &${class_name}_property_${prop.name},
        % else:
        .info = NULL, /* load from /usr/share/dbus-1/interfaces/${intf.name} by lb_init */
        % endif
        .offset = offsetof(${class_name}, ${prop.name}),
% if codegen_version >= 3:
        .flags = ${prop.desc_flags},
        .set = ${class_name}_set_${prop.name}_variant,
        .get = ${class_name}_get_${prop.name}_variant
% else:
        .flags = ${prop.desc_flags}
% endif
    },
<% id = id + 1 %>\
    % endfor
    .__reserved__ =
    {
        .name = NULL,       /* __reserved__ */
    },
};

const ${class_name}_Properties *${class_name}_properties_const(void)
{
    return &_${class_name}_properties;
}

% for method in intf.fake_methods:
% if not method.is_plugin:
## 方法${method.name}的请求体序列化函数
/* ${class_name}_${method.name}_Req请求结构体类型序列化（struct转GVariant）函数 */
GVariant *${class_name}_${method.name}_Req_encode(${class_name}_${method.name}_Req *value)
{
    static ${class_name}_${method.name}_Req default_val;
    if (!value) {
        value = &default_val;
    }
    __attribute__((unused)) GVariant *tmp = NULL;
    GVariantBuilder builder;
    const gchar *sig = "${method.in_signature}";
    g_variant_builder_init(&builder, G_VARIANT_TYPE(sig));
    % for prop in method.parameters.parameters:
        % for line in prop.encode_func():
    ${line.replace("<arg_out>", "tmp").replace("n_<arg_name>", "value->n_" + prop.name).replace("<arg_name>", "value->" + prop.name)};
        % endfor
    g_variant_builder_add_value(&builder, tmp);
    % endfor
    return g_variant_builder_end(&builder);
}

## 方法${method.name}的请求体反序列化函数
/* ${class_name}_${method.name}_Req结构体类型反序列化（GVariant转struct）函数，返回以NULL结束的指针数组 */
${class_name}_${method.name}_Req *${class_name}_${method.name}_Req_decode(GVariant *in)
{
    GVariantIter iter;
    __attribute__((unused)) GVariant *tmp = NULL;
    ${class_name}_${method.name}_Req *output = g_new0(${class_name}_${method.name}_Req, 1);
    if (!in) {
        return output;
    }

    (void)g_variant_iter_init(&iter, in);
    % for prop in method.parameters.parameters:
    /* process ${prop.name} */
    tmp = g_variant_iter_next_value(&iter);
        % for line in prop.const_decode_func():
    ${line.replace("<arg_name>", "tmp").replace("n_<arg_in>", "output->n_" + prop.name).replace("<arg_in>", "output->" + prop.name)};
        % endfor
    g_variant_unref(tmp);
    % endfor
    return output;
}
% endif

## 方法${method.name}的请求体释放函数
/* ${class_name}_${method.name}_Req结构体指针释放 */
void ${class_name}_${method.name}_Req_free(${class_name}_${method.name}_Req **value)
{
    if (!value || !(*value)) {
        return;
    }
    % for prop in method.parameters.parameters:
        % for line in prop.const_free_func():
    ${line.replace("<arg_name>", "(*value)->" + prop.name)};
        % endfor
    % endfor
    g_free(*value);
    *value = NULL;
}

% if not method.is_plugin:
/* ${class_name}_${method.name}_Rsp请求结构体类型序列化（struct转GVariant）函数 */
GVariant *${class_name}_${method.name}_Rsp_encode(${class_name}_${method.name}_Rsp *value)
{
    static ${class_name}_${method.name}_Rsp default_val;
    if (!value) {
        value = &default_val;
    }
    __attribute__((unused)) GVariant *tmp = NULL;
    GVariantBuilder builder;
    const gchar *sig = "${method.out_signature}";
    g_variant_builder_init(&builder, G_VARIANT_TYPE(sig));
    % for prop in method.returns.parameters:
        % for line in prop.encode_func():
    ${line.replace("<arg_out>", "tmp").replace("n_<arg_name>", "value->n_" + prop.name).replace("<arg_name>", "value->" + prop.name)};
        % endfor
    g_variant_builder_add_value(&builder, tmp);
    % endfor
    return g_variant_builder_end(&builder);
}

## 方法${method.name}的响应体反序列化函数
/* ${class_name}_${method.name}_Rsp结构体类型反序列化（GVariant转struct）函数，返回以NULL结束的指针数组 */
${class_name}_${method.name}_Rsp *${class_name}_${method.name}_Rsp_decode(GVariant *in)
{
    GVariantIter iter;
    __attribute__((unused)) GVariant *tmp = NULL;
    ${class_name}_${method.name}_Rsp *output = g_new0(${class_name}_${method.name}_Rsp, 1);
    if (!in) {
        return output;
    }

    (void)g_variant_iter_init(&iter, in);
    % for prop in method.returns.parameters:
    /* process ${prop.name} */
    tmp = g_variant_iter_next_value(&iter);
        % for line in prop.decode_func():
    ${line.replace("<arg_name>", "tmp").replace("n_<arg_in>", "output->n_" + prop.name).replace("<arg_in>", "output->" + prop.name)};
        % endfor
    g_variant_unref(tmp);
    % endfor
    return output;
}
% endif

## 方法${method.name}的响应体释放函数
/* ${class_name}_${method.name}_Rsp结构体指针释放 */
void ${class_name}_${method.name}_Rsp_free(${class_name}_${method.name}_Rsp **value)
{
    if (!value || !(*value)) {
        return;
    }
    % for prop in method.returns.parameters:
        % for line in prop.free_func():
    ${line.replace("<arg_name>", "(*value)->" + prop.name)};
        % endfor
    % endfor
    g_free(*value);
    *value = NULL;
}

% endfor
static ${class_name}_Methods _${class_name}_methods =
{
% for method in intf.methods:
    .${method.name} = {
        .name = "${method.name}",
        .req_signature = "${method.in_signature}",
        .req_decode = (lbo_message_decode_handler)${class_name}_${method.name}_Req_decode,
        .req_encode = (lbo_message_encode_handler)${class_name}_${method.name}_Req_encode,
        .req_free = (lbo_message_free_handler)${class_name}_${method.name}_Req_free,
        .rsp_signature = "${method.out_signature}",
        .rsp_decode = (lbo_message_decode_handler)${class_name}_${method.name}_Rsp_decode,
        .rsp_encode = (lbo_message_encode_handler)${class_name}_${method.name}_Rsp_encode,
        .rsp_free = (lbo_message_free_handler)${class_name}_${method.name}_Rsp_free,
    },
% endfor
    .__reserved__ = {
        .name = NULL,
    }
};

${class_name}_Methods *${class_name}_methods(void)
{
    return &_${class_name}_methods;
}

% if len(intf.plugin.actions) > 0:
    % for action in intf.plugin.actions:
typedef struct {
    gpointer user_data;
    ${class_name}_${action.name}_action action;
} _${class_name}_${action.name}_PluginAction;
static GSList *_${class_name}_${action.name}_actions = NULL;
static GMutex _${class_name}_${action.name}_lock;

/* Register a new plugin action, can't register repeated with same action */
int ${class_name}_${action.name}_register(const gchar *req_signature, const gchar *rsp_signature,
    ${class_name}_${action.name}_action action, gpointer user_data)
{
    if (!req_signature) {
        log_error("Register ${action.name} failed because parameter req_signature is NULL");
        return -1;
    }
    if (!rsp_signature) {
        log_error("Register ${action.name} failed because parameter rsp_signature is NULL");
        return -1;
    }
    if (g_strcmp0(req_signature, "${action.in_signature}") != 0) {
        log_error("Register ${action.name} failed because parameter "
            "req_signature not match with \"{action.in_signature}\", get \"%s\"", req_signature);
        return -1;
    }
    if (g_strcmp0(rsp_signature, "${action.out_signature}") != 0) {
        log_error("Register ${action.name} failed because parameter "
            "rsp_signature not match with \"{action.out_signature}\", get \"%s\"", rsp_signature);
        return -1;
    }
    g_mutex_lock(&_${class_name}_${action.name}_lock);
    for (GSList *item = _${class_name}_${action.name}_actions; item; item = item->next) {
        _${class_name}_${action.name}_PluginAction *old_handler = (_${class_name}_${action.name}_PluginAction *)item->data;
        if (action == old_handler->action || user_data == old_handler->user_data) {
            g_mutex_unlock(&_${class_name}_${action.name}_lock);
            return 0;
        }
    }
    _${class_name}_${action.name}_PluginAction *handler = g_new0(_${class_name}_${action.name}_PluginAction, 1);
    handler->user_data = user_data;
    handler->action = action;
    _${class_name}_${action.name}_actions = g_slist_append(_${class_name}_${action.name}_actions, handler);
    g_mutex_unlock(&_${class_name}_${action.name}_lock);
    return 0;
}

void ${class_name}_${action.name}_unregister(${class_name}_${action.name}_action action)
{
    g_mutex_lock(&_${class_name}_${action.name}_lock);
    for (GSList *item = _${class_name}_${action.name}_actions; item; item = item->next) {
        _${class_name}_${action.name}_PluginAction *old_handler = (_${class_name}_${action.name}_PluginAction *)item->data;
        if (action == old_handler->action) {
            _${class_name}_${action.name}_actions = g_slist_remove(_${class_name}_${action.name}_actions, old_handler);
            g_free(old_handler);
            break;
        }
        old_handler = NULL;
    }
    g_mutex_unlock(&_${class_name}_${action.name}_lock);
}

<% RSP_PARA = f'' %>\
<% REQ_PARA = f'' %>\
<% REQ_NAME = f'' %>\
    % if len(action.returns.parameters) > 0:
<% RSP_PARA = f', {class_name}_{action.name}_Rsp **rsp' %>\
    % endif
    % if len(action.parameters.parameters) > 0:
<% REQ_PARA = f', const {class_name}_{action.name}_Req *req' %>\
<% REQ_NAME = f', req' %>\
    % endif
int ${class_name}_${action.name}_run(const ${class_name} *object${REQ_PARA}${RSP_PARA})
{
    gint result = 0;
    g_mutex_lock(&_${class_name}_${action.name}_lock);
    for (GSList *item = _${class_name}_${action.name}_actions; item; item = item->next) {
        _${class_name}_${action.name}_PluginAction *handler = (_${class_name}_${action.name}_PluginAction *)item->data;
    % if len(action.returns.parameters) > 0:
        if (rsp && *rsp) {
            ${class_name}_${action.name}_Rsp_free(rsp);
        }
        gint ret = handler->action(object${REQ_NAME}, rsp, handler->user_data);
    % else:
        gint ret = handler->action(object${REQ_NAME}, handler->user_data);
    % endif
        if (ret != 0)
            result = ret;
        % if action.policy == "return_any_success":
        /* return when any action success(ret == 0) */
        if (ret == 0)
            break;
        % elif action.policy == "return_any_fail":
        /* return when any action failed(ret != 0) */
        if (ret != 0)
            break;
        % endif
    }
    g_mutex_unlock(&_${class_name}_${action.name}_lock);
    return result;
}

    % endfor
% endif
% for signal in intf.signals:
## 方法${method.name}的响应体序列化函数
/* ${class_name}_${signal.name}_Msg请求结构体类型序列化（struct转GVariant）函数 */
GVariant *${class_name}_${signal.name}_Msg_encode(${class_name}_${signal.name}_Msg *value)
{
    static ${class_name}_${signal.name}_Msg default_val;
    if (!value) {
        value = &default_val;
    }
    __attribute__((unused)) GVariant *tmp = NULL;
    GVariantBuilder builder;
    const gchar *sig = "${signal.signature}";
    g_variant_builder_init(&builder, G_VARIANT_TYPE(sig));
    % for prop in signal.properties.parameters:
        % for line in prop.encode_func():
    ${line.replace("<arg_out>", "tmp").replace("n_<arg_name>", "value->n_" + prop.name).replace("<arg_name>", "value->" + prop.name)};
        % endfor
    g_variant_builder_add_value(&builder, tmp);
    % endfor
    return g_variant_builder_end(&builder);
}

## 方法${signal.name}的响应体反序列化函数
/* ${class_name}_${signal.name}_Msg结构体类型反序列化（GVariant转struct）函数，返回以NULL结束的指针数组 */
${class_name}_${signal.name}_Msg *${class_name}_${signal.name}_Msg_decode(GVariant *in)
{
    GVariantIter iter;
    __attribute__((unused)) GVariant *tmp = NULL;
    ${class_name}_${signal.name}_Msg *output = g_new0(${class_name}_${signal.name}_Msg, 1);
    if (!in) {
        return output;
    }

    (void)g_variant_iter_init(&iter, in);
    % for prop in signal.properties.parameters:
    /* process ${prop.name} */
    tmp = g_variant_iter_next_value(&iter);
        % for line in prop.const_decode_func():
    ${line.replace("<arg_name>", "tmp").replace("n_<arg_in>", "output->n_" + prop.name).replace("<arg_in>", "output->" + prop.name)};
        % endfor
    g_variant_unref(tmp);
    % endfor
    return output;
}

## 方法${signal.name}的响应体释放函数
/* ${class_name}_${signal.name}_Msg结构体指针释放 */
void ${class_name}_${signal.name}_Msg_free(${class_name}_${signal.name}_Msg **value)
{
    if (!value || !(*value)) {
        return;
    }

    % for prop in signal.properties.parameters:
        % for line in prop.const_free_func():
    ${line.replace("<arg_name>", "(*value)->" + prop.name)};
        % endfor
    % endfor
    g_free(*value);
    *value = NULL;
}

% endfor
static ${class_name}_Signals _${class_name}_signals = {
    % for signal in intf.signals:
    .${signal.name} = {
        .name = "${signal.name}",
        .msg_signature = "${signal.signature}",
        .msg_decode = (lbo_message_decode_handler)${class_name}_${signal.name}_Msg_decode,
        .msg_encode = (lbo_message_encode_handler)${class_name}_${signal.name}_Msg_encode,
        .msg_free = (lbo_message_free_handler)${class_name}_${signal.name}_Msg_free,
    },
    % endfor
    .__reserved__ = {
        .name = NULL,
    }
};

${class_name}_Signals *${class_name}_signals(void)
{
    return &_${class_name}_signals;
}

% for prop in intf.properties:
static gboolean _validate_odf_prop_${prop.name}(yaml_document_t *doc, GHashTable *prop_table,
    GString *prop, GSList **error_list)
{
    gboolean valid = TRUE;
    gsize len = prop->len;
    yaml_node_t *node = g_hash_table_lookup(prop_table, "${prop.name}");
    do {
        if (!node) {
    ## 检查属性是否存在
    % if "required" in prop.flags:
            *error_list = g_slist_append(*error_list, g_error_new(ODF_ERROR, ODF_ERROR_PROP_MISSING, "Property ${prop.name} is missing"));
            valid = FALSE;
    % endif
            break;
        }
        g_string_append(prop, ".${prop.name}");
    % if "refobj" not in prop.flags:
        if (validate_odf_as_ref_prop(doc, node, prop))
            break;
    % endif
    % if len(prop.odf_validate(True)) > 1:
        % for func in prop.odf_validate(True):
        if (valid && !${func})
            valid = FALSE;
        % endfor
    % else:
        % for func in prop.odf_validate(True):
        valid = ${func};
        % endfor
    % endif
    } while (0);
    g_string_truncate(prop, len);
    return valid;
}

%endfor
gboolean ${intf.name.replace(".", "_")}_validate_odf(yaml_document_t *doc, yaml_node_t *node,
    const gchar *object_name, GSList **error_list)
{
    g_assert(doc && node && object_name && error_list);
    if (!doc || !node || !object_name || !error_list) {
        return FALSE;
    }

    if (node->type != YAML_MAPPING_NODE) {
        *error_list = g_slist_append(*error_list, g_error_new(ODF_ERROR, ODF_ERROR_PROP_VALIDATE_TYPE_ERROR,
            "the node type of object %s is not a mapping, get %s", object_name, lb_yaml_node_type_str(node->type)));
        return FALSE;
    }
    cleanup_gstring GString *prop = g_string_sized_new(128);
    g_string_printf(prop, "%s", object_name);
    gboolean valid = TRUE;
    GHashTable *prop_table = load_yaml_mapping_to_hash_table(doc, node);
    % for prop in stru.values.parameters:
    valid = _validate_odf_prop_${prop.name}(doc, prop_table, prop, error_list) && valid;
    % endfor
    g_hash_table_destroy(prop_table);
    return valid;
}

% if len(intf.plugin.actions) > 0:
static void __attribute__((constructor(101))) ${class_name}_public_register(void)
{
    % for action in intf.plugin.actions:
    g_mutex_init(&_${class_name}_${action.name}_lock);
    % endfor
}

% endif