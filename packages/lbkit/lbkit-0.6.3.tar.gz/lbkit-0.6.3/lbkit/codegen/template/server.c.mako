<% from lbkit.codegen.ctype_defination import StringValidator %>\
#include "lb_base.h"
#include "${intf.name}.h"

<%
class_name = intf.alias
properties = "_" + class_name + "_properties"
signal_processer = "_" + class_name + "_signals"
%>\
## 定义结构体ODF加载函数
% for name, stru in intf.structures.items():
/* ${name} structure object */
/* START: 结构体${name}及其数组类型的ODF加载函数 */
${name} *_load_odf_as_${name}(yaml_document_t *doc, yaml_node_t *node);
${name} **_load_odf_as_${name}_v(yaml_document_t *doc, yaml_node_t *node);

% endfor
## 定义枚举ODF加载函数
% for name, enum in intf.enumerations.items():
/* START: 枚举${name}及其数组类型的ODF加载函数 */
${name} _load_odf_as_${name}(yaml_document_t *doc, yaml_node_t *node);
${name} *_load_odf_as_${name}_v(yaml_document_t *doc, yaml_node_t *node, gsize *n);

% endfor
## 定义字典ODF加载函数
% for name, dictionary in intf.dictionaries.items():
/* START: 字典${name}及其数组类型的ODF加载函数 */
${name} *_load_odf_as_${name}(yaml_document_t *doc, yaml_node_t *node);
${name} **_load_odf_as_${name}_v(yaml_document_t *doc, yaml_node_t *node);

% endfor
## 定义结构体ODF加载函数
% for name, stru in intf.structures.items():
/* ${name} structure object */
/* START: 结构体${name}及其数组类型的ODF加载函数 */
${name} *_load_odf_as_${name}(yaml_document_t *doc, yaml_node_t *node)
{
<% cnt = 0 %>\
    % for prop in stru.values.parameters:
        % if prop.odf_load_func() is not None:
<% cnt = cnt + 1 %>\
        % endif
    % endfor
% if cnt == 0:
    return g_new0(${name}, 1);
% else:
    __attribute__((unused)) yaml_node_t *val;
    ${name} *output = g_new0(${name}, 1);
    GHashTable *prop_table = load_yaml_mapping_to_hash_table(doc, node);
    % for prop in stru.values.parameters:
        % if prop.odf_load_func() is not None:
    /* process ${prop.name} */
    val = g_hash_table_lookup(prop_table, "${prop.name}");
    if (val)
        ${prop.odf_load_func().replace("n_<arg_name>", "output->n_" + prop.name).replace("<arg_name>", "output->" + prop.name).replace("<node>", "val")};
        % endif
    % endfor

    g_hash_table_destroy(prop_table);
    return output;
% endif
}

${name} **_load_odf_as_${name}_v(yaml_document_t *doc, yaml_node_t *node)
{
    yaml_node_t *val;
    gint i = 0;
    if (node->type != YAML_SEQUENCE_NODE) {
        log_warn("Load array ${name} failed because node type error, need type 1(sequence), get type %d", node->type);
        return g_new0(${name} *, 1);
    }
    yaml_node_item_t *top = node->data.sequence.items.top;
    yaml_node_item_t *start = node->data.sequence.items.start;
    gsize cnt = ((gsize)top - (gsize)start) / sizeof(yaml_node_item_t);
    ${name} **output = g_new0(${name} *, cnt + 1);

    for (yaml_node_item_t *item = start; item < top; item++) {
        val = yaml_document_get_node(doc, *item);
        output[i++] = _load_odf_as_${name}(doc, val);
    }
    return output;
}

% endfor
## 定义枚举ODF加载函数
% for name, enum in intf.enumerations.items():
${name} _load_odf_as_${name}(yaml_document_t *doc, yaml_node_t *node)
{
    g_assert(node->type == YAML_SCALAR_NODE);
    if (node->type != YAML_SCALAR_NODE) {
        return _${name}Invalid;
    }

    for (int i = 0; i <= ${len(enum.values.parameters)}; i++) {
        if (g_strcmp0(node->data.scalar.value, ${name}_as_string(i)) == 0) {
            return (${name})i;
        }
    }
    return _${name}Invalid;
}

