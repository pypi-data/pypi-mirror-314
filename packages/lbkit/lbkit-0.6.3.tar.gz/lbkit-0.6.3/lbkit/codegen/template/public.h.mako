#ifndef __${"_".join(intf.name.upper().split(".", -1))}_PUB_H__
#define __${"_".join(intf.name.upper().split(".", -1))}_PUB_H__

#include <glib-2.0/glib.h>
#include <glib-2.0/gio/gio.h>
#include "lb_base.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Interface ${intf.alias} codegen start */

<% class_name = intf.alias %>\
% for name, stru in intf.structures.items():
/*
 * structure: ${name}
% if len(stru.description.strip()) > 0:
 *
 % for line in stru.description.split("\n"):
   % if len(line.strip()) > 0:
 * ${line.strip()}
   % endif
 % endfor
% endif
 */
typedef struct _${name} ${name};
% endfor
% for name, enum in intf.enumerations.items():
/*
 * enumeration: ${name}
% if len(enum.description.strip()) > 0:
 *
 % for line in enum.description.split("\n"):
   % if len(line.strip()) > 0:
 * ${line.strip()}
   % endif
 % endfor
% endif
 */
typedef enum _${name} ${name};
% endfor
% for name, dictionary in intf.dictionaries.items():
/*
 * dictionary: ${name}
% if len(dictionary.description.strip()) > 0:
 *
 % for line in dictionary.description.split("\n"):
   % if len(line.strip()) > 0:
 * ${line.strip()}
   % endif
 % endfor
% endif
 */
typedef struct _${name}${dictionary.key} ${name}${dictionary.key};
typedef struct _${name} ${name};
% endfor

% for name, stru in intf.structures.items():
    % if name != class_name:
/*
 * structure: ${name}
% if len(stru.description.strip()) > 0:
 *
 % for line in stru.description.split("\n"):
   % if len(line.strip()) > 0:
 * ${line.strip()}
   % endif
 % endfor
% endif
 */
struct _${name} {
        % for prop in stru.values.parameters:
            % for dec in prop.declare():
    ${dec.replace("<arg_name>", prop.name).replace("<const>", "")};
            % endfor
        % endfor
};

    % endif
%endfor
% for name, enum in intf.enumerations.items():
## 枚举定义
enum _${name} {
    % for value in enum.values.parameters:
    ${name}_${value.name},
    % endfor
    _${name}Invalid,
};

const gchar *${name}_as_string(${name} value);

% endfor
% for name, dictionary in intf.dictionaries.items():
struct _${name}${dictionary.key} {
    % for value in dictionary.values.parameters:
        % for line in value.declare():
    ${line.replace("<arg_name>", value.name).replace("<const>", "")};
        % endfor
    % endfor
};
/* Drop ${name}${dictionary.key} and the memory contained within it */
void ${name}${dictionary.key}_free(${name}${dictionary.key} **obj);
<% key_declare = ", ".join(dictionary.key_obj.declare()).replace("<arg_name>", "key").replace("<const>", "const ") %>
typedef void (*${name}_func)(${key_declare}, ${name}${dictionary.key} *value, gpointer user_data);
struct _${name} {
    /* the ownership NOT transferred */
    ${name}${dictionary.key} *(*lookup)(const ${name} *dict, ${key_declare});
    /* if return TRUE, ownership of `value` is transferred to the dict */
    gboolean (*insert)(const ${name} *dict, ${key_declare}, ${name}${dictionary.key} **value);
    gboolean (*remove)(const ${name} *dict, ${key_declare});
    gboolean (*contains)(const ${name} *dict, ${key_declare});
    void (*clear)(const ${name} *dict);
    void (*foreach)(const ${name} *dict, ${name}_func func, gpointer user_data);
};
/* Create a new ${name} object */
${name} *${name}_new(void);

% endfor
## 定义结构体编解码和释放函数
% for name, stru in intf.structures.items():
/* ${name} structure object */
/* START: 结构体${name}及其数组类型的序列化、反序列化、释放函数 */
GVariant *${name}_encode(const ${name} *value);
${name} *${name}_decode(GVariant *in);
// Clean up the memory of structure and it's all members, `*value` will to NULL
void ${name}_free(${name} **value);
// Clean up the memory of members managed by structure ${name}
void ${name}_clean(${name} *value);

${name} **${name}_decode_v(GVariant *in);
GVariant *${name}_encode_v(${name} * const *value);
// Clean up the memory of structure array and it's all members, `*value` will to NULL
void ${name}_free_v(${name} ***value);
/* END: 结构体${name}及其数组类型的序列化、反序列化、释放函数 */

% endfor
## 定义枚举编解码函数
% for name, enum in intf.enumerations.items():
/* START: 枚举${name}及其数组类型的序列化、反序列化、释放函数 */
GVariant *${name}_encode(${name} value);
${name} ${name}_decode(GVariant *in);

GVariant *${name}_encode_v(const ${name} *value, gsize n);
${name} *${name}_decode_v(GVariant *in, gsize *n);
/* END: 枚举${name}及其数组类型的序列化、反序列化、释放函数 */

% endfor
## 定义字典编解码和释放函数
% for name, dictionary in intf.dictionaries.items():
/* START: 字典${name}及其数组类型的序列化、反序列化、释放函数 */
GVariant *${name}_encode(const ${name} *value);
${name} *${name}_decode(GVariant *in);
void ${name}_free(${name} **value);

GVariant *${name}_encode_v(${name} * const *value);
${name} **${name}_decode_v(GVariant *in);
void ${name}_free_v(${name} ***value);
/* END: 字典${name}及其数组类型的序列化、反序列化、释放函数 */

