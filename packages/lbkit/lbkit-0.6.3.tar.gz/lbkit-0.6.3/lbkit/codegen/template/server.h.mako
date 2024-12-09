#ifndef __${"_".join(intf.name.upper().split(".", -1))}_SRV_H__
#define __${"_".join(intf.name.upper().split(".", -1))}_SRV_H__

#include <glib-2.0/glib.h>
#include <glib-2.0/gio/gio.h>
#include "lb_base.h"
#include "public/${intf.name}.h"

#ifdef __cplusplus
extern "C" {
#endif
<% class_name = intf.alias %>\

% for prop in intf.properties:
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
    % if prop.deprecated:
__attribute__((__deprecated__)) void ${class_name}_set_${prop.name}(const ${class_name} *object, ${", ".join(prop.declare()).replace("<arg_name>", "value").replace("<const>", "const ")});
    % else:
void ${class_name}_set_${prop.name}(const ${class_name} *object, ${", ".join(prop.declare()).replace("<arg_name>", "value").replace("<const>", "const ")});
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
    % if len(signal.properties.parameters) > 0:
gboolean ${class_name}_${signal.name}_Signal(const ${class_name} *object, const gchar *destination,
    const ${class_name}_${signal.name}_Msg *msg, GError **error);
    % else:
gboolean ${class_name}_${signal.name}_Signal(const ${class_name} *object, const gchar *destination, GError **error);
    % endif
% endfor

#define ${class_name.upper()}_NAME    "${intf.name}"
% for prop in intf.properties:
#define ${class_name.upper()}_${prop.name}_NAME    "${prop.name}"
% endfor

LBInterface *${class_name}_interface(void);
#define ${class_name.upper()}_INTERFACE ${class_name}_interface()
${class_name}_Properties *${class_name}_properties(void);

#ifdef __cplusplus
}
#endif

#endif /* __${"_".join(intf.name.upper().split(".", -1))}_H__ */