${name} *_load_odf_as_${name}_v(yaml_document_t *doc, yaml_node_t *node, gsize *n)
{
    g_assert(doc && node && n);
    yaml_node_t *val;
    gint i = 0;
    if (node->type != YAML_SEQUENCE_NODE) {
        log_warn("Load array ${name} failed because node type error, need type 1(sequence), get type %d", node->type);
        return g_new0(${name}, 1);
    }
    yaml_node_item_t *top = node->data.sequence.items.top;
    yaml_node_item_t *start = node->data.sequence.items.start;
    *n = ((gsize)top - (gsize)start) / sizeof(yaml_node_item_t);
    ${name} *output = g_new0(${name}, *n);

    for (yaml_node_item_t *item = start; item < top; item++) {
        val = yaml_document_get_node(doc, *item);
        output[i++] = _load_odf_as_${name}(doc, val);
    }
    return output;
}

% endfor
## 定义字典ODF加载函数
% for name, dictionary in intf.dictionaries.items():
${name} *_load_odf_as_${name}(yaml_document_t *doc, yaml_node_t *node)
{
    GHashTable *prop_table = NULL;
    yaml_node_t *val = NULL;
    ${name} *dict = ${name}_new();
    yaml_node_item_t *top = node->data.sequence.items.top;
    yaml_node_item_t *start = node->data.sequence.items.start;
    for (yaml_node_item_t *item = start; item < top; item++) {
        val = yaml_document_get_node(doc, *item);
        ## 转换成hash表以获取key和properties
        prop_table = load_yaml_mapping_to_hash_table(doc, val);
        yaml_node_t *key = g_hash_table_lookup(prop_table, "key");
        yaml_node_t *properties = g_hash_table_lookup(prop_table, "properties");
        g_hash_table_destroy(prop_table);

        ${", ".join(dictionary.key_obj.declare()).replace("<arg_name>", "key_val").replace("<const>", "")};
        ${dictionary.key_obj.odf_load_func().replace("<arg_name>", "key_val").replace("<node>", "key")};

        ## 创建一个新的字典成员
        ${name}${dictionary.key} *item = g_new0(${name}${dictionary.key}, 1);
        ## 转换成hash表
        prop_table = load_yaml_mapping_to_hash_table(doc, properties);
        ## 迭代所有成员并从odf中还原数据
        % for prop in dictionary.values.parameters:
            % if prop.odf_load_func() is not None:
        val = g_hash_table_lookup(prop_table, "${prop.name}");
        if (val)
            ${prop.odf_load_func().replace("n_<arg_name>", "item->n_" + prop.name).replace("<arg_name>", "item->" + prop.name).replace("<node>", "val")};
            % endif
        % endfor
        g_hash_table_destroy(prop_table);
        dict->insert(dict, key_val, &item);
        % for line in dictionary.key_obj.free_func():
        ${line.replace("<arg_name>", "key_val")};
        % endfor
    }
    return dict;
}

${name} **_load_odf_as_${name}_v(yaml_document_t *doc, yaml_node_t *node)
{
    yaml_node_t *val;
    gint i = 0;
    if (node->type != YAML_SEQUENCE_NODE) {
        log_warn("Load array ${name} failed because node type error, need type 1(sequence), get type %d", node->type);
        return g_new0(${name} *, 1);
    }
    yaml_node_item_t *top = node->data.sequence.items.top;
    yaml_node_item_t *start = node->data.sequence.items.start;
    gsize cnt = ((gsize)top - (gsize)start) / sizeof(yaml_node_item_t);
    ${name} **output = g_new0(${name} *, cnt + 1);

    for (yaml_node_item_t *item = start; item < top; item++) {
        val = yaml_document_get_node(doc, *item);
        output[i++] = _load_odf_as_${name}(doc, val);
    }
    return output;
}

% endfor
static ${class_name}_Properties ${properties};
static const ${class_name}_Signals *${signal_processer} = NULL;

% for prop in intf.properties:
    % if prop.deprecated:
