#ifndef __${"_".join(intf.name.upper().split(".", -1))}_CLI_H__
#define __${"_".join(intf.name.upper().split(".", -1))}_CLI_H__

#include <glib-2.0/glib.h>
#include <glib-2.0/gio/gio.h>
#include "lb_base.h"
#include "public/${intf.name}.h"

#ifdef __cplusplus
extern "C" {
#endif
<% class_name = intf.alias + "_Cli"%>
typedef ${intf.alias} ${class_name};
typedef ${intf.alias}_Properties ${class_name}_Properties;

% for prop in intf.properties:
% if not prop.private:
/*
 * property: ${prop.name}
% if len(prop.description.strip()) > 0:
 *
 % for line in prop.description.split("\n"):
   % if len(line.strip()) > 0:
 * ${line.strip()}
   % endif
 % endfor
% endif
 */
## 私有属性或者只读属性不允许写
% if not prop.private and prop.access != "read":
    % if prop.deprecated:
__attribute__((__deprecated__)) gint ${class_name}_set_${prop.name}(const ${class_name} *object, ${", ".join(prop.declare()).replace("<arg_name>", "value").replace("<const>", "const ")}, GError **error);
    % else:
gint ${class_name}_set_${prop.name}(const ${class_name} *object, ${", ".join(prop.declare()).replace("<arg_name>", "value").replace("<const>", "const ")}, GError **error);
    % endif
% endif
% if not prop.private and prop.access != "write":
    % if prop.deprecated:
__attribute__((__deprecated__)) gint ${class_name}_get_${prop.name}(const ${class_name} *object, ${", ".join(prop.out_declare()).replace("<arg_name>", "value").replace("<const>", "")}, GError **error);
    % else:
gint ${class_name}_get_${prop.name}(const ${class_name} *object, ${", ".join(prop.out_declare()).replace("<arg_name>", "value").replace("<const>", "")}, GError **error);
    % endif
% endif
% endif
% endfor

% for method in intf.methods:
<% RSP_PARA = f'' %>\
<% REQ_PARA = f'' %>\
    % if len(method.returns.parameters) > 0:
<% RSP_PARA = f'{intf.alias}_{method.name}_Rsp **rsp, ' %>\
    % endif
    % if len(method.parameters.parameters) > 0:
<% REQ_PARA = f'const {intf.alias}_{method.name}_Req *req, ' %>\
    % endif
/*
 * method: ${method.name}
% if len(method.description.strip()) > 0:
 *
 % for line in method.description.split("\n"):
   % if len(line.strip()) > 0:
 * ${line.strip()}
   % endif
 % endfor
% endif
 */
    % if method.deprecated:
__attribute__((__deprecated__)) int ${class_name}_Call_${method.name}(const ${class_name} *object,
    ${REQ_PARA}${RSP_PARA}gint timeout,
    GError **error);
    % else:
int ${class_name}_Call_${method.name}(const ${class_name} *object,
    ${REQ_PARA}${RSP_PARA}gint timeout,
    GError **error);
    % endif
% endfor

% for signal in intf.signals:
/*
 * signal: ${signal.name}
% if len(signal.description.strip()) > 0:
 *
 % for line in signal.description.split("\n"):
   % if len(line.strip()) > 0:
 * ${line.strip()}
   % endif
 % endfor
% endif
 */
typedef void (*${class_name}_${signal.name}_Signal)(const ${class_name} *object, const gchar *destination,
    const ${intf.alias}_${signal.name}_Msg *req, gpointer user_data);
/**/
    % if signal.deprecated:
__attribute__((__deprecated__)) guint ${class_name}_Subscribe_${signal.name}(${class_name}_${signal.name}_Signal handler,
    const gchar *bus_name, const gchar *object_path, const gchar *arg0, gpointer user_data);
    % else:
guint ${class_name}_Subscribe_${signal.name}(${class_name}_${signal.name}_Signal handler,
    const gchar *bus_name, const gchar *object_path, const gchar *arg0, gpointer user_data);
    % endif
    % if signal.deprecated:
__attribute__((__deprecated__)) void ${class_name}_Unsubscribe_${signal.name}(guint *id);
    % else:
void ${class_name}_Unsubscribe_${signal.name}(guint *id);
    % endif

% endfor
#define ${class_name.upper()}_NAME    "${intf.name}"
% for prop in intf.properties:
#define ${class_name.upper()}_${prop.name}_NAME    "${prop.name}"
% endfor

${class_name}_Properties *${class_name}_properties(void);
LBInterface *${class_name}_interface(void);
#define ${class_name.upper()}_INTERFACE ${class_name}_interface()

#ifdef __cplusplus
}
#endif

#endif /* __${"_".join(intf.name.upper().split(".", -1))}_CLI_H__ */