% endfor
### 开始生成方法的请求体、响应体和处理函数
% for method in intf.fake_methods:
/* ${method.name}方法的请求体 */
typedef struct {
        % for arg in method.parameters.parameters:
            % for dec in arg.const_declare():
    ${dec.replace("<arg_name>", arg.name).replace("<const>", "")};
            % endfor
        % endfor
} ${class_name}_${method.name}_Req;

/* ${method.name}方法的响应体 */
typedef struct {
        % for arg in method.returns.parameters:
            % for dec in arg.declare():
    ${dec.replace("<arg_name>", arg.name).replace("<const>", "")};
            % endfor
        % endfor
} ${class_name}_${method.name}_Rsp;

% if not method.is_plugin:
typedef int (*${class_name}_${method.name}_Method)(const ${class_name} *object,
    const ${class_name}_${method.name}_Req *req,
    ${class_name}_${method.name}_Rsp **rsp,
    GError **error, gpointer ext_data);
% endif
GVariant *${class_name}_${method.name}_Req_encode(${class_name}_${method.name}_Req *value);
${class_name}_${method.name}_Req *${class_name}_${method.name}_Req_decode(GVariant *in);
void ${class_name}_${method.name}_Req_free(${class_name}_${method.name}_Req **value);
GVariant *${class_name}_${method.name}_Rsp_encode(${class_name}_${method.name}_Rsp *value);
${class_name}_${method.name}_Rsp *${class_name}_${method.name}_Rsp_decode(GVariant *in);
void ${class_name}_${method.name}_Rsp_free(${class_name}_${method.name}_Rsp **value);
%endfor

/* ${intf.name}的方法集合 */
typedef struct {
% for method in intf.methods:
    struct {
        const gchar *const name;
        const gchar *const req_signature;
        lbo_message_decode_handler req_decode;
        lbo_message_encode_handler req_encode;
        lbo_message_free_handler req_free;
        const gchar *const rsp_signature;
        lbo_message_decode_handler rsp_decode;
        lbo_message_encode_handler rsp_encode;
        lbo_message_free_handler rsp_free;
        ${class_name}_${method.name}_Method handler;
    } ${method.name};
% endfor
    LBMethod __reserved__;
} ${class_name}_Methods;

% if len(intf.plugin.actions) > 0:
% for action in intf.plugin.actions:
<% RSP_PARA = f'' %>\
<% REQ_PARA = f'' %>\
    % if len(action.returns.parameters) > 0:
<% RSP_PARA = f', {class_name}_{action.name}_Rsq **rsp' %>\
    % endif
    % if len(action.parameters.parameters) > 0:
<% REQ_PARA = f', const {class_name}_{action.name}_Req *req' %>\
    % endif
typedef int (*${class_name}_${action.name}_action)(const ${class_name} *object${REQ_PARA}${RSP_PARA}, gpointer user_data);

/* Register a new plugin action, can't register repeated with same action and user_data */
int ${class_name}_${action.name}_register(const gchar *req_signature, const gchar *rsp_signature,
    ${class_name}_${action.name}_action action, gpointer user_data);
void ${class_name}_${action.name}_unregister(${class_name}_${action.name}_action action);
int ${class_name}_${action.name}_run(const ${class_name} *object${REQ_PARA}${RSP_PARA});

% endfor
% endif
### 开始生成方法的请求体、响应体和处理函数
% for signal in intf.signals:
/* ${signal.name}信号的消息体 */
typedef struct {
        % for arg in signal.properties.parameters:
            % for dec in arg.const_declare():
    ${dec.replace("<arg_name>", arg.name).replace("<const>", "")};
            % endfor
        % endfor
} ${class_name}_${signal.name}_Msg;
${class_name}_${signal.name}_Msg *${class_name}_${signal.name}_Msg_decode(GVariant *in);
GVariant *${class_name}_${signal.name}_Msg_encode(${class_name}_${signal.name}_Msg *value);
void ${class_name}_${signal.name}_Msg_free(${class_name}_${signal.name}_Msg **value);

%endfor
typedef struct {
% for signal in intf.signals:
    struct {
        const gchar *const name;
        const gchar *const msg_signature;
        lbo_message_decode_handler msg_decode;
        lbo_message_encode_handler msg_encode;
        lbo_message_free_handler msg_free;
    } ${signal.name};
% endfor
    LBSignal __reserved__;
} ${class_name}_Signals;

% for name, stru in intf.structures.items():
    % if name == class_name:
struct _${name} {
    LBBase _base;        /* Notice: property name can't be _base */
    char __reserved__[8]; /* 8bytes reserved space, can't be modified */
        % for prop in stru.values.parameters:
            % for dec in prop.declare():
    ${dec.replace("<arg_name>", prop.name).replace("<const>", "")};
            % endfor
        % endfor
};

    % endif
%endfor
typedef struct {
% for prop in intf.properties:
    LBProperty ${prop.name};
% endfor
    LBProperty __reserved__;
} ${class_name}_Properties;

gboolean ${intf.name.replace(".", "_")}_validate_odf(yaml_document_t *doc, yaml_node_t *node,
    const gchar *object_name, GSList **error_list);
// 不要使用此函数返回的对象，需要使用${class_name}_properties() 或${class_name}_Cli_properties()
const ${class_name}_Properties *${class_name}_properties_const(void);
// 同时加载客户端和服务端时Processer是共享的，因此可以直接调用Processer定义的handler函数
${class_name}_Signals *${class_name}_signals(void);
${class_name}_Methods *${class_name}_methods(void);
/* Interface ${intf.name} codegen finish */

#ifdef __cplusplus
}
#endif

#endif /* __${"_".join(intf.alias.upper().split(".", -1))}_PUB_H__ */
