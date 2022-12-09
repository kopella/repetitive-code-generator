#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rcgen import *

'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

x0 = 0
x1 = 1
x2 = 2
x3 = 3
x4 = 4
'''

with RCodeGen("test\\test.py") as test_py_file:
    test_py_file.add("#!/usr/bin/env python")
    test_py_file.add("# -*- coding: utf-8 -*-")
    test_py_file.blank_line()
    for i in range(5):
        with test_py_file.repetitive_code(xi="x"+str(i), i=str(i)):
            test_py_file.add("${xi} = ${i}")

# The following is part of the code from my project pure-ogl-demo(https://github.com/kopella/pure-ogl-demo)

'''
# include "${platform}_ogl.h"

# include "ogl_func.h"
# include "utils.h"

/* OpenGL functions */
${func_type} ${func}
// ...

void get_functions()
{
  ${func} = (${func_type})${get_func_proc}("${func}");
  if (!${func}) {
    error_to_console("Failed to get ${func} function.");
  }
  // ...
}
'''
gl_funcs = [
    "glCreateProgram",
    "glLinkProgram",
    "glUseProgram",
    "glDeleteProgram"
]

with RCodeGen("test\\test.c", "  ") as test_c_file:
    test_c_file.add_dict(platform="win")
    test_c_file.add("#include \"${platform}_ogl.h\"")
    test_c_file.blank_line()
    test_c_file.add("#include \"ogl_func.h\"")
    test_c_file.add("#include \"utils.h\"")
    test_c_file.blank_line()
    test_c_file.add("/* OpenGL functions */")
    for gl_func in gl_funcs:
        with test_c_file.repetitive_code(func=gl_func, func_type="PFN"+gl_func.upper()+"PROC"):
            test_c_file.add("${func_type} ${func}")
    test_c_file.blank_line()
    with test_c_file.sub_hierarc("void get_functions()", "block"):
        for gl_func in gl_funcs:
            with test_c_file.repetitive_code(
                    func=gl_func, func_type="PFN"+gl_func.upper()+"PROC", get_func_proc="wglGetProcAddress"):
                test_c_file.add(
                    "${func} = (${func_type})${get_func_proc}(\"${func}\");")
                with test_c_file.sub_hierarc("if (!${func})", "block"):
                    test_c_file.add(
                        "error_to_console(\"Failed to get ${func} function.\");")
