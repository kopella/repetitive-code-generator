#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

x0 = 0
x1 = 1
x2 = 2
x3 = 3
x4 = 4
'''

from rcgen import RCodeGen
with RCodeGen("test\\test.py") as test_file:
    test_file.add("#!/usr/bin/env python")
    test_file.add("# -*- coding: utf-8 -*-")
    test_file.blank_line()
    for i in range(5):
        with test_file.repetitive_code(xi="x"+str(i), i=str(i)):
            test_file.add("${xi} = ${i}")

'''
#include "${platform}_ogl.h"

#include "ogl_func.h"
#include "utils.h"

void get_functions() {
  ${function} = (${function_type})${}("${function}");
  if (!glAttachShader) {
    ${error_message_function}("Failed to get ${function} function.");
  }
  // ...
}
'''