__attribute__((__deprecated__)) void ${class_name}_set_${prop.name}(const ${class_name} *object,
    ${", ".join(prop.declare()).replace("<arg_name>", "value").replace("<const>", "const ")})
    % else:
void ${class_name}_set_${prop.name}(const ${class_name} *object,
    ${", ".join(prop.declare()).replace("<arg_name>", "value").replace("<const>", "const ")})
    % endif
{
    GVariant *tmp = NULL;
    % for line in prop.encode_func():
    ${line.replace("<arg_out>", "tmp").replace("n_<arg_name>", "n_value").replace("<arg_name>", "value")};
    % endfor
    lbo_set_memory((LBO *)object, &_${class_name}_properties.${prop.name}, tmp);
    g_variant_unref(tmp);
}

% endfor
% for signal in intf.signals:
<% REQ_PARA = f'' %>\
    % if len(signal.properties.parameters) > 0:
<% REQ_PARA = f'const {class_name}_{signal.name}_Msg *msg, ' %>\
    % endif
    % if signal.deprecated:
__attribute__((__deprecated__)) gboolean ${class_name}_${signal.name}_Signal(const ${class_name} *object,
    const gchar *destination, ${REQ_PARA}GError **error)
    % else:
gboolean ${class_name}_${signal.name}_Signal(const ${class_name} *object, const gchar *destination,
    ${REQ_PARA}GError **error)
    % endif
{
    if (error == NULL) {
        log_error("Emit ${signal.name} with parameter error, error is NULL");
        return FALSE;
    }
    if (object == NULL) {
        *error = g_error_new(G_DBUS_ERROR, G_DBUS_ERROR_FAILED, "Emit ${signal.name} with parameter error, object is NULL");
        return FALSE;
    }
    % if len(signal.properties.parameters) == 0:
    void *msg = NULL;
    % endif
    return lb_impl.emit_signal((LBO *)object, destination,
        (const LBSignal *)&${signal_processer}->${signal.name}, msg, error);
}

% endfor
static LBO *_${class_name}_create(const gchar *obj_name, gpointer opaque);
static void _${class_name}_destroy(LBO *obj);
static void _load_from_odf(yaml_document_t *doc, yaml_node_t *node, LBO *lb_obj,
    lbo_property_reference_loaded_handler ref_loaded, gpointer user_data);

static LBInterface _${class_name}_interface = {
    .create = _${intf.alias}_create,
    .destroy = _${class_name}_destroy,
    .validate_odf = ${intf.name.replace(".", "_")}_validate_odf,
    .load_from_odf = _load_from_odf,
    .is_remote = 0,
    .name = "${intf.name}",
    .properties = (LBProperty *)&${properties},
    .interface = NULL,  /* load from usr/share/dbus-1/interfaces/${intf.name} by lb_init */
};

% for prop in intf.properties:
static void _load_odf_as_prop_${prop.name}(yaml_document_t *doc, GHashTable *prop_table,
    ${class_name} *obj, lbo_property_reference_loaded_handler ref_loaded, gpointer user_data)
{
    __attribute__((unused)) gint i = 0;
    const gchar *flags = NULL;
    yaml_node_t *val = g_hash_table_lookup(prop_table, "_${prop.name}_flags");
    if (val && val->type == YAML_SCALAR_NODE) {
        flags = (const gchar *)val->data.scalar.value;
    }
    val = g_hash_table_lookup(prop_table, "${prop.name}");
    ## validate接口在加载odf前完成属性是否必选校验，此处如果是必选属性一定存在
    if (!val) {
        ## 设置默认值
        % if prop.default:
            % if prop.ctype == "boolean":
                % if prop.default:
        obj->${prop.name} = TRUE;
                % endif
            % elif prop.ctype in ["byte", "int16", "uint16", "int32", "uint32", "int64", "uint64", "size", "ssize", "double"]:
                    % if prop.ctype == "uint64":
        obj->${prop.name} = ${prop.default}UL;
                    % elif prop.ctype == "int64":
        obj->${prop.name} = ${prop.default}LL;
                    % else:
        obj->${prop.name} = ${prop.default};
                    % endif
            % elif prop.ctype in ["object_path", "string", "signature"]:
        obj->${prop.name} = g_strdup("${prop.default}");
            % elif prop.ctype == "array[boolean]":
        i = 0;
        obj->n_${prop.name} = ${len(prop.default)};
        obj->${prop.name} = g_new0(gboolean, obj->n_${prop.name});
                % for val in prop.default:
                    % if val:
        obj->${prop.name}[i++] = TRUE;
                    % else:
        obj->${prop.name}[i++] = FALSE;
                    % endif
                % endfor
            % elif prop.ctype in ["array[byte]", "array[int16]", "array[uint16]", "array[int32]", "array[uint32]", "array[int64]", "array[uint64]", "array[size]", "array[ssize]", "array[double]"]:
<% ctype = prop.ctype[6:-1]%>
        i = 0;
        obj->n_${prop.name} = ${len(prop.default)};
        obj->${prop.name} = g_new0(g${ctype},  obj->n_${prop.name});
                % for val in prop.default:
                    % if prop.ctype == "array[uint64]":
        obj->${prop.name}[i++] = ${val}UL;
                    % elif prop.ctype == "array[int64]":
        obj->${prop.name}[i++] = ${val}LL;
                    % else:
        obj->${prop.name}[i++] = ${val};
                    % endif
                % endfor
            % elif prop.ctype in ["array[object_path]", "array[string]", "array[signature]"]:
        i = 0;
        obj->${prop.name} = g_new0(gchar *, ${len(prop.default) + 1});
                % for val in prop.default:
        obj->${prop.name}[i++] = g_strdup("${val}");
                % endfor
            % endif
        % endif
        if (flags) {
            ## 属性不存在时传入的value为空，需要开发者在回调函数中完成异常（有flags无属性值）处理
            ref_loaded(obj, &${properties}.${prop.name}, doc, NULL, user_data, flags);
        }
        return;
    }
    % if "refobj" in prop.flags:
    ref_loaded(obj, &${properties}.${prop.name}, doc, val, user_data, flags);
    % else:
    const gchar *val_str  = (const gchar *)val->data.scalar.value;
    if (val->type == YAML_SCALAR_NODE && val_str[0] == '$' &&
        g_regex_match(lb_ref_prop_regex(), val_str, 0, NULL)) {
        ref_loaded(obj, &${properties}.${prop.name}, doc, val, user_data, flags);
    } else {
        % if prop.odf_load_func() is not None:
        ${prop.odf_load_func().replace("n_<arg_name>", "obj->n_" + prop.name).replace("<arg_name>", "obj->" + prop.name).replace("<node>", "val")};
        % endif
        if (flags) {
            ref_loaded(obj, &${properties}.${prop.name}, NULL, NULL, user_data, flags);
        }
    }
    % endif
}

% endfor
static void _load_from_odf(yaml_document_t *doc, yaml_node_t *node, LBO *lb_obj,
    lbo_property_reference_loaded_handler ref_loaded, gpointer user_data)
{
    g_assert(doc && node && lb_obj);
    if (!lb_obj) {
        return;
    }
<% cnt = 0 %>\
    % for prop in intf.properties:
        % if prop.odf_load_func() is not None:
<% cnt = cnt + 1 %>\
        % endif
    % endfor
% if cnt == 0:
    return;
% else:
    ${class_name} *obj = (${class_name} *)lb_obj;
    ${class_name}_clean(obj);
    GHashTable *prop_table = load_yaml_mapping_to_hash_table(doc, node);
    % for prop in intf.properties:
    _load_odf_as_prop_${prop.name}(doc, prop_table, obj, ref_loaded, user_data);
    % endfor

    g_hash_table_destroy(prop_table);
% endif
}

/**
 * @brief 销毁对象
 *
 * @param lb_obj 待销毁的对象句柄
 */
static void _${class_name}_destroy(LBO *lb_obj)
{
    g_assert(lb_obj);
    ${class_name} *obj = (${class_name} *)lb_obj;
    g_rec_mutex_clear(obj->_base.lock);
    g_free(obj->_base.lock);
    ${class_name}_clean(obj);
    memset(obj, 0, sizeof(${class_name}));
    g_free(obj);
}

/**
 * @brief 分配对象
 *
 * @param obj_name 对象名，需要由调用者分配内存
 * @param opaque 上层应用需要写入对象的用户数据，由上层应用使用
 */
static LBO *_${class_name}_create(const gchar *obj_name, gpointer opaque)
{
    __attribute__((unused)) gint i = 0;
    ${class_name} *obj = g_new0(${class_name}, 1);
    memcpy(obj->_base.magic, LB_MAGIC, strlen(LB_MAGIC) + 1);
    obj->_base.lock = g_new0(GRecMutex, 1);
    g_rec_mutex_init(obj->_base.lock);
    obj->_base.name = obj_name;
    obj->_base.intf = &_${class_name}_interface;
    obj->_base.opaque = opaque;
    % for prop in intf.properties:
        % if prop.default:
            % if prop.ctype == "boolean":
                % if prop.default:
    obj->${prop.name} = TRUE;
                % endif
            % elif prop.ctype in ["byte", "int16", "uint16", "int32", "uint32", "int64", "uint64", "size", "ssize", "double"]:
                    % if prop.ctype == "uint64":
    obj->${prop.name} = ${prop.default}UL;
                    % elif prop.ctype == "int64":
    obj->${prop.name} = ${prop.default}LL;
                    % else:
    obj->${prop.name} = ${prop.default};
                    % endif
            % elif prop.ctype in ["object_path", "string", "signature"]:
    obj->${prop.name} = g_strdup("${prop.default}");
            % elif prop.ctype == "array[boolean]":
    i = 0;
    obj->n_${prop.name} = ${len(prop.default)};
    obj->${prop.name} = g_new0(gboolean, obj->n_${prop.name});
                % for val in prop.default:
                    % if val:
    obj->${prop.name}[i++] = TRUE;
                    % else:
    obj->${prop.name}[i++] = FALSE;
                    % endif
                % endfor
            % elif prop.ctype in ["array[byte]", "array[int16]", "array[uint16]", "array[int32]", "array[uint32]", "array[int64]", "array[uint64]", "array[size]", "array[ssize]", "array[double]"]:
<% ctype = prop.ctype[6:-1]%>
    i = 0;
    obj->n_${prop.name} = ${len(prop.default)};
    obj->${prop.name} = g_new0(g${ctype},  obj->n_${prop.name});
                % for val in prop.default:
                    % if prop.ctype == "array[uint64]":
    obj->${prop.name}[i++] = ${val}UL;
                    % elif prop.ctype == "array[int64]":
    obj->${prop.name}[i++] = ${val}LL;
                    % else:
    obj->${prop.name}[i++] = ${val};
                    % endif
                % endfor
            % elif prop.ctype in ["array[object_path]", "array[string]", "array[signature]"]:
    i = 0;
    obj->${prop.name} = g_new0(gchar *, ${len(prop.default) + 1});
                % for val in prop.default:
    obj->${prop.name}[i++] = g_strdup("${val}");
                % endfor
            % endif
        % endif
    % endfor
    return (LBO *)obj;
}

LBInterface *${class_name}_interface(void)
{
    return &_${class_name}_interface;
}

${class_name}_Properties *${class_name}_properties(void)
{
    return &${properties};
}

static void __attribute__((constructor(150))) ${class_name}_register(void)
{
    // 从公共库中复制信号处理函数
    ${signal_processer} = ${class_name}_signals();
    // 从公共库中复制方法处理函数
    _${class_name}_interface.methods = (LBMethod *)${class_name}_methods();
    _${class_name}_interface.signals = (LBSignal *)${class_name}_signals();

    // 从公共库中复制属性信息
    memcpy(&${properties}, ${class_name}_properties_const(), sizeof(${properties}));
    lb_interface_register(&_${class_name}_interface,
                           "${intf.introspect_xml_sha256}",
                           "/usr/share/dbus-1/interfaces/${intf.name}.xml");
}
